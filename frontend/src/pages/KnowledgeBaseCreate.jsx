import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createArticle } from '../api/knowledgebase';

export default function KnowledgeBaseCreate() {
  const [form, setForm] = useState({ title: '', content: '', category: '' });
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const { data } = await createArticle(form);
      navigate(`/kb/${data.id}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      <h2>Artikel Baru</h2>
      <form className="form-card" onSubmit={handleSubmit}>
        <label>Judul<input value={form.title} onChange={update('title')} required /></label>
        <label>Kategori<input value={form.category} onChange={update('category')} /></label>
        <label>Konten<textarea rows={10} value={form.content} onChange={update('content')} required /></label>
        <button type="submit" disabled={submitting}>{submitting ? 'Menyimpan...' : 'Simpan'}</button>
      </form>
    </div>
  );
}
