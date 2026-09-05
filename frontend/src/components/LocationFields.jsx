import { useEffect, useState } from "react";
import api from "../services/api";

export default function LocationFields({ form, setForm }) {
  const [states, setStates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [blocks, setBlocks] = useState([]);
  const [villages, setVillages] = useState([]);
  const [locationError, setLocationError] = useState("");

  useEffect(() => { api.get("/locations/states").then(r=>setStates(r.data)).catch(()=>{}); }, []);
  useEffect(() => {
    setDistricts([]); setBlocks([]); setVillages([]);
    if (form.state_id) api.get(`/locations/states/${form.state_id}/districts`).then(r=>setDistricts(r.data)).catch(()=>{});
  }, [form.state_id]);
  useEffect(() => {
    setBlocks([]); setVillages([]);
    if (form.district_id) api.get(`/locations/districts/${form.district_id}/blocks`).then(r=>setBlocks(r.data)).catch(()=>{});
  }, [form.district_id]);
  useEffect(() => {
    setVillages([]);
    if (form.block_id) api.get(`/locations/blocks/${form.block_id}/villages`).then(r=>setVillages(r.data)).catch(()=>{});
  }, [form.block_id]);

  const update = (key, value) => setForm(prev=>({...prev,[key]:value}));

  function useGPS() {
    setLocationError("");
    if (!navigator.geolocation) return setLocationError("Geolocation is not supported by this browser.");
    navigator.geolocation.getCurrentPosition(
      pos => setForm(prev=>({...prev,
        latitude:Number(pos.coords.latitude.toFixed(7)),
        longitude:Number(pos.coords.longitude.toFixed(7))
      })),
      err => setLocationError(err.message || "Unable to obtain location."),
      {enableHighAccuracy:true, timeout:10000}
    );
  }

  return (
    <section className="form-section">
      <div className="section-title">Location</div>
      <div className="grid-2">
        <label>State
          <select value={form.state_id||""} onChange={e=>update("state_id",e.target.value?Number(e.target.value):null)}>
            <option value="">Select state</option>{states.map(s=><option key={s.id} value={s.id}>{s.name}</option>)}
          </select>
        </label>
        <label>District
          <select value={form.district_id||""} disabled={!form.state_id} onChange={e=>update("district_id",e.target.value?Number(e.target.value):null)}>
            <option value="">Select district</option>{districts.map(x=><option key={x.id} value={x.id}>{x.name}</option>)}
          </select>
        </label>
        <label>Block / Mandal
          <select value={form.block_id||""} disabled={!form.district_id} onChange={e=>update("block_id",e.target.value?Number(e.target.value):null)}>
            <option value="">Select block / mandal</option>{blocks.map(x=><option key={x.id} value={x.id}>{x.name}</option>)}
          </select>
        </label>
        <label>Village
          <select value={form.village_id||""} disabled={!form.block_id} onChange={e=>update("village_id",e.target.value?Number(e.target.value):null)}>
            <option value="">Select village</option>{villages.map(x=><option key={x.id} value={x.id}>{x.name}</option>)}
          </select>
        </label>
      </div>
      <label>Address
        <textarea value={form.address_line||""} onChange={e=>update("address_line",e.target.value)} placeholder="House / street / locality"></textarea>
      </label>
      <div className="grid-2">
        <label>Pincode<input value={form.pincode||""} onChange={e=>update("pincode",e.target.value)}/></label>
        <div className="gps-box">
          <button type="button" className="btn secondary" onClick={useGPS}>📍 Use My Current Location</button>
          {form.latitude && form.longitude && <div className="gps-readout">{form.latitude}, {form.longitude}</div>}
        </div>
      </div>
      {locationError && <div className="error small">{locationError}</div>}
      <p className="hint">GPS provides coordinates. Use the official administrative data import for complete block/village dropdown coverage.</p>
    </section>
  );
}
