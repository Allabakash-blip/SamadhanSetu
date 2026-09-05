import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";
import LocationFields from "../components/LocationFields";

export default function CompleteProfile() {
  const {user,refreshMe}=useAuth(); const navigate=useNavigate();
  const [picture,setPicture]=useState(null); const [error,setError]=useState("");
  const [form,setForm]=useState({
    role:user?.role||"CITIZEN",phone:user?.phone||"",address_line:"",
    state_id:null,district_id:null,block_id:null,village_id:null,pincode:"",
    latitude:null,longitude:null,university_name:"",university_type:"",
    registration_number:"",department:"",designation:"",city:"",expertise:"",
    company_name:"",company_type:"",website:"",available_support:"",
    government_department:"",official_id:""
  });

  async function submit(e) {
    e.preventDefault(); setError("");
    try {
      await api.post("/auth/complete-profile",form);
      if(picture) {
        const fd=new FormData(); fd.append("file",picture);
        await api.post("/auth/profile-picture",fd,{headers:{"Content-Type":"multipart/form-data"}});
      }
      await refreshMe(); navigate("/dashboard");
    } catch(err) { setError(err.response?.data?.detail||"Could not complete profile"); }
  }

  return <main className="page"><div className="page-card">
    <div className="eyebrow">STEP 2 OF 2</div><h1>Complete your profile</h1>
    <p className="muted">These details will later support location analytics and institutional matching.</p>
    {error&&<div className="error">{error}</div>}
    <form onSubmit={submit}>
      <label>Profile Picture<input type="file" accept="image/png,image/jpeg,image/webp" onChange={e=>setPicture(e.target.files?.[0]||null)}/></label>
      <label>Mobile Number<input value={form.phone} onChange={e=>setForm({...form,phone:e.target.value})}/></label>

      {(form.role==="CITIZEN"||form.role==="UNIVERSITY"||form.role==="INDUSTRY")&&<LocationFields form={form} setForm={setForm}/>}

      {form.role==="UNIVERSITY"&&<section className="form-section">
        <div className="section-title">University information</div><div className="grid-2">
          <label>University Name<input required value={form.university_name} onChange={e=>setForm({...form,university_name:e.target.value})}/></label>
          <label>University Type<input value={form.university_type} onChange={e=>setForm({...form,university_type:e.target.value})}/></label>
          <label>Registration / Institution ID<input value={form.registration_number} onChange={e=>setForm({...form,registration_number:e.target.value})}/></label>
          <label>Department<input value={form.department} onChange={e=>setForm({...form,department:e.target.value})}/></label>
          <label>Designation<input value={form.designation} onChange={e=>setForm({...form,designation:e.target.value})}/></label>
          <label>City<input value={form.city} onChange={e=>setForm({...form,city:e.target.value})}/></label>
        </div>
        <label>Areas of Expertise<textarea value={form.expertise} onChange={e=>setForm({...form,expertise:e.target.value})} placeholder="AI, IoT, water resources, agriculture, healthcare..."/></label>
        <div className="notice">University accounts are PENDING until administrator verification.</div>
      </section>}

      {form.role==="INDUSTRY"&&<section className="form-section">
        <div className="section-title">Industry information</div><div className="grid-2">
          <label>Company Name<input required value={form.company_name} onChange={e=>setForm({...form,company_name:e.target.value})}/></label>
          <label>Company Type<input value={form.company_type} onChange={e=>setForm({...form,company_type:e.target.value})}/></label>
          <label>Website<input value={form.website} onChange={e=>setForm({...form,website:e.target.value})}/></label>
          <label>City<input value={form.city} onChange={e=>setForm({...form,city:e.target.value})}/></label>
        </div>
        <label>Areas of Expertise<textarea value={form.expertise} onChange={e=>setForm({...form,expertise:e.target.value})}/></label>
        <label>Available Support<textarea value={form.available_support} onChange={e=>setForm({...form,available_support:e.target.value})} placeholder="Mentoring, funding, hardware, testing..."/></label>
        <div className="notice">Industry accounts are PENDING until administrator verification.</div>
      </section>}

      {form.role==="GOVERNMENT"&&<section className="form-section">
        <div className="section-title">Government information</div><div className="grid-2">
          <label>Department<input required value={form.government_department} onChange={e=>setForm({...form,government_department:e.target.value})}/></label>
          <label>Designation<input value={form.designation} onChange={e=>setForm({...form,designation:e.target.value})}/></label>
          <label>Official ID<input value={form.official_id} onChange={e=>setForm({...form,official_id:e.target.value})}/></label>
        </div>
        <div className="notice">Government accounts are PENDING until administrator verification.</div>
      </section>}

      <button className="btn primary full">Save Profile & Continue</button>
    </form>
  </div></main>;
}
