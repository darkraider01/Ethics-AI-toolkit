"""
Explainability Module for Ethics Toolkit
Provides model explanations using SHAP and other techniques
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    print("Warning: SHAP not available")
    SHAP_AVAILABLE = False

class ModelExplainer:
    """
    Main class for explaining ML model predictions
    """
    
    def __init__(self, model, X_train, model_type='auto'):
        """
        Initialize the explainer
        
        Args:
            model: Trained ML model
            X_train: Training data (for background)
            model_type: 'linear', 'tree', or 'auto'
        """
        self.model = model
        # Ensure X_train is numeric and handle potential non-numeric columns
        self.X_train = X_train.select_dtypes(include=np.number).copy()
        # Drop columns that are all NaN, which might result from conversion
        self.X_train = self.X_train.dropna(axis=1, how='all')
        self.model_type = model_type
        self.explainer = None
        self.feature_names = self.X_train.columns.tolist() if hasattr(self.X_train, 'columns') else None
        
        if SHAP_AVAILABLE:
            self._setup_explainer()
    
    def _setup_explainer(self):
        """Setup appropriate SHAP explainer"""
        if self.model_type == 'auto':
            # Try to auto-detect model type
            model_name = type(self.model).__name__.lower()
            
            if 'linear' in model_name or 'logistic' in model_name:
                self.model_type = 'linear'
            elif 'forest' in model_name or 'tree' in model_name or 'gbm' in model_name:
                self.model_type = 'tree'
            else:
                self.model_type = 'kernel'  # Default fallback
        
        try:
            if self.model_type == 'linear':
                self.explainer = shap.LinearExplainer(self.model, self.X_train)
            elif self.model_type == 'tree':
                self.explainer = shap.TreeExplainer(self.model)
            else:
                # Use KernelExplainer as fallback (slower but works for any model)
                self.explainer = shap.KernelExplainer(
                    self.model.predict_proba, 
                    shap.sample(self.X_train, 100)
                )
            
            print(f"Initialized {self.model_type} explainer successfully")
            
        except Exception as e:
            print(f"Error setting up explainer: {e}")
            self.explainer = None
    
    def explain_prediction(self, X_sample, show_plots=True):
        """
        Explain individual prediction(s)
        
        Args:
            X_sample: Single sample or batch to explain
            show_plots: Whether to display visualizations
        """
        if not SHAP_AVAILABLE or self.explainer is None:
            return self._basic_feature_importance()
        
        try:
            # Get SHAP values
            # Convert X_sample to numpy array for SHAP consistency
            shap_values = self.explainer.shap_values(X_sample.values)
            
            # Handle binary classification case
            if isinstance(shap_values, list) and len(shap_values) == 2:
                shap_values = shap_values[1]  # Take positive class
            
            # Create explanations
            explanations = {
                'shap_values': shap_values,
                'feature_importance': self._get_feature_importance(shap_values, X_sample),
                'prediction': self.model.predict(X_sample),
                'prediction_proba': self.model.predict_proba(X_sample) if hasattr(self.model, 'predict_proba') else None
            }
            
            if show_plots and hasattr(X_sample, 'shape') and X_sample.shape[0] == 1:
                self._plot_individual_explanation(shap_values[0], X_sample.iloc[0])
            
            return explanations
            
        except Exception as e:
            print(f"Error explaining prediction: {e}")
            return self._basic_feature_importance()
    
    def global_explanation(self, X_test, max_samples=100):
        """
        Generate global model explanation
        
        Args:
            X_test: Test data for explanation
            max_samples: Maximum samples to use
        """
        if not SHAP_AVAILABLE or self.explainer is None:
            return self._basic_feature_importance()
        
        # Limit samples for performance
        if len(X_test) > max_samples:
            X_sample = X_test.sample(max_samples, random_state=42)
        else:
            X_sample = X_test
        
        try:
            # Convert X_sample to numpy array for SHAP consistency
            shap_values = self.explainer.shap_values(X_sample.values)
            
            # Handle binary classification
            if isinstance(shap_values, list) and len(shap_values) == 2:
                shap_values = shap_values[1]
            
            # Create summary plots
            plt.figure(figsize=(10, 6))
            shap.summary_plot(shap_values, X_sample, plot_type="bar", show=False)
            plt.title("Global Feature Importance")
            plt.tight_layout()
            plt.show()
            
            plt.figure(figsize=(10, 6))
            shap.summary_plot(shap_values, X_sample, show=False)
            plt.title("Feature Impact Distribution")
            plt.tight_layout()
            plt.show()
            
            return {
                'shap_values': shap_values,
                'feature_importance': np.abs(shap_values).mean(0),
                'feature_names': self.feature_names
            }
            
        except Exception as e:
            print(f"Error in global explanation: {e}")
            return self._basic_feature_importance()
    
    def _plot_individual_explanation(self, shap_values, sample):
        """Plot waterfall chart for individual prediction"""
        try:
            plt.figure(figsize=(10, 4))
            
            if hasattr(shap, 'waterfall_plot'):
                shap.waterfall_plot(
                    self.explainer.expected_value,
                    shap_values,
                    sample,
                    show=False
                )
            else:
                # Fallback to force plot
                shap.force_plot(
                    self.explainer.expected_value,
                    shap_values,
                    sample,
                    matplotlib=True,
                    show=False
                )
            
            plt.title("Prediction Explanation")
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"Error plotting explanation: {e}")
    
    def _get_feature_importance(self, shap_values, X_sample):
        """Extract feature importance from SHAP values"""
        if len(shap_values.shape) == 1:
            importance = np.abs(shap_values)
        else:
            importance = np.abs(shap_values).mean(0)
        
        if self.feature_names:
            return dict(zip(self.feature_names, importance))
        else:
            return {f'feature_{i}': imp for i, imp in enumerate(importance)}
    
    def _basic_feature_importance(self):
        """Fallback feature importance for models without SHAP"""
        try:
            if hasattr(self.model, 'feature_importances_'):
                importance = self.model.feature_importances_
            elif hasattr(self.model, 'coef_'):
                importance = np.abs(self.model.coef_[0])
            else:
                return {"error": "No feature importance available"}
            
            if self.feature_names:
                return dict(zip(self.feature_names, importance))
            else:
                return {f'feature_{i}': imp for i, imp in enumerate(importance)}
                
        except Exception as e:
            return {"error": f"Could not extract feature importance: {e}"}
    
    def generate_text_explanation(self, X_sample, prediction=None):
        """
        Generate human-readable text explanation
        """
        try:
            if prediction is None:
                prediction = self.model.predict(X_sample)[0]
                prob = self.model.predict_proba(X_sample)[0] if hasattr(self.model, 'predict_proba') else None
            
            explanations = self.explain_prediction(X_sample, show_plots=False)
            feature_importance = explanations.get('feature_importance', {})
            
            # Sort features by importance
            sorted_features = sorted(feature_importance.items(), key=lambda x: abs(x[1]), reverse=True)
            
            # Generate text
            outcome = "approved" if prediction == 1 else "rejected"
            confidence = f" (confidence: {prob[1]:.1%})" if prob is not None else ""
            
            text = f"This loan application was {outcome}{confidence}.\n\n"
            text += "Key factors influencing this decision:\n"
            
            for i, (feature, importance) in enumerate(sorted_features[:3]):
                if hasattr(X_sample, 'iloc'):
                    value = X_sample.iloc[0][feature]
                else:
                    value = X_sample[feature]
                
                direction = "increased" if importance > 0 else "decreased"
                text += f"{i+1}. {feature.replace('_', ' ').title()}: {value} ({direction} approval likelihood)\n"
            
            return text
            
        except Exception as e:
            return f"Error generating explanation: {e}"
