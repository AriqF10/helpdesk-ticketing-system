import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { addComment, getTicket, updateTicket, uploadAttachment } from '../api/tickets';
import { getTechnicians } from '../api/auth';
import { useAuth } from '../context/AuthContext';

const STATUS_OPTIONS = ['open', 'in_progress', 'resolved', 'closed'];
const STATUS_LABELS = { open: 'Open', in_progress: 'In Progress', resolved: 'Resolved', closed: 'Closed' };
const PRIORITY_LABELS = { low: 'Low', medium: 'Medium', high: 'High', urgent: 'Urgent' };

export default function TicketDetail() {
  const { id } = useParams();
  const { user } = useAuth();
  const [ticket, setTicket] = useState(null);
  const [technicians, setTechnicians] = useState([]);
  const [comment, setComment] = useState('');
  const [isInternal, setIsInternal] = useState(false);
  const [file, setFile] = useState(null);

  const isStaff = user?.role === 'admin' || user?.role === 'technician';

  const load = () => getTicket(id).then(({ data }) => setTicket(data));

  useEffect(() => {
    load();
    if (isStaff) getTechnicians().then(({ data }) => setTechnicians(data.results ?? data));
  }, [id]);

  if (!ticket) return <div className="page-loading">Loading...</div>;

  const handleStatusChange = async (e) => {
    await updateTicket(id, { status: e.target.value });
    load();
  };

  const handleAssign = async (e) => {
    await updateTicket(id, { assigned_to: e.target.value || null });
    load();
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    if (!comment.trim()) return;
    await addComment(id, { message: comment, is_internal_note: isInternal });
    setComment('');
    setIsInternal(false);
    load();
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    await uploadAttachment(id, file);
    setFile(null);
    load();
  };

  return (
    <div>
      <div className="page-header">
        <h2>#{ticket.id} {ticket.title}</h2>
        <span className={`badge badge-${ticket.status}`}>{STATUS_LABELS[ticket.status]}</span>
      </div>

      <div className="ticket-meta">
        <span><strong>Prioritas:</strong> {PRIORITY_LABELS[ticket.priority]}</span>
        <span><strong>Kategori:</strong> {ticket.category || '-'}</span>
        <span><strong>Pemohon:</strong> {ticket.created_by?.username}</span>
        <span><strong>Teknisi:</strong> {ticket.assigned_to?.username || 'Belum ditugaskan'}</span>
        <span className={ticket.resolution_sla_breached ? 'sla-breach' : ''}>
          <strong>SLA Resolusi:</strong> {new Date(ticket.resolution_due_at).toLocaleString('id-ID')}
        </span>
      </div>

      <p className="ticket-description">{ticket.description}</p>

      {isStaff && (
        <div className="staff-controls">
          <label>
            Ubah Status
            <select value={ticket.status} onChange={handleStatusChange}>
              {STATUS_OPTIONS.map((s) => <option key={s} value={s}>{STATUS_LABELS[s]}</option>)}
            </select>
          </label>
          <label>
            Assign Teknisi
            <select value={ticket.assigned_to?.id || ''} onChange={handleAssign}>
              <option value="">-- Belum ditugaskan --</option>
              {technicians.map((t) => <option key={t.id} value={t.id}>{t.username}</option>)}
            </select>
          </label>
        </div>
      )}

      <h3>Attachments</h3>
      <ul className="attachment-list">
        {ticket.attachments.map((a) => (
          <li key={a.id}><a href={a.file} target="_blank" rel="noreferrer">{a.file.split('/').pop()}</a></li>
        ))}
        {ticket.attachments.length === 0 && <li className="empty-row">Tidak ada lampiran.</li>}
      </ul>
      <form onSubmit={handleUpload} className="upload-form">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit" disabled={!file}>Upload</button>
      </form>

      <h3>Komentar</h3>
      <ul className="comment-list">
        {ticket.comments.map((c) => (
          <li key={c.id} className={c.is_internal_note ? 'comment-internal' : ''}>
            <div className="comment-head">
              <strong>{c.author?.username}</strong>
              <span>{new Date(c.created_at).toLocaleString('id-ID')}</span>
              {c.is_internal_note && <span className="badge badge-internal">Internal</span>}
            </div>
            <p>{c.message}</p>
          </li>
        ))}
        {ticket.comments.length === 0 && <li className="empty-row">Belum ada komentar.</li>}
      </ul>
      <form onSubmit={handleCommentSubmit} className="comment-form">
        <textarea rows={3} value={comment} onChange={(e) => setComment(e.target.value)} placeholder="Tulis komentar..." />
        {isStaff && (
          <label className="checkbox-label">
            <input type="checkbox" checked={isInternal} onChange={(e) => setIsInternal(e.target.checked)} />
            Catatan internal (tidak terlihat oleh pemohon)
          </label>
        )}
        <button type="submit">Kirim Komentar</button>
      </form>
    </div>
  );
}
