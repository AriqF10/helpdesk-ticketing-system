import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createTicket } from '../api/tickets';

export default function TicketCreate() {
  const [form, setForm] = useState({ title: '', description: '', priority: 'medium', category: '' });
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      const { data } = await createTicket(form);
      navigate(`/tickets/${data.id}`);
    } catch (err) {
      setError('Gagal membuat tiket. Periksa kembali data.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h2>Buat Tiket Baru</h2>
      <form className="form-card" onSubmit={handleSubmit}>
        {error && <p className="error-text">{error}</p>}
        <label>Judul<input value={form.title} onChange={update('title')} required /></label>
        <label>Deskripsi<textarea rows={5} value={form.description} onChange={update('description')} required /></label>
        <label>
          Prioritas
          <select value={form.priority} onChange={update('priority')}>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="urgent">Urgent</option>
          </select>
        </label>
        <label>Kategori<input value={form.category} onChange={update('category')} placeholder="mis. Hardware, Software, Network" /></label>
        <button type="submit" disabled={submitting}>{submitting ? 'Mengirim...' : 'Kirim Tiket'}</button>
      </form>
    </div>
  );
}
