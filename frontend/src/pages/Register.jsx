import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

const roles=[
  ["CITIZEN","Individual Citizen"],
  ["COMMUNITY_GROUP","Community Group"],
  ["PRI","Panchayati Raj Institution (PRI)"],
  ["ULB","Urban Local Body (ULB)"],
  ["UNIVERSITY","University / Higher Education"],
  ["INDUSTRY","Industry / Startup / MSME / CSR"],
  ["GOVERNMENT","Government Department"]
];

export default function Register() {
  const [form,setForm]=useState({name:"",email:"",phone:"",password:"",confirm:"",role:"CITIZEN"});
  const [error,setError]=useState("");
  const {saveSession}=useAuth(); const navigate=useNavigate();

  async function submit(e) {
    e.preventDefault(); setError("");
    if(form.password!==form.confirm) return setError("Passwords do not match");
    try {
      const {data}=await api.post("/auth/register",form);
      saveSession(data); navigate("/complete-profile");
    } catch(err) { setError(err.response?.data?.detail||"Registration failed"); }
  }

  return <main className="auth-page"><div className="auth-card wide">
    <div className="eyebrow">CREATE ACCOUNT</div>
    <h1>Join the innovation network</h1>
    <p className="muted">Basic account first; role-specific profile information comes next.</p>
    {error&&<div className="error">{error}</div>}
    <form onSubmit={submit}><div className="grid-2">
      <label>Full Name<input required value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/></label>
      <label>Mobile Number<input value={form.phone} onChange={e=>setForm({...form,phone:e.target.value})}/></label>
      <label>Email<input type="email" required value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/></label>
      <label>Role<select value={form.role} onChange={e=>setForm({...form,role:e.target.value})}>{roles.map(([v,l])=><option key={v} value={v}>{l}</option>)}</select></label>
      <label>Password<input type="password" minLength="8" required value={form.password} onChange={e=>setForm({...form,password:e.target.value})}/></label>
      <label>Confirm Password<input type="password" minLength="8" required value={form.confirm} onChange={e=>setForm({...form,confirm:e.target.value})}/></label>
    </div><button className="btn primary full">Create Account</button></form>
    <p className="center muted">Already have an account? <Link to="/login">Login</Link></p>
  </div></main>;
}
