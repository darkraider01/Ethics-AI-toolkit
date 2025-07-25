"""
Unified Ethics Pipeline
Integrates all ethics modules into a single analysis workflow
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import warnings
warnings.filterwarnings('ignore')

# Import all modules
from bias_detector import BiasDetector
from explainability import ModelExplainer
from privacy_analyzer import PrivacyAnalyzer
from hallucination_detector import HallucinationDetector

class EthicsToolkitPipeline:
    """
    Main pipeline that orchestrates all ethics analyses
    """
    
    def __init__(self, enable_models=True):
        """
        Initialize the ethics pipeline
        
        Args:
            enable_models: Whether to enable AI models (slower but more features)
        """
        self.enable_models = enable_models
        self.results = {}
        
        # Initialize components
        self.bias_detector = None
        self.explainer = None
        self.privacy_analyzer = PrivacyAnalyzer()
        self.hallucination_detector = HallucinationDetector(use_models=enable_models)
        
        print("Ethics Toolkit Pipeline initialized!")
    
    def run_full_audit(self, dataset: pd.DataFrame,
                       X_processed: pd.DataFrame,
                       y_processed: pd.Series,
                       label_column: str,
                       protected_attributes: List[str],
                       model: Any,
                       test_prompts: List[str] = None,
                       reference_facts: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Run complete ethics audit
        
        Args:
            dataset: Dataset to analyze
            label_column: Target variable column name
            protected_attributes: List of protected attribute columns
            model: Trained ML model
            test_prompts: Optional prompts for hallucination testing
            reference_facts: Optional reference facts for hallucination detection
            
        Returns:
            Complete audit results
        """
        print("🔍 Starting comprehensive ethics audit...")
        
        audit_results = {
            'dataset_info': {
                'shape': dataset.shape,
                'columns': list(dataset.columns),
                'label_column': label_column,
                'protected_attributes': protected_attributes
            },
            'bias_analysis': {},
            'explainability_analysis': {},
            'privacy_analysis': {},
            'hallucination_analysis': {},
            'summary': {}
        }
        
        # 1. Bias Detection
        print("\n1️⃣ Running bias detection...")
        try:
            self.bias_detector = BiasDetector(
                dataset, label_column, protected_attributes, X_processed, y_processed
            )
            audit_results['bias_analysis'] = self.bias_detector.generate_report()
            print("✅ Bias analysis complete")
        except Exception as e:
            print(f"❌ Bias analysis failed: {e}")
            audit_results['bias_analysis'] = {'error': str(e)}
        
        # 2. Explainability
        print("\n2️⃣ Running explainability analysis...")
        try:
            self.explainer = ModelExplainer(model, X_processed)
            
            # Global explanation
            global_explanation = self.explainer.global_explanation(
                X_processed.sample(min(100, len(X_processed)), random_state=42)
            )
            
            # Local explanation (sample)
            sample_row = X_processed.sample(1, random_state=42)
            local_explanation = self.explainer.generate_text_explanation(sample_row)
            
            audit_results['explainability_analysis'] = {
                'global': global_explanation,
                'local_example': local_explanation,
                'feature_columns': X_processed.columns.tolist()
            }
            print("✅ Explainability analysis complete")
        except Exception as e:
            print(f"❌ Explainability analysis failed: {e}")
            audit_results['explainability_analysis'] = {'error': str(e)}
        
        # 3. Privacy Analysis
        print("\n3️⃣ Running privacy analysis...")
        try:
            audit_results['privacy_analysis'] = self.privacy_analyzer.analyze_dataset(dataset)
            print("✅ Privacy analysis complete")
        except Exception as e:
            print(f"❌ Privacy analysis failed: {e}")
            audit_results['privacy_analysis'] = {'error': str(e)}
        
        # 4. Hallucination Detection
        print("\n4️⃣ Running hallucination detection...")
        try:
            if test_prompts:
                hallucination_results = self.hallucination_detector.comprehensive_analysis(
                    test_prompts, reference_facts
                )
                audit_results['hallucination_analysis'] = hallucination_results
                print("✅ Hallucination analysis complete")
            else:
                print("⚠️ No test prompts provided, skipping hallucination detection")
                audit_results['hallucination_analysis'] = {'skipped': 'No test prompts provided'}
        except Exception as e:
            print(f"❌ Hallucination analysis failed: {e}")
            audit_results['hallucination_analysis'] = {'error': str(e)}
        
        # 5. Generate Summary
        print("\n5️⃣ Generating summary...")
        audit_results['summary'] = self._generate_summary(audit_results)
        
        print("\n🎉 Ethics audit complete!")
        self.results = audit_results
        return audit_results
    
    def _generate_summary(self, audit_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall summary of audit results"""
        summary = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'overall_status': 'PASSED',
            'issues_found': [],
            'recommendations': [],
            'risk_level': 'LOW'
        }
        
        # Check bias results
        bias_results = audit_results.get('bias_analysis', {})
        if 'error' not in bias_results:
            # Look for bias indicators (simplified)
            if any('WARNING' in str(v) for v in bias_results.values()):
                summary['issues_found'].append('Potential bias detected')
                summary['overall_status'] = 'FAILED'
                summary['risk_level'] = 'HIGH'
        
        # Check privacy results  
        privacy_results = audit_results.get('privacy_analysis', {})
        if privacy_results.get('pii_detected'):
            summary['issues_found'].append('PII detected in dataset')
            summary['risk_level'] = 'MEDIUM'
        
        # Check hallucination results
        hallucination_results = audit_results.get('hallucination_analysis', {})
        if hallucination_results.get('summary', {}).get('hallucination_rate', 0) > 0.2:
            summary['issues_found'].append('High hallucination rate detected')
            summary['overall_status'] = 'FAILED'
        
        # Generate recommendations
        if summary['issues_found']:
            summary['recommendations'] = [
                "Review and address identified bias patterns",
                "Implement data anonymization for PII",
                "Add fact-checking mechanisms for model outputs",
                "Consider retraining models with bias mitigation techniques"
            ]
        else:
            summary['recommendations'] = [
                "Continue monitoring for emerging ethical issues",
                "Regular re-auditing recommended",
                "Consider implementing continuous monitoring"
            ]
        
        return summary
    
    def generate_compliance_score(self) -> float:
        """
        Generate overall compliance score (0-100)
        """
        if not self.results:
            return 0.0
        
        score = 100.0
        
        # Deduct points for issues
        issues = self.results.get('summary', {}).get('issues_found', [])
        
        # Each issue type deducts points
        for issue in issues:
            if 'bias' in issue.lower():
                score -= 40  # Bias is critical
            elif 'pii' in issue.lower():
                score -= 20  # Privacy is important
            elif 'hallucination' in issue.lower():
                score -= 30  # Accuracy is crucial
        
        return max(0.0, score)
