import React, { useEffect, useState } from "react";
import { initTelegram, getTelegramUser } from "./telegram";
import TeacherApp from "./pages/TeacherApp";
import StudentCabinet from "./pages/StudentCabinet";

const TEACHER_ID = Number(import.meta.env.VITE_TEACHER_TELEGRAM_ID || 0);

export default function App() {
  const [ready, setReady] = useState(false);
  const [isTeacher, setIsTeacher] = useState(false);

  useEffect(() => {
    initTelegram();
    const user = getTelegramUser();
    setIsTeacher(Boolean(TEACHER_ID) && user?.id === TEACHER_ID);
    setReady(true);
  }, []);

  if (!ready) return null;

  return <div className="app">{isTeacher ? <TeacherApp /> : <StudentCabinet />}</div>;
}
