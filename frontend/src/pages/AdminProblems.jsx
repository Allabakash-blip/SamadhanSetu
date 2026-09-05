import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function AdminProblems() {
  const navigate = useNavigate();
  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    try {
      setLoading(true);
      const { data } = await api.get("/admin/problems");
      setProblems(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load problems.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  if (loading) return <main className="page"><div className="panel">Loading reported problems...</div></main>;

  return (
    <main className="page">
      <div className="dashboard-head">
        <div>
          <div className="eyebrow">ADMINISTRATION</div>
          <h1>Reported Problems</h1>
          <p className="muted">Review citizen reports, set priority and assign them to verified representatives.</p>
        </div>
        <button className="btn secondary" onClick={() => navigate("/admin")}>← Admin Dashboard</button>
      </div>

      {error && <div className="error">{error}</div>}

      {problems.length === 0 ? (
        <div className="panel empty-state"><strong>No problems reported yet</strong><p>Citizen submissions will appear here.</p></div>
      ) : (
        <section className="panel">
          <div className="admin-table-wrap">
            <table className="admin-table">
              <thead><tr><th>ID</th><th>Problem</th><th>Category</th><th>Priority</th><th>Status</th><th>Reporter</th><th>Assignment</th><th>Action</th></tr></thead>
              <tbody>
                {problems.map(p => (
                  <tr key={p.id}>
                    <td>#{p.id}</td>
                    <td><strong>{p.title}</strong></td>
                    <td>{p.category}</td>
                    <td><span className={`priority-pill priority-${String(p.priority).toLowerCase()}`}>{p.priority}</span></td>
                    <td><span className="problem-status">{String(p.status).replaceAll("_"," ")}</span></td>
                    <td>{p.reporter?.name}</td>
                    <td>{p.assignment ? `${p.assignment.assignee.name} (${p.assignment.organization_role})` : "Unassigned"}</td>
                    <td><button className="btn secondary" onClick={() => navigate(`/admin/problems/${p.id}`)}>Manage</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </main>
  );
}
