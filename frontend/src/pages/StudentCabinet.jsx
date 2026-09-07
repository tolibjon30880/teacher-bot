import React, { useEffect, useState } from "react";
import { api } from "../api/client";

function scoreClass(score) {
  if (score === null || score === undefined) return "";
  return score >= 70 ? "good" : "";
}

export default function StudentCabinet() {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getMyStats()
      .then(setStats)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Yuklanmoqda…</div>;

  if (error) {
    return (
      <div className="empty-state">
        <div className="glyph">📭</div>
        <p>{error}</p>
        <p style={{ fontSize: 13 }}>
          Guruhga qo'shilish uchun o'qituvchingizdan taklif havolasini so'rang.
        </p>
      </div>
    );
  }

  return (
    <>
      <div className="board-header">
        <p className="eyebrow">Shaxsiy kabinet</p>
        <h1>{stats.full_name}</h1>
        <p className="sub">
          {stats.total_lessons} ta dars qayd etilgan
        </p>
      </div>

      <div className="content">
        <div className="stat-grid">
          <div className="stat-box">
            <div className="value">
              {stats.average_score !== null ? Math.round(stats.average_score) : "—"}
            </div>
            <div className="label">O'rtacha ball</div>
          </div>
          <div className="stat-box">
            <div className="value">{Math.round(stats.attendance_rate)}%</div>
            <div className="label">Davomat</div>
          </div>
          <div className="stat-box">
            <div className="value">{stats.missed}</div>
            <div className="label">Qoldirilgan</div>
          </div>
        </div>

        <div className="section-title">Darslar tarixi</div>

        {stats.history.length === 0 ? (
          <div className="empty-state">
            <div className="glyph">📖</div>
            <p>Hali hech qanday dars qayd etilmagan.</p>
          </div>
        ) : (
          <div className="ledger">
            {stats.history.map((h, i) => (
              <div className="ledger-row" key={i}>
                <div>
                  <div className="name">
                    {new Date(h.date).toLocaleDateString("uz-UZ", {
                      day: "numeric",
                      month: "long",
                    })}
                  </div>
                  <div className="meta">
                    {h.present ? "Keldi" : "Kelmadi"}
                    {h.homework_done !== null &&
                      (h.homework_done ? " · Uy vazifa bajarilgan" : " · Uy vazifa yo'q")}
                    {h.note ? ` · ${h.note}` : ""}
                  </div>
                </div>
                <div className={`score-badge ${scoreClass(h.score)}`}>
                  {h.score !== null && h.score !== undefined ? Math.round(h.score) : "–"}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
