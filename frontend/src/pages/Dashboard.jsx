import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

const content = {
  CITIZEN: { title: "Citizen Dashboard", subtitle: "Report local societal challenges and follow their progress.", cards: ["My Problems", "Under Review", "In Progress", "Resolved"], actions: ["Report a Problem", "My Submissions"] },
  UNIVERSITY: { title: "University Dashboard", subtitle: "Review challenges, build multidisciplinary teams and submit solutions.", cards: ["Assigned Challenges", "Active Projects", "Teams", "Completed"], actions: ["Assigned Problems", "My Projects", "My Teams"] },
  INDUSTRY: { title: "Industry Dashboard", subtitle: "Support projects through mentoring, funding, technology and testing.", cards: ["Available Projects", "Supported Projects", "Active Partnerships", "Support Offers"], actions: ["Available Projects", "My Support"] },
  GOVERNMENT: { title: "Government Dashboard", subtitle: "Monitor challenges, participation and project impact.", cards: ["Total Users", "Pending Validation", "Universities", "Industries"], actions: ["Assigned Problems", "Analytics", "Map"] },
  ADMIN: { title: "Admin Dashboard", subtitle: "Verify organizations and manage platform users.", cards: ["Total Users", "Pending Accounts", "Universities", "Industries"], actions: ["Verify Accounts", "Manage Users", "Manage Problems"] },
};

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [summary, setSummary] = useState(null);
  const [industrySummary, setIndustrySummary] = useState(null);
  const c = content[user?.role] || content.CITIZEN;

  useEffect(() => {
    api.get("/dashboard/summary").then((r) => setSummary(r.data)).catch(() => {});
    if (user?.role === "INDUSTRY") {
      Promise.all([api.get("/industry/projects"), api.get("/industry/support")])
        .then(([projects, support]) => setIndustrySummary({
          available: projects.data.length,
          offers: support.data.offers.length,
          supported: support.data.offers.filter(o => ["ACCEPTED"].includes(o.status)).length,
          active: support.data.partnerships.filter(p => p.status === "ACTIVE").length,
        }))
        .catch(() => {});
    }
  }, [user?.role]);

  const showsRealCounts = user?.role === "ADMIN" || user?.role === "GOVERNMENT";
  const values = user?.role === "CITIZEN" && summary
    ? [summary.counts.my_problems, summary.counts.under_review, summary.counts.in_progress, summary.counts.resolved]
    : user?.role === "UNIVERSITY" && summary
      ? [summary.counts.assigned_challenges, summary.counts.active_projects, summary.counts.teams, summary.counts.completed]
      : showsRealCounts && summary
        ? [summary.counts.total_users, summary.counts.pending_accounts, summary.counts.universities, summary.counts.industries]
        : user?.role === "INDUSTRY" && industrySummary
        ? [industrySummary.available, industrySummary.supported, industrySummary.active, industrySummary.offers]
        : [0, 0, 0, 0];

  function handleAction(action) {
    if (user?.role === "ADMIN") {
      if (action === "Manage Problems") {
        navigate("/admin/problems");
      } else {
        navigate("/admin");
      }
      return;
    }
    if (user?.role === "CITIZEN" && action === "Report a Problem") {
      navigate("/report-problem");
      return;
    }
    if (user?.role === "CITIZEN" && action === "My Submissions") {
      navigate("/my-problems");
      return;
    }
    if (["UNIVERSITY", "GOVERNMENT"].includes(user?.role) && action === "Assigned Problems") {
      navigate("/representative/problems");
      return;
    }
    if (user?.role === "INDUSTRY" && action === "Available Projects") { navigate("/industry/projects"); return; }
    if (user?.role === "INDUSTRY" && action === "My Support") { navigate("/industry/support"); return; }
    if (user?.role === "ADMIN" && action === "Manage Problems") {
      navigate("/admin/problems");
      return;
    }
    alert(`${action} will be implemented in a future milestone.`);
  }

  return (
    <main className="page">
      <div className="dashboard-head">
        <div>
          <div className="eyebrow">SOCIAL INNOVATION COLLABORATION PORTAL</div>
          <h1>{c.title}</h1>
          <p className="muted">{c.subtitle}</p>
        </div>
        <div className="profile-mini">
          {user?.profile_picture_url ? <img src={user.profile_picture_url} alt="" /> : <div className="avatar">{user?.name?.[0]?.toUpperCase()}</div>}
          <div><strong>{user?.name}</strong><br /><span>{user?.email}</span></div>
        </div>
      </div>

      {user?.account_status === "PENDING" && <div className="notice">Your organization account is pending verification. Restricted organization actions should remain unavailable until verification.</div>}

      <div className="stats-grid">
        {c.cards.map((label, i) => <div className="stat-card" key={label}><span>{label}</span><strong>{values[i] ?? 0}</strong></div>)}
      </div>

      <div className="dashboard-grid">
        <section className="panel">
          <h2>Quick Actions</h2>
          <div className="action-grid">
            {c.actions.map((action) => (
              <button className="action-card" key={action} onClick={() => handleAction(action)} type="button">
                {action}<span>→</span>
              </button>
            ))}
          </div>
        </section>
        <section className="panel">
          <h2>Platform flow</h2>
          <p>Citizen challenge → AI classification → institutional matching → project collaboration → measurable social impact.</p>
          <div className="flow-mini"><span>Challenge</span><b>→</b><span>Match</span><b>→</b><span>Project</span><b>→</b><span>Impact</span></div>
        </section>
      </div>
    </main>
  );
}
