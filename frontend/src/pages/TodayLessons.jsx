import React, { useEffect, useState } from "react";
import { api } from "../api/client";

const STATUS_LABEL = {
  pending: "Belgilanmagan",
  held: "O'tdi",
  cancelled: "Bekor qilindi",
};

export default function TodayLessons({ onOpenLesson }) {
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = () => {
    setLoading(true);
    api
      .getTodaysLessons()
      .then(setLessons)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  const markCancelled = async (lessonId) => {
    await api.setLessonStatus(lessonId, "cancelled");
    load();
  };

  if (loading) return <div className="loading">Yuklanmoqda…</div>;
  if (error) return <div className="error-box">{error}</div>;

  if (lessons.length === 0) {
    return (
      <div className="empty-state">
        <div className="glyph">🗓️</div>
        <p>Bugun jadval bo'yicha dars yo'q.</p>
      </div>
    );
  }

  return (
    <div>
      {lessons.map((lesson) => (
        <div className="card" key={lesson.id}>
          <p className="card-title">Guruh #{lesson.group_id} — {lesson.time}</p>
          <p className="card-sub">
            <span className="pill">{STATUS_LABEL[lesson.status]}</span>
          </p>
          <div className="btn-row">
            <button className="btn btn-primary" onClick={() => onOpenLesson(lesson)}>
              Davomat belgilash
            </button>
            {lesson.status === "pending" && (
              <button
                className="btn btn-danger"
                onClick={() => markCancelled(lesson.id)}
              >
                Bekor qilish
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
