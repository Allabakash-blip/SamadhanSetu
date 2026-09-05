import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";
import GoogleLoginButton from "../components/GoogleLoginButton";

export default function Login() {
  const [form,setForm]=useState({email:"",password:""});
  const [error,setError]=useState("");
  const {saveSession}=useAuth();
  const navigate=useNavigate();

  async function submit(e) {
    e.preventDefault(); setError("");
    try {
      const {data}=await api.post("/auth/login",form);
      saveSession(data);
      navigate(data.user.account_status==="INCOMPLETE" ? "/complete-profile" : data.user.role === "ADMIN" ? "/admin" : "/dashboard");
    } catch(err) { setError(err.response?.data?.detail||"Login failed"); }
  }

  return <main className="auth-page"><div className="auth-card">
    <div className="eyebrow">SMART INDIA HACKATHON 2026</div>
    <h1>Welcome back</h1><p className="muted">Social Innovation Collaboration Portal</p>
    {error&&<div className="error">{error}</div>}
    <form onSubmit={submit}>
      <label>Email<input type="email" required value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/></label>
      <label>Password<input type="password" required value={form.password} onChange={e=>setForm({...form,password:e.target.value})}/></label>
      <button className="btn primary full">Login</button>
    </form>
    <div className="divider"><span>OR</span></div>
    <GoogleLoginButton/>
    <p className="center muted">New here? <Link to="/register">Create an account</Link></p>
  </div></main>;
}
