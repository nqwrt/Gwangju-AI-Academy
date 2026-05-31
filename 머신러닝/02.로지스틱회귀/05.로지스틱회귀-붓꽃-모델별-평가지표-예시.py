import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# -----------------------------
# 1. 데이터 로드
# -----------------------------
from sklearn.datasets import load_breast_cancer
data = load_breast_cancer()

X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# -----------------------------
# 2. 모델 정의 (AutoML 핵심)
# -----------------------------
models = {
    "Logistic Regression": LogisticRegression(max_iter=5000),
    "Random Forest": RandomForestClassifier(n_estimators=100),
    "Gradient Boosting": GradientBoostingClassifier()
}

# -----------------------------
# 3. 평가 함수
# -----------------------------
def evaluate_model(model):
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    return {
        "Accuracy": accuracy_score(y_test, pred),
        "Precision": precision_score(y_test, pred),
        "Recall": recall_score(y_test, pred),
        "F1": f1_score(y_test, pred),
        "ROC-AUC": roc_auc_score(y_test, prob) if prob is not None else 0,
        "Confusion Matrix": confusion_matrix(y_test, pred)
    }

# -----------------------------
# 4. 모델 평가 실행
# -----------------------------
results = {}

for name, model in models.items():
    results[name] = evaluate_model(model)

# -----------------------------
# 5. UI
# -----------------------------
st.title("🤖 AutoML 모델 비교 대시보드")

# -----------------------------
# 6. 성능 테이블
# -----------------------------
st.subheader("📊 모델 성능 비교")

df_result = pd.DataFrame({
    model: {
        "Accuracy": results[model]["Accuracy"],
        "Precision": results[model]["Precision"],
        "Recall": results[model]["Recall"],
        "F1": results[model]["F1"],
        "ROC-AUC": results[model]["ROC-AUC"]
    }
    for model in results
}).T

st.dataframe(df_result)

# -----------------------------
# 7. 최고 모델 자동 선택
# -----------------------------
best_model = df_result["F1"].idxmax()

st.success(f"🏆 Best Model (F1 기준): {best_model}")

# -----------------------------
# 8. Confusion Matrix
# -----------------------------
st.subheader("📉 Confusion Matrix (Best Model)")

cm = results[best_model]["Confusion Matrix"]

fig, ax = plt.subplots()
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
st.pyplot(fig)

# -----------------------------
# 9. 그래프 비교
# -----------------------------
st.subheader("📈 F1 Score 비교")

fig2, ax2 = plt.subplots()
df_result["F1"].plot(kind="bar", ax=ax2)
ax2.set_ylim(0, 1)
ax2.set_ylabel("F1 Score")
st.pyplot(fig2)