import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { listArticles } from '../api/knowledgebase';
import { useAuth } from '../context/AuthContext';

export default function KnowledgeBaseList() {
  const [articles, setArticles] = useState([]);
  const [search, setSearch] = useState('');
  const { user } = useAuth();
  const isStaff = user?.role === 'admin' || user?.role === 'technician';

  useEffect(() => {
    listArticles(search ? { search } : {}).then(({ data }) => setArticles(data.results ?? data));
  }, [search]);

  return (
    <div>
      <div className="page-header">
        <h2>Knowledge Base</h2>
        {isStaff && <Link to="/kb/new" className="btn-primary">+ Artikel Baru</Link>}
      </div>
      <input
        className="search-box"
        placeholder="Cari artikel..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <div className="article-grid">
        {articles.map((a) => (
          <Link to={`/kb/${a.id}`} key={a.id} className="article-card">
            <h3>{a.title}</h3>
            <span className="article-category">{a.category || 'Umum'}</span>
            <p>{a.content.slice(0, 120)}...</p>
          </Link>
        ))}
        {articles.length === 0 && <p className="empty-row">Tidak ada artikel.</p>}
      </div>
    </div>
  );
}
