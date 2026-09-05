import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";

const statuses = ["SUBMITTED","UNDER_REVIEW","VALIDATED","ASSIGNED","IN_PROGRESS","SOLUTION_PROPOSED","PILOT","IMPLEMENTED","CLOSED","REJECTED"];
const priorities = ["LOW","MEDIUM","HIGH","CRITICAL"];

function formatStatus(value) {
  return String(value || "").replaceAll("_", " ");
}

export default function AdminProblemDetails() {
  const { problemId } = useParams();
  const navigate = useNavigate();
  const [problem, setProblem] = useState(null);
  const [representatives, setRepresentatives] = useState([]);
  const [assigneeId, setAssigneeId] = useState("");
  const [remarks, setRemarks] = useState("");
  const [status, setStatus] = useState("");
  const [priority, setPriority] = useState("");
  const [note, setNote] = useState("");
  const [comment, setComment] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [matches, setMatches] = useState([]);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiLoaded, setAiLoaded] = useState(false);

  async function load() {
    try {
      setLoading(true);
      const [p, reps] = await Promise.all([
        api.get(`/admin/problems/${problemId}`),
        api.get("/admin/problem-representatives"),
      ]);
      setProblem(p.data);
      setRepresentatives(reps.data);
      setStatus(p.data.status);
      setPriority(p.data.priority);
      setAssigneeId(p.data.assignment?.assignee?.id?.toString() || "");
      setRemarks(p.data.assignment?.remarks || "");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load problem.");
    } finally { setLoading(false); }
  }

  useEffect(() => { load(); }, [problemId]);

  async function assign() {
    if (!assigneeId) return alert("Select a verified representative.");
    try {
      setSaving(true);
      await api.put(`/admin/problems/${problemId}/assign`, { assignee_id: Number(assigneeId), remarks });
      await load();
      alert("Problem assigned successfully.");
    } catch (err) { alert(err.response?.data?.detail || "Unable to assign problem."); }
    finally { setSaving(false); }
  }

  async function updateProblem() {
    try {
      setSaving(true);
      await api.put(`/admin/problems/${problemId}/update`, { status, priority, note });
      setNote("");
      await load();
      alert("Problem updated successfully.");
    } catch (err) { alert(err.response?.data?.detail || "Unable to update problem."); }
    finally { setSaving(false); }
  }

  async function addComment() {
    if (!comment.trim()) return;
    try {
      setSaving(true);
      await api.post(`/collaboration/problems/${problemId}/comments`, { comment });
      setComment("");
      await load();
    } catch (err) { alert(err.response?.data?.detail || "Unable to add comment."); }
    finally { setSaving(false); }
  }

  async function runAiMatching() {
    try {
      setAiLoading(true);
      setError("");
      const { data } = await api.get(`/ai/problems/${problemId}/matches?limit=5`);
      setAiAnalysis(data.analysis);
      setMatches(data.matches || []);
      setAiLoaded(true);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to run AI classification and matching.");
    } finally {
      setAiLoading(false);
    }
  }

  if (loading) return <main className="page"><div className="panel">Loading problem...</div></main>;
  if (!problem) return <main className="page"><div className="panel"><div className="error">{error || "Problem not found."}</div></div></main>;

  return (
    <main className="page">
      <button className="btn secondary back-button" onClick={() => navigate("/admin/problems")}>← All Problems</button>
      {error && <div className="error">{error}</div>}

      <section className="panel ai-panel">
        <div className="ai-panel-head">
          <div>
            <span className="eyebrow">MILESTONE 7</span>
            <h2>🤖 AI Classification & Institutional Matching</h2>
            <p className="muted">Analyze the reported problem and rank approved organization representatives using transparent, explainable matching signals.</p>
          </div>
          <button className="btn primary" disabled={aiLoading} onClick={runAiMatching}>
            {aiLoading ? "Analyzing..." : aiLoaded ? "↻ Re-analyze" : "Run AI Analysis"}
          </button>
        </div>

        {aiLoaded && aiAnalysis && (
          <div className="ai-analysis-grid">
            <div className="ai-classification-card">
              <span className="ai-label">Predicted Category</span>
              <strong>{aiAnalysis.predicted_category}</strong>
              <div className="ai-confidence">
                <div className="ai-confidence-head"><span>Confidence</span><b>{aiAnalysis.confidence}%</b></div>
                <div className="analytics-track"><div className="analytics-fill" style={{width: `${aiAnalysis.confidence}%`}} /></div>
              </div>
            </div>
            <div className="ai-classification-card">
              <span className="ai-label">Suggested Priority</span>
              <strong className={`priority-pill priority-${String(aiAnalysis.priority).toLowerCase()}`}>{aiAnalysis.priority}</strong>
              <p>{aiAnalysis.priority_reason}</p>
            </div>
            <div className="ai-classification-card">
              <span className="ai-label">Required Expertise</span>
              <div className="ai-tags">{(aiAnalysis.required_expertise || []).slice(0, 6).map(x => <span key={x}>{x}</span>)}</div>
            </div>
            <div className="ai-classification-card">
              <span className="ai-label">Matched Keywords</span>
              <div className="ai-tags">{(aiAnalysis.matched_keywords || []).length ? aiAnalysis.matched_keywords.map(x => <span key={x}>{x}</span>) : <span>No strong keyword evidence</span>}</div>
            </div>
          </div>
        )}

        {aiLoaded && (
          <div className="ai-matches">
            <div className="ai-matches-head">
              <div><h3>Recommended Representatives</h3><p className="muted">Only active, administrator-approved organization accounts are considered.</p></div>
            </div>
            {matches.length === 0 ? (
              <div className="ai-empty">No verified representative currently matches this problem. Approve organization accounts or update their expertise/location profiles.</div>
            ) : (
              <div className="ai-match-list">
                {matches.map(match => (
                  <div className="ai-match-card" key={match.user_id}>
                    <div className="ai-rank">#{match.rank}</div>
                    <div className="ai-match-main">
                      <strong>{match.name}</strong>
                      <span>{match.organization || "Organization"} · {match.role}</span>
                      <div className="ai-reasons">{(match.match_reasons || []).slice(0, 3).map(reason => <small key={reason}>✓ {reason}</small>)}</div>
                    </div>
                    <div className="ai-score"><b>{match.score}%</b><span>match</span></div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </section>

      <div className="collab-layout">
        <section className="panel">
          <div className="problem-card-head">
            <div><span className="problem-category">{problem.category}</span><h1>{problem.title}</h1></div>
            <span className="problem-status">{formatStatus(problem.status)}</span>
          </div>
          <p className="problem-description">{problem.description}</p>
          <div className="detail-grid">
            <div><span>Reporter</span><strong>{problem.reporter?.name} ({problem.reporter?.email})</strong></div>
            <div><span>Priority</span><strong>{problem.priority}</strong></div>
            <div><span>Affected People</span><strong>{problem.affected_people ?? "-"}</strong></div>
            <div><span>Submitted</span><strong>{new Date(problem.created_at).toLocaleString()}</strong></div>
            <div className="detail-full"><span>Address</span><strong>{problem.address || "-"}</strong></div>
            <div><span>GPS</span><strong>{problem.latitude && problem.longitude ? `${problem.latitude}, ${problem.longitude}` : "Not provided"}</strong></div>
          </div>
          {problem.media?.length > 0 && <><hr/><h2>Evidence</h2><div className="problem-media-grid">{problem.media.map(m => <div className="problem-media" key={m.id}>{m.media_type === "IMAGE" ? <img src={m.url} alt={m.original_filename || "Evidence"} /> : <video src={m.url} controls />}</div>)}</div></>}

          <hr/><h2>Progress Timeline</h2>
          <div className="problem-timeline">
            <div className="timeline-step active"><strong>SUBMITTED</strong><span>{new Date(problem.created_at).toLocaleString()}</span></div>
            {problem.timeline?.map(h => <div className="timeline-step active" key={h.id}><strong>{formatStatus(h.status)}</strong><span>{h.note || "Status updated"} · {h.changed_by?.name} · {new Date(h.created_at).toLocaleString()}</span></div>)}
          </div>

          <hr/><h2>Collaboration Comments</h2>
          <div className="comments-list">
            {(problem.comments || []).length === 0 ? <p className="muted">No comments yet.</p> : problem.comments.map(c => <div className="comment-card" key={c.id}><strong>{c.user?.name} · {c.user?.role}</strong><p>{c.comment}</p><small>{new Date(c.created_at).toLocaleString()}</small></div>)}
          </div>
          <div className="comment-compose"><textarea rows="3" value={comment} onChange={e => setComment(e.target.value)} placeholder="Add an administrative comment..." /><button className="btn primary" disabled={saving} onClick={addComment}>Add Comment</button></div>
        </section>

        <aside className="panel collab-side">
          <h2>Manage Problem</h2>
          <label>Priority<select value={priority} onChange={e => setPriority(e.target.value)}>{priorities.map(x => <option key={x}>{x}</option>)}</select></label>
          <label>Status<select value={status} onChange={e => setStatus(e.target.value)}>{statuses.map(x => <option key={x}>{x}</option>)}</select></label>
          <label>Update note<textarea rows="3" value={note} onChange={e => setNote(e.target.value)} placeholder="Why is this status changing?" /></label>
          <button className="btn primary full-button" disabled={saving} onClick={updateProblem}>Save Status / Priority</button>

          <hr/>
          <h2>Assign Representative</h2>
          <p className="hint">Only active, administrator-approved organization representatives are listed.</p>
          <label>Representative<select value={assigneeId} onChange={e => setAssigneeId(e.target.value)}><option value="">Select representative</option>{representatives.map(r => <option key={r.id} value={r.id}>{r.name} — {r.role}{r.organization ? ` — ${r.organization}` : ""}</option>)}</select></label>
          <label>Assignment remarks<textarea rows="4" value={remarks} onChange={e => setRemarks(e.target.value)} placeholder="Instructions for the representative..." /></label>
          <button className="btn approve full-button" disabled={saving || !assigneeId} onClick={assign}>Assign Problem</button>

          <hr/>
          <h3>Current Assignment</h3>
          {problem.assignment ? <div className="assignment-card"><strong>{problem.assignment.assignee.name}</strong><span>{problem.assignment.organization_role}</span><span>{problem.assignment.assignee.organization || ""}</span><small>{problem.assignment.remarks || "No remarks"}</small></div> : <p className="muted">Not assigned yet.</p>}
        </aside>
      </div>
    </main>
  );
}
