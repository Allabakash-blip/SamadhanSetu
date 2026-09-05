import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function GoogleLoginButton() {
  const container = useRef(null);
  const { saveSession } = useAuth();
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    let attempts = 0;
    const init = () => {
      if (!window.google?.accounts?.id || !container.current) {
        if (attempts++ < 30) setTimeout(init, 300);
        return;
      }
      const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
      if (!clientId) { setError("Google Client ID is not configured."); return; }

      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: async (response) => {
          try {
            const { data } = await api.post("/auth/google", { credential: response.credential });
            saveSession(data);
            navigate(data.user.account_status === "INCOMPLETE" ? "/complete-profile" : data.user.role === "ADMIN" ? "/admin" : "/dashboard");
          } catch (err) {
            setError(err.response?.data?.detail || "Google login failed.");
          }
        },
      });
      container.current.innerHTML = "";
      window.google.accounts.id.renderButton(container.current, {
        theme: "outline", size: "large", width: 360, text: "continue_with"
      });
    };
    init();
  }, [saveSession]);

  return <div><div ref={container}></div>{error && <div className="error small">{error}</div>}</div>;
}