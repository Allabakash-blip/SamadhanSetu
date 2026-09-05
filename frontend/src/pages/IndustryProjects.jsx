import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function IndustryProjects() {
  const navigate = useNavigate();
  const [projects,setProjects]=useState([]); const [loading,setLoading]=useState(true); const [error,setError]=useState("");
  useEffect(()=>{ api.get("/industry/projects").then(r=>setProjects(r.data)).catch(e=>setError(e.response?.data?.detail||"Unable to load available projects.")).finally(()=>setLoading(false)); },[]);
  if(loading) return <main className="page"><div className="panel">Loading available projects...</div></main>;
  return <main className="page">
    <div className="dashboard-head"><div><div className="eyebrow">INDUSTRY PARTNERSHIP · MILESTONE 8</div><h1>Available Projects</h1><p className="muted">Discover validated societal challenges and offer mentoring, funding, prototyping, testing or technology support.</p></div><button className="btn secondary" onClick={()=>navigate("/dashboard")}>← Dashboard</button></div>
    {error&&<div className="error">{error}</div>}
    {projects.length===0 ? <div className="panel empty-state"><strong>No projects available</strong><p>Validated and active citizen challenges will appear here when they are ready for industry collaboration.</p></div> :
      <div className="problem-list">{projects.map(p=><article className="problem-card" key={p.id} onClick={()=>navigate(`/industry/projects/${p.id}`)}>
        <div className="problem-card-head"><div><span className="problem-category">{p.category}</span><h2>{p.title}</h2></div><span className="problem-status">{String(p.status).replaceAll("_"," ")}</span></div>
        <p>{p.description}</p><div className="problem-card-footer"><span>Priority: <strong>{p.priority}</strong></span><span>Affected: <strong>{p.affected_people ?? 0}</strong></span>{p.offer_status&&<span>Offer: <strong>{p.offer_status}</strong></span>}</div>
      </article>)}</div>}
  </main>;
}
