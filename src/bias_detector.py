"""
Bias Detection Module for Ethics Toolkit
"""

import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

try:
    from fairlearn.metrics import (
        MetricFrame, 
        selection_rate,
        demographic_parity_difference,
        equalized_odds_difference
    )
    FAIRLEARN_AVAILABLE = True
except ImportError:
    print("Warning: Fairlearn not available")
    FAIRLEARN_AVAILABLE = False

class BiasDetector:
    def __init__(self, dataset, label_column, protected_attributes, X_processed=None, y_processed=None):
        self.dataset = dataset.copy() # Original dataset for basic analysis
        self.label_column = label_column
        self.protected_attributes = protected_attributes
        self.X_processed = X_processed
        self.y_processed = y_processed
        self.results = {}
    
    def basic_bias_analysis(self):
        """Perform basic bias analysis"""
        print("=== BASIC BIAS ANALYSIS ===")
        
        for attr in self.protected_attributes:
            print(f"\n--- Analysis for {attr} ---")

            temp_dataset = self.dataset.copy()

            # Ensure the label column is numeric for aggregation
            if temp_dataset[self.label_column].dtype == 'object':
                unique_labels = temp_dataset[self.label_column].unique()
                if len(unique_labels) == 2:
                    # Map to 0 and 1, assuming binary classification
                    mapping = {unique_labels[0]: 0, unique_labels[1]: 1}
                    temp_dataset[self.label_column] = temp_dataset[self.label_column].map(mapping)
                else:
                    print(f"Warning: Label column '{self.label_column}' has more than two unique string values or is non-numeric. Skipping basic bias analysis for this attribute.")
                    continue
            
            # Conditionally convert protected attribute to numeric if it's typically numeric
            if attr.lower() in ['age', 'income']: # Add other numeric-like attributes here if any
                if temp_dataset[attr].dtype == 'object':
                    try:
                        temp_dataset[attr] = pd.to_numeric(temp_dataset[attr], errors='coerce')
                        temp_dataset = temp_dataset.dropna(subset=[attr]) # Drop NaNs only for these converted columns
                        print(f"Note: Converted '{attr}' to numeric for basic bias analysis.")
                    except Exception as e:
                        print(f"Warning: Could not convert '{attr}' to numeric: {e}. Skipping basic bias analysis for this attribute.")
                        continue
            
            # Calculate approval rates by group
            group_stats = temp_dataset.groupby(attr)[self.label_column].agg([
                'count', 'sum', 'mean'
            ]).round(4)
            
            group_stats.columns = ['total_cases', 'approvals', 'approval_rate']
            print(group_stats)
            
            # Calculate disparate impact ratio
            max_rate = group_stats['approval_rate'].max()
            min_rate = group_stats['approval_rate'].min()
            
            if max_rate > 0:
                disparate_impact_ratio = min_rate / max_rate
                print(f"\nDisparate Impact Ratio: {disparate_impact_ratio:.3f}")
                
                if disparate_impact_ratio < 0.8:
                    print("⚠️  WARNING: Potential bias detected! (Ratio < 0.8)")
                else:
                    print("✅ No significant bias detected (Ratio >= 0.8)")
    
    def fairlearn_analysis(self, model=None):
        """Use Fairlearn for bias analysis"""
        if not FAIRLEARN_AVAILABLE:
            print("Fairlearn not available. Skipping advanced analysis.")
            return
            
        print("\n=== FAIRLEARN BIAS ANALYSIS ===")
        
        # Prepare data
        if self.X_processed is not None and self.y_processed is not None:
            X = self.X_processed
            y = self.y_processed
            self.dataset_for_analysis = self.dataset # Keep original for sensitive_features
        else:
            # Fallback if pre-processed data not provided
            feature_columns = [col for col in self.dataset.columns
                               if col not in [self.label_column] + self.protected_attributes]
            X = self.dataset[feature_columns]
            y = self.dataset[self.label_column]
            self.dataset_for_analysis = self.dataset # Keep original for sensitive_features
            
        # Train model if none provided (or use the one from pipeline)
        if model is None:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=42
            )
            model = LogisticRegression(random_state=42, max_iter=1000)
            model.fit(X_train, y_train)
            X, y = X_test, y_test
            self.dataset_for_analysis = self.dataset.loc[X.index] # Re-align dataset_for_analysis
        
        # Get predictions
        y_pred = model.predict(X)
        
        # Analyze each protected attribute
        for attr in self.protected_attributes:
            # Need to get sensitive features from the original dataset, not X (which is encoded)
            sensitive_features = self.dataset_for_analysis[attr]
            
            print(f"\n--- Fairlearn Analysis for {attr} ---")
            
            # Create MetricFrame
            mf = MetricFrame(
                metrics={'selection_rate': selection_rate},
                y_true=y,
                y_pred=y_pred,
                sensitive_features=sensitive_features
            )
            
            print("Selection rates by group:")
            print(mf.by_group.round(4))
            
            # Calculate fairness metrics
            dem_parity_diff = demographic_parity_difference(
                y, y_pred, sensitive_features=sensitive_features
            )
            
            print(f"Demographic Parity Difference: {dem_parity_diff:.4f}")
            
            self.results[f'{attr}_fairlearn_metrics'] = mf.by_group
            self.results[f'{attr}_demographic_parity_diff'] = dem_parity_diff
    
    def generate_report(self):
        """Generate comprehensive bias report"""
        print("\n" + "="*50)
        print("COMPREHENSIVE BIAS REPORT")
        print("="*50)
        
        self.basic_bias_analysis()
        self.fairlearn_analysis()
        
        return self.results
