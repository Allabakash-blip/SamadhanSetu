import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

const implementationStatuses = [
  ["IMPLEMENTATION_STARTED", "Implementation Started"],
  ["IMPLEMENTATION_IN_PROGRESS", "Implementation In Progress"],
  ["IMPLEMENTED", "Implemented"],
];

export default function IndustrySupport(){
 const navigate=useNavigate();
 const [data,setData]=useState({offers:[],partnerships:[]});
 const [loading,setLoading]=useState(true);
 const [error,setError]=useState("");
 const [busy,setBusy]=useState(null);
 const [progress,setProgress]=useState({});
 const [openProgress,setOpenProgress]=useState(null);

 async function load(){
  try{
   setLoading(true);
   const r=await api.get("/industry/support");
   setData(r.data);
   const active=(r.data.partnerships||[]).filter(x=>x.status==="ACTIVE");
   const results=await Promise.all(active.map(async x=>{
    try{
     const rr=await api.get(`/industry/partnerships/${x.id}/implementation`);
     return [x.id,rr.data];
    }catch(e){ return [x.id,{solution:null,updates:[]}]; }
   }));
   setProgress(Object.fromEntries(results));
  }catch(e){
   setError(e.response?.data?.detail||"Unable to load support activity.");
  }finally{setLoading(false);}
 }

 useEffect(()=>{load()},[]);

 async function complete(id){
  try{
   await api.put(`/industry/partnerships/${id}/status`,{status:"COMPLETED"});
   await load();
  }catch(e){alert(e.response?.data?.detail||"Unable to update partnership.");}
 }

 async function saveProgress(id){
  const item=progress[id]||{};
  const form=item.form||{status:"IMPLEMENTATION_STARTED",note:""};
  if(form.note.trim().length<5){alert("Add an implementation note of at least 5 characters.");return;}
  try{
   setBusy(id);
   await api.post(`/industry/partnerships/${id}/implementation-updates`,{
    status:form.status,
    note:form.note.trim()
   });
   alert("Implementation progress saved.");
   await load();
  }catch(e){
   const d=e.response?.data?.detail;
   alert(Array.isArray(d)?d.map(x=>`${x.loc?.join(".")||"field"}: ${x.msg}`).join("\n"):(d||"Unable to save implementation progress."));
  }finally{setBusy(null);}
 }

 function updateForm(id,key,value){
  setProgress(prev=>({...prev,[id]:{...(prev[id]||{}),form:{...((prev[id]||{}).form||{status:"IMPLEMENTATION_STARTED",note:""}),[key]:value}}}));
 }

 if(loading)return <main className="page"><div className="panel">Loading support activity...</div></main>;

 return <main className="page">
  <div className="dashboard-head">
   <div><div className="eyebrow">INDUSTRY PARTNERSHIP · IMPLEMENTATION</div><h1>My Support</h1><p className="muted">Track support offers, active partnerships and implementation progress.</p></div>
   <button className="btn secondary" onClick={()=>navigate("/dashboard")}>← Dashboard</button>
  </div>
  {error&&<div className="error">{error}</div>}

  <section className="panel">
   <div className="admin-section-header"><div><h2>Support Offers</h2><p className="muted">Offers submitted to citizen challenges.</p></div><button className="btn primary" onClick={()=>navigate("/industry/projects")}>Find Projects →</button></div>
   {data.offers.length===0?<div className="empty-state"><strong>No support offers yet</strong><p>Browse available projects and offer practical support.</p></div>:
   <div className="industry-offer-grid">{data.offers.map(o=><article className="industry-offer-card" key={o.id}>
    <div className="problem-card-head"><div><span className="problem-category">{o.support_type.replaceAll("_"," ")}</span><h3>{o.title}</h3></div><span className="problem-status">{o.status.replaceAll("_"," ")}</span></div>
    <p><strong>{o.problem_title}</strong> · {o.problem_category}</p><p>{o.description}</p><small>{o.amount||"No funding amount"} · {o.duration||"Duration not specified"}</small>
   </article>)}</div>}
  </section>

  <section className="panel">
   <div className="admin-section-header"><div><h2>Active Partnerships</h2><p className="muted">Accepted support relationships contributing to project delivery.</p></div></div>
   {data.partnerships.length===0?<div className="empty-state"><strong>No active partnerships</strong><p>When an admin approves one of your support offers, the partnership will appear here.</p></div>:
   <div className="industry-offer-grid">{data.partnerships.map(x=>{
    const p=progress[x.id]||{solution:null,updates:[]};
    const form=p.form||{status:"IMPLEMENTATION_STARTED",note:""};
    return <article className="industry-offer-card" key={x.id}>
     <div className="problem-card-head"><div><span className="problem-category">{x.support_type.replaceAll("_"," ")}</span><h3>{x.problem_title}</h3></div><span className="problem-status">{x.status}</span></div>
     <p>{x.scope}</p>
     <small>Started {new Date(x.started_at).toLocaleString()}</small>

     {x.status==="ACTIVE"&&<div className="implementation-box">
      <div className="implementation-head"><strong>Implementation Progress</strong><span className="muted">{p.solution?`Solution: ${p.solution.title}`:"Waiting for an approved solution"}</span></div>
      {p.updates?.length>0&&<div className="progress-history">{p.updates.slice().reverse().map(u=><div className="progress-item" key={u.id}><strong>{u.status.replaceAll("_"," ")}</strong><span>{new Date(u.created_at).toLocaleString()}</span><p>{u.note}</p></div>)}</div>}
      {p.solution&&<button className="btn secondary" onClick={()=>setOpenProgress(openProgress===x.id?null:x.id)}>{openProgress===x.id?"Close":"Add Progress Update"}</button>}
      {openProgress===x.id&&p.solution&&<div className="solution-form">
       <label>Implementation Status<select value={form.status} onChange={e=>updateForm(x.id,"status",e.target.value)}>{implementationStatuses.map(([v,l])=><option key={v} value={v}>{l}</option>)}</select></label>
       <label>Progress Note<textarea rows="5" value={form.note} onChange={e=>updateForm(x.id,"note",e.target.value)} placeholder="Describe work completed, field testing, equipment installed, deployment progress, etc."/></label>
       <button className="btn primary" disabled={busy===x.id} onClick={()=>saveProgress(x.id)}>{busy===x.id?"Saving...":"Save Progress Update"}</button>
      </div>}
      {!p.solution&&<div className="notice">An approved university solution is required before implementation updates can be recorded.</div>}
      {p.solution?.status==="IMPLEMENTED"&&<div className="success-notice">Solution marked implemented. Citizen verification can now complete the impact workflow.</div>}
     </div>}

     {x.status==="ACTIVE"&&<button className="btn secondary" onClick={()=>complete(x.id)}>Mark Partnership Completed</button>}
     {x.status==="COMPLETED"&&<div className="success-notice">Partnership completed.</div>}
    </article>
   })}</div>}
  </section>
 </main>
}
