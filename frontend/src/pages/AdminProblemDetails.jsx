import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../services/api";

const statuses = [
  "SUBMITTED",
  "UNDER_REVIEW",
  "VALIDATED",
  "ASSIGNED",
  "IN_PROGRESS",
  "SOLUTION_PROPOSED",
  "PILOT",
  "IMPLEMENTED",
  "CLOSED",
  "REJECTED",
];

const priorities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];

function formatStatus(value) {
  return String(value || "").replaceAll("_", " ");
}

function formatFactorName(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function getScorePercentage(score, maxScore) {
  if (!maxScore) return 0;
  return Math.min(100, Math.max(0, (score / maxScore) * 100));
}

function getAvailabilityClass(status) {
  const value = String(status || "").toUpperCase();

  if (value === "AVAILABLE") return "available";
  if (value === "LIMITED") return "limited";
  if (value === "UNAVAILABLE") return "unavailable";

  return "available";
}

export default function AdminProblemDetails() {
  const { problemId } = useParams();
  const navigate = useNavigate();

  const [problem, setProblem] = useState(null);
  const [representatives, setRepresentatives] = useState([]);
  const [assigneeId, setAssigneeId] = useState("");
  const [remarks, setRemarks] = useState("");
  const [status, setStatus] = useState("");
  const [priority, setPriority] = useState("");
  const [note, setNote] = useState("");
  const [comment, setComment] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [matches, setMatches] = useState([]);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiLoaded, setAiLoaded] = useState(false);

  async function load() {
    try {
      setLoading(true);

      const [p, reps] = await Promise.all([
        api.get(`/admin/problems/${problemId}`),
        api.get("/admin/problem-representatives"),
      ]);

      setProblem(p.data);
      setRepresentatives(reps.data);
      setStatus(p.data.status);
      setPriority(p.data.priority);
      setAssigneeId(
        p.data.assignment?.assignee?.id?.toString() || ""
      );
      setRemarks(p.data.assignment?.remarks || "");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to load problem."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [problemId]);

  async function assign() {
    if (!assigneeId) {
      return alert("Select a verified representative.");
    }

    try {
      setSaving(true);

      await api.put(
        `/admin/problems/${problemId}/assign`,
        {
          assignee_id: Number(assigneeId),
          remarks,
        }
      );

      await load();

      alert("Problem assigned successfully.");
    } catch (err) {
      alert(
        err.response?.data?.detail ||
          "Unable to assign problem."
      );
    } finally {
      setSaving(false);
    }
  }

  async function updateProblem() {
    try {
      setSaving(true);

      await api.put(
        `/admin/problems/${problemId}/update`,
        {
          status,
          priority,
          note,
        }
      );

      setNote("");

      await load();

      alert("Problem updated successfully.");
    } catch (err) {
      alert(
        err.response?.data?.detail ||
          "Unable to update problem."
      );
    } finally {
      setSaving(false);
    }
  }

  async function addComment() {
    if (!comment.trim()) return;

    try {
      setSaving(true);

      await api.post(
        `/collaboration/problems/${problemId}/comments`,
        {
          comment,
        }
      );

      setComment("");

      await load();
    } catch (err) {
      alert(
        err.response?.data?.detail ||
          "Unable to add comment."
      );
    } finally {
      setSaving(false);
    }
  }

  async function runAiMatching() {
    try {
      setAiLoading(true);
      setError("");

      const { data } = await api.get(
        `/ai/problems/${problemId}/matches?limit=5`
      );

      setAiAnalysis(data.analysis);
      setMatches(data.matches || []);
      setAiLoaded(true);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to run AI classification and matching."
      );
    } finally {
      setAiLoading(false);
    }
  }

  if (loading) {
    return (
      <main className="page">
        <div className="panel">
          Loading problem...
        </div>
      </main>
    );
  }

  if (!problem) {
    return (
      <main className="page">
        <div className="panel">
          <div className="error">
            {error || "Problem not found."}
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="page">
      <button
        className="btn secondary back-button"
        onClick={() => navigate("/admin/problems")}
      >
        ← All Problems
      </button>

      {error && <div className="error">{error}</div>}

      <section className="panel ai-panel">
        <div className="ai-panel-head">
          <div>
            <span className="eyebrow">
              MILESTONE 7
            </span>

            <h2>
              🤖 AI Classification & Institutional Matching
            </h2>

            <p className="muted">
              Analyze the reported problem and rank
              approved organization representatives using
              transparent, explainable matching signals.
            </p>
          </div>

          <button
            className="btn primary"
            disabled={aiLoading}
            onClick={runAiMatching}
          >
            {aiLoading
              ? "Analyzing..."
              : aiLoaded
              ? "↻ Re-analyze"
              : "Run AI Analysis"}
          </button>
        </div>

        {aiLoaded && aiAnalysis && (
          <div className="ai-analysis-grid">
            <div className="ai-classification-card">
              <span className="ai-label">
                Predicted Category
              </span>

              <strong>
                {aiAnalysis.predicted_category}
              </strong>

              <div className="ai-confidence">
                <div className="ai-confidence-head">
                  <span>Confidence</span>
                  <b>{aiAnalysis.confidence}%</b>
                </div>

                <div className="analytics-track">
                  <div
                    className="analytics-fill"
                    style={{
                      width: `${aiAnalysis.confidence}%`,
                    }}
                  />
                </div>
              </div>
            </div>

            <div className="ai-classification-card">
              <span className="ai-label">
                Suggested Priority
              </span>

              <strong
                className={`priority-pill priority-${String(
                  aiAnalysis.priority
                ).toLowerCase()}`}
              >
                {aiAnalysis.priority}
              </strong>

              <p>{aiAnalysis.priority_reason}</p>
            </div>

            <div className="ai-classification-card">
              <span className="ai-label">
                Required Expertise
              </span>

              <div className="ai-tags">
                {(aiAnalysis.required_expertise || [])
                  .slice(0, 6)
                  .map((x) => (
                    <span key={x}>{x}</span>
                  ))}
              </div>
            </div>

            <div className="ai-classification-card">
              <span className="ai-label">
                Matched Keywords
              </span>

              <div className="ai-tags">
                {(aiAnalysis.matched_keywords || [])
                  .length ? (
                  aiAnalysis.matched_keywords.map((x) => (
                    <span key={x}>{x}</span>
                  ))
                ) : (
                  <span>
                    No strong keyword evidence
                  </span>
                )}
              </div>
            </div>
          </div>
        )}

        {aiLoaded && (
          <div className="ai-matches">
            <div className="ai-matches-head">
              <div>
                <h3>
                  Recommended Representatives
                </h3>

                <p className="muted">
                  Representatives are ranked using
                  expertise, category relevance, location,
                  organization capability, availability and
                  relevant experience.
                </p>
              </div>
            </div>

            {matches.length === 0 ? (
              <div className="ai-empty">
                No verified representative currently matches
                this problem. Approve organization accounts
                or update their expertise/location profiles.
              </div>
            ) : (
              <div className="ai-match-list">
                {matches.map((match) => {
                  const breakdown =
                    match.score_breakdown || {};

                  return (
                    <div
                      className="ai-match-card"
                      key={match.user_id}
                    >
                      <div className="ai-rank">
                        #{match.rank}
                      </div>

                      <div className="ai-match-main">
                        <strong>{match.name}</strong>

                        <span>
                          {match.organization ||
                            "Organization"}{" "}
                          · {match.role}
                        </span>

                        {/* Transparent Score Breakdown */}
                        <div
                          className="ai-score-breakdown"
                          style={{
                            marginTop: "14px",
                          }}
                        >
                          <div
                            style={{
                              display: "flex",
                              justifyContent:
                                "space-between",
                              alignItems: "center",
                              marginBottom: "8px",
                            }}
                          >
                            <strong>
                              Match Score Breakdown
                            </strong>

                            <span>
                              {match.score}/100
                            </span>
                          </div>

                          {Object.entries(breakdown).map(
                            ([factor, details]) => {
                              const score =
                                Number(
                                  details?.score || 0
                                );

                              const maxScore =
                                Number(
                                  details?.max_score || 0
                                );

                              const percentage =
                                getScorePercentage(
                                  score,
                                  maxScore
                                );

                              return (
                                <div
                                  key={factor}
                                  style={{
                                    marginBottom:
                                      "10px",
                                  }}
                                >
                                  <div
                                    style={{
                                      display: "flex",
                                      justifyContent:
                                        "space-between",
                                      gap: "12px",
                                      fontSize:
                                        "0.85rem",
                                      marginBottom:
                                        "4px",
                                    }}
                                  >
                                    <span>
                                      {formatFactorName(
                                        factor
                                      )}
                                    </span>

                                    <strong>
                                      {score}/{maxScore}
                                    </strong>
                                  </div>

                                  <div
                                    className="analytics-track"
                                    style={{
                                      height: "7px",
                                    }}
                                  >
                                    <div
                                      className="analytics-fill"
                                      style={{
                                        width: `${percentage}%`,
                                      }}
                                    />
                                  </div>

                                  {details?.matched_terms
                                    ?.length >
                                    0 && (
                                    <small
                                      className="muted"
                                      style={{
                                        display:
                                          "block",
                                        marginTop:
                                          "4px",
                                      }}
                                    >
                                      Matched:{" "}
                                      {details.matched_terms.join(
                                        ", "
                                      )}
                                    </small>
                                  )}

                                  {factor ===
                                    "availability" &&
                                    details?.status && (
                                      <small
                                        className={`availability-badge ${getAvailabilityClass(
                                          details.status
                                        )}`}
                                        style={{
                                          display:
                                            "inline-block",
                                          marginTop:
                                            "5px",
                                        }}
                                      >
                                        Availability:{" "}
                                        {
                                          details.status
                                        }
                                      </small>
                                    )}
                                </div>
                              );
                            }
                          )}
                        </div>

                        {/* Transparent Reasons */}
                        <div
                          className="ai-reasons"
                          style={{
                            marginTop: "14px",
                          }}
                        >
                          <strong
                            style={{
                              display: "block",
                              marginBottom: "6px",
                            }}
                          >
                            Why this match?
                          </strong>

                          {(match.match_reasons || [])
                            .length > 0 ? (
                            match.match_reasons.map(
                              (reason, index) => (
                                <small
                                  key={`${match.user_id}-reason-${index}`}
                                  style={{
                                    display: "block",
                                    marginBottom: "4px",
                                  }}
                                >
                                  ✓ {reason}
                                </small>
                              )
                            )
                          ) : (
                            <small className="muted">
                              No detailed matching
                              explanation available.
                            </small>
                          )}
                        </div>
                      </div>

                      <div className="ai-score">
                        <b>{match.score}%</b>
                        <span>match</span>

                        {match.availability_status && (
                          <small
                            className={`availability-badge ${getAvailabilityClass(
                              match.availability_status
                            )}`}
                            style={{
                              marginTop: "8px",
                              display: "inline-block",
                            }}
                          >
                            {match.availability_status}
                          </small>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}
      </section>

      <div className="collab-layout">
        <section className="panel">
          <div className="problem-card-head">
            <div>
              <span className="problem-category">
                {problem.category}
              </span>

              <h1>{problem.title}</h1>
            </div>

            <span className="problem-status">
              {formatStatus(problem.status)}
            </span>
          </div>

          <p className="problem-description">
            {problem.description}
          </p>

          <div className="detail-grid">
            <div>
              <span>Reporter</span>
              <strong>
                {problem.reporter?.name} (
                {problem.reporter?.email})
              </strong>
            </div>

            <div>
              <span>Priority</span>
              <strong>{problem.priority}</strong>
            </div>

            <div>
              <span>Affected People</span>
              <strong>
                {problem.affected_people ?? "-"}
              </strong>
            </div>

            <div>
              <span>Submitted</span>
              <strong>
                {new Date(
                  problem.created_at
                ).toLocaleString()}
              </strong>
            </div>

            <div className="detail-full">
              <span>Address</span>
              <strong>
                {problem.address || "-"}
              </strong>
            </div>

            <div>
              <span>GPS</span>
              <strong>
                {problem.latitude &&
                problem.longitude
                  ? `${problem.latitude}, ${problem.longitude}`
                  : "Not provided"}
              </strong>
            </div>
          </div>

          {problem.media?.length > 0 && (
            <>
              <hr />

              <h2>Evidence</h2>

              <div className="problem-media-grid">
                {problem.media.map((m) => (
                  <div
                    className="problem-media"
                    key={m.id}
                  >
                    {m.media_type === "IMAGE" ? (
                      <img
                        src={m.url}
                        alt={
                          m.original_filename ||
                          "Evidence"
                        }
                      />
                    ) : (
                      <video
                        src={m.url}
                        controls
                      />
                    )}
                  </div>
                ))}
              </div>
            </>
          )}

          <hr />

          <h2>Progress Timeline</h2>

          <div className="problem-timeline">
            <div className="timeline-step active">
              <strong>SUBMITTED</strong>

              <span>
                {new Date(
                  problem.created_at
                ).toLocaleString()}
              </span>
            </div>

            {problem.timeline?.map((h) => (
              <div
                className="timeline-step active"
                key={h.id}
              >
                <strong>
                  {formatStatus(h.status)}
                </strong>

                <span>
                  {h.note || "Status updated"} ·{" "}
                  {h.changed_by?.name} ·{" "}
                  {new Date(
                    h.created_at
                  ).toLocaleString()}
                </span>
              </div>
            ))}
          </div>

          <hr />

          <h2>Collaboration Comments</h2>

          <div className="comments-list">
            {(problem.comments || []).length ===
            0 ? (
              <p className="muted">
                No comments yet.
              </p>
            ) : (
              problem.comments.map((c) => (
                <div
                  className="comment-card"
                  key={c.id}
                >
                  <strong>
                    {c.user?.name} ·{" "}
                    {c.user?.role}
                  </strong>

                  <p>{c.comment}</p>

                  <small>
                    {new Date(
                      c.created_at
                    ).toLocaleString()}
                  </small>
                </div>
              ))
            )}
          </div>

          <div className="comment-compose">
            <textarea
              rows="3"
              value={comment}
              onChange={(e) =>
                setComment(e.target.value)
              }
              placeholder="Add an administrative comment..."
            />

            <button
              className="btn primary"
              disabled={saving}
              onClick={addComment}
            >
              Add Comment
            </button>
          </div>
        </section>

        <aside className="panel collab-side">
          <h2>Manage Problem</h2>

          <label>
            Priority

            <select
              value={priority}
              onChange={(e) =>
                setPriority(e.target.value)
              }
            >
              {priorities.map((x) => (
                <option key={x}>{x}</option>
              ))}
            </select>
          </label>

          <label>
            Status

            <select
              value={status}
              onChange={(e) =>
                setStatus(e.target.value)
              }
            >
              {statuses.map((x) => (
                <option key={x}>{x}</option>
              ))}
            </select>
          </label>

          <label>
            Update note

            <textarea
              rows="3"
              value={note}
              onChange={(e) =>
                setNote(e.target.value)
              }
              placeholder="Why is this status changing?"
            />
          </label>

          <button
            className="btn primary full-button"
            disabled={saving}
            onClick={updateProblem}
          >
            Save Status / Priority
          </button>

          <hr />

          <h2>Assign Representative</h2>

          <p className="hint">
            Only active, administrator-approved
            organization representatives are listed.
          </p>

          <label>
            Representative

            <select
              value={assigneeId}
              onChange={(e) =>
                setAssigneeId(e.target.value)
              }
            >
              <option value="">
                Select representative
              </option>

              {representatives.map((r) => (
                <option
                  key={r.id}
                  value={r.id}
                >
                  {r.name} — {r.role}
                  {r.organization
                    ? ` — ${r.organization}`
                    : ""}
                </option>
              ))}
            </select>
          </label>

          <label>
            Assignment remarks

            <textarea
              rows="4"
              value={remarks}
              onChange={(e) =>
                setRemarks(e.target.value)
              }
              placeholder="Instructions for the representative..."
            />
          </label>

          <button
            className="btn approve full-button"
            disabled={saving || !assigneeId}
            onClick={assign}
          >
            Assign Problem
          </button>

          <hr />

          <h3>Current Assignment</h3>

          {problem.assignment ? (
            <div className="assignment-card">
              <strong>
                {problem.assignment.assignee.name}
              </strong>

              <span>
                {
                  problem.assignment
                    .organization_role
                }
              </span>

              <span>
                {problem.assignment.assignee
                  .organization || ""}
              </span>

              <small>
                {problem.assignment.remarks ||
                  "No remarks"}
              </small>
            </div>
          ) : (
            <p className="muted">
              Not assigned yet.
            </p>
          )}
        </aside>
      </div>
    </main>
  );
}