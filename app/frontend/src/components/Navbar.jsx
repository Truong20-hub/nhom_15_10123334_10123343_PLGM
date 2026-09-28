export default function Navbar({
  backendStatusText,
  backendOk,
  modelKey,
  onModelChange,
  theme,
  onToggleTheme,
}) {
  return (
    <header className="navbar">
      <div className="nav-container">
        <div className="brand">
          <div className="brand-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect>
              <line x1="12" y1="18" x2="12.01" y2="18"></line>
            </svg>
          </div>
          <div>
            <h1 className="brand-title">Mobile Price AI</h1>
            <p className="brand-subtitle">Học máy cơ bản • Kaggle Benchmark</p>
          </div>
        </div>

        <div className="header-badges">
          <div
            className="badge badge-pulse"
            id="statusBadge"
            style={backendOk ? { borderColor: "rgba(16, 185, 129, 0.4)" } : undefined}
          >
            <span className="pulse-dot"></span>
            <span>{backendStatusText}</span>
          </div>
          <div className="badge badge-model">
            <span className="badge-label">Model:</span>
            <select
              className="model-select"
              value={modelKey}
              onChange={(e) => onModelChange(e.target.value)}
            >
              <option value="lr">Logistic Regression</option>
              <option value="knn">KNN</option>
              <option value="svm">SVM</option>
              <option value="nai">Naive Bayes</option>
              <option value="best">Best Model (Auto)</option>
            </select>
            <span className="badge-tag">v1.0.0</span>
          </div>
          <div className="badge badge-acc">
            <span className="badge-label">Accuracy:</span>
            <strong>97.5%</strong>
          </div>
          <button
            className="btn-icon"
            title="Chuyển chế độ sáng/tối"
            aria-label="Toggle theme"
            onClick={onToggleTheme}
          >
            <svg className="sun-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="5"></circle>
              <line x1="12" y1="1" x2="12" y2="3"></line>
              <line x1="12" y1="21" x2="12" y2="23"></line>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
              <line x1="1" y1="12" x2="3" y2="12"></line>
              <line x1="21" y1="12" x2="23" y2="12"></line>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
}