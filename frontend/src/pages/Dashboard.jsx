import { useEffect, useState } from 'react';
import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { getDashboard } from '../api/tickets';

const STATUS_COLORS = { open: '#3b82f6', in_progress: '#f59e0b', resolved: '#10b981', closed: '#6b7280' };
const PRIORITY_LABELS = { low: 'Low', medium: 'Medium', high: 'High', urgent: 'Urgent' };
const STATUS_LABELS = { open: 'Open', in_progress: 'In Progress', resolved: 'Resolved', closed: 'Closed' };

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getDashboard().then(({ data }) => setData(data));
  }, []);

  if (!data) return <div className="page-loading">Loading dashboard...</div>;

  const statusData = Object.entries(data.by_status).map(([key, value]) => ({
    name: STATUS_LABELS[key], value, key,
  }));
  const priorityData = Object.entries(data.by_priority).map(([key, value]) => ({
    name: PRIORITY_LABELS[key], value,
  }));

  return (
    <div>
      <h2>Dashboard</h2>
      <div className="stat-cards">
        <div className="stat-card">
          <span className="stat-value">{data.total}</span>
          <span className="stat-label">Total Tiket</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{data.by_status.open || 0}</span>
          <span className="stat-label">Open</span>
        </div>
        <div className="stat-card">
          <span className="stat-value">{data.by_status.in_progress || 0}</span>
          <span className="stat-label">In Progress</span>
        </div>
        <div className="stat-card stat-card-danger">
          <span className="stat-value">{data.sla_breached}</span>
          <span className="stat-label">SLA Breached</span>
        </div>
      </div>

      <div className="chart-grid">
        <div className="chart-box">
          <h3>Tiket by Status</h3>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={statusData} dataKey="value" nameKey="name" outerRadius={90} label>
                {statusData.map((entry) => (
                  <Cell key={entry.key} fill={STATUS_COLORS[entry.key]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="chart-box">
          <h3>Tiket by Priority</h3>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={priorityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
