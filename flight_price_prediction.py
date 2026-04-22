"""
Flight Ticket Price Prediction - Machine Learning Project
Arden University - COM7022 Machine Learning
Assignment: AeroInsights Analytics Practical Project

This script:
1. Preprocesses and explores the flight booking dataset
2. Performs statistical hypothesis testing
3. Builds and evaluates multiple regression models
4. Saves each visualization as a separate image
5. Provides interpretable outputs for academic reporting

Author: Farid Negahbani (SID:24154844)
"""

import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error,
    mean_absolute_percentage_error
)

# =============================================================================
# 0. CONFIGURATION
# =============================================================================
print("=" * 100)
print("FLIGHT TICKET PRICE PREDICTION - COMPLETE MACHINE LEARNING PROJECT")
print("=" * 100)

OUTPUT_DIR = "outputs"
PLOTS_DIR = os.path.join(OUTPUT_DIR, "plots")
TABLES_DIR = os.path.join(OUTPUT_DIR, "tables")

os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# =============================================================================
# 1. HELPER FUNCTIONS
# =============================================================================
def save_current_plot(filename):
    path = os.path.join(PLOTS_DIR, filename)
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[X] Saved plot: {path}")

def rmsle_score(y_true, y_pred):
    """
    Root Mean Squared Logarithmic Error
    Protect against negative predictions by clipping at zero.
    """
    y_pred_safe = np.maximum(y_pred, 0)
    return np.sqrt(np.mean((np.log1p(y_pred_safe) - np.log1p(y_true)) ** 2))

def print_section(title):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)

def print_subsection(title):
    print("\n" + "-" * 100)
    print(title)
    print("-" * 100)

def evaluate_regression_model(model_name, y_train, y_train_pred, y_test, y_test_pred):
    train_r2 = r2_score(y_train, y_train_pred)
    test_r2 = r2_score(y_test, y_test_pred)

    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))

    train_mae = mean_absolute_error(y_train, y_train_pred)
    test_mae = mean_absolute_error(y_test, y_test_pred)

    train_mape = mean_absolute_percentage_error(y_train, y_train_pred)
    test_mape = mean_absolute_percentage_error(y_test, y_test_pred)

    train_rmsle = rmsle_score(y_train, y_train_pred)
    test_rmsle = rmsle_score(y_test, y_test_pred)

    metrics = {
        "Model": model_name,
        "Train_R2": train_r2,
        "Test_R2": test_r2,
        "Train_RMSE": train_rmse,
        "Test_RMSE": test_rmse,
        "Train_MAE": train_mae,
        "Test_MAE": test_mae,
        "Train_MAPE": train_mape,
        "Test_MAPE": test_mape,
        "Train_RMSLE": train_rmsle,
        "Test_RMSLE": test_rmsle
    }

    print(f"\n{model_name} Performance:")
    print(f"   Train R²     : {train_r2:.4f}")
    print(f"   Test R²      : {test_r2:.4f}")
    print(f"   Train RMSE   : ₹{train_rmse:.2f}")
    print(f"   Test RMSE    : ₹{test_rmse:.2f}")
    print(f"   Train MAE    : ₹{train_mae:.2f}")
    print(f"   Test MAE     : ₹{test_mae:.2f}")
    print(f"   Train MAPE   : {train_mape:.4f} ({train_mape*100:.2f}%)")
    print(f"   Test MAPE    : {test_mape:.4f} ({test_mape*100:.2f}%)")
    print(f"   Train RMSLE  : {train_rmsle:.4f}")
    print(f"   Test RMSLE   : {test_rmsle:.4f}")

    return metrics

# =============================================================================
# 2. DATA LOADING
# =============================================================================
print_section("1. DATA LOADING")

excel_path = r"Dataset\Flight_dataset_4039.xlsx"
csv_path = r"Dataset\Flight_dataset_4039.csv"

if os.path.exists(excel_path):
    df = pd.read_excel(excel_path)
    data_source = excel_path
elif os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    data_source = csv_path
else:
    raise FileNotFoundError(
        "Dataset file not found. Please place either:\n"
        "- Dataset\\Flight_dataset_4039.xlsx\n"
        "- Dataset\\Flight_dataset_4039.csv"
    )

print(f"Dataset loaded from: {data_source}")
print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")
print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# =============================================================================
# 3. DATA PREPROCESSING
# =============================================================================
print_section("2. DATA PREPROCESSING")

print("Initial Columns:")
print(list(df.columns))

print("\nData Types:")
print(df.dtypes)

duplicates_before = df.duplicated().sum()
df = df.drop_duplicates()
print(f"\nDuplicates removed: {duplicates_before}")
print(f"Shape after duplicate removal: {df.shape}")

columns_to_drop = []
for col in ["Unnamed: 0", "flight"]:
    if col in df.columns:
        columns_to_drop.append(col)

if columns_to_drop:
    df = df.drop(columns=columns_to_drop)
    print(f"Columns dropped: {columns_to_drop}")
else:
    print("No unnecessary columns found to drop from ['Unnamed: 0', 'flight']")

print("\nMissing values before handling:")
missing_before = df.isnull().sum()
print(missing_before[missing_before > 0] if (missing_before > 0).any() else "No missing values found.")

if "price" not in df.columns:
    raise ValueError("Target column 'price' not found in dataset.")

df = df.dropna(subset=["price"])

for col in ["duration", "days_left"]:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

# Fill missing categorical values with mode if any exist
categorical_candidate_cols = [
    "airline", "source_city", "departure_time", "stops",
    "arrival_time", "destination_city", "class"
]
for col in categorical_candidate_cols:
    if col in df.columns and df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].mode()[0])

print("\nMissing values after handling:")
missing_after = df.isnull().sum()
print(missing_after[missing_after > 0] if (missing_after > 0).any() else "No missing values remain.")

print(f"\nFinal cleaned dataset shape: {df.shape}")

# =============================================================================
# 4. FEATURE ENGINEERING
# =============================================================================
print_section("3. FEATURE ENGINEERING")

# Route feature
if "source_city" in df.columns and "destination_city" in df.columns:
    df["route"] = df["source_city"].astype(str) + "-" + df["destination_city"].astype(str)
    print(f"Created route feature with {df['route'].nunique()} unique routes")

# Duration in minutes
if "duration" in df.columns:
    df["duration_minutes"] = (df["duration"] * 60).round(0)
    print("Created duration_minutes feature from duration")

# Days left bins
if "days_left" in df.columns:
    df["booking_window_group"] = pd.cut(
        df["days_left"],
        bins=[-1, 3, 7, 14, 30, df["days_left"].max()],
        labels=["Last_3_days", "4_7_days", "8_14_days", "15_30_days", "30+_days"]
    )
    print("Created booking_window_group feature from days_left")

print("\nFeature Engineering Summary:")
engineered_cols = [col for col in ["route", "duration_minutes", "booking_window_group"] if col in df.columns]
print(engineered_cols if engineered_cols else "No engineered features created")

# =============================================================================
# 5. EXPLORATORY DATA ANALYSIS
# =============================================================================
print_section("4. EXPLORATORY DATA ANALYSIS")

categorical_features = [col for col in [
    "airline", "source_city", "departure_time", "stops",
    "arrival_time", "destination_city", "class", "route", "booking_window_group"
] if col in df.columns]

numerical_features = [col for col in ["duration", "duration_minutes", "days_left", "price"] if col in df.columns]

print(f"Categorical features ({len(categorical_features)}): {categorical_features}")
print(f"Numerical features ({len(numerical_features)}): {numerical_features}")

print_subsection("Summary Statistics")
print(df[numerical_features].describe().T)

# =============================================================================
# 6. VISUALIZATIONS - EACH PLOT SAVED SEPARATELY
# =============================================================================
print_section("5. VISUALIZATIONS")

# 1. Histogram of Prices
plt.figure(figsize=(10, 6))
plt.hist(df["price"], bins=50, color="skyblue", edgecolor="black", alpha=0.75)
plt.title("Distribution of Flight Ticket Prices", fontweight="bold")
plt.xlabel("Price (₹)")
plt.ylabel("Frequency")
plt.grid(axis="y", alpha=0.3)
save_current_plot("01_price_distribution_histogram.png")

# 2. Boxplot: Price by Airline
if "airline" in df.columns:
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="airline", y="price")
    plt.title("Price Distribution by Airline", fontweight="bold")
    plt.xlabel("Airline")
    plt.ylabel("Price (₹)")
    plt.xticks(rotation=45, ha="right")
    save_current_plot("02_price_by_airline_boxplot.png")

# 3. Boxplot: Price by Class
if "class" in df.columns:
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x="class", y="price")
    plt.title("Price Distribution by Class", fontweight="bold")
    plt.xlabel("Class")
    plt.ylabel("Price (₹)")
    save_current_plot("03_price_by_class_boxplot.png")

# 4. Boxplot: Price by Stops
if "stops" in df.columns:
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x="stops", y="price")
    plt.title("Price Distribution by Number of Stops", fontweight="bold")
    plt.xlabel("Stops")
    plt.ylabel("Price (₹)")
    plt.xticks(rotation=20)
    save_current_plot("04_price_by_stops_boxplot.png")

# 5. Scatter: Duration vs Price
if "duration" in df.columns:
    plt.figure(figsize=(10, 6))
    plt.scatter(df["duration"], df["price"], alpha=0.3, s=12, color="green")
    plt.title("Duration vs Price", fontweight="bold")
    plt.xlabel("Duration (hours)")
    plt.ylabel("Price (₹)")
    plt.grid(alpha=0.3)
    save_current_plot("05_duration_vs_price_scatter.png")

# 6. Scatter: Days Left vs Price
if "days_left" in df.columns:
    plt.figure(figsize=(10, 6))
    plt.scatter(df["days_left"], df["price"], alpha=0.3, s=12, color="orange")
    plt.title("Days Left vs Price", fontweight="bold")
    plt.xlabel("Days Left to Departure")
    plt.ylabel("Price (₹)")
    plt.grid(alpha=0.3)
    save_current_plot("06_days_left_vs_price_scatter.png")

# 7. Bar: Average Price by Airline
if "airline" in df.columns:
    plt.figure(figsize=(12, 6))
    avg_price_airline = df.groupby("airline")["price"].mean().sort_values(ascending=False)
    avg_price_airline.plot(kind="bar", color="coral")
    plt.title("Average Price by Airline", fontweight="bold")
    plt.xlabel("Airline")
    plt.ylabel("Average Price (₹)")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", alpha=0.3)
    save_current_plot("07_average_price_by_airline_bar.png")

# 8. Bar: Average Price by Class
if "class" in df.columns:
    plt.figure(figsize=(8, 6))
    avg_price_class = df.groupby("class")["price"].mean().sort_values(ascending=False)
    avg_price_class.plot(kind="bar", color="lightgreen")
    plt.title("Average Price by Class", fontweight="bold")
    plt.xlabel("Class")
    plt.ylabel("Average Price (₹)")
    plt.xticks(rotation=0)
    plt.grid(axis="y", alpha=0.3)
    save_current_plot("08_average_price_by_class_bar.png")

# 9. Bar: Average Price by Stops
if "stops" in df.columns:
    plt.figure(figsize=(8, 6))
    avg_price_stops = df.groupby("stops")["price"].mean().sort_values(ascending=False)
    avg_price_stops.plot(kind="bar", color="lightblue")
    plt.title("Average Price by Number of Stops", fontweight="bold")
    plt.xlabel("Stops")
    plt.ylabel("Average Price (₹)")
    plt.xticks(rotation=20)
    plt.grid(axis="y", alpha=0.3)
    save_current_plot("09_average_price_by_stops_bar.png")

# 10. Boxplot: Price by Source City
if "source_city" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="source_city", y="price")
    plt.title("Price Distribution by Source City", fontweight="bold")
    plt.xlabel("Source City")
    plt.ylabel("Price (₹)")
    plt.xticks(rotation=45, ha="right")
    save_current_plot("10_price_by_source_city_boxplot.png")

# 11. Boxplot: Price by Destination City
if "destination_city" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="destination_city", y="price")
    plt.title("Price Distribution by Destination City", fontweight="bold")
    plt.xlabel("Destination City")
    plt.ylabel("Price (₹)")
    plt.xticks(rotation=45, ha="right")
    save_current_plot("11_price_by_destination_city_boxplot.png")

# 12. Boxplot: Price by Departure Time
if "departure_time" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="departure_time", y="price")
    plt.title("Price Distribution by Departure Time", fontweight="bold")
    plt.xlabel("Departure Time")
    plt.ylabel("Price (₹)")
    plt.xticks(rotation=45, ha="right")
    save_current_plot("12_price_by_departure_time_boxplot.png")

# 13. Boxplot: Price by Arrival Time
if "arrival_time" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="arrival_time", y="price")
    plt.title("Price Distribution by Arrival Time", fontweight="bold")
    plt.xlabel("Arrival Time")
    plt.ylabel("Price (₹)")
    plt.xticks(rotation=45, ha="right")
    save_current_plot("13_price_by_arrival_time_boxplot.png")

# 14. Boxplot: Price by Route (Top 15 Routes only for readability)
if "route" in df.columns:
    top_routes = df["route"].value_counts().head(15).index
    df_top_routes = df[df["route"].isin(top_routes)]
    plt.figure(figsize=(14, 7))
    sns.boxplot(data=df_top_routes, x="route", y="price")
    plt.title("Price Distribution by Route (Top 15 Routes)", fontweight="bold")
    plt.xlabel("Route")
    plt.ylabel("Price (₹)")
    plt.xticks(rotation=45, ha="right")
    save_current_plot("14_price_by_route_top15_boxplot.png")

# 15. Correlation Heatmap
corr_cols = [col for col in ["duration", "duration_minutes", "days_left", "price"] if col in df.columns]
if len(corr_cols) >= 2:
    plt.figure(figsize=(8, 6))
    corr_matrix = df[corr_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, square=True)
    plt.title("Correlation Heatmap - Numerical Features", fontweight="bold")
    save_current_plot("15_correlation_heatmap.png")
else:
    corr_matrix = pd.DataFrame()

# =============================================================================
# 7. STATISTICAL HYPOTHESIS TESTING
# =============================================================================
print_section("6. STATISTICAL HYPOTHESIS TESTING")

# Hypothesis 1: Airline vs Price
if "airline" in df.columns:
    print_subsection("Hypothesis Test 1: ANOVA - Price Across Airlines")
    print("H0: Average ticket price is the same across all airlines")
    print("H1: At least one airline has a significantly different average price")

    airline_groups = [group["price"].values for _, group in df.groupby("airline")]
    f_stat_airline, p_value_airline = stats.f_oneway(*airline_groups)

    print(f"F-statistic: {f_stat_airline:.4f}")
    print(f"P-value    : {p_value_airline:.6e}")
    if p_value_airline < 0.05:
        print("Decision   : Reject H0")
    else:
        print("Decision   : Fail to Reject H0")

# Hypothesis 2: Class vs Price
if "class" in df.columns:
    print_subsection("Hypothesis Test 2: T-Test - Business vs Economy")
    print("H0: Business and Economy have the same average price")
    print("H1: Business and Economy have different average prices")

    business_prices = df[df["class"] == "Business"]["price"]
    economy_prices = df[df["class"] == "Economy"]["price"]

    t_stat_class, p_value_class = stats.ttest_ind(
        business_prices,
        economy_prices,
        equal_var=False
    )

    print(f"T-statistic: {t_stat_class:.4f}")
    print(f"P-value    : {p_value_class:.6e}")
    if p_value_class < 0.05:
        print("Decision   : Reject H0")
    else:
        print("Decision   : Fail to Reject H0")

# Hypothesis 3: Departure Time vs Price
if "departure_time" in df.columns:
    print_subsection("Hypothesis Test 3: ANOVA - Price Across Departure Time")
    print("H0: Average ticket price is the same across all departure times")
    print("H1: At least one departure time group has a different average price")

    departure_groups = [group["price"].values for _, group in df.groupby("departure_time")]
    f_stat_departure, p_value_departure = stats.f_oneway(*departure_groups)

    print(f"F-statistic: {f_stat_departure:.4f}")
    print(f"P-value    : {p_value_departure:.6e}")
    if p_value_departure < 0.05:
        print("Decision   : Reject H0")
    else:
        print("Decision   : Fail to Reject H0")

# Hypothesis 4: Route vs Price
if "route" in df.columns:
    print_subsection("Hypothesis Test 4: ANOVA - Price Across Routes")
    print("H0: Average ticket price is the same across all routes")
    print("H1: At least one route has a different average price")

    route_groups = [group["price"].values for _, group in df.groupby("route")]
    f_stat_route, p_value_route = stats.f_oneway(*route_groups)

    print(f"F-statistic: {f_stat_route:.4f}")
    print(f"P-value    : {p_value_route:.6e}")
    if p_value_route < 0.05:
        print("Decision   : Reject H0")
    else:
        print("Decision   : Fail to Reject H0")

# =============================================================================
# 8. VARIABLE JUSTIFICATION
# =============================================================================
print_section("7. JUSTIFICATION OF INDEPENDENT VARIABLES")

feature_justification = {
    "airline": "Different airlines follow different pricing strategies, service levels, and brand positioning.",
    "source_city": "Origin city influences demand patterns, airport traffic, and fare levels.",
    "departure_time": "Departure timing affects convenience and demand, which can change ticket prices.",
    "stops": "Flights with fewer stops are often more convenient and may command premium pricing.",
    "arrival_time": "Arrival timing may affect customer preference and route attractiveness.",
    "destination_city": "Destination city reflects route demand, market competition, and regional pricing differences.",
    "class": "Business and Economy classes have fundamentally different pricing structures.",
    "duration": "Longer or shorter travel duration can indicate route convenience and service quality.",
    "duration_minutes": "Provides a more granular numerical representation of travel duration.",
    "days_left": "Booking lead time is strongly linked to fare fluctuation and revenue management strategy.",
    "route": "The source-destination combination directly captures route-specific pricing behavior."
}

for key, value in feature_justification.items():
    if key in df.columns or key == "duration_minutes":
        print(f"- {key}: {value}")

print("\nDropped / Excluded Variables Justification:")
print("- flight: Dropped because flight identifier behaves like an ID and may not generalize well.")
print("- Unnamed: 0: Dropped because it is only an index column and has no predictive meaning.")

# =============================================================================
# 9. ENCODING AND MODEL PREPARATION
# =============================================================================
print_section("8. ENCODING AND MODEL PREPARATION")

df_model = df.copy()

# Label encoding for tree models and baseline consistency
# Note: For a more statistically strict linear interpretation, one-hot encoding is preferable.
categorical_to_encode = [col for col in [
    "airline", "source_city", "departure_time", "stops",
    "arrival_time", "destination_city", "class", "route", "booking_window_group"
] if col in df_model.columns]

label_encoders = {}
for col in categorical_to_encode:
    le = LabelEncoder()
    df_model[col + "_encoded"] = le.fit_transform(df_model[col].astype(str))
    label_encoders[col] = le
    print(f"[X] Encoded {col} -> {col + '_encoded'} ({len(le.classes_)} classes)")

feature_columns = [col for col in [
    "airline_encoded",
    "source_city_encoded",
    "departure_time_encoded",
    "stops_encoded",
    "arrival_time_encoded",
    "destination_city_encoded",
    "class_encoded",
    "route_encoded",
    "booking_window_group_encoded",
    "duration",
    "duration_minutes",
    "days_left"
] if col in df_model.columns]

X = df_model[feature_columns].copy()
y = df_model["price"].copy()

X = X.fillna(X.median(numeric_only=True))

print(f"\nSelected feature columns ({len(feature_columns)}):")
print(feature_columns)
print(f"Feature matrix shape: {X.shape}")
print(f"Target shape: {y.shape}")

# =============================================================================
# 10. TRAIN-TEST SPLIT AND SCALING
# =============================================================================
print_section("9. TRAIN-TEST SPLIT AND SCALING")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("StandardScaler applied for linear-based models")

# =============================================================================
# 11. MODEL 1 - LINEAR REGRESSION
# =============================================================================
print_section("10. MODEL 1 - LINEAR REGRESSION")

lr_model = LinearRegression()
lr_model.fit(X_train_scaled, y_train)

y_train_pred_lr = lr_model.predict(X_train_scaled)
y_test_pred_lr = lr_model.predict(X_test_scaled)

metrics_lr = evaluate_regression_model(
    "Linear Regression",
    y_train, y_train_pred_lr,
    y_test, y_test_pred_lr
)

feature_importance_lr = pd.DataFrame({
    "Feature": feature_columns,
    "Coefficient": lr_model.coef_
})
feature_importance_lr["Abs_Coefficient"] = feature_importance_lr["Coefficient"].abs()
feature_importance_lr = feature_importance_lr.sort_values("Abs_Coefficient", ascending=False)

print("\nTop 10 Linear Regression Coefficients:")
print(feature_importance_lr.head(10).to_string(index=False))

# =============================================================================
# 12. MODEL 2 - RIDGE REGRESSION
# =============================================================================
print_section("11. MODEL 2 - RIDGE REGRESSION")

ridge_model = Ridge(alpha=1.0, random_state=42)
ridge_model.fit(X_train_scaled, y_train)

y_train_pred_ridge = ridge_model.predict(X_train_scaled)
y_test_pred_ridge = ridge_model.predict(X_test_scaled)

metrics_ridge = evaluate_regression_model(
    "Ridge Regression",
    y_train, y_train_pred_ridge,
    y_test, y_test_pred_ridge
)

# =============================================================================
# 13. MODEL 3 - LASSO REGRESSION
# =============================================================================
print_section("12. MODEL 3 - LASSO REGRESSION")

lasso_model = Lasso(alpha=0.1, random_state=42, max_iter=10000)
lasso_model.fit(X_train_scaled, y_train)

y_train_pred_lasso = lasso_model.predict(X_train_scaled)
y_test_pred_lasso = lasso_model.predict(X_test_scaled)

metrics_lasso = evaluate_regression_model(
    "Lasso Regression",
    y_train, y_train_pred_lasso,
    y_test, y_test_pred_lasso
)

# =============================================================================
# 14. MODEL 4 - RANDOM FOREST REGRESSOR
# =============================================================================
print_section("13. MODEL 4 - RANDOM FOREST REGRESSOR")

rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)

y_train_pred_rf = rf_model.predict(X_train)
y_test_pred_rf = rf_model.predict(X_test)

metrics_rf = evaluate_regression_model(
    "Random Forest Regressor",
    y_train, y_train_pred_rf,
    y_test, y_test_pred_rf
)

feature_importance_rf = pd.DataFrame({
    "Feature": feature_columns,
    "Importance": rf_model.feature_importances_
}).sort_values("Importance", ascending=False)

print("\nTop 10 Random Forest Feature Importances:")
print(feature_importance_rf.head(10).to_string(index=False))

# =============================================================================
# 15. MODEL COMPARISON
# =============================================================================
print_section("14. MODEL COMPARISON")

all_metrics = pd.DataFrame([metrics_lr, metrics_ridge, metrics_lasso, metrics_rf])

display_cols = [
    "Model", "Train_R2", "Test_R2",
    "Train_RMSE", "Test_RMSE",
    "Train_MAE", "Test_MAE",
    "Train_MAPE", "Test_MAPE",
    "Train_RMSLE", "Test_RMSLE"
]

print(all_metrics[display_cols].to_string(index=False))

all_metrics.to_csv(os.path.join(TABLES_DIR, "model_performance_summary.csv"), index=False)
print(f"\n[X] Saved table: {os.path.join(TABLES_DIR, 'model_performance_summary.csv')}")

best_model_row = all_metrics.sort_values(by=["Test_R2", "Test_RMSE"], ascending=[False, True]).iloc[0]
best_model_name = best_model_row["Model"]

print(f"\nSelected Best Model: {best_model_name}")
print("Selection basis: Highest Test R² and lower error values on unseen data.")

# =============================================================================
# 16. INDIVIDUAL MODEL PLOTS - SAVED SEPARATELY
# =============================================================================
print_section("15. MODEL DIAGNOSTIC PLOTS")

# Linear Regression - Actual vs Predicted
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_test_pred_lr, alpha=0.3, s=12, color="blue")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
plt.title("Linear Regression - Actual vs Predicted", fontweight="bold")
plt.xlabel("Actual Price (₹)")
plt.ylabel("Predicted Price (₹)")
plt.grid(alpha=0.3)
save_current_plot("16_linear_regression_actual_vs_predicted.png")

# Linear Regression - Residual Plot
plt.figure(figsize=(8, 6))
residuals_lr = y_test - y_test_pred_lr
plt.scatter(y_test_pred_lr, residuals_lr, alpha=0.3, s=12, color="blue")
plt.axhline(y=0, color="red", linestyle="--", lw=2)
plt.title("Linear Regression - Residual Plot", fontweight="bold")
plt.xlabel("Predicted Price (₹)")
plt.ylabel("Residuals (₹)")
plt.grid(alpha=0.3)
save_current_plot("17_linear_regression_residuals.png")

# Linear Regression - Feature Coefficients
plt.figure(figsize=(10, 6))
top_lr = feature_importance_lr.head(10).sort_values("Abs_Coefficient", ascending=True)
plt.barh(top_lr["Feature"], top_lr["Abs_Coefficient"], color="skyblue")
plt.title("Linear Regression - Top 10 Features by Absolute Coefficient", fontweight="bold")
plt.xlabel("Absolute Coefficient")
plt.ylabel("Feature")
plt.grid(axis="x", alpha=0.3)
save_current_plot("18_linear_regression_feature_importance.png")

# Ridge - Actual vs Predicted
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_test_pred_ridge, alpha=0.3, s=12, color="purple")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
plt.title("Ridge Regression - Actual vs Predicted", fontweight="bold")
plt.xlabel("Actual Price (₹)")
plt.ylabel("Predicted Price (₹)")
plt.grid(alpha=0.3)
save_current_plot("19_ridge_actual_vs_predicted.png")

# Lasso - Actual vs Predicted
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_test_pred_lasso, alpha=0.3, s=12, color="brown")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
plt.title("Lasso Regression - Actual vs Predicted", fontweight="bold")
plt.xlabel("Actual Price (₹)")
plt.ylabel("Predicted Price (₹)")
plt.grid(alpha=0.3)
save_current_plot("20_lasso_actual_vs_predicted.png")

# Random Forest - Actual vs Predicted
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_test_pred_rf, alpha=0.3, s=12, color="green")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
plt.title("Random Forest - Actual vs Predicted", fontweight="bold")
plt.xlabel("Actual Price (₹)")
plt.ylabel("Predicted Price (₹)")
plt.grid(alpha=0.3)
save_current_plot("21_random_forest_actual_vs_predicted.png")

# Random Forest - Residual Plot
plt.figure(figsize=(8, 6))
residuals_rf = y_test - y_test_pred_rf
plt.scatter(y_test_pred_rf, residuals_rf, alpha=0.3, s=12, color="green")
plt.axhline(y=0, color="red", linestyle="--", lw=2)
plt.title("Random Forest - Residual Plot", fontweight="bold")
plt.xlabel("Predicted Price (₹)")
plt.ylabel("Residuals (₹)")
plt.grid(alpha=0.3)
save_current_plot("22_random_forest_residuals.png")

# Random Forest - Feature Importance
plt.figure(figsize=(10, 6))
top_rf = feature_importance_rf.head(10).sort_values("Importance", ascending=True)
plt.barh(top_rf["Feature"], top_rf["Importance"], color="lightgreen")
plt.title("Random Forest - Top 10 Feature Importances", fontweight="bold")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.grid(axis="x", alpha=0.3)
save_current_plot("23_random_forest_feature_importance.png")

# =============================================================================
# 17. REGRESSION COEFFICIENT INTERPRETATION
# =============================================================================
print_section("16. REGRESSION COEFFICIENT INTERPRETATION")

print(f"Linear Regression Intercept: ₹{lr_model.intercept_:.2f}")
print("\nTop coefficient interpretations:")

for _, row in feature_importance_lr.head(10).iterrows():
    feature = row["Feature"]
    coeff = row["Coefficient"]
    direction = "increases" if coeff > 0 else "decreases"
    print(f"- {feature}: A one-unit increase is associated with a {direction} of ₹{abs(coeff):.2f} in predicted price (holding other variables constant).")

print("\nImportant Note:")
print("For label-encoded categorical features, coefficient interpretation should be treated cautiously.")
print("One-Hot Encoding would provide more statistically interpretable coefficients for purely nominal variables.")

# =============================================================================
# 18. KEY FINDINGS
# =============================================================================
print_section("17. KEY FINDINGS")

if "airline" in df.columns:
    most_expensive_airline = df.groupby("airline")["price"].mean().idxmax()
    cheapest_airline = df.groupby("airline")["price"].mean().idxmin()
else:
    most_expensive_airline = "N/A"
    cheapest_airline = "N/A"

if "class" in df.columns:
    business_mean = df[df["class"] == "Business"]["price"].mean() if "Business" in df["class"].astype(str).unique() else np.nan
    economy_mean = df[df["class"] == "Economy"]["price"].mean() if "Economy" in df["class"].astype(str).unique() else np.nan
else:
    business_mean = np.nan
    economy_mean = np.nan

duration_price_corr = df[["duration", "price"]].corr().loc["duration", "price"] if "duration" in df.columns else np.nan
daysleft_price_corr = df[["days_left", "price"]].corr().loc["days_left", "price"] if "days_left" in df.columns else np.nan

print(f"""
1. Dataset contains {len(df):,} cleaned samples.
2. Price range: ₹{df['price'].min():.0f} to ₹{df['price'].max():.0f}
3. Most expensive airline on average: {most_expensive_airline}
4. Most economical airline on average: {cheapest_airline}
5. Business average price: ₹{business_mean:.2f}
6. Economy average price: ₹{economy_mean:.2f}
7. Duration-Price correlation: {duration_price_corr:.4f}
8. DaysLeft-Price correlation: {daysleft_price_corr:.4f}
9. Best selected model: {best_model_name}
10. The selected model explains approximately {best_model_row['Test_R2']*100:.2f}% of the variance in ticket prices on test data.
""")

print("Interpretive Summary:")
print("- Ticket prices vary significantly across airlines, routes, class types, and departure timings.")
print("- Booking lead time is an important pricing driver and reflects airline revenue management behavior.")
print("- Travel class is one of the strongest determinants of airfare level.")
print("- Route-specific behavior matters; therefore, including route improves predictive context.")
print("- Random Forest often performs better because airfare pricing patterns are not purely linear.")

# =============================================================================
# 19. LIMITATIONS AND IMPROVEMENT POINTS
# =============================================================================
print_section("18. LIMITATIONS AND FUTURE IMPROVEMENTS")

print("""
LIMITATIONS:
1. Label encoding of nominal categorical variables may reduce interpretability for linear models.
2. Seasonal effects, holidays, demand shocks, and fuel prices are not included.
3. The model assumes that historical relationships remain stable over time.
4. Airline pricing is dynamic and may change with external market conditions.
5. Some route/time interactions may be non-linear and only partially captured.

SUGGESTED IMPROVEMENTS:
1. Use One-Hot Encoding for linear regression models.
2. Apply cross-validation and hyperparameter tuning.
3. Add calendar variables such as month, weekday, holiday period, and festival season.
4. Introduce route distance if available from external sources.
5. Test additional models such as XGBoost, Gradient Boosting, and ElasticNet.
""")

# =============================================================================
# 20. SAVE IMPORTANT TABLES
# =============================================================================
print_section("19. SAVING IMPORTANT OUTPUT TABLES")

feature_importance_lr.to_csv(os.path.join(TABLES_DIR, "linear_regression_coefficients.csv"), index=False)
feature_importance_rf.to_csv(os.path.join(TABLES_DIR, "random_forest_feature_importance.csv"), index=False)

if not corr_matrix.empty:
    corr_matrix.to_csv(os.path.join(TABLES_DIR, "correlation_matrix.csv"))

print(f"[X] Saved table: {os.path.join(TABLES_DIR, 'linear_regression_coefficients.csv')}")
print(f"[X] Saved table: {os.path.join(TABLES_DIR, 'random_forest_feature_importance.csv')}")
if not corr_matrix.empty:
    print(f"[X] Saved table: {os.path.join(TABLES_DIR, 'correlation_matrix.csv')}")

print_section("20. ANALYSIS COMPLETE")
print("All requested processing, hypothesis testing, regression modeling, evaluation, and separate plot saving are complete.")
print(f"Plots saved in : {PLOTS_DIR}")
print(f"Tables saved in: {TABLES_DIR}")
print("=" * 100)
