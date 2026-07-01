import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listTickets } from '../api/tickets';

const STATUS_LABELS = { open: 'Open', in_progress: 'In Progress', resolved: 'Resolved', closed: 'Closed' };
const PRIORITY_LABELS = { low: 'Low', medium: 'Medium', high: 'High', urgent: 'Urgent' };

export default function TicketList() {
  const [tickets, setTickets] = useState([]);
  const [filters, setFilters] = useState({ status: '', priority: '' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const params = {};
    if (filters.status) params.status = filters.status;
    if (filters.priority) params.priority = filters.priority;
    listTickets(params)
      .then(({ data }) => setTickets(data.results ?? data))
      .finally(() => setLoading(false));
  }, [filters]);

  return (
    <div>
      <div className="page-header">
        <h2>Tiket</h2>
        <Link to="/tickets/new" className="btn-primary">+ Buat Tiket</Link>
      </div>

      <div className="filters">
        <select value={filters.status} onChange={(e) => setFilters({ ...filters, status: e.target.value })}>
          <option value="">Semua Status</option>
          {Object.entries(STATUS_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
        </select>
        <select value={filters.priority} onChange={(e) => setFilters({ ...filters, priority: e.target.value })}>
          <option value="">Semua Prioritas</option>
          {Object.entries(PRIORITY_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
        </select>
      </div>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>#</th><th>Judul</th><th>Status</th><th>Prioritas</th><th>Pemohon</th><th>Teknisi</th><th>SLA</th>
            </tr>
          </thead>
          <tbody>
            {tickets.map((t) => (
              <tr key={t.id}>
                <td><Link to={`/tickets/${t.id}`}>#{t.id}</Link></td>
                <td><Link to={`/tickets/${t.id}`}>{t.title}</Link></td>
                <td><span className={`badge badge-${t.status}`}>{STATUS_LABELS[t.status]}</span></td>
                <td><span className={`badge badge-priority-${t.priority}`}>{PRIORITY_LABELS[t.priority]}</span></td>
                <td>{t.created_by?.username}</td>
                <td>{t.assigned_to?.username || '-'}</td>
                <td>{t.resolution_sla_breached ? <span className="sla-breach">Breached</span> : 'OK'}</td>
              </tr>
            ))}
            {tickets.length === 0 && (
              <tr><td colSpan={7} className="empty-row">Tidak ada tiket.</td></tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
