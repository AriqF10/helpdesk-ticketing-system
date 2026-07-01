import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { register } from '../api/auth';
import { useAuth } from '../context/AuthContext';

export default function Register() {
  const [form, setForm] = useState({
    username: '', email: '', password: '', first_name: '', last_name: '', department: '',
  });
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSubmitting(true);
    try {
      await register(form);
      await login(form.username, form.password);
      navigate('/');
    } catch (err) {
      const data = err.response?.data;
      setError(data ? Object.values(data).flat().join(' ') : 'Registrasi gagal.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Buat Akun</h2>
        {error && <p className="error-text">{error}</p>}
        <label>Username<input value={form.username} onChange={update('username')} required /></label>
        <label>Email<input type="email" value={form.email} onChange={update('email')} required /></label>
        <label>Password<input type="password" value={form.password} onChange={update('password')} required /></label>
        <label>Nama Depan<input value={form.first_name} onChange={update('first_name')} /></label>
        <label>Nama Belakang<input value={form.last_name} onChange={update('last_name')} /></label>
        <label>Departemen<input value={form.department} onChange={update('department')} /></label>
        <button type="submit" disabled={submitting}>{submitting ? 'Memproses...' : 'Daftar'}</button>
        <p className="auth-switch">Sudah punya akun? <Link to="/login">Masuk</Link></p>
      </form>
    </div>
  );
}
