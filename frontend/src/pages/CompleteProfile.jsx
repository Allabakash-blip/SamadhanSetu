import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";
import LocationFields from "../components/LocationFields";

export default function CompleteProfile() {
  const { user, refreshMe } = useAuth();
  const navigate = useNavigate();

  const [picture, setPicture] = useState(null);
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    role: user?.role || "CITIZEN",
    phone: user?.phone || "",
    address_line: "",

    state_id: null,
    district_id: null,
    block_id: null,
    village_id: null,
    pincode: "",

    latitude: null,
    longitude: null,

    university_name: "",
    university_type: "",
    registration_number: "",
    department: "",
    designation: "",
    city: "",
    expertise: "",

    company_name: "",
    company_type: "",
    website: "",
    available_support: "",

    government_department: "",
    official_id: "",

    organization_name: "",
    organization_type: "",
    organization_registration_number: "",
    ward: "",

    // Feature 08: Advanced Representative Matching
    availability_status: "AVAILABLE",
    relevant_experience: "",
    years_of_experience: ""
  });

  function updateField(field, value) {
    setForm((previousForm) => ({
      ...previousForm,
      [field]: value
    }));
  }

  async function submit(e) {
    e.preventDefault();
    setError("");

    try {
      const payload = {
        ...form,
        years_of_experience:
          form.years_of_experience === ""
            ? null
            : Number(form.years_of_experience)
      };

      await api.post(
        "/auth/complete-profile",
        payload
      );

      if (picture) {
        const fd = new FormData();

        fd.append("file", picture);

        await api.post(
          "/auth/profile-picture",
          fd,
          {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          }
        );
      }

      await refreshMe();

      navigate("/dashboard");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Could not complete profile"
      );
    }
  }

  return (
    <main className="page">
      <div className="page-card">

        <div className="eyebrow">
          STEP 2 OF 2
        </div>

        <h1>
          Complete your profile
        </h1>

        <p className="muted">
          These details will later support location analytics
          and institutional matching.
        </p>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        <form onSubmit={submit}>

          <label>
            Profile Picture

            <input
              type="file"
              accept="image/png,image/jpeg,image/webp"
              onChange={(e) =>
                setPicture(
                  e.target.files?.[0] || null
                )
              }
            />
          </label>

          <label>
            Mobile Number

            <input
              value={form.phone}
              onChange={(e) =>
                updateField(
                  "phone",
                  e.target.value
                )
              }
            />
          </label>

          {/* Location */}
          {[
            "CITIZEN",
            "COMMUNITY_GROUP",
            "PRI",
            "ULB",
            "UNIVERSITY",
            "INDUSTRY",
            "GOVERNMENT"
          ].includes(form.role) && (
            <LocationFields
              form={form}
              setForm={setForm}
            />
          )}

          {/* ==================================================
              COMMUNITY GROUP / PRI / ULB
          ================================================== */}

          {[
            "COMMUNITY_GROUP",
            "PRI",
            "ULB"
          ].includes(form.role) && (
            <section className="form-section">

              <div className="section-title">
                {form.role === "COMMUNITY_GROUP"
                  ? "Community group information"
                  : form.role === "PRI"
                  ? "Panchayati Raj Institution information"
                  : "Urban Local Body information"}
              </div>

              <div className="grid-2">

                <label>
                  Organization / Institution Name

                  <input
                    required
                    value={form.organization_name}
                    onChange={(e) =>
                      updateField(
                        "organization_name",
                        e.target.value
                      )
                    }
                  />
                </label>

                <label>
                  Registration / Institution ID

                  <input
                    value={
                      form.organization_registration_number
                    }
                    onChange={(e) =>
                      updateField(
                        "organization_registration_number",
                        e.target.value
                      )
                    }
                  />
                </label>

                <label>
                  Representative Designation

                  <input
                    required
                    value={form.designation}
                    onChange={(e) =>
                      updateField(
                        "designation",
                        e.target.value
                      )
                    }
                  />
                </label>

                {form.role === "ULB" && (
                  <label>
                    Ward

                    <input
                      value={form.ward}
                      onChange={(e) =>
                        updateField(
                          "ward",
                          e.target.value
                        )
                      }
                    />
                  </label>
                )}

                {form.role === "ULB" && (
                  <label>
                    City / Town

                    <input
                      value={form.city}
                      onChange={(e) =>
                        updateField(
                          "city",
                          e.target.value
                        )
                      }
                    />
                  </label>
                )}

              </div>

              <div className="notice">
                This account is PENDING until administrator
                verification. Once approved, it can submit
                and track societal challenges on behalf of
                the organization.
              </div>

            </section>
          )}

          {/* ==================================================
              UNIVERSITY
          ================================================== */}

          {form.role === "UNIVERSITY" && (
            <section className="form-section">

              <div className="section-title">
                University information
              </div>

              <div className="grid-2">

                <label>
                  University Name

                  <input
                    required
                    value={form.university_name}
                    onChange={(e) =>
                      updateField(
                        "university_name",
                        e.target.value
                      )
                    }
                  />
                </label>

                <label>
                  University Type

                  <input
                    value={form.university_type}
                    onChange={(e) =>
                      updateField(
                        "university_type",
                        e.target.value
                      )
                    }
                  />
                </label>

                <label>
                  Registration / Institution ID

                  <input
                    value={form.registration_number}
                    onChange={(e) =>
                      updateField(
                        "registration_number",
                        e.target.value
                      )
                    }
                  />
                </label>

                <label>
                  Department

                  <input
                    value={form.department}
                    onChange={(e) =>
                      updateField(
                        "department",
                        e.target.value
                      )
                    }
                  />
                </label>

                <label>
                  Designation

                  <input
                    value={form.designation}
                    onChange={(e) =>
                      updateField(
                        "designation",
                        e.target.value
                      )
                    }
                  />
                </label>

                <label>
                  City

                  <input
                    value={form.city}
                    onChange={(e) =>
                      updateField(
                        "city",
                        e.target.value
                      )
                    }
                  />
                </label>

              </div>

              <label>
                Areas of Expertise

                <textarea
                  value={form.expertise}
                  onChange={(e) =>
                    updateField(
                      "expertise",
                      e.target.value
                    )
                  }
                  placeholder="AI, IoT, water resources, agriculture, healthcare..."
                />
              </label>

              {/* Feature 08 */}
              <div className="section-title">
                Matching & Availability
              </div>

              <div className="grid-2">

                <label>
                  Availability

                  <select
                    value={form.availability_status}
                    onChange={(e) =>
                      updateField(
                        "availability_status",
                        e.target.value
                      )
                    }
                  >
                    <option value="AVAILABLE">
                      Available
                    </option>

                    <option value="LIMITED">
                      Limited Availability
                    </option>

                    <option value="UNAVAILABLE">
                      Currently Unavailable
                    </option>
                  </select>
                </label>

                <label>
                  Years of Experience

                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={form.years_of_experience}
                    onChange={(e) =>
                      updateField(
                        "years_of_experience",
                        e.target.value
                      )
                    }
                    placeholder="e.g. 5"
                  />
                </label>

              </div>

              <label>
                Relevant Experience

                <textarea
                  value={form.relevant_experience}
                  onChange={(e) =>
                    updateField(
                      "relevant_experience",
                      e.target.value
                    )
                  }
                  placeholder="Describe projects, research, technologies, domains or previous work relevant to social innovation challenges..."
                />
              </label>

              <div className="notice">
                University accounts are PENDING until
                administrator verification.
              </div>

            </section>
          )}

          {/* ==================================================
              INDUSTRY
          ================================================== */}

          {form.role === "INDUSTRY" && (
            <section className="form-section">

              <div className="section-title">
                Industry information
              </div>

              <div className="grid-2">

                <label>
                  Company Name

                  <input
                    required
                    value={form.company_name}
                    onChange={(e) =>
                      updateField(
                        "company_name",
                        e.target.value
                      )
                    }
                  />
                </label>

                <label>
                  Company Type

                  <input
                    value={form.company_type}
                    onChange={(e) =>
                      updateField(
                        "company_type",
                        e.target.value
                      )
                    }
                  />
                </label>

                <label>
                  Website

                  <input
                    value={form.website}
                    onChange={(e) =>
                      updateField(
                        "website",
                        e.target.value
                      )
                    }
                  />
                </label>

                <label>
                  City

                  <input
                    value={form.city}
                    onChange={(e) =>
                      updateField(
                        "city",
                        e.target.value
                      )
                    }
                  />
                </label>

              </div>

              <label>
                Areas of Expertise

                <textarea
                  value={form.expertise}
                  onChange={(e) =>
                    updateField(
                      "expertise",
                      e.target.value
                    )
                  }
                />
              </label>

              <label>
                Available Support

                <textarea
                  value={form.available_support}
                  onChange={(e) =>
                    updateField(
                      "available_support",
                      e.target.value
                    )
                  }
                  placeholder="Mentoring, funding, hardware, testing..."
                />
              </label>

              {/* Feature 08 */}
              <div className="section-title">
                Matching & Availability
              </div>

              <div className="grid-2">

                <label>
                  Availability

                  <select
                    value={form.availability_status}
                    onChange={(e) =>
                      updateField(
                        "availability_status",
                        e.target.value
                      )
                    }
                  >
                    <option value="AVAILABLE">
                      Available
                    </option>

                    <option value="LIMITED">
                      Limited Availability
                    </option>

                    <option value="UNAVAILABLE">
                      Currently Unavailable
                    </option>
                  </select>
                </label>

                <label>
                  Years of Experience

                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={form.years_of_experience}
                    onChange={(e) =>
                      updateField(
                        "years_of_experience",
                        e.target.value
                      )
                    }
                    placeholder="e.g. 8"
                  />
                </label>

              </div>

              <label>
                Relevant Experience

                <textarea
                  value={form.relevant_experience}
                  onChange={(e) =>
                    updateField(
                      "relevant_experience",
                      e.target.value
                    )
                  }
                  placeholder="Describe previous projects, solutions, technologies, industries or capabilities relevant to social innovation challenges..."
                />
              </label>

              <div className="notice">
                Industry accounts are PENDING until
                administrator verification.
              </div>

            </section>
          )}

          {/* ==================================================
              GOVERNMENT
          ================================================== */}

          {form.role === "GOVERNMENT" && (
            <section className="form-section">

              <div className="section-title">
                Government information
              </div>

              <div className="grid-2">

                <label>
                  Department

                  <input
                    required
                    value={form.government_department}
                    onChange={(e) =>
                      updateField(
                        "government_department",
                        e.target.value
                      )
                    }
                  />
                </label>

                <label>
                  Designation

                  <input
                    value={form.designation}
                    onChange={(e) =>
                      updateField(
                        "designation",
                        e.target.value
                      )
                    }
                  />
                </label>

                <label>
                  Official ID

                  <input
                    value={form.official_id}
                    onChange={(e) =>
                      updateField(
                        "official_id",
                        e.target.value
                      )
                    }
                  />
                </label>

              </div>

              {/* Feature 08 */}
              <div className="section-title">
                Matching & Availability
              </div>

              <div className="grid-2">

                <label>
                  Availability

                  <select
                    value={form.availability_status}
                    onChange={(e) =>
                      updateField(
                        "availability_status",
                        e.target.value
                      )
                    }
                  >
                    <option value="AVAILABLE">
                      Available
                    </option>

                    <option value="LIMITED">
                      Limited Availability
                    </option>

                    <option value="UNAVAILABLE">
                      Currently Unavailable
                    </option>
                  </select>
                </label>

                <label>
                  Years of Experience

                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={form.years_of_experience}
                    onChange={(e) =>
                      updateField(
                        "years_of_experience",
                        e.target.value
                      )
                    }
                    placeholder="e.g. 10"
                  />
                </label>

              </div>

              <label>
                Relevant Experience

                <textarea
                  value={form.relevant_experience}
                  onChange={(e) =>
                    updateField(
                      "relevant_experience",
                      e.target.value
                    )
                  }
                  placeholder="Describe relevant government programs, departments, projects, policies or implementation experience..."
                />
              </label>

              <div className="notice">
                Government accounts are PENDING until
                administrator verification.
              </div>

            </section>
          )}

          <button className="btn primary full">
            Save Profile & Continue
          </button>

        </form>

      </div>
    </main>
  );
}