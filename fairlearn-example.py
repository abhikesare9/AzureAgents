# pip install fairlearn scikit-learn pandas matplotlib

from fairlearn.reductions import ExponentiatedGradient, DemographicParity
from fairlearn.metrics import MetricFrame, selection_rate
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

# Load local dataset (no internet needed)
data = load_breast_cancer(as_frame=True)
X = data.data
y = data.target

# Simulate a sensitive feature (age_group) by binning 'mean radius'
# Let's assume 'mean radius' can act like a proxy for some demographic group
X["age_group"] = pd.cut(X["mean radius"], bins=[0, 14, 20, 30], labels=["young", "middle", "old"])

# Separate sensitive feature
sensitive_feature = X["age_group"]
X = X.drop(columns=["age_group"])  # Remove it from training features

# Train-test split
X_train, X_test, y_train, y_test, sf_train, sf_test = train_test_split(
    X, y, sensitive_feature, test_size=0.3, random_state=42, stratify=y
)

# Train baseline model
baseline_model = LogisticRegression(max_iter=1000)
baseline_model.fit(X_train, y_train)
baseline_preds = baseline_model.predict(X_test)

print("📊 Baseline Accuracy:", accuracy_score(y_test, baseline_preds))
print("📊 Baseline Selection Rate by Group:")
print(
    MetricFrame(
        metrics=selection_rate,
        y_true=y_test,
        y_pred=baseline_preds,
        sensitive_features=sf_test
    )
)

# Train Fair Model with Demographic Parity constraint
fair_model = ExponentiatedGradient(
    LogisticRegression(solver='liblinear'),
    constraints=DemographicParity(),
    sample_weight_name='sample_weight'
)

fair_model.fit(X_train, y_train, sensitive_features=sf_train)
fair_preds = fair_model.predict(X_test)

print("\n✅ Fair Model Accuracy:", accuracy_score(y_test, fair_preds))
print("✅ Fair Model Selection Rate by Group:")
print(
    MetricFrame(
        metrics=selection_rate,
        y_true=y_test,
        y_pred=fair_preds,
        sensitive_features=sf_test
    )
)
