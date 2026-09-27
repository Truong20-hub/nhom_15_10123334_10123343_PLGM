import { useCallback, useRef, useState } from "react";

/** Quản lý danh sách Toast hiển thị góc màn hình */
export function useToasts() {
  const [toasts, setToasts] = useState([]);
  const idRef = useRef(0);

  const showToast = useCallback((message, isError = false) => {
    const id = idRef.current++;
    setToasts((prev) => [...prev, { id, message, isError }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 3500);
  }, []);

  return { toasts, showToast };
}
