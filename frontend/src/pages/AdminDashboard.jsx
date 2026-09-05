import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [dashboard, setDashboard] = useState(null);
  const [pending, setPending] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(null);
  const [error, setError] = useState("");

  async function loadData() {
    try {
      setLoading(true);
      setError("");
      const [d, p, u] = await Promise.all([
        api.get("/admin/dashboard"),
        api.get("/admin/verifications/pending"),
        api.get("/admin/users"),
      ]);
      setDashboard(d.data);
      setPending(p.data);
      setUsers(u.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load administrator data.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadData(); }, []);

  async function updateVerification(userId, action) {
    if (action === "reject" && !window.confirm("Are you sure you want to reject this account?")) return;
    try {
      setActionLoading(userId);
      await api.put(`/admin/users/${userId}/${action}`);
      await loadData();
    } catch (err) {
      alert(err.response?.data?.detail || `Unable to ${action} this account.`);
    } finally {
      setActionLoading(null);
    }
  }

  if (loading) return <main className="page"><div className="panel"><h2>Loading administrator dashboard...</h2></div></main>;

  const counts = dashboard?.counts || {};

  return (
    <main className="page">
      <div className="dashboard-head">
        <div>
          <div className="eyebrow">ADMINISTRATION</div>
          <h1>Admin Dashboard</h1>
          <p className="muted">Verify institutions, manage users and oversee the Social Innovation Collaboration Portal.</p>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="stats-grid">
        <div className="stat-card"><span>Total Users</span><strong>{counts.total_users ?? 0}</strong></div>
        <div className="stat-card"><span>Citizens</span><strong>{counts.citizens ?? 0}</strong></div>
        <div className="stat-card"><span>Universities</span><strong>{counts.universities ?? 0}</strong></div>
        <div className="stat-card"><span>Industries</span><strong>{counts.industries ?? 0}</strong></div>
        <div className="stat-card"><span>Government</span><strong>{counts.government_users ?? 0}</strong></div>
        <div className="stat-card"><span>Pending Verification</span><strong>{counts.pending_total ?? 0}</strong></div>
      </div>

      <section className="panel admin-problems-link-panel">
        <div className="admin-section-header">
          <div><h2>Impact & Analytics</h2><p className="muted">View platform-wide problem trends, solution outcomes and reported impact.</p></div>
          <button className="btn primary" onClick={() => navigate("/admin/analytics")}>Open Impact Analytics →</button>
        </div>
      </section>

      <section className="panel admin-problems-link-panel">
        <div className="admin-section-header">
          <div><h2>Industry Partnerships</h2><p className="muted">Review industry support offers for mentoring, funding, prototyping, testing and technology transfer.</p></div>
          <button className="btn primary" onClick={() => navigate("/admin/industry-partnerships")}>Manage Industry Support →</button>
        </div>
      </section>

      <section className="panel admin-problems-link-panel">
        <div className="admin-section-header">
          <div><h2>Problem Management</h2><p className="muted">Review citizen reports, assign verified representatives and track progress.</p></div>
          <button className="btn primary" onClick={() => navigate("/admin/problems")}>Manage Reported Problems →</button>
        </div>
      </section>

      <section className="panel">
        <div className="admin-section-header">
          <div><h2>Pending Verifications</h2><p className="muted">University, industry and government accounts waiting for administrator approval.</p></div>
        </div>

        {pending.length === 0 ? (
          <div className="empty-state"><strong>No pending accounts</strong><p>There are currently no organization accounts waiting for verification.</p></div>
        ) : (
          <div className="admin-table-wrap">
            <table className="admin-table">
              <thead><tr><th>User</th><th>Email</th><th>Role</th><th>Status</th><th>Registered</th><th>Actions</th></tr></thead>
              <tbody>
                {pending.map((user) => (
                  <tr key={user.id}>
                    <td><strong>{user.name}</strong></td>
                    <td>{user.email}</td>
                    <td><span className="role-pill">{user.role}</span></td>
                    <td><span className="status-pending">{user.verification_status}</span></td>
                    <td>{user.created_at ? new Date(user.created_at).toLocaleDateString() : "-"}</td>
                    <td>
                      <div className="table-actions">
                        <button className="btn secondary" onClick={() => navigate(`/admin/users/${user.id}`)}>View</button>
                        <button className="btn approve" disabled={actionLoading === user.id} onClick={() => updateVerification(user.id, "approve")}>{actionLoading === user.id ? "..." : "Approve"}</button>
                        <button className="btn reject" disabled={actionLoading === user.id} onClick={() => updateVerification(user.id, "reject")}>Reject</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="panel admin-users-panel">
        <div className="admin-section-header"><div><h2>All Users</h2><p className="muted">Complete list of accounts registered on the platform.</p></div></div>
        <div className="admin-table-wrap">
          <table className="admin-table">
            <thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Account Status</th><th>Verification</th></tr></thead>
            <tbody>{users.map((user) => <tr key={user.id}><td>{user.name}</td><td>{user.email}</td><td><span className="role-pill">{user.role || "NOT SET"}</span></td><td>{user.account_status}</td><td>{user.verification_status || "-"}</td></tr>)}</tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
