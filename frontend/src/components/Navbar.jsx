import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  if (!user) return null;
  return (
    <header className="navbar">
      <Link className="brand" to="/dashboard">SIH Portal</Link>
      <div className="nav-right">
        <span className="role-pill">{user.role}</span>
        <Link className="nav-link" to="/notifications">Notifications</Link><span className="nav-user">{user.name}</span>
        <button className="btn ghost" onClick={() => {logout(); navigate("/login");}}>Logout</button>
      </div>
    </header>
  );
}
