export function getTelegram() {
  return window.Telegram?.WebApp ?? null;
}

export function initTelegram() {
  const tg = getTelegram();
  if (tg) {
    tg.ready();
    tg.expand();
  }
  return tg;
}

export function getInitData() {
  return getTelegram()?.initData ?? "";
}

export function getTelegramUser() {
  return getTelegram()?.initDataUnsafe?.user ?? null;
}
