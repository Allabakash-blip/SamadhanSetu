import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";

const statuses = ["IN_PROGRESS","SOLUTION_PROPOSED","PILOT","IMPLEMENTED","CLOSED"];

export default function RepresentativeProblemDetails() {
  const { problemId } = useParams();
  const navigate = useNavigate();
  const [problem, setProblem] = useState(null);
  const [status, setStatus] = useState("IN_PROGRESS");
  const [note, setNote] = useState("");
  const [comment, setComment] = useState("");
  const [solution, setSolution] = useState({title:"",description:"",benefits:"",estimated_cost:"",required_resources:"",implementation_time:""});
  const [solutionImages, setSolutionImages] = useState([]);
  const [solutionVideos, setSolutionVideos] = useState([]);
  const [solutionSaving, setSolutionSaving] = useState(false);
  const [implStatus, setImplStatus] = useState("IMPLEMENTATION_STARTED");
  const [implNote, setImplNote] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    try {
      setLoading(true);
      const { data } = await api.get(`/representative/problems/${problemId}`);
      setProblem(data);
      setStatus(data.status === "ASSIGNED" ? "IN_PROGRESS" : data.status);
    } catch (err) { setError(err.response?.data?.detail || "Unable to load assigned problem."); }
    finally { setLoading(false); }
  }
  useEffect(() => { load(); }, [problemId]);

  async function updateStatus() {
    try { setSaving(true); await api.put(`/representative/problems/${problemId}/status`, { status, note }); setNote(""); await load(); }
    catch (err) { alert(err.response?.data?.detail || "Unable to update status."); }
    finally { setSaving(false); }
  }
  async function addComment() {
    if (!comment.trim()) return;
    try { setSaving(true); await api.post(`/collaboration/problems/${problemId}/comments`, { comment }); setComment(""); await load(); }
    catch (err) { alert(err.response?.data?.detail || "Unable to add comment."); }
    finally { setSaving(false); }
  }

  async function proposeSolution() {
    if (!solution.title.trim() || !solution.description.trim()) return alert("Solution title and description are required.");
    try {
      setSolutionSaving(true);
      const form = new FormData();
      form.append("solution_data", JSON.stringify(solution));
      solutionImages.forEach(f => form.append("images", f));
      solutionVideos.forEach(f => form.append("videos", f));
      await api.post(`/representative/problems/${problemId}/solutions`, form);
      setSolution({title:"",description:"",benefits:"",estimated_cost:"",required_resources:"",implementation_time:""});
      setSolutionImages([]); setSolutionVideos([]);
      await load();
      alert("Solution proposed successfully.");
    } catch (err) { alert(err.response?.data?.detail || "Unable to propose solution."); }
    finally { setSolutionSaving(false); }
  }

  async function implementationUpdate() {
    if (!implNote.trim()) return alert("Add an implementation note.");
    try {
      setSolutionSaving(true);
      const current = (problem.solutions || []).find(s => s.status !== "REJECTED");
      if (!current) return alert("Propose a solution first.");
      await api.post(`/solutions/${current.id}/implementation-updates`, {status: implStatus, note: implNote});
      setImplNote(""); await load();
    } catch (err) { alert(err.response?.data?.detail || "Unable to update implementation."); }
    finally { setSolutionSaving(false); }
  }

  if (loading) return <main className="page"><div className="panel">Loading problem...</div></main>;
  if (!problem) return <main className="page"><div className="panel"><div className="error">{error || "Problem not found."}</div></div></main>;

  return <main className="page">
    <button className="btn secondary back-button" onClick={() => navigate("/representative/problems")}>← Assigned Problems</button>
    {error && <div className="error">{error}</div>}
    <div className="collab-layout">
      <section className="panel">
        <div className="problem-card-head"><div><span className="problem-category">{problem.category}</span><h1>{problem.title}</h1></div><span className="problem-status">{String(problem.status).replaceAll("_"," ")}</span></div>
        <p className="problem-description">{problem.description}</p>
        <div className="detail-grid">
          <div><span>Reported By</span><strong>{problem.reporter?.name}</strong></div><div><span>Priority</span><strong>{problem.priority}</strong></div>
          <div><span>Reporter Email</span><strong>{problem.reporter?.email}</strong></div><div><span>Submitted</span><strong>{new Date(problem.created_at).toLocaleString()}</strong></div>
          <div className="detail-full"><span>Address</span><strong>{problem.address || "-"}</strong></div><div><span>GPS</span><strong>{problem.latitude && problem.longitude ? `${problem.latitude}, ${problem.longitude}` : "Not provided"}</strong></div>
        </div>
        {problem.media?.length > 0 && <><hr/><h2>Evidence</h2><div className="problem-media-grid">{problem.media.map(m => <div className="problem-media" key={m.id}>{m.media_type === "IMAGE" ? <img src={m.url} alt={m.original_filename || "Evidence"} /> : <video src={m.url} controls />}</div>)}</div></>}
        <hr/><h2>Progress Timeline</h2><div className="problem-timeline">
          <div className="timeline-step active"><strong>SUBMITTED</strong><span>{new Date(problem.created_at).toLocaleString()}</span></div>
          {problem.timeline?.map(h => <div className="timeline-step active" key={h.id}><strong>{String(h.status).replaceAll("_"," ")}</strong><span>{h.note || "Status updated"} · {h.changed_by?.name} · {new Date(h.created_at).toLocaleString()}</span></div>)}
        </div>
        <hr/><h2>Collaboration Comments</h2>
        {(problem.comments || []).map(c => <div className="comment-card" key={c.id}><strong>{c.user?.name} · {c.user?.role}</strong><p>{c.comment}</p><small>{new Date(c.created_at).toLocaleString()}</small></div>)}
        <div className="comment-compose"><textarea rows="3" value={comment} onChange={e => setComment(e.target.value)} placeholder="Share progress, findings or questions..." /><button className="btn primary" disabled={saving} onClick={addComment}>Add Comment</button></div>

        <hr/><h2>Solution Proposal</h2>
        {(problem.solutions || []).map(s => <div className="solution-card" key={s.id}>
          <div className="solution-head"><div><span className="problem-category">SOLUTION</span><h3>{s.title}</h3></div><span className="problem-status">{String(s.status).replaceAll("_"," ")}</span></div>
          <p>{s.description}</p>
          <div className="detail-grid"><div><span>Benefits</span><strong>{s.benefits || "-"}</strong></div><div><span>Estimated Cost</span><strong>{s.estimated_cost || "-"}</strong></div><div><span>Resources</span><strong>{s.required_resources || "-"}</strong></div><div><span>Time</span><strong>{s.implementation_time || "-"}</strong></div></div>
          {s.media?.length > 0 && <div className="problem-media-grid">{s.media.map(m => <div className="problem-media" key={m.id}>{m.media_type === "IMAGE" ? <img src={m.url} alt={m.original_filename || "Solution evidence"} /> : <video src={m.url} controls />}</div>)}</div>}
          {s.feedback?.map(f => <div className="comment-card" key={f.id}><strong>{f.user?.name} · {f.decision}</strong><p>{f.feedback}</p></div>)}
        </div>)}
        <div className="solution-form">
          <h3>Propose a Solution</h3>
          <div className="grid-2">
            <label>Title<input value={solution.title} onChange={e=>setSolution({...solution,title:e.target.value})}/></label>
            <label>Estimated Cost<input value={solution.estimated_cost} onChange={e=>setSolution({...solution,estimated_cost:e.target.value})}/></label>
            <label className="full-width">Description<textarea value={solution.description} onChange={e=>setSolution({...solution,description:e.target.value})}/></label>
            <label>Benefits<textarea value={solution.benefits} onChange={e=>setSolution({...solution,benefits:e.target.value})}/></label>
            <label>Required Resources<textarea value={solution.required_resources} onChange={e=>setSolution({...solution,required_resources:e.target.value})}/></label>
            <label>Implementation Time<input value={solution.implementation_time} onChange={e=>setSolution({...solution,implementation_time:e.target.value})}/></label>
          </div>
          <label>Supporting Images<input type="file" accept="image/*" multiple onChange={e=>setSolutionImages([...e.target.files])}/></label>
          <label>Supporting Videos<input type="file" accept="video/*" multiple onChange={e=>setSolutionVideos([...e.target.files])}/></label>
          <button className="btn primary" disabled={solutionSaving} onClick={proposeSolution}>{solutionSaving ? "Saving..." : "Submit Solution Proposal"}</button>
        </div>
      </section>
      <aside className="panel collab-side"><h2>Update Progress</h2>
        <label>Status<select value={status} onChange={e => setStatus(e.target.value)}>{statuses.map(s => <option key={s} value={s}>{s.replaceAll("_"," ")}</option>)}</select></label>
        <label>Progress note<textarea rows="5" value={note} onChange={e => setNote(e.target.value)} placeholder="Describe what has been done or what happens next..." /></label>
        <button className="btn primary full-button" disabled={saving} onClick={updateStatus}>Update Status</button>
        <hr/><h3>Assignment</h3>
        {problem.assignment && <div className="assignment-card"><strong>{problem.assignment.assignee.name}</strong><span>{problem.assignment.organization_role}</span><span>{problem.assignment.assignee.organization || ""}</span><small>{problem.assignment.remarks || "No instructions from admin."}</small></div>}
        <hr/><h3>Implementation</h3>
        <label>Status<select value={implStatus} onChange={e=>setImplStatus(e.target.value)}>
          <option value="IMPLEMENTATION_STARTED">Implementation Started</option><option value="IMPLEMENTATION_IN_PROGRESS">Implementation In Progress</option><option value="IMPLEMENTED">Implemented</option><option value="VERIFIED">Citizen Verified</option>
        </select></label>
        <label>Implementation note<textarea rows="4" value={implNote} onChange={e=>setImplNote(e.target.value)} placeholder="Describe the implementation work..." /></label>
        <button className="btn primary full-button" disabled={solutionSaving} onClick={implementationUpdate}>Save Implementation Update</button>
      </aside>
    </div>
  </main>;
}
