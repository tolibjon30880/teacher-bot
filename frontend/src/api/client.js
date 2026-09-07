import { getInitData } from "../telegram";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-Telegram-Init-Data": getInitData(),
      ...options.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `So'rov xatosi: ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  // O'qituvchi
  getGroups: () => request("/api/teacher/groups"),
  createGroup: (name) =>
    request("/api/teacher/groups", { method: "POST", body: JSON.stringify({ name }) }),
  getStudents: (groupId) => request(`/api/teacher/groups/${groupId}/students`),
  getSchedule: (groupId) => request(`/api/teacher/groups/${groupId}/schedule`),
  addScheduleEntry: (groupId, weekday, time) =>
    request(`/api/teacher/groups/${groupId}/schedule`, {
      method: "POST",
      body: JSON.stringify({ weekday, time }),
    }),
  getTodaysLessons: () => request("/api/teacher/lessons/today"),
  setLessonStatus: (lessonId, status) =>
    request(`/api/teacher/lessons/${lessonId}/status?status=${status}`, { method: "POST" }),
  submitAttendance: (lessonId, records) =>
    request(`/api/teacher/lessons/${lessonId}/attendance`, {
      method: "POST",
      body: JSON.stringify(records),
    }),

  // O'quvchi
  getMyStats: () => request("/api/student/stats"),
};
