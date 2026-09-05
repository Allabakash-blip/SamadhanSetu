import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function RepresentativeProblems() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/representative/problems")
      .then(r => setProblems(r.data))
      .catch(err => setError(err.response?.data?.detail || "Unable to load assigned problems."))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <main className="page"><div className="panel">Loading assigned problems...</div></main>;

  return <main className="page">
    <div className="dashboard-head"><div><div className="eyebrow">{user?.role} REPRESENTATIVE</div><h1>Assigned Problems</h1><p className="muted">Work on citizen-reported challenges assigned to you and keep the citizen informed.</p></div><button className="btn secondary" onClick={() => navigate("/dashboard")}>← Dashboard</button></div>
    {error && <div className="error">{error}</div>}
    {problems.length === 0 ? <div className="panel empty-state"><strong>No problems assigned</strong><p>When an administrator assigns a challenge to you, it will appear here.</p></div> :
      <div className="problem-list">{problems.map(p => <article className="problem-card" key={p.id} onClick={() => navigate(`/representative/problems/${p.id}`)}>
        <div className="problem-card-head"><div><span className="problem-category">{p.category}</span><h2>{p.title}</h2></div><span className="problem-status">{String(p.status).replaceAll("_"," ")}</span></div>
        <p>{p.description}</p><div className="problem-card-footer"><span>Priority: <strong>{p.priority}</strong></span><span>Citizen: <strong>{p.reporter?.name}</strong></span></div>
      </article>)}</div>}
  </main>;
}
