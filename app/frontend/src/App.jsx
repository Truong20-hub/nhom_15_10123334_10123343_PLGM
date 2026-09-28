import { useCallback, useEffect, useState } from "react";
import Navbar from "./components/Navbar.jsx";
import PresetsBar from "./components/PresetsBar.jsx";
import HardwareForm from "./components/HardwareForm.jsx";
import ResultCard from "./components/ResultCard.jsx";
import HistoryCard from "./components/HistoryCard.jsx";
import ToastContainer from "./components/ToastContainer.jsx";
import { useHistory } from "./hooks/useHistory.js";
import { useToasts } from "./hooks/useToasts.js";
import { checkSystemHealth, evaluateModel, generateRequestId, logStructured, predictPriceRange } from "./api.js";
import { DEFAULT_FEATURES, EVAL_DATASET, LABELS, MODEL_FILE_MAP, PRESETS, SLIDER_GROUPS } from "./constants.js";

// Danh sách phẳng tất cả field slider + toggle, dùng để xáo trộn ngẫu nhiên
const ALL_SLIDER_FIELDS = SLIDER_GROUPS.flatMap((g) => g.fields);
const ALL_TOGGLE_FIELDS = SLIDER_GROUPS.flatMap((g) => g.toggles || []);

export default function App() {
  const [features, setFeatures] = useState(DEFAULT_FEATURES);
  const [modelKey, setModelKey] = useState("best");
  const [theme, setTheme] = useState("dark");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [backendStatusText, setBackendStatusText] = useState("Backend: Đang kết nối...");
  const [backendOk, setBackendOk] = useState(false);

  const { history, addHistoryItem, refreshHistory } = useHistory();
  const { toasts, showToast } = useToasts();

  // Đồng bộ data-theme lên thẻ <html> giống bản HTML gốc
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  // Kiểm tra sức khỏe hệ thống khi nạp trang
  useEffect(() => {
    (async () => {
      try {
        const ok = await checkSystemHealth();
        if (ok) {
          setBackendStatusText("Hệ thống: Sẵn sàng (AI Connected)");
          setBackendOk(true);
        } else {
          setBackendStatusText("Backend: AI service chưa kết nối");
        }
      } catch {
        setBackendStatusText("Backend: Chưa kết nối (kiểm tra port 5000)");
      }
    })();
  }, []);

  const handleFieldChange = useCallback((name, value) => {
    setFeatures((prev) => ({ ...prev, [name]: value }));
  }, []);

  const handleToggleChange = useCallback((name, checked) => {
    setFeatures((prev) => ({ ...prev, [name]: checked ? 1 : 0 }));
  }, []);

  const applyPreset = useCallback((presetKey, presetLabel) => {
    const preset = PRESETS[presetKey];
    if (!preset) return;
    setFeatures((prev) => ({ ...prev, ...preset }));
    showToast(`Đã áp dụng cấu hình: ${presetLabel}`);
  }, [showToast]);

  const randomizeForm = useCallback(() => {
    setFeatures((prev) => {
      const next = { ...prev };

      // Xáo trộn từng slider trong phạm vi min/max/step của nó
      for (const field of ALL_SLIDER_FIELDS) {
        const { name, min, max, step } = field;
        const stepsCount = Math.floor((max - min) / step);
        const randStep = Math.floor(Math.random() * (stepsCount + 1));
        let randVal = min + randStep * step;
        if (step < 1) randVal = Math.round(randVal * 10) / 10;
        next[name] = randVal;
      }

      // Xáo trộn các toggle (70% khả năng bật, giống bản gốc)
      for (const toggle of ALL_TOGGLE_FIELDS) {
        next[toggle.name] = Math.random() > 0.3 ? 1 : 0;
      }

      return next;
    });
    showToast("Đã xáo trộn ngẫu nhiên các đặc trưng!");
  }, [showToast]);

  const resetForm = useCallback(() => {
    setFeatures((prev) => ({ ...prev, ...PRESETS.mid }));
    showToast("Đã đặt lại cấu hình mặc định (Tầm trung)");
  }, [showToast]);

  const handleSubmit = useCallback(async () => {
    const reqId = generateRequestId();
    logStructured("INFO", reqId, "click Dự đoán -> POST /predict");
    setIsSubmitting(true);

    const modelFile = MODEL_FILE_MAP[modelKey] || MODEL_FILE_MAP.best;

    try {
      const { labelIndex, model, latencyMs } = await predictPriceRange(features, modelFile, reqId);

      logStructured("INFO", reqId, `200 OK total ${latencyMs}ms, price_range: ${labelIndex}`);

      // Hiện kết quả dự đoán trước, không chờ evaluate (evaluate có thể chậm hơn)
      setResult({ requestId: reqId, labelIndex, model, latencyMs, metrics: null, metricsLoading: true });

      // Gọi song song việc lấy chỉ số đánh giá model (precision/recall/f1/confusion matrix)
      evaluateModel(model, EVAL_DATASET, reqId)
        .then((metrics) => {
          logStructured("INFO", reqId, `Evaluate OK, accuracy=${metrics?.accuracy}`);
          setResult((prev) => (prev && prev.requestId === reqId ? { ...prev, metrics, metricsLoading: false } : prev));
        })
        .catch((err) => {
          logStructured("ERROR", reqId, `Lỗi evaluate: ${err.message}`);
          setResult((prev) => (prev && prev.requestId === reqId ? { ...prev, metrics: null, metricsLoading: false } : prev));
          showToast("Không lấy được chỉ số đánh giá model (evaluate)", true);
        });

      addHistoryItem({
        request_id: reqId,
        label_index: labelIndex,
        model,
        latency_ms: latencyMs,
        prediction: LABELS[labelIndex]?.name || `Class ${labelIndex}`,
        features,
        timestamp: new Date().toISOString(),
      });
    } catch (err) {
      logStructured("ERROR", reqId, `Lỗi API: ${err.message}`);
      showToast(err.message || "Không thể kết nối Backend. Kiểm tra server Node (port 5000) đã chạy chưa!", true);
    } finally {
      setIsSubmitting(false);
    }
  }, [features, modelKey, addHistoryItem, showToast]);

  return (
    <>
      <div className="glow-orb orb-1"></div>
      <div className="glow-orb orb-2"></div>

      <Navbar
        backendStatusText={backendStatusText}
        backendOk={backendOk}
        modelKey={modelKey}
        onModelChange={setModelKey}
        theme={theme}
        onToggleTheme={() => setTheme((t) => (t === "light" ? "dark" : "light"))}
      />

      <main className="main-layout">
        <PresetsBar onApplyPreset={applyPreset} onRandomize={randomizeForm} />

        <div className="content-grid">
          <HardwareForm
            features={features}
            onFieldChange={handleFieldChange}
            onToggleChange={handleToggleChange}
            onSubmit={handleSubmit}
            onReset={resetForm}
            isSubmitting={isSubmitting}
          />

          <aside className="results-column">
            <ResultCard result={result} />
            <HistoryCard history={history} onRefresh={() => { refreshHistory(); showToast("Đã làm mới danh sách lịch sử!"); }} />
          </aside>
        </div>
      </main>

      <ToastContainer toasts={toasts} />
    </>
  );
}