import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { deleteArticle, getArticle } from '../api/knowledgebase';
import { useAuth } from '../context/AuthContext';

export default function KnowledgeBaseDetail() {
  const { id } = useParams();
  const [article, setArticle] = useState(null);
  const { user } = useAuth();
  const navigate = useNavigate();
  const isStaff = user?.role === 'admin' || user?.role === 'technician';

  useEffect(() => {
    getArticle(id).then(({ data }) => setArticle(data));
  }, [id]);

  if (!article) return <div className="page-loading">Loading...</div>;

  const handleDelete = async () => {
    if (!confirm('Hapus artikel ini?')) return;
    await deleteArticle(id);
    navigate('/kb');
  };

  return (
    <div>
      <div className="page-header">
        <h2>{article.title}</h2>
        {isStaff && <button onClick={handleDelete} className="btn-danger">Hapus</button>}
      </div>
      <span className="article-category">{article.category || 'Umum'}</span>
      <p className="ticket-description">{article.content}</p>
      <p className="article-meta">Oleh {article.author?.username} &middot; {new Date(article.created_at).toLocaleDateString('id-ID')}</p>
    </div>
  );
}
