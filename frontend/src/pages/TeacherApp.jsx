import React, { useState } from "react";
import TodayLessons from "./TodayLessons";
import LessonAttendance from "./LessonAttendance";
import GroupsList from "./GroupsList";

export default function TeacherApp() {
  const [tab, setTab] = useState("today"); // "today" | "groups"
  const [openLesson, setOpenLesson] = useState(null);

  if (openLesson) {
    return (
      <LessonAttendance
        lesson={openLesson}
        onBack={() => setOpenLesson(null)}
      />
    );
  }

  return (
    <>
      <div className="board-header">
        <p className="eyebrow">Boshqaruv paneli</p>
        <h1>{tab === "today" ? "Bugungi darslar" : "Guruhlarim"}</h1>
        <p className="sub">
          {new Date().toLocaleDateString("uz-UZ", {
            weekday: "long",
            day: "numeric",
            month: "long",
          })}
        </p>
      </div>

      <div className="content">
        <div className="btn-row" style={{ marginBottom: 18 }}>
          <button
            className={`btn ${tab === "today" ? "btn-primary" : "btn-outline"}`}
            onClick={() => setTab("today")}
          >
            Bugungi darslar
          </button>
          <button
            className={`btn ${tab === "groups" ? "btn-primary" : "btn-outline"}`}
            onClick={() => setTab("groups")}
          >
            Guruhlar
          </button>
        </div>

        {tab === "today" ? (
          <TodayLessons onOpenLesson={setOpenLesson} />
        ) : (
          <GroupsList />
        )}
      </div>
    </>
  );
}
