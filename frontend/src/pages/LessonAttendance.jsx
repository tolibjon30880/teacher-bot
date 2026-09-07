import React, { useEffect, useState } from "react";
import { api } from "../api/client";

export default function LessonAttendance({ lesson, onBack }) {
  const [students, setStudents] = useState([]);
  const [records, setRecords] = useState({}); // student_id -> {present, homework_done, score}
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .getStudents(lesson.group_id)
      .then((list) => {
        setStudents(list);
        const initial = {};
        list.forEach((s) => {
          initial[s.id] = { present: true, homework_done: null, score: "" };
        });
        setRecords(initial);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [lesson.group_id]);

  const updateRecord = (studentId, patch) => {
    setRecords((prev) => ({ ...prev, [studentId]: { ...prev[studentId], ...patch } }));
  };

  const save = async () => {
    setSaving(true);
    setError(null);
    try {
      await api.setLessonStatus(lesson.id, "held");
      const payload = students.map((s) => ({
        student_id: s.id,
        present: records[s.id].present,
        homework_done: records[s.id].homework_done,
        score: records[s.id].score === "" ? null : Number(records[s.id].score),
      }));
      await api.submitAttendance(lesson.id, payload);
      onBack();
    } catch (e) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      <div className="board-header">
        <button
          onClick={onBack}
          style={{
            background: "none",
            border: "none",
            color: "var(--chalk-dim)",
            fontSize: 13,
            padding: 0,
            marginBottom: 10,
            cursor: "pointer",
          }}
        >
          ← Orqaga
        </button>
        <p className="eyebrow">Davomat va baho</p>
        <h1>Guruh #{lesson.group_id}</h1>
        <p className="sub">{lesson.time}</p>
      </div>

      <div className="content">
        {loading && <div className="loading">Yuklanmoqda…</div>}
        {error && <div className="error-box">{error}</div>}

        {!loading &&
          students.map((s) => {
            const rec = records[s.id];
            return (
              <div className="card" key={s.id}>
                <p className="card-title">{s.full_name}</p>

                <p className="card-sub" style={{ marginBottom: 8 }}>Davomat</p>
                <div className="toggle-group" style={{ marginBottom: 12 }}>
                  <button
                    className={`toggle-btn ${rec.present ? "active-yes" : ""}`}
                    onClick={() => updateRecord(s.id, { present: true })}
                  >
                    Keldi
                  </button>
                  <button
                    className={`toggle-btn ${!rec.present ? "active-no" : ""}`}
                    onClick={() => updateRecord(s.id, { present: false })}
                  >
                    Kelmadi
                  </button>
                </div>

                <p className="card-sub" style={{ marginBottom: 8 }}>Uy vazifa</p>
                <div className="toggle-group" style={{ marginBottom: 12 }}>
                  <button
                    className={`toggle-btn ${rec.homework_done === true ? "active-yes" : ""}`}
                    onClick={() => updateRecord(s.id, { homework_done: true })}
                  >
                    Bajargan
                  </button>
                  <button
                    className={`toggle-btn ${rec.homework_done === false ? "active-no" : ""}`}
                    onClick={() => updateRecord(s.id, { homework_done: false })}
                  >
                    Bajarmagan
                  </button>
                </div>

                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <span className="card-sub" style={{ margin: 0 }}>Ball (0-100)</span>
                  <input
                    className="score-input"
                    type="number"
                    min="0"
                    max="100"
                    value={rec.score}
                    onChange={(e) => updateRecord(s.id, { score: e.target.value })}
                    placeholder="—"
                  />
                </div>
              </div>
            );
          })}

        {!loading && students.length > 0 && (
          <button className="btn btn-primary" style={{ width: "100%" }} onClick={save} disabled={saving}>
            {saving ? "Saqlanmoqda…" : "Saqlash"}
          </button>
        )}
      </div>
    </>
  );
}
