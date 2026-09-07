import React, { useEffect, useState } from "react";
import { api } from "../api/client";

const WEEKDAYS = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"];

export default function GroupsList() {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newName, setNewName] = useState("");
  const [expandedId, setExpandedId] = useState(null);
  const [schedule, setSchedule] = useState([]);
  const [newWeekday, setNewWeekday] = useState(0);
  const [newTime, setNewTime] = useState("14:00");

  const load = () => {
    setLoading(true);
    api.getGroups().then(setGroups).finally(() => setLoading(false));
  };

  useEffect(load, []);

  const createGroup = async () => {
    if (!newName.trim()) return;
    await api.createGroup(newName.trim());
    setNewName("");
    load();
  };

  const openSchedule = async (groupId) => {
    if (expandedId === groupId) {
      setExpandedId(null);
      return;
    }
    setExpandedId(groupId);
    const entries = await api.getSchedule(groupId);
    setSchedule(entries);
  };

  const addSchedule = async (groupId) => {
    await api.addScheduleEntry(groupId, newWeekday, newTime);
    const entries = await api.getSchedule(groupId);
    setSchedule(entries);
  };

  if (loading) return <div className="loading">Yuklanmoqda…</div>;

  return (
    <div>
      <div className="card">
        <p className="card-title">Yangi guruh</p>
        <p className="card-sub">
          Nomini kiriting. Taklif havolasini olish uchun botda /groups buyrug'idan foydalaning.
        </p>
        <div style={{ display: "flex", gap: 8 }}>
          <input
            className="score-input"
            style={{ width: "auto", flex: 1, textAlign: "left", color: "var(--ink)" }}
            placeholder="masalan: 9-A"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
          />
          <button className="btn btn-primary" onClick={createGroup}>
            Qo'shish
          </button>
        </div>
      </div>

      {groups.length === 0 ? (
        <div className="empty-state">
          <div className="glyph">🏫</div>
          <p>Hali guruh yo'q.</p>
        </div>
      ) : (
        groups.map((g) => (
          <div className="card" key={g.id}>
            <p className="card-title">{g.name}</p>
            <button className="btn btn-outline" onClick={() => openSchedule(g.id)}>
              {expandedId === g.id ? "Jadvalni yopish" : "Dars jadvali"}
            </button>

            {expandedId === g.id && (
              <div style={{ marginTop: 14 }}>
                {schedule.length === 0 ? (
                  <p className="card-sub">Hali jadval kiritilmagan.</p>
                ) : (
                  <div className="ledger" style={{ marginBottom: 12 }}>
                    {schedule.map((s) => (
                      <div className="ledger-row" key={s.id}>
                        <span className="name">{WEEKDAYS[s.weekday]}</span>
                        <span className="meta">{s.time}</span>
                      </div>
                    ))}
                  </div>
                )}

                <div style={{ display: "flex", gap: 8 }}>
                  <select
                    value={newWeekday}
                    onChange={(e) => setNewWeekday(Number(e.target.value))}
                    style={{ flex: 1, borderRadius: 7, border: "1.5px solid var(--paper-line)", padding: 8 }}
                  >
                    {WEEKDAYS.map((d, i) => (
                      <option value={i} key={i}>{d}</option>
                    ))}
                  </select>
                  <input
                    type="time"
                    value={newTime}
                    onChange={(e) => setNewTime(e.target.value)}
                    style={{ borderRadius: 7, border: "1.5px solid var(--paper-line)", padding: 8 }}
                  />
                  <button className="btn btn-primary" onClick={() => addSchedule(g.id)}>
                    +
                  </button>
                </div>
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );
}
