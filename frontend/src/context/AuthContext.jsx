import { createContext, useContext, useEffect, useState } from "react";
import api from "../services/api";
import React from 'react';
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem("sih_user")) || null; }
    catch { return null; }
  });

  function saveSession(data) {
    localStorage.setItem("sih_access_token", data.access_token);
    localStorage.setItem("sih_user", JSON.stringify(data.user));
    setUser(data.user);
  }

  function logout() {
    localStorage.removeItem("sih_access_token");
    localStorage.removeItem("sih_user");
    setUser(null);
  }

  async function refreshMe() {
    try {
      const { data } = await api.get("/auth/me");
      localStorage.setItem("sih_user", JSON.stringify(data));
      setUser(data);
    } catch {
      logout();
    }
  }

  useEffect(() => {
    if (localStorage.getItem("sih_access_token")) refreshMe();
  }, []);

  return <AuthContext.Provider value={{user, saveSession, logout, refreshMe}}>{children}</AuthContext.Provider>;
}

export function useAuth() { return useContext(AuthContext); }
