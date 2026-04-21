"""
Configuration File for Flight Price Prediction Model
This file stores all hyperparameters and configuration settings
for easy modification without editing the main script.
"""

# ============================================================================
# DATA CONFIGURATION
# ============================================================================
DATA_CONFIG = {
    'input_file': 'Flight_dataset_4039_.csv',
    'output_dir': './',
    'random_state': 42,
    'test_size': 0.30,  # 70-30 train-test split for large dataset
    'sample_size': None,  # None = use full dataset, 0.1 = use 10% sample
}

# ============================================================================
# FEATURE ENGINEERING CONFIGURATION
# ============================================================================
FEATURE_CONFIG = {
    'categorical_features': [
        'airline',
        'source_city',
        'departure_time',
        'stops',
        'arrival_time',
        'destination_city',
        'class'
    ],
    'numerical_features': [
        'duration',
        'days_left',
        'price'
    ],
    'features_to_drop': [
        'Unnamed: 0',
        'flight'
    ],
    'target_variable': 'price',
    'scaling_method': 'standard',  # 'standard' or 'minmax'
}

# ============================================================================
# PREPROCESSING CONFIGURATION
# ============================================================================
PREPROCESSING_CONFIG = {
    'missing_value_strategy': 'median',  # 'mean', 'median', 'drop'
    'remove_duplicates': True,
    'remove_outliers': False,  # Set True to use IQR method
    'outlier_iqr_multiplier': 1.5,
    'handle_missing_price': 'drop',  # Drop rows with missing target
    'handle_missing_duration': 'median',
    'handle_missing_days_left': 'median',
}

# ============================================================================
# LINEAR REGRESSION CONFIGURATION
# ============================================================================
LINEAR_REGRESSION_CONFIG = {
    'algorithm': 'LinearRegression',
    'fit_intercept': True,
    'normalize': False,
    'copy_X': True,
    'n_jobs': None,
}

# ============================================================================
# RANDOM FOREST CONFIGURATION
# ============================================================================
RANDOM_FOREST_CONFIG = {
    'algorithm': 'RandomForestRegressor',
    'n_estimators': 100,  # Number of trees
    'max_depth': 20,  # Maximum tree depth
    'min_samples_split': 5,  # Minimum samples to split node
    'min_samples_leaf': 2,  # Minimum samples at leaf
    'min_weight_fraction_leaf': 0.0,
    'max_features': 'sqrt',  # Number of features to consider
    'max_samples': None,  # Number of samples to draw
    'bootstrap': True,  # Use bootstrap sampling
    'oob_score': False,  # Out-of-bag score
    'n_jobs': -1,  # Use all processors
    'random_state': 42,
    'verbose': 0,
    'warm_start': False,
}

# ============================================================================
# VISUALIZATION CONFIGURATION
# ============================================================================
VISUALIZATION_CONFIG = {
    'dpi': 300,  # Resolution (higher = better quality, larger file)
    'figsize': (20, 16),  # Default figure size (width, height)
    'style': 'seaborn-v0_8-darkgrid',  # Plot style
    'color_palette': 'husl',  # Color palette
    'plot_alpha': 0.7,  # Transparency level
    'scatter_size': 10,  # Size of scatter plot points
    'scatter_alpha': 0.3,  # Transparency of scatter plots
    'save_format': 'png',  # 'png', 'pdf', 'jpg'
    'bbox_inches': 'tight',  # Crop whitespace
}

# ============================================================================
# EVALUATION METRICS CONFIGURATION
# ============================================================================
METRICS_CONFIG = {
    'metrics': [
        'r2_score',
        'mean_squared_error',
        'mean_absolute_error',
        'mean_absolute_percentage_error'
    ],
    'cross_validation': False,  # Use cross-validation
    'cv_folds': 5,  # Number of CV folds
}

# ============================================================================
# HYPOTHESIS TESTING CONFIGURATION
# ============================================================================
HYPOTHESIS_TEST_CONFIG = {
    'alpha': 0.05,  # Significance level
    'test_airlines': True,  # ANOVA test for airline effect
    'test_class': True,  # T-test for class effect
    'test_correlation': True,  # Correlation analysis
    'anova_method': 'f_oneway',  # ANOVA implementation
    'ttest_equal_var': True,  # T-test variance assumption
}

# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================
OUTPUT_CONFIG = {
    'save_visualizations': True,
    'save_metrics': True,
    'save_model': False,  # Set True to pickle trained models
    'output_files': {
        'eda_viz': '01_eda_visualizations.png',
        'correlation': '02_correlation_heatmap.png',
        'model_comparison': '03_model_predictions_comparison.png',
        'metrics_summary': 'model_performance_summary.csv',
        'lr_model': 'linear_regression_model.pkl',
        'rf_model': 'random_forest_model.pkl',
        'scaler': 'scaler.pkl',
    },
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOGGING_CONFIG = {
    'verbose': True,  # Print detailed output
    'print_interval': 1000,  # Print every N records during processing
    'log_to_file': False,  # Save logs to file
    'log_file': 'analysis.log',
}

# ============================================================================
# PERFORMANCE TUNING CONFIGURATION
# ============================================================================
PERFORMANCE_CONFIG = {
    'use_gpu': False,  # Use GPU if available
    'n_jobs': -1,  # Number of parallel jobs (-1 = all cores)
    'cache_training': True,  # Cache training data
    'batch_size': 1000,  # Processing batch size
}
