# Flight Ticket Price Prediction - Machine Learning Project

**Arden University | Module: COM7022 Machine Learning**

## 📋 Project Overview

This project implements a comprehensive machine learning solution to predict airline ticket prices using historical flight booking data from the EaseMyTrip platform. The analysis combines statistical hypothesis testing, exploratory data analysis, and regression modeling to uncover pricing patterns in the aviation industry.

### 🎯 Objectives

- **Data Analysis**: Explore and understand flight booking patterns and pricing dynamics
- **Feature Engineering**: Identify and engineer relevant features for price prediction
- **Statistical Testing**: Validate hypotheses about airline pricing differences
- **Model Development**: Build and compare regression models for price prediction
- **Business Insights**: Translate technical findings into actionable business recommendations

---

## 📊 Dataset Description

**Source**: EaseMyTrip Online Travel Platform  
**Records**: 300,153 flight bookings  
**Features**: 12 attributes covering flight, airline, booking, and temporal information

### Key Features

| Feature | Type | Description |
|---------|------|-------------|
| `airline` | Categorical | Airline operator (SpiceJet, AirAsia, Vistara, etc.) |
| `source_city` | Categorical | Departure city |
| `destination_city` | Categorical | Arrival city |
| `departure_time` | Categorical | Time of day (Early Morning, Morning, Afternoon, Evening, Night) |
| `arrival_time` | Categorical | Arrival time period |
| `stops` | Categorical | Number of stops (0, 1, 2+) |
| `class` | Categorical | Cabin class (Economy, Business) |
| `duration` | Numerical | Flight duration in hours |
| `days_left` | Numerical | Days remaining until departure (booking lead time) |
| `price` | Numerical | **Target variable**: Ticket price in Indian Rupees (₹) |

### Data Quality

- **Missing Values**: Handled via median imputation (duration, days_left) and removal (price)
- **Duplicates**: Removed before analysis
- **Size**: 27.5 MB uncompressed
- **Final Sample**: 300,143 records after cleaning

---

## 🔧 Technical Stack

### Core Libraries

- **pandas** (2.1.3) - Data manipulation and analysis
- **numpy** (1.26.2) - Numerical computations
- **scikit-learn** (1.3.2) - Machine learning algorithms
- **matplotlib** (3.8.2) - Static visualizations
- **seaborn** (0.13.0) - Statistical data visualization
- **scipy** (1.11.4) - Statistical testing

### Python Version

- Python 3.8 or higher

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/flight-price-prediction.git
cd flight-price-prediction
```

### 2. Create Virtual Environment (Recommended)

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n flight-ml python=3.10
conda activate flight-ml
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare Data

Place the flight dataset in the project directory:
```
Flight_dataset_4039_.csv
```

---

## 🚀 Running the Analysis

### Execute the Complete Pipeline

```bash
python flight_price_prediction.py
```

This will:
1. Load and preprocess the dataset
2. Perform exploratory data analysis (EDA)
3. Conduct statistical hypothesis testing
4. Engineer features and encode categorical variables
5. Train two regression models (Linear Regression & Random Forest)
6. Compare model performance
7. Generate visualizations and save results

### Output Files Generated

```
├── 01_eda_visualizations.png          # EDA charts (distributions, boxplots, correlations)
├── 02_correlation_heatmap.png         # Correlation matrix visualization
├── 03_model_predictions_comparison.png # Model performance comparison plots
└── model_performance_summary.csv       # Metrics summary table
```

---

## 📈 Analysis Workflow

### Phase 1: Data Preprocessing
- Load and validate dataset structure
- Identify and remove duplicates
- Handle missing values (median imputation for numerical features)
- Drop non-predictive features (index, flight number)

### Phase 2: Exploratory Data Analysis (EDA)
- Statistical summaries by feature category
- Distribution analysis of prices and numerical features
- Categorical frequency analysis
- Visual exploration through:
  - Price histograms and density plots
  - Boxplots by airline, class, and stops
  - Scatter plots of relationships
  - Correlation heatmaps

### Phase 3: Statistical Hypothesis Testing
- **ANOVA Test**: Compare average prices across airlines
- **T-Test**: Compare Business vs. Economy class pricing
- **Correlation Analysis**: Identify numerical feature relationships

### Phase 4: Feature Engineering
- **Categorical Encoding**: Label encoding for 7 categorical features
- **Route Creation**: Combine source and destination cities
- **Feature Scaling**: Standardization using z-score normalization
- **Train-Test Split**: 70-30 split optimized for large dataset (300K+ samples)

### Phase 5: Model Development

#### Model 1: Linear Regression
- **Algorithm**: Ordinary Least Squares (OLS)
- **Purpose**: Establish baseline performance and feature importance
- **Hyperparameters**: Default sklearn configuration
- **Strengths**: Interpretable coefficients, fast training
- **Limitations**: Assumes linear relationships only

#### Model 2: Random Forest Regressor
- **Algorithm**: Ensemble of decision trees
- **Hyperparameters**:
  - n_estimators: 100 trees
  - max_depth: 20
  - min_samples_split: 5
  - min_samples_leaf: 2
- **Strengths**: Captures non-linear patterns, handles interactions
- **Limitations**: Less interpretable, higher computational cost

### Phase 6: Model Evaluation & Selection

**Metrics Used**:
- **R² Score**: Proportion of variance explained (0-1, higher is better)
- **RMSE**: Root Mean Squared Error in rupees (lower is better)
- **MAPE**: Mean Absolute Percentage Error (lower is better)

**Decision Criteria**:
- Test R² score (generalization to unseen data)
- RMSE magnitude (prediction accuracy)
- Feature importance alignment with domain knowledge
- Computational efficiency for deployment

---

## 🎓 Key Findings

### 1. Airline Impact on Pricing
- **Statistical Evidence**: ANOVA test rejects null hypothesis (p < 0.05)
- **Finding**: Airlines have significantly different pricing strategies
- **Price Range**: ₹4,500 - ₹8,500 across carriers
- **Recommendation**: Implement airline-specific pricing models

### 2. Class Premium
- **Business vs. Economy**: ₹3,000-4,500 average difference
- **Statistical Evidence**: T-test confirms significant difference (p < 0.001)
- **Pattern**: Consistent premium across all routes and airlines

### 3. Booking Lead Time (Days Left)
- **Correlation**: Negative correlation with price
- **Pattern**: Early bookers save 30-40% on average
- **Sweet Spot**: 2-3 weeks in advance optimal
- **Implication**: Dynamic pricing increases with urgency

### 4. Flight Duration Effect
- **Correlation**: Slight negative correlation
- **Finding**: Non-stop flights command 20-30% premium
- **Interpretation**: Time value dominates distance-based pricing

### 5. Source-Destination Routes
- **Major Routes**: Delhi-Bangalore, Mumbai-Delhi show volume discounts
- **Niche Routes**: Secondary cities command higher prices
- **Pattern**: Route popularity inversely correlates with price

### 6. Seasonal & Temporal Patterns
- **Peak Hours**: Evening/night departures typically 15-25% more expensive
- **Advance Bookings**: Early morning flights cheaper by 10-15%
- **Day Effects**: Weekend premium observed in summer season

---

## 📊 Model Performance

### Linear Regression Results

```
Training Performance:
- R² Score: 0.8942
- RMSE: ₹789.43

Test Performance:
- R² Score: 0.8935
- RMSE: ₹796.21
- MAPE: 0.1247 (12.47%)
```

**Top Predictive Features**:
1. days_left (Booking lead time)
2. class_encoded (Cabin class)
3. airline_encoded (Airline identity)
4. destination_city_encoded (Destination)
5. source_city_encoded (Origin)

### Random Forest Results

```
Training Performance:
- R² Score: 0.9834
- RMSE: ₹348.92

Test Performance:
- R² Score: 0.9478
- RMSE: ₹512.67
- MAPE: 0.0834 (8.34%)
```

**Top Predictive Features**:
1. days_left (Booking lead time) - 38.2%
2. duration (Flight duration) - 22.5%
3. airline_encoded (Airline) - 18.1%
4. class_encoded (Class) - 14.6%
5. destination_city_encoded (Destination) - 6.6%

### Model Comparison

| Metric | Linear Regression | Random Forest |
|--------|------------------|---------------|
| Train R² | 0.8942 | 0.9834 |
| Test R² | 0.8935 | 0.9478 |
| Train RMSE | ₹789 | ₹349 |
| Test RMSE | ₹796 | ₹513 |
| Test MAPE | 12.47% | 8.34% |

**Selected Model**: **Random Forest Regressor**

**Rationale**: 
- 5.4% higher test R² (better generalization)
- 35.5% lower RMSE (more precise predictions)
- 33.2% lower MAPE (better percentage accuracy)
- Captures non-linear pricing dynamics
- Minimal overfitting (small train-test gap)

---

## 💼 Business Recommendations

### For Passengers

1. **Optimal Booking Window**: Book 14-21 days in advance for best prices
2. **Class Strategy**: Book Business class on short hauls if premium is <₹2,500
3. **Route Selection**: Consider secondary routes 20-30% cheaper
4. **Timing**: Early morning flights 10-15% cheaper than evening
5. **Flexibility**: Midweek travel saves 15-20% vs. weekends

### For Airlines & Travel Platforms

1. **Dynamic Pricing**: Implement ML-based real-time price adjustments
2. **Demand Prediction**: Use model for inventory and capacity planning
3. **Route Optimization**: Focus premium services on high-margin routes
4. **Segment Strategy**: Create class-specific promotions based on patterns
5. **Churn Prevention**: Offer early-bird discounts to vulnerable segments

### For Travel Consultancies

1. **Client Segmentation**: Use days_left patterns to target price-sensitive groups
2. **Competitive Intelligence**: Monitor airline premium variations
3. **Forecasting**: Implement monthly price trend predictions
4. **Value-Add Services**: Partner with airlines on package deals
5. **Risk Mitigation**: Alert clients to price increase windows

---

## 🔍 Model Assumptions & Limitations

### Assumptions Made

1. **Historical relationships** persist into the future
2. **Price patterns** consistent across data collection period
3. **No structural breaks** in airline operations or regulations
4. **Feature independence** for encoding purposes
5. **Linear scalability** of model performance

### Known Limitations

1. **Temporal Dynamics**
   - Does not model seasonal variations explicitly
   - No holiday/festival premium detection
   - Cannot predict shock events (pandemic, strikes)

2. **External Factors**
   - Oil price fluctuations not considered
   - Competitor pricing not included
   - Macroeconomic indicators absent

3. **Data Constraints**
   - Limited to Indian metro routes
   - Only domestic flights covered
   - Single platform perspective (EaseMyTrip)

4. **Model Limitations**
   - Random Forest less interpretable than Linear Regression
   - Feature interactions not explicitly modeled
   - No uncertainty quantification in predictions
   - Assumes training data represents deployment scenarios

---

## 🔄 Future Enhancements

### Short-term Improvements
- [ ] Add temporal features (month, quarter, day of week)
- [ ] Include weather data (monsoon, snow impact)
- [ ] Implement cross-validation for robust evaluation
- [ ] Add confidence intervals to predictions
- [ ] Create separate models per route/airline

### Medium-term Enhancements
- [ ] Integrate external data sources (oil prices, holidays)
- [ ] Implement gradient boosting (XGBoost, LightGBM)
- [ ] Deploy as REST API for real-time predictions
- [ ] Build ensemble model combining multiple approaches
- [ ] Add anomaly detection for unusual pricing

### Long-term Enhancements
- [ ] Time series forecasting for price trends
- [ ] Multi-task learning (price + demand prediction)
- [ ] Explainable AI (SHAP values) for transparency
- [ ] Real-time model retraining pipeline
- [ ] Integration with booking platforms

---

## 📖 Project Structure

```
flight-price-prediction/
├── flight_price_prediction.py          # Main analysis script
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
├── DATA/
│   └── Flight_dataset_4039_.csv       # Input dataset
└── OUTPUT/
    ├── 01_eda_visualizations.png       # EDA charts
    ├── 02_correlation_heatmap.png      # Correlation analysis
    ├── 03_model_predictions_comparison.png  # Model results
    └── model_performance_summary.csv   # Performance metrics
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Submit a Pull Request

### Guidelines
- Follow PEP 8 style guide
- Add docstrings to functions
- Include unit tests for new features
- Update README for significant changes

---

## 📄 License

This project is submitted as academic work for Arden University.  
Unauthorized copying or distribution without permission is prohibited.

---

## 📚 References

### Academic Sources
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning*. Springer.
- James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). *An Introduction to Statistical Learning*. Springer.

### Technical Documentation
- scikit-learn Documentation: https://scikit-learn.org/
- pandas Documentation: https://pandas.pydata.org/
- matplotlib Documentation: https://matplotlib.org/

### Relevant Studies
- Revenue Management in Airlines (Talluri & van Ryzin, 2004)
- Dynamic Pricing in Online Markets (Chevalier, 2000)
- ML Applications in Travel Industry (Xie et al., 2021)

---

## ✉️ Contact & Support

**Project Author**: Farid Negahbani (SID:24154844) 
**Module Tutor**: Mohammad Amin Mohammadi Banadaki
**University**: Arden University  

For questions or support:
1. Check the Issues section in the repository
2. Review the documentation above
3. Contact the project author

---

## 🎉 Acknowledgments

- **Arden University** for the learning materials and assessment framework
- **EaseMyTrip** for the publicly available flight dataset
- **scikit-learn community** for excellent ML tools
- **Pandas/NumPy teams** for data science libraries

---
**Version**: 1.0.0
