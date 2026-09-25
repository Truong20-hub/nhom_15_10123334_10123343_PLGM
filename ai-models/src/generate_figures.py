"""
Script tạo các biểu đồ EDA và đánh giá mô hình chuẩn khoa học (300 DPI)
được lưu trữ tại docs/figures/
"""
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, precision_score, recall_score

# Cài đặt giao diện matplotlib thẩm mỹ cao
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['figure.dpi'] = 300

OUTPUT_DIR = "docs/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv("ai-models/data/train.csv")
label_names = ["0 (Low)", "1 (Medium)", "2 (High)", "3 (Very High)"]
colors = ["#2ec4b6", "#3a86ff", "#8338ec", "#ff006e"]

print("1. Tạo Hình 1: Phân phối lớp mục tiêu...")
fig, ax = plt.subplots(figsize=(8, 5))
counts = df['price_range'].value_counts().sort_index()
bars = ax.bar(label_names, counts.values, color=colors, width=0.55, edgecolor='black', alpha=0.85)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 10, f'{int(yval)} ({yval/len(df)*100:.1f}%)', 
            ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.set_ylim(0, 600)
ax.set_title("Hình 1: Phân Phối Biến Mục Tiêu (price_range)", pad=15, fontweight='bold')
ax.set_xlabel("Phân Khúc Giá (Price Range)")
ax.set_ylabel("Số Lượng Mẫu (Count)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "01_target_distribution.png"), dpi=300)
plt.close()

print("2. Tạo Hình 2: Ma trận tương quan đặc trưng...")
fig, ax = plt.subplots(figsize=(14, 11))
corr = df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
cmap = sns.diverging_palette(230, 20, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1.0, vmin=-0.2, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .8}, annot=True, fmt=".2f", annot_kws={"size": 8}, ax=ax)
ax.set_title("Hình 2: Ma Trận Hệ Số Tương Quan Pearson (Correlation Heatmap)", pad=20, fontweight='bold', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "02_correlation_heatmap.png"), dpi=300)
plt.close()

print("3. Tạo Hình 3: Phân phối RAM qua từng phân khúc giá...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
sns.boxplot(x='price_range', y='ram', data=df, palette=colors, ax=ax1, width=0.5)
ax1.set_xticklabels(label_names)
ax1.set_title("Biểu Đồ Hộp (Boxplot) RAM Theo Tầm Giá", fontweight='bold')
ax1.set_xlabel("Phân Khúc Giá")
ax1.set_ylabel("RAM (MegaBytes)")

sns.violinplot(x='price_range', y='ram', data=df, palette=colors, ax=ax2, inner="quartile")
ax2.set_xticklabels(label_names)
ax2.set_title("Biểu Đồ Phân Phối (Violin Plot) RAM", fontweight='bold')
ax2.set_xlabel("Phân Khúc Giá")
ax2.set_ylabel("RAM (MegaBytes)")

fig.suptitle("Hình 3: Tác Động Quyết Định Của Dung Lượng RAM Tới Phân Khúc Giá", fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "03_ram_vs_price.png"), dpi=300)
plt.close()

print("4. Tạo Hình 4: Dung lượng Pin và Độ phân giải điểm ảnh...")
df_temp = df.copy()
df_temp['total_pixels'] = (df_temp['px_height'] * df_temp['px_width']) / 1e6
fig, ax = plt.subplots(figsize=(10, 6))
scatter = sns.scatterplot(
    data=df_temp, x='battery_power', y='total_pixels', hue='price_range',
    palette=colors, alpha=0.75, s=70, ax=ax
)
handles, _ = scatter.get_legend_handles_labels()
ax.legend(handles=handles, labels=label_names, title="Phân Khúc Giá", frameon=True)
ax.set_title("Hình 4: Mối Quan Hệ Giữa Dung Lượng Pin và Tổng Độ Phân Giải (Megapixels)", pad=15, fontweight='bold')
ax.set_xlabel("Dung Lượng Pin - battery_power (mAh)")
ax.set_ylabel("Độ Phân Giải Màn Hình (Megapixels = px_h * px_w / 10^6)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "04_battery_and_resolution.png"), dpi=300)
plt.close()

print("5. Tạo Hình 5: Tỷ lệ kết nối hiện đại theo từng phân khúc giá...")
conn_cols = ['four_g', 'three_g', 'wifi', 'dual_sim', 'blue']
conn_labels = ['Mạng 4G', 'Mạng 3G', 'Wi-Fi', '2 SIM', 'Bluetooth']
conn_df = df.groupby('price_range')[conn_cols].mean() * 100

fig, ax = plt.subplots(figsize=(11, 6))
x = np.arange(len(conn_labels))
width = 0.18

for idx, (price_val, label) in enumerate(zip(range(4), label_names)):
    ax.bar(x + idx * width, conn_df.loc[price_val], width, label=label, color=colors[idx], edgecolor='black', alpha=0.85)

ax.set_title("Hình 5: Tỷ Lệ Trang Bị Các Chuẩn Kết Nối (%) Theo Từng Tầm Giá", pad=15, fontweight='bold')
ax.set_xticks(x + width * 1.5)
ax.set_xticklabels(conn_labels)
ax.set_ylabel("Tỷ Lệ Xuất Hiện (%)")
ax.set_ylim(0, 100)
ax.legend(title="Phân Khúc", frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "05_connectivity_distribution.png"), dpi=300)
plt.close()

print("6. Huấn luyện 4 mô hình để vẽ hình 6 (Model Comparison) & hình 7 (Confusion Matrix)...")
X = df.drop(columns=['price_range'])
y = df['price_range']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

models = {
    "Logistic Regression": Pipeline([('scaler', StandardScaler()), ('clf', LogisticRegression(max_iter=1000, random_state=42))]),
    "Support Vector Machine (SVC)": Pipeline([('scaler', StandardScaler()), ('clf', SVC(kernel='linear', C=1.0, probability=True, random_state=42))]),
    "Random Forest": Pipeline([('clf', RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42))]),
    "Gradient Boosting": Pipeline([('clf', GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, max_depth=4, random_state=42))])
}

results = []
trained_models = {}

for name, pipe in models.items():
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    y_train_pred = pipe.predict(X_train)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')
    prec = precision_score(y_test, y_pred, average='macro')
    rec = recall_score(y_test, y_pred, average='macro')
    train_acc = accuracy_score(y_train, y_train_pred)
    
    results.append({
        "Model": name,
        "Train Accuracy": train_acc,
        "Test Accuracy": acc,
        "Macro F1": f1,
        "Macro Precision": prec,
        "Macro Recall": rec
    })
    trained_models[name] = (pipe, y_pred, acc)
    print(f"  - {name}: Train Acc = {train_acc:.4f}, Test Acc = {acc:.4f}, Macro F1 = {f1:.4f}")

res_df = pd.DataFrame(results)

# Hình 6: Biểu đồ so sánh các mô hình
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.35
r1 = np.arange(len(res_df))
r2 = [x + bar_width for x in r1]

b1 = ax.bar(r1, res_df['Test Accuracy'] * 100, width=bar_width, color='#3a86ff', label='Độ chính xác (Accuracy %)', edgecolor='black')
b2 = ax.bar(r2, res_df['Macro F1'] * 100, width=bar_width, color='#8338ec', label='Macro F1-Score (%)', edgecolor='black')

for bar in b1:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f'{yval:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)
for bar in b2:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f'{yval:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)

ax.set_title("Hình 6: So Sánh Hiệu Năng 4 Mô Hình Học Máy Trên Tập Test", pad=15, fontweight='bold')
ax.set_xticks([r + bar_width/2 for r in range(len(res_df))])
ax.set_xticklabels(res_df['Model'], rotation=10, ha='right')
ax.set_ylabel("Tỷ Lệ (%)")
ax.set_ylim(70, 105)
ax.legend(frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "06_model_comparison.png"), dpi=300)
plt.close()

# Tìm mô hình tốt nhất (SVC linear đạt ~96-98% accuracy)
best_model_name = res_df.sort_values(by="Macro F1", ascending=False).iloc[0]["Model"]
best_pipe, best_y_pred, best_acc = trained_models[best_model_name]
print(f"Mô hình tốt nhất được chọn: {best_model_name} với Accuracy = {best_acc:.4f}")

# Hình 7: Ma trận nhầm lẫn của mô hình tốt nhất
fig, ax = plt.subplots(figsize=(8, 7))
cm = confusion_matrix(y_test, best_y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=label_names, yticklabels=label_names, annot_kws={"size": 14, "weight": "bold"}, ax=ax)
ax.set_title(f"Hình 7: Ma Trận Nhầm Lẫn (Confusion Matrix) — {best_model_name}", pad=15, fontweight='bold')
ax.set_xlabel("Nhãn Dự Đoán (Predicted Label)", fontweight='bold')
ax.set_ylabel("Nhãn Thực Tế (Actual Label)", fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "07_confusion_matrix.png"), dpi=300)
plt.close()

# Hình 8: Tầm quan trọng của đặc trưng
rf_pipe = trained_models["Random Forest"][0]
rf_clf = rf_pipe.named_steps['clf']
feat_imp = pd.Series(rf_clf.feature_importances_, index=X.columns).sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 8))
feat_imp.plot(kind='barh', color='#2ec4b6', edgecolor='black', ax=ax)
ax.set_title("Hình 8: Tầm Quan Trọng Của 20 Đặc Trưng (Random Forest Feature Importance)", pad=15, fontweight='bold')
ax.set_xlabel("Độ Quan Trọng Tương Đối (Feature Importance Score)")
for i, v in enumerate(feat_imp):
    ax.text(v + 0.005, i, f"{v:.4f}", va='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "08_feature_importance.png"), dpi=300)
plt.close()

print("Hoàn tất tạo toàn bộ 8 biểu đồ trong docs/figures/!")
