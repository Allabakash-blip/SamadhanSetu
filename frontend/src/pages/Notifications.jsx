import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function Notifications() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  async function load() {
    try { const { data } = await api.get("/notifications"); setItems(data); }
    catch {} finally { setLoading(false); }
  }
  useEffect(() => { load(); }, []);

  async function read(item) {
    if (!item.is_read) { try { await api.put(`/notifications/${item.id}/read`); } catch {} }
    if (item.problem_id) {
      if (user?.role === "CITIZEN") navigate(`/my-problems/${item.problem_id}`);
      else if (user?.role === "ADMIN") navigate(`/admin/problems/${item.problem_id}`);
      else if (user?.role === "INDUSTRY") navigate(`/industry/projects/${item.problem_id}`);
      else navigate(`/representative/problems/${item.problem_id}`);
    }
    await load();
  }

  if (loading) return <main className="page"><div className="panel">Loading notifications...</div></main>;
  return <main className="page">
    <div className="dashboard-head"><div><div className="eyebrow">UPDATES</div><h1>Notifications</h1><p className="muted">Stay informed about assignments, comments and problem progress.</p></div></div>
    <section className="panel">
      {items.length === 0 ? <div className="empty-state"><strong>No notifications</strong><p>New problem activity will appear here.</p></div> :
      <div className="notification-list">{items.map(n => <button className={`notification-card ${n.is_read ? "read" : "unread"}`} key={n.id} onClick={() => read(n)} type="button"><div><strong>{n.title}</strong><p>{n.message}</p><small>{new Date(n.created_at).toLocaleString()}</small></div>{!n.is_read && <span className="notification-dot">NEW</span>}</button>)}</div>}
    </section>
  </main>;
}
