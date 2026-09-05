import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";

export default function AdminUserDetails() {
  const { userId } = useParams();
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadUser() {
    try {
      setLoading(true);
      const response = await api.get(`/admin/users/${userId}`);
      setUser(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load user.");
    } finally { setLoading(false); }
  }

  useEffect(() => { loadUser(); }, [userId]);

  async function changeStatus(action) {
    if (action === "reject" && !window.confirm("Are you sure you want to reject this account?")) return;
    try {
      setActionLoading(true);
      await api.put(`/admin/users/${userId}/${action}`);
      await loadUser();
    } catch (err) {
      alert(err.response?.data?.detail || "Unable to update account.");
    } finally { setActionLoading(false); }
  }

  if (loading) return <main className="page"><div className="panel">Loading user details...</div></main>;
  if (!user) return <main className="page"><div className="panel"><h2>User not found</h2><button className="btn secondary" onClick={() => navigate("/admin")}>Back</button></div></main>;

  const p = user.profile || {};
  const row = (label, value) => <div><span>{label}</span><strong>{value || "-"}</strong></div>;

  return (
    <main className="page">
      <button className="btn secondary back-button" onClick={() => navigate("/admin")}>← Back to Admin Dashboard</button>
      {error && <div className="error">{error}</div>}
      <div className="admin-detail-grid">
        <section className="panel">
          <div className="user-detail-header">
            {user.profile_picture_url ? <img src={user.profile_picture_url} alt="" className="large-profile-picture" /> : <div className="large-avatar">{user.name?.[0]?.toUpperCase()}</div>}
            <div><h1>{user.name}</h1><p className="muted">{user.email}</p><span className="role-pill">{user.role}</span></div>
          </div>
          <div className="detail-section"><h2>Account Information</h2><div className="detail-grid">
            {row("Full Name", user.name)}{row("Email", user.email)}{row("Phone", user.phone)}{row("Role", user.role)}{row("Account Status", user.account_status)}{row("Verification Status", user.verification_status)}
          </div></div>
        </section>

        <section className="panel">
          <h2>Organization Profile</h2>
          {user.role === "UNIVERSITY" && <div className="detail-grid">
            {row("University", p.university_name)}{row("University Type", p.university_type)}{row("Registration Number", p.registration_number)}{row("Department", p.department)}{row("Designation", p.designation)}{row("City", p.city)}{row("Address", p.address)}{row("Expertise", p.expertise)}
          </div>}
          {user.role === "INDUSTRY" && <div className="detail-grid">
            {row("Company", p.company_name)}{row("Company Type", p.company_type)}{row("Website", p.website)}{row("City", p.city)}{row("Address", p.address)}{row("Expertise", p.expertise)}{row("Available Support", p.available_support)}
          </div>}
          {user.role === "GOVERNMENT" && <div className="detail-grid">{row("Department", p.department)}{row("Designation", p.designation)}{row("Official ID", p.official_id)}</div>}
          {user.role === "CITIZEN" && <p className="muted">Citizen accounts do not require administrator verification.</p>}

          {["UNIVERSITY", "INDUSTRY", "GOVERNMENT"].includes(user.role) && (
            <div className="admin-verification-actions">
              <button className="btn approve large-button" disabled={actionLoading} onClick={() => changeStatus("approve")}>{actionLoading ? "Processing..." : "✓ Approve Account"}</button>
              <button className="btn reject large-button" disabled={actionLoading} onClick={() => changeStatus("reject")}>✕ Reject Account</button>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
