# O'qituvchi kundaligi — Telegram bot + Mini App

Bitta o'qituvchi uchun: guruhlar (sinflar), dars jadvali, davomat, uy vazifa va
100 ballik baholash tizimi. Har bir o'quvchi mini app orqali o'z shaxsiy
kabinetini ko'radi.

## Tuzilma

```
teacher-bot/
├── backend/          FastAPI (mini app API) + aiogram (Telegram bot)
│   ├── app/
│   │   ├── models/       SQLAlchemy modellari
│   │   ├── routers/      API endpointlari (teacher.py, student.py)
│   │   ├── schemas/      Pydantic sxemalar
│   │   ├── bot/          Telegram bot handlerlari
│   │   ├── database.py
│   │   ├── config.py
│   │   ├── telegram_auth.py   Mini App initData tekshiruvi
│   │   └── main.py       FastAPI ilova
│   └── requirements.txt
└── frontend/         React mini app (Vite)
    └── src/
        ├── pages/     TeacherApp, TodayLessons, LessonAttendance, GroupsList, StudentCabinet
        ├── api/       backend bilan aloqa
        └── telegram.js
```

## 1-qadam: Bot yaratish

1. Telegram'da [@BotFather](https://t.me/BotFather) bilan gaplashing.
2. `/newbot` buyrug'ini yuboring, nom va username bering.
3. Sizga beriladigan **tokenni** saqlab qo'ying — bu `BOT_TOKEN`.
4. O'zingizning Telegram ID'ingizni bilish uchun [@userinfobot](https://t.me/userinfobot) ga yozing — bu `TEACHER_TELEGRAM_ID`.

## 2-qadam: Backend'ni ishga tushirish

```bash
cd backend
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# .env faylini oching va BOT_TOKEN, TEACHER_TELEGRAM_ID'ni to'ldiring
```

API serverini ishga tushirish:
```bash
uvicorn app.main:app --reload --port 8000
```

Botni (alohida terminalda) ishga tushirish:
```bash
python -m app.bot.run_bot
```

## 3-qadam: Frontend (mini app)ni ishga tushirish

```bash
cd frontend
npm install
cp .env.example .env
# VITE_TEACHER_TELEGRAM_ID'ni backend'dagi bilan bir xil qiling
npm run dev
```

Lokal test uchun bu `http://localhost:5173` da ochiladi. **Lekin Telegram Mini
App faqat HTTPS manzillarda ishlaydi** — shuning uchun productionga chiqarish
kerak (quyida).

## 4-qadam: Production'ga chiqarish (qisqacha)

1. **Backend**: Railway, Render, yoki har qanday VPS'ga joylashtiring
   (FastAPI + bot bir jarayonda yoki ikkita alohida servis sifatida ishlaydi).
2. **Frontend**: `npm run build` qiling, natijadagi `dist/` papkasini Vercel,
   Netlify yoki Railway static hosting orqali joylashtiring — sizga HTTPS
   manzil beriladi (masalan `https://your-app.vercel.app`).
3. Backend `.env`dagi `MINI_APP_URL`ni shu manzilga o'zgartiring.
4. Frontend `.env`dagi `VITE_API_URL`ni backend manzilingizga o'zgartiring va
   qayta build qiling.
5. @BotFather'da `/mybots` → botingiz → **Bot Settings** → **Menu Button** →
   mini app URL'ini kiriting — shunda bot pastida doim "Kabinet" tugmasi
   turadi.

## Foydalanish

**O'qituvchi:**
- `/newgroup 9-A` — yangi guruh (sinf) yaratadi, taklif havolasini beradi
- `/groups` — barcha guruhlar va ularning havolalarini ko'rsatadi
- Havolani guruhga yuboradi → o'quvchilar bosib qo'shiladi
- Mini app orqali: dars jadvalini kiritadi, har kuni "Bugungi darslar"da
  davomat/uy vazifa/ballarni belgilaydi

**O'quvchi:**
- Havola orqali `/start` bosadi → guruhga avtomatik qo'shiladi
- Mini app orqali o'z ballari, davomati va dars tarixini ko'radi

## Keyingi bosqich (hozircha kiritilmagan)

- Ota-onalar uchun alohida ko'rinish — baza tuzilmasi shunga moslab
  qurilgan (`students` jadvaliga `parent_telegram_id` qo'shish va yangi
  router yozish orqali oson kengaytiriladi)
- Bir nechta o'qituvchi (hozir faqat bitta `TEACHER_TELEGRAM_ID`)

## Eslatma

Bu kod bu yerda **network bo'lmagan muhitda** yozilgan — paketlar
o'rnatilib, to'liq ishga tushirib sinalmagan (faqat Python sintaksisi
tekshirilgan). Birinchi marta ishga tushirganda kichik xatoliklar chiqishi
mumkin — shunday bo'lsa, xato matnini menga yuboring, birga tuzatamiz.
