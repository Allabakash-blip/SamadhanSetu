import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function MyProblems() {
  const navigate = useNavigate();
  const { user } = useAuth();

  const [problems, setProblems] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  useEffect(() => {
    api
      .get("/problems/mine")
      .then((response) => {
        setProblems(response.data);
      })
      .catch((err) => {
        setError(
          err.response?.data?.detail ||
            "Unable to load your problems."
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <main className="page">
      <div className="dashboard-head">
        <div>
          <div className="eyebrow">
            {user?.role === "GOVERNMENT" ? "GOVERNMENT DEPARTMENT" : user?.role === "PRI" ? "PANCHAYATI RAJ INSTITUTION" : user?.role === "ULB" ? "URBAN LOCAL BODY" : user?.role === "COMMUNITY_GROUP" ? "COMMUNITY GROUP" : "CITIZEN"}
          </div>

          <h1>My Problems</h1>

          <p className="muted">
            Track societal challenges submitted by you or your represented organization.
          </p>
        </div>

        <button
          className="btn primary"
          onClick={() =>
            navigate("/report-problem")
          }
        >
          + Report Problem
        </button>
      </div>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {loading ? (
        <div className="panel">
          Loading...
        </div>
      ) : problems.length === 0 ? (
        <div className="panel empty-state">
          <strong>
            No problems reported yet
          </strong>

          <p>
            Report a local problem to start
            contributing to the platform.
          </p>

          <button
            className="btn primary"
            onClick={() =>
              navigate("/report-problem")
            }
          >
            Report Your First Problem
          </button>
        </div>
      ) : (
        <div className="problem-list">
          {problems.map((problem) => (
            <article
              className="problem-card"
              key={problem.id}
              onClick={() =>
                navigate(
                  `/my-problems/${problem.id}`
                )
              }
            >
              <div className="problem-card-head">
                <div>
                  <span className="problem-category">
                    {problem.category}
                  </span>

                  <h2>
                    {problem.title}
                  </h2>
                </div>

                <span
                  className={`problem-status status-${problem.status.toLowerCase()}`}
                >
                  {problem.status}
                </span>
              </div>

              <p>
                {problem.description}
              </p>

              <div className="problem-card-footer">
                <span>
                  Priority:{" "}
                  <strong>
                    {problem.priority}
                  </strong>
                </span>

                <span>
                  Submitted:{" "}
                  {new Date(
                    problem.created_at
                  ).toLocaleDateString()}
                </span>
              </div>
            </article>
          ))}
        </div>
      )}
    </main>
  );
}