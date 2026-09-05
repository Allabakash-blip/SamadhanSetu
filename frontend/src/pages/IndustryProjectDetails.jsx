import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";

const supportTypes=["MENTORING","FUNDING","TECHNICAL","PROTOTYPING","TESTING","TECHNOLOGY_TRANSFER","CSR","OTHER"];

export default function IndustryProjectDetails(){
 const {problemId}=useParams(); const navigate=useNavigate(); const [p,setP]=useState(null); const [loading,setLoading]=useState(true); const [saving,setSaving]=useState(false); const [error,setError]=useState("");
 const [form,setForm]=useState({support_type:"TECHNICAL",title:"",description:"",amount:"",duration:""});
 async function load(){try{setLoading(true);const r=await api.get(`/industry/projects/${problemId}`);setP(r.data);if(r.data.existing_offer?.status==="PROPOSED"){setForm({support_type:r.data.existing_offer.support_type,title:r.data.existing_offer.title,description:r.data.existing_offer.description,amount:r.data.existing_offer.amount||"",duration:r.data.existing_offer.duration||""});}}catch(e){setError(e.response?.data?.detail||"Unable to load project.")}finally{setLoading(false)}}
 useEffect(()=>{load()},[problemId]);
 async function submit(){
  const title=form.title.trim(), description=form.description.trim();
  if(!title||!description)return alert("Add a support title and description.");
  if(title.length<3)return alert("Offer title must be at least 3 characters.");
  if(description.length<10)return alert("Support description must be at least 10 characters.");
  try{
   setSaving(true);
   await api.post(`/industry/projects/${problemId}/offers`,{
    support_type:form.support_type,
    title,
    description,
    amount:form.amount.trim()||null,
    duration:form.duration.trim()||null
   });
   await load();
   alert("Support offer submitted to the platform.");
  }catch(e){
   const detail=e.response?.data?.detail;
   let message="Unable to submit support offer.";
   if(Array.isArray(detail)){
    message=detail.map(x=>`${x.loc?.join(".")||"field"}: ${x.msg}`).join("\n");
   }else if(typeof detail==="string") message=detail;
   alert(message);
  }finally{setSaving(false)}
 }
 if(loading)return <main className="page"><div className="panel">Loading project...</div></main>;
 if(!p)return <main className="page"><div className="panel"><div className="error">{error||"Project not found."}</div></div></main>;
 const offer=p.existing_offer;
 return <main className="page">
  <button className="btn secondary back-button" onClick={()=>navigate("/industry/projects")}>← Available Projects</button>{error&&<div className="error">{error}</div>}
  <div className="collab-layout">
   <section className="panel"><div className="problem-card-head"><div><span className="problem-category">{p.category}</span><h1>{p.title}</h1></div><span className="problem-status">{String(p.status).replaceAll("_"," ")}</span></div>
    <p className="problem-description">{p.description}</p><div className="detail-grid"><div><span>Priority</span><strong>{p.priority}</strong></div><div><span>Affected People</span><strong>{p.affected_people??0}</strong></div><div className="detail-full"><span>Address</span><strong>{p.address||"-"}</strong></div><div><span>Reported</span><strong>{new Date(p.created_at).toLocaleString()}</strong></div></div>
    <hr/><h2>Why industry collaboration?</h2><p className="muted">Industry partners can contribute practical mentoring, funding, prototyping, testing, CSR support and technology transfer to move a university-led solution toward deployment.</p>
    {p.assignment&&<div className="assignment-card"><strong>Current institutional lead</strong><span>{p.assignment.organization_role}</span></div>}
    {p.partnerships?.length>0&&<><hr/><h2>Active Partnerships</h2>{p.partnerships.map(x=><div className="solution-card" key={x.id}><div className="solution-head"><div><span className="problem-category">{x.support_type.replaceAll("_"," ")}</span><h3>{x.industry.organization}</h3></div><span className="problem-status">{x.status}</span></div><p>{x.scope}</p></div>)}</>}
   </section>
   <aside className="panel collab-side"><h2>Offer Industry Support</h2>{offer&&<div className={`notice ${offer.status==="ACCEPTED"?"success-notice":""}`}>Existing offer: <strong>{offer.status.replaceAll("_"," ")}</strong></div>}
    {(!offer||offer.status==="REJECTED")&&<div className="solution-form">
      <label>Support Type<select value={form.support_type} onChange={e=>setForm({...form,support_type:e.target.value})}>{supportTypes.map(x=><option key={x}>{x.replaceAll("_"," ")}</option>)}</select></label>
      <label>Offer Title<input value={form.title} onChange={e=>setForm({...form,title:e.target.value})} placeholder="e.g. Prototype and field testing support"/></label>
      <label>What will you provide?<textarea rows="6" value={form.description} onChange={e=>setForm({...form,description:e.target.value})} placeholder="Describe mentoring, funding, equipment, testing, deployment or technology transfer support..."/></label>
      <label>Funding / Estimated Amount<input value={form.amount} onChange={e=>setForm({...form,amount:e.target.value})} placeholder="Optional"/></label>
      <label>Duration<input value={form.duration} onChange={e=>setForm({...form,duration:e.target.value})} placeholder="e.g. 3 months"/></label>
      <button className="btn primary full-button" disabled={saving} onClick={submit}>{saving?"Submitting...":"Submit Support Offer"}</button>
    </div>}
    {offer?.status==="ACCEPTED"&&<p className="muted">This support offer has been accepted. The partnership is active and visible under My Support.</p>}
   </aside>
  </div>
 </main>;
}
