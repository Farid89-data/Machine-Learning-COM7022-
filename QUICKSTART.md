# Quick Start Guide

## 🚀 Get Up and Running in 5 Minutes

### Step 1: Prerequisites Check
```bash
python --version  # Should be 3.8+
pip --version
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Prepare Your Data
- Download `Flight_dataset_4039_.csv` from the provided location
- Place it in the project root directory (same folder as `flight_price_prediction.py`)

### Step 4: Run the Analysis
```bash
python flight_price_prediction.py
```

Expected runtime: 5-10 minutes depending on your system

### Step 5: Check Results
After execution completes, you'll find:
- `01_eda_visualizations.png` - Data exploration charts
- `02_correlation_heatmap.png` - Feature correlations  
- `03_model_predictions_comparison.png` - Model performance comparison
- `model_performance_summary.csv` - Detailed metrics

---

## 📊 What the Script Does

### Automatically Executes:

1. **Data Loading & Cleaning** (2 min)
   - Loads 300K+ flight records
   - Removes duplicates and handles missing values
   - Validates data integrity

2. **Exploratory Analysis** (1 min)
   - Statistical summaries
   - Feature distributions
   - Categorical breakdowns

3. **Visualizations** (1 min)
   - 9 EDA charts
   - Correlation heatmap
   - Distribution plots

4. **Hypothesis Testing** (30 sec)
   - ANOVA test for airline pricing
   - T-test for class differences
   - Correlation analysis

5. **Feature Engineering** (1 min)
   - Encoding categorical variables
   - Feature scaling
   - Route feature creation

6. **Model Training** (3-5 min)
   - Linear Regression model
   - Random Forest model (100 trees)
   - 70-30 train-test split

7. **Evaluation & Reporting** (1 min)
   - Performance metrics
   - Feature importance
   - Model comparison

---

## 💡 Key Outputs Explained

### 01_eda_visualizations.png
9-panel visualization showing:
- Price distribution (histogram)
- Prices by airline, class, and stops (boxplots)
- Duration vs. price relationship
- Booking lead time vs. price
- Average prices by category

**Use for**: Understanding data patterns and outliers

### 02_correlation_heatmap.png
Correlation matrix for numerical features (duration, days_left, price)

**Use for**: Identifying which features most closely relate to price

### 03_model_predictions_comparison.png
6-panel comparison showing:
- Linear Regression: Actual vs. Predicted
- Linear Regression: Residuals
- Linear Regression: Top features
- Random Forest: Actual vs. Predicted
- Random Forest: Residuals
- Random Forest: Top features

**Use for**: Evaluating model accuracy and identifying which features drive predictions

### model_performance_summary.csv
Performance metrics table:
- R² scores (training and testing)
- RMSE values
- MAPE percentage errors

**Use for**: Detailed model comparison and reporting

---

## 🔧 Customization Options

### Modify Train-Test Split
In the script, find this line:
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42  # Change 0.30 to 0.20 for 80-20 split
)
```

### Adjust Random Forest Parameters
```python
rf_model = RandomForestRegressor(
    n_estimators=100,      # More trees = better but slower
    max_depth=20,          # Limit tree depth to prevent overfitting
    random_state=42        # Fixed for reproducibility
)
```

### Change Output Image Resolution
```python
plt.savefig('filename.png', dpi=300, bbox_inches='tight')  # Change dpi for resolution
```

---

## ❓ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"
**Solution**: 
```bash
pip install -r requirements.txt
# OR
pip install pandas numpy scikit-learn matplotlib seaborn scipy
```

### Issue: "FileNotFoundError: Flight_dataset_4039_.csv"
**Solution**: 
- Check dataset is in the same directory as the script
- Verify filename matches exactly (including capitalization)

### Issue: Script runs slowly
**Solution**:
- This is normal for 300K records
- On standard laptops: 5-10 minutes
- On high-end machines: 2-3 minutes
- Consider reducing dataset size for testing:
  ```python
  df = pd.read_csv('Flight_dataset_4039_.csv').sample(frac=0.1)  # Use 10% sample
  ```

### Issue: Memory error
**Solution**:
- Reduce dataset size (see above)
- Close other applications
- Ensure at least 4GB RAM available

---

## 📈 Understanding the Results

### R² Score
- **Range**: 0 to 1
- **Meaning**: Proportion of price variance explained
- **Example**: R² = 0.95 means model explains 95% of price variation

### RMSE (Root Mean Squared Error)
- **Unit**: Same as target (₹)
- **Meaning**: Average prediction error in rupees
- **Example**: RMSE = ₹500 means predictions off by ₹500 on average

### MAPE (Mean Absolute Percentage Error)
- **Unit**: Percentage (%)
- **Meaning**: Average percentage error
- **Example**: MAPE = 8.34% means predictions off by ~8% on average

### Better or Worse?
- **Lower** RMSE = Better
- **Lower** MAPE = Better
- **Higher** R² = Better

---

## 🎯 What's Next?

After running the initial analysis:

1. **Review Visualizations**
   - Are the patterns as expected?
   - Any surprising outliers?

2. **Check Model Performance**
   - Which model performs better?
   - Is accuracy sufficient for use?

3. **Examine Feature Importance**
   - Which factors most affect price?
   - How do these align with business knowledge?

4. **Generate Report**
   - Combine findings with visualizations
   - Write management summary
   - Make recommendations

5. **Deploy Model** (Optional)
   - Save trained model
   - Create prediction API
   - Integrate with booking system

---

## 📞 Need Help?

1. **Check documentation** - See README.md for detailed explanations
2. **Review comments** - Script has extensive inline comments
3. **Check inputs** - Verify dataset format matches expectations
4. **Verify Python version** - Ensure using Python 3.8+

---

**Ready? Run: `python flight_price_prediction.py`** ✈️
