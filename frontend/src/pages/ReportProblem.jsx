import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../services/api";
import { useAuth } from "../context/AuthContext";

const categories = [
  "Water Resources",
  "Sanitation",
  "Healthcare",
  "Education",
  "Agriculture",
  "Roads & Transport",
  "Electricity",
  "Environment",
  "Waste Management",
  "Public Safety",
  "Employment",
  "Other",
];

export default function ReportProblem() {
  const navigate = useNavigate();
  const { user } = useAuth();
const submitterLabels = {
  CITIZEN: "INDIVIDUAL CITIZEN",
  COMMUNITY_GROUP: "COMMUNITY GROUP",
  PRI: "PANCHAYATI RAJ INSTITUTION",
  ULB: "URBAN LOCAL BODY",
  GOVERNMENT: "GOVERNMENT DEPARTMENT",
};

const submitterLabel =
  submitterLabels[user?.role] || "CHALLENGE SUBMITTER";
  const [form, setForm] = useState({
    title: "",
    description: "",
    category: "",

    state_id: "",
    district_id: "",
    block_id: "",
    village_id: "",

    address: "",
    pincode: "",

    latitude: "",
    longitude: "",

    affected_people: "",
    additional_details: "",
  });

  const [states, setStates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [blocks, setBlocks] = useState([]);
  const [villages, setVillages] = useState([]);

  const [images, setImages] = useState([]);
  const [videos, setVideos] = useState([]);

  const [loading, setLoading] = useState(false);
  const [locationLoading, setLocationLoading] =
    useState(false);

  const [error, setError] = useState("");

  // ------------------------------------------------------
  // Load states
  // ------------------------------------------------------

  useEffect(() => {
    api
      .get("/locations/states")
      .then((response) => {
        setStates(response.data);
      })
      .catch(() => {
        setError("Unable to load states.");
      });
  }, []);

  // ------------------------------------------------------
  // Districts
  // ------------------------------------------------------

  useEffect(() => {
    if (!form.state_id) {
      setDistricts([]);
      return;
    }

    api
      .get(
        `/locations/states/${form.state_id}/districts`
      )
      .then((response) => {
        setDistricts(response.data);
      })
      .catch(() => {});
  }, [form.state_id]);

  // ------------------------------------------------------
  // Blocks
  // ------------------------------------------------------

  useEffect(() => {
    if (!form.district_id) {
      setBlocks([]);
      return;
    }

    api
      .get(
        `/locations/districts/${form.district_id}/blocks`
      )
      .then((response) => {
        setBlocks(response.data);
      })
      .catch(() => {});
  }, [form.district_id]);

  // ------------------------------------------------------
  // Villages
  // ------------------------------------------------------

  useEffect(() => {
    if (!form.block_id) {
      setVillages([]);
      return;
    }

    api
      .get(
        `/locations/blocks/${form.block_id}/villages`
      )
      .then((response) => {
        setVillages(response.data);
      })
      .catch(() => {});
  }, [form.block_id]);

  function updateField(name, value) {
    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  }

  // ------------------------------------------------------
  // GPS
  // ------------------------------------------------------

  function getCurrentLocation() {
    if (!navigator.geolocation) {
      setError(
        "Geolocation is not supported by this browser."
      );
      return;
    }

    setLocationLoading(true);
    setError("");

    navigator.geolocation.getCurrentPosition(
      (position) => {
        updateField(
          "latitude",
          position.coords.latitude
        );

        updateField(
          "longitude",
          position.coords.longitude
        );

        setLocationLoading(false);
      },
      () => {
        setLocationLoading(false);

        setError(
          "Unable to get your current location. Please allow location access."
        );
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
      }
    );
  }

  // ------------------------------------------------------
  // Submit
  // ------------------------------------------------------

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");

    if (!form.title.trim()) {
      setError("Please enter a problem title.");
      return;
    }

    if (!form.description.trim()) {
      setError(
        "Please describe the problem."
      );
      return;
    }

    if (!form.category) {
      setError(
        "Please select a problem category."
      );
      return;
    }

    try {
      setLoading(true);

      const data = new FormData();

      data.append(
        "problem_data",
        JSON.stringify({
          ...form,

          state_id: form.state_id
            ? Number(form.state_id)
            : null,

          district_id: form.district_id
            ? Number(form.district_id)
            : null,

          block_id: form.block_id
            ? Number(form.block_id)
            : null,

          village_id: form.village_id
            ? Number(form.village_id)
            : null,

          latitude: form.latitude
            ? Number(form.latitude)
            : null,

          longitude: form.longitude
            ? Number(form.longitude)
            : null,

          affected_people:
            form.affected_people
              ? Number(
                  form.affected_people
                )
              : null,
        })
      );

      images.forEach((image) => {
        data.append("images", image);
      });

      videos.forEach((video) => {
        data.append("videos", video);
      });

      await api.post(
        "/problems",
        data,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      alert(
        "Problem submitted successfully."
      );

      navigate("/my-problems");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to submit the problem."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="page">
      <div className="dashboard-head">
        <div>
          <div className="eyebrow">
  {submitterLabel}
</div>

          <h1>Report a Problem</h1>

          <p className="muted">
            Report a local problem so that it can be
            reviewed and eventually connected with
            universities, industry and government.
          </p>
        </div>
      </div>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      <form
        className="panel problem-form"
        onSubmit={handleSubmit}
      >
        <h2>Problem Information</h2>

        <div className="form-grid">
          <label>
            Problem Title *
            <input
              type="text"
              value={form.title}
              onChange={(e) =>
                updateField(
                  "title",
                  e.target.value
                )
              }
              placeholder="Example: Drinking water shortage"
              required
            />
          </label>

          <label>
            Category *
            <select
              value={form.category}
              onChange={(e) =>
                updateField(
                  "category",
                  e.target.value
                )
              }
              required
            >
              <option value="">
                Select category
              </option>

              {categories.map((category) => (
                <option
                  value={category}
                  key={category}
                >
                  {category}
                </option>
              ))}
            </select>
          </label>

          <label className="full-width">
            Description *
            <textarea
              rows="6"
              value={form.description}
              onChange={(e) =>
                updateField(
                  "description",
                  e.target.value
                )
              }
              placeholder="Describe the problem in detail..."
              required
            />
          </label>

          <label>
            Affected People
            <input
              type="number"
              min="0"
              value={form.affected_people}
              onChange={(e) =>
                updateField(
                  "affected_people",
                  e.target.value
                )
              }
              placeholder="Approximate number"
            />
          </label>

          <label>
            Pincode
            <input
              type="text"
              value={form.pincode}
              onChange={(e) =>
                updateField(
                  "pincode",
                  e.target.value
                )
              }
              placeholder="6 digit pincode"
            />
          </label>

          <label className="full-width">
            Additional Details
            <textarea
              rows="4"
              value={form.additional_details}
              onChange={(e) =>
                updateField(
                  "additional_details",
                  e.target.value
                )
              }
              placeholder="Any additional information..."
            />
          </label>
        </div>

        <hr />

        <h2>Problem Location</h2>

        <div className="location-button-row">
          <button
            type="button"
            className="btn secondary"
            onClick={getCurrentLocation}
            disabled={locationLoading}
          >
            {locationLoading
              ? "Getting Location..."
              : "📍 Use My Current Location"}
          </button>

          {form.latitude &&
            form.longitude && (
              <span className="location-success">
                Location captured
              </span>
            )}
        </div>

        <div className="form-grid">
          <label>
            State
            <select
              value={form.state_id}
              onChange={(e) => {
                updateField(
                  "state_id",
                  e.target.value
                );

                updateField(
                  "district_id",
                  ""
                );

                updateField(
                  "block_id",
                  ""
                );

                updateField(
                  "village_id",
                  ""
                );
              }}
            >
              <option value="">
                Select state
              </option>

              {states.map((state) => (
                <option
                  key={state.id}
                  value={state.id}
                >
                  {state.name ||
                    state.state_name ||
                    state.name_en}
                </option>
              ))}
            </select>
          </label>

          <label>
            District
            <select
              value={form.district_id}
              onChange={(e) => {
                updateField(
                  "district_id",
                  e.target.value
                );

                updateField(
                  "block_id",
                  ""
                );

                updateField(
                  "village_id",
                  ""
                );
              }}
              disabled={!form.state_id}
            >
              <option value="">
                Select district
              </option>

              {districts.map((district) => (
                <option
                  key={district.id}
                  value={district.id}
                >
                  {district.name ||
                    district.district_name ||
                    district.name_en}
                </option>
              ))}
            </select>
          </label>

          <label>
            Block / Mandal
            <select
              value={form.block_id}
              onChange={(e) => {
                updateField(
                  "block_id",
                  e.target.value
                );

                updateField(
                  "village_id",
                  ""
                );
              }}
              disabled={!form.district_id}
            >
              <option value="">
                Select block / mandal
              </option>

              {blocks.map((block) => (
                <option
                  key={block.id}
                  value={block.id}
                >
                  {block.name ||
                    block.block_name ||
                    block.name_en}
                </option>
              ))}
            </select>
          </label>

          <label>
            Village
            <select
              value={form.village_id}
              onChange={(e) =>
                updateField(
                  "village_id",
                  e.target.value
                )
              }
              disabled={!form.block_id}
            >
              <option value="">
                Select village
              </option>

              {villages.map((village) => (
                <option
                  key={village.id}
                  value={village.id}
                >
                  {village.name ||
                    village.village_name ||
                    village.name_en}
                </option>
              ))}
            </select>
          </label>

          <label className="full-width">
            Address / Landmark
            <textarea
              rows="3"
              value={form.address}
              onChange={(e) =>
                updateField(
                  "address",
                  e.target.value
                )
              }
              placeholder="Enter the exact location or nearby landmark"
            />
          </label>
        </div>

        {form.latitude &&
          form.longitude && (
            <div className="gps-box">
              <strong>
                GPS Coordinates
              </strong>

              <span>
                Latitude: {form.latitude}
              </span>

              <span>
                Longitude: {form.longitude}
              </span>
            </div>
          )}

        <hr />

        <h2>Photos</h2>

        <label className="upload-box">
          <span>
            Select problem photos
          </span>

          <input
            type="file"
            accept="image/*"
            multiple
            onChange={(e) =>
              setImages(
                Array.from(
                  e.target.files || []
                )
              )
            }
          />

          {images.length > 0 && (
            <small>
              {images.length} image(s)
              selected
            </small>
          )}
        </label>

        <h2>Videos</h2>

        <label className="upload-box">
          <span>
            Select problem videos
          </span>

          <input
            type="file"
            accept="video/*"
            multiple
            onChange={(e) =>
              setVideos(
                Array.from(
                  e.target.files || []
                )
              )
            }
          />

          {videos.length > 0 && (
            <small>
              {videos.length} video(s)
              selected
            </small>
          )}
        </label>

        <div className="form-actions">
          <button
            type="button"
            className="btn secondary"
            onClick={() =>
              navigate("/dashboard")
            }
          >
            Cancel
          </button>

          <button
            type="submit"
            className="btn primary"
            disabled={loading}
          >
            {loading
              ? "Submitting..."
              : "Submit Problem"}
          </button>
        </div>
      </form>
    </main>
  );
}