import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";

function SolutionCard({solution, problemId, onDone}) {
  const [feedback,setFeedback]=useState("");
  const [decision,setDecision]=useState("APPROVE");
  const [saving,setSaving]=useState(false);
  async function submit() {
    if(!feedback.trim()) return alert("Please add feedback.");
    try { setSaving(true); await api.post(`/solutions/${solution.id}/feedback`, {decision, feedback}); setFeedback(""); await onDone(); }
    catch(err){ alert(err.response?.data?.detail || "Unable to submit feedback."); }
    finally{ setSaving(false); }
  }
  async function verify() {
    if(!feedback.trim()) return alert("Please add verification comments.");
    try {
      setSaving(true);
      await api.post(`/solutions/${solution.id}/verify`, {decision:"VERIFY", feedback});
      setFeedback("");
      await onDone();
    } catch(err) {
      alert(err.response?.data?.detail || "Unable to verify solution.");
    } finally { setSaving(false); }
  }
  return <div className="solution-card">
    <div className="solution-head"><div><span className="problem-category">SOLUTION</span><h3>{solution.title}</h3></div><span className="problem-status">{String(solution.status).replaceAll("_"," ")}</span></div>
    <p>{solution.description}</p>
    <div className="detail-grid"><div><span>Benefits</span><strong>{solution.benefits || "-"}</strong></div><div><span>Estimated Cost</span><strong>{solution.estimated_cost || "-"}</strong></div><div><span>Resources</span><strong>{solution.required_resources || "-"}</strong></div><div><span>Time</span><strong>{solution.implementation_time || "-"}</strong></div></div>
    {solution.media?.length>0 && <div className="problem-media-grid">{solution.media.map(m=><div className="problem-media" key={m.id}>{m.media_type==="IMAGE"?<img src={m.url} alt={m.original_filename||"Solution evidence"}/>:<video src={m.url} controls/>}</div>)}</div>}
    {solution.implementation_updates?.length>0 && <div className="problem-timeline">{solution.implementation_updates.map(u=><div className="timeline-step active" key={u.id}><strong>{u.status.replaceAll("_"," ")}</strong><span>{u.note} · {u.user?.name} · {new Date(u.created_at).toLocaleString()}</span></div>)}</div>}
    {(solution.feedback||[]).map(f=><div className="comment-card" key={f.id}><strong>{f.user?.name} · {f.decision}</strong><p>{f.feedback}</p></div>)}
{solution.status === "IMPLEMENTED" && <div className="solution-feedback">
      <h4>Verify Implemented Solution</h4>
      <p className="muted">The solution has been implemented. Confirm whether it solved the reported problem.</p>
      <textarea rows="3" value={feedback} onChange={e=>setFeedback(e.target.value)} placeholder="Describe the outcome you observed..." />
      <button className="btn primary" disabled={saving} onClick={verify}>{saving?"Verifying...":"Verify Solution"}</button>
    </div>}
    {!["VERIFIED","REJECTED","IMPLEMENTED"].includes(solution.status) && <div className="solution-feedback"><h4>Your Feedback</h4><select value={decision} onChange={e=>setDecision(e.target.value)}><option value="APPROVE">Approve Solution</option><option value="CHANGES_REQUESTED">Request Changes</option><option value="REJECT">Reject Solution</option></select><textarea rows="3" value={feedback} onChange={e=>setFeedback(e.target.value)} placeholder="Explain your feedback..." /><button className="btn primary" disabled={saving} onClick={submit}>{saving?"Submitting...":"Submit Feedback"}</button></div>}
  </div>;
}

export default function ProblemDetails() {
  const { problemId } = useParams();
  const navigate = useNavigate();
  const [problem, setProblem] = useState(null);
  const [collab, setCollab] = useState({ assignment: null, timeline: [], comments: [] });
  const [solutions, setSolutions] = useState([]);
  const [comment, setComment] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    try {
      setLoading(true);
     const [p, c, s] = await Promise.all([
  api.get(`/problems/${problemId}`),
  api.get(`/citizen/problems/${problemId}/collaboration`),
  api.get(`/problems/${problemId}/solutions`),
]);

setProblem(p.data);
setCollab(c.data);
setSolutions(s.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load problem.");
    } finally { setLoading(false); }
  }
  useEffect(() => { load(); }, [problemId]);

  async function addComment() {
    if (!comment.trim()) return;
    try { setSaving(true); await api.post(`/collaboration/problems/${problemId}/comments`, { comment }); setComment(""); await load(); }
    catch (err) { alert(err.response?.data?.detail || "Unable to add comment."); }
    finally { setSaving(false); }
  }

  if (loading) return <main className="page"><div className="panel">Loading problem...</div></main>;
  if (error || !problem) return <main className="page"><div className="panel"><div className="error">{error || "Problem not found."}</div><button className="btn secondary" onClick={() => navigate("/my-problems")}>← Back</button></div></main>;

  return <main className="page">
    <button className="btn secondary" onClick={() => navigate("/my-problems")}>← My Problems</button>
    <section className="panel problem-detail">
      <div className="problem-card-head"><div><span className="problem-category">{problem.category}</span><h1>{problem.title}</h1></div><span className="problem-status">{String(problem.status).replaceAll("_"," ")}</span></div>
      <div className="detail-grid">
        <div className="detail-full"><span>Description</span><strong>{problem.description}</strong></div>
        <div><span>Priority</span><strong>{problem.priority}</strong></div><div><span>Submitted</span><strong>{new Date(problem.created_at).toLocaleString()}</strong></div>
        <div><span>Affected People</span><strong>{problem.affected_people ?? "-"}</strong></div><div><span>Address</span><strong>{problem.address || "-"}</strong></div>
        <div><span>Pincode</span><strong>{problem.pincode || "-"}</strong></div><div><span>GPS</span><strong>{problem.latitude && problem.longitude ? `${problem.latitude}, ${problem.longitude}` : "Not provided"}</strong></div>
        <div className="detail-full"><span>Additional Details</span><strong>{problem.additional_details || "-"}</strong></div>
      </div>

      {problem.media?.length > 0 && <><hr/><h2>Uploaded Evidence</h2><div className="problem-media-grid">{problem.media.map(m => <div className="problem-media" key={m.id}>{m.media_type === "IMAGE" ? <img src={m.url} alt={m.original_filename || "Problem evidence"} /> : <video src={m.url} controls />}</div>)}</div></>}

      <hr/><h2>Current Assignment</h2>
      {collab.assignment ? (
        <div className="assignment-card">
          <strong>{collab.assignment.assignee.name}</strong>
          <span>{collab.assignment.organization_role}</span>
          <span>{collab.assignment.assignee.organization || ""}</span>
          <small>{collab.assignment.remarks || "No assignment remarks."}</small>
        </div>
      ) : (
        <p className="muted">
          {problem.status === "CLOSED"
            ? "This problem has been resolved and verified by the citizen."
            : problem.status === "IMPLEMENTED"
              ? "The solution has been implemented and is awaiting citizen verification."
              : problem.status === "REJECTED"
                ? "This problem was rejected by the administrator."
                : problem.status === "SUBMITTED"
                  ? "Your report is waiting for administrator review and assignment."
                  : "Your report is progressing through the collaboration workflow."}
        </p>
      )}

      <hr/><h2>Progress Timeline</h2><div className="problem-timeline">
        <div className="timeline-step active"><strong>SUBMITTED</strong><span>{new Date(problem.created_at).toLocaleString()}</span></div>
        {collab.timeline.map(h => <div className="timeline-step active" key={h.id}><strong>{String(h.status).replaceAll("_"," ")}</strong><span>{h.note || "Status updated"} · {h.changed_by?.name} · {new Date(h.created_at).toLocaleString()}</span></div>)}
      </div>

      <hr/><h2>Solution Proposals</h2>
     {solutions.length === 0 ? (
  <p className="muted">No solution has been proposed yet.</p>
) : (
  solutions.map(s => (
    <SolutionCard
      key={s.id}
      solution={s}
      problemId={problemId}
      onDone={load}
    />
  ))
)}
      <hr/><h2>Collaboration</h2>
      {(collab.comments || []).map(c => <div className="comment-card" key={c.id}><strong>{c.user?.name} · {c.user?.role}</strong><p>{c.comment}</p><small>{new Date(c.created_at).toLocaleString()}</small></div>)}
      <div className="comment-compose"><textarea rows="3" value={comment} onChange={e => setComment(e.target.value)} placeholder="Ask a question or add information..." /><button className="btn primary" disabled={saving} onClick={addComment}>Add Comment</button></div>
    </section>
  </main>;
}
