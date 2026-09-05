import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Register from "./pages/Register";
import CompleteProfile from "./pages/CompleteProfile";
import Dashboard from "./pages/Dashboard";
import AdminDashboard from "./pages/AdminDashboard";
import AdminUserDetails from "./pages/AdminUserDetails";
import ReportProblem from "./pages/ReportProblem";
import MyProblems from "./pages/MyProblems";
import ProblemDetails from "./pages/ProblemDetails";
import AdminProblems from "./pages/AdminProblems";
import AdminProblemDetails from "./pages/AdminProblemDetails";
import RepresentativeProblems from "./pages/RepresentativeProblems";
import RepresentativeProblemDetails from "./pages/RepresentativeProblemDetails";
import Notifications from "./pages/Notifications";
import AdminAnalytics from "./pages/AdminAnalytics";
import AdminIndustryPartnerships from "./pages/AdminIndustryPartnerships";
import IndustryProjects from "./pages/IndustryProjects";
import IndustryProjectDetails from "./pages/IndustryProjectDetails";
import IndustrySupport from "./pages/IndustrySupport";

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/complete-profile" element={<ProtectedRoute><CompleteProfile /></ProtectedRoute>} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/admin" element={<ProtectedRoute roles={["ADMIN"]}><AdminDashboard /></ProtectedRoute>} />
        <Route path="/admin/users/:userId" element={<ProtectedRoute roles={["ADMIN"]}><AdminUserDetails /></ProtectedRoute>} />
        <Route path="/admin/problems" element={<ProtectedRoute roles={["ADMIN"]}><AdminProblems /></ProtectedRoute>} />
        <Route path="/admin/problems/:problemId" element={<ProtectedRoute roles={["ADMIN"]}><AdminProblemDetails /></ProtectedRoute>} />
        <Route path="/admin/analytics" element={<ProtectedRoute roles={["ADMIN"]}><AdminAnalytics /></ProtectedRoute> } />
        <Route path="/admin/industry-partnerships" element={<ProtectedRoute roles={["ADMIN"]}><AdminIndustryPartnerships /></ProtectedRoute>} />
        <Route path="/report-problem" element={<ProtectedRoute roles={["CITIZEN","COMMUNITY_GROUP","PRI","ULB","GOVERNMENT"]}><ReportProblem /></ProtectedRoute>} />
        <Route path="/my-problems" element={<ProtectedRoute roles={["CITIZEN","COMMUNITY_GROUP","PRI","ULB","GOVERNMENT"]}><MyProblems /></ProtectedRoute>} />
        <Route path="/my-problems/:problemId" element={<ProtectedRoute roles={["CITIZEN","COMMUNITY_GROUP","PRI","ULB","GOVERNMENT"]}><ProblemDetails /></ProtectedRoute>} />
        <Route path="/representative/problems" element={<ProtectedRoute roles={["UNIVERSITY","INDUSTRY","GOVERNMENT"]}><RepresentativeProblems /></ProtectedRoute>} />
        <Route path="/representative/problems/:problemId" element={<ProtectedRoute roles={["UNIVERSITY","INDUSTRY","GOVERNMENT"]}><RepresentativeProblemDetails /></ProtectedRoute>} />
        <Route path="/industry/projects" element={<ProtectedRoute roles={["INDUSTRY"]}><IndustryProjects /></ProtectedRoute>} />
        <Route path="/industry/projects/:problemId" element={<ProtectedRoute roles={["INDUSTRY"]}><IndustryProjectDetails /></ProtectedRoute>} />
        <Route path="/industry/support" element={<ProtectedRoute roles={["INDUSTRY"]}><IndustrySupport /></ProtectedRoute>} />
        <Route path="/notifications" element={<ProtectedRoute><Notifications /></ProtectedRoute>} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </>
  );
}
