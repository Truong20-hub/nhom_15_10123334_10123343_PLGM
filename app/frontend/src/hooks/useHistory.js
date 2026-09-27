import { useCallback, useState } from "react";
import { HISTORY_KEY, HISTORY_MAX } from "../constants.js";

function readHistory() {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
  } catch {
    return [];
  }
}

/** Quản lý lịch sử dự đoán (lưu local, backend chưa có /api/history) */
export function useHistory() {
  const [history, setHistory] = useState(readHistory);

  const addHistoryItem = useCallback((item) => {
    const list = readHistory();
    list.unshift(item);
    const trimmed = list.slice(0, HISTORY_MAX);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(trimmed));
    setHistory(trimmed);
  }, []);

  const refreshHistory = useCallback(() => {
    setHistory(readHistory());
  }, []);

  return { history, addHistoryItem, refreshHistory };
}
