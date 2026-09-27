export default function ToastContainer({ toasts }) {
  return (
    <div className="toast-container">
      {toasts.map((t) => (
        <div key={t.id} className={`toast${t.isError ? " toast-error" : ""}`}>
          {t.message}
        </div>
      ))}
    </div>
  );
}
