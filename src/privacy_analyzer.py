"""
Privacy Risk Analyzer for Ethics Toolkit
Detects potential privacy risks in datasets and model outputs
"""

import pandas as pd
import numpy as np
import re
import hashlib
from typing import List, Dict, Any

class PrivacyAnalyzer:
    """
    Analyzes datasets and model outputs for privacy risks
    """
    
    def __init__(self):
        # Common PII patterns
        self.pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'zipcode': r'\b\d{5}(-\d{4})?\b',
        }
        
        # Common names (simplified list for demo)
        self.common_names = {
            'first_names': ['john', 'mary', 'james', 'patricia', 'robert', 'jennifer', 
                           'michael', 'linda', 'william', 'elizabeth', 'david', 'barbara'],
            'last_names': ['smith', 'johnson', 'williams', 'brown', 'jones', 'garcia',
                          'miller', 'davis', 'rodriguez', 'martinez', 'hernandez']
        }
    
    def analyze_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze dataset for privacy risks
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with privacy risk assessment
        """
        results = {
            'pii_detected': {},
            'quasi_identifiers': [],
            'uniqueness_risk': {},
            'recommendations': []
        }
        
        print("=== PRIVACY RISK ANALYSIS ===")
        
        # 1. PII Detection
        results['pii_detected'] = self._detect_pii(df)
        
        # 2. Quasi-identifier detection
        results['quasi_identifiers'] = self._detect_quasi_identifiers(df)
        
        # 3. Uniqueness analysis
        results['uniqueness_risk'] = self._analyze_uniqueness(df)
        
        # 4. Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _detect_pii(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Detect personally identifiable information"""
        pii_found = {}
        
        print("\n--- PII Detection ---")
        
        for column in df.columns:
            column_pii = []
            
            if df[column].dtype == 'object':  # Text columns
                # Convert to string and combine all values
                text_data = ' '.join(df[column].astype(str).values)
                
                # Check each PII pattern
                for pii_type, pattern in self.pii_patterns.items():
                    matches = re.findall(pattern, text_data, re.IGNORECASE)
                    if matches:
                        column_pii.append(f"{pii_type}: {len(matches)} instances")
                        
                # Check for names
                name_matches = self._detect_names(text_data)
                if name_matches:
                    column_pii.extend(name_matches)
            
            if column_pii:
                pii_found[column] = column_pii
                print(f"⚠️  Column '{column}': {', '.join(column_pii)}")
        
        if not pii_found:
            print("✅ No obvious PII detected")
        
        return pii_found
    
    def _detect_names(self, text: str) -> List[str]:
        """Detect potential names in text"""
        text_lower = text.lower()
        name_matches = []
        
        # Check for first names
        first_name_count = sum(1 for name in self.common_names['first_names'] 
                              if name in text_lower)
        if first_name_count > 0:
            name_matches.append(f"potential_first_names: {first_name_count}")
        
        # Check for last names
        last_name_count = sum(1 for name in self.common_names['last_names'] 
                             if name in text_lower)
        if last_name_count > 0:
            name_matches.append(f"potential_last_names: {last_name_count}")
        
        return name_matches
    
    def _detect_quasi_identifiers(self, df: pd.DataFrame) -> List[str]:
        """Detect quasi-identifiers that could be used for re-identification"""
        quasi_identifiers = []
        
        print("\n--- Quasi-Identifier Detection ---")
        
        # Common quasi-identifiers
        potential_qi = {
            'age': ['age', 'birth_year', 'dob'],
            'location': ['zip', 'zipcode', 'city', 'state', 'address', 'location'],
            'demographic': ['gender', 'race', 'ethnicity', 'marital_status'],
            'professional': ['job_title', 'employer', 'salary', 'income'],
            'temporal': ['date', 'timestamp', 'time']
        }
        
        for qi_type, keywords in potential_qi.items():
            found_columns = []
            for col in df.columns:
                if any(keyword in col.lower() for keyword in keywords):
                    found_columns.append(col)
            
            if found_columns:
                quasi_identifiers.extend(found_columns)
                print(f"⚠️  {qi_type.title()} quasi-identifiers: {found_columns}")
        
        if not quasi_identifiers:
            print("✅ No obvious quasi-identifiers detected")
        
        return list(set(quasi_identifiers))  # Remove duplicates
    
    def _analyze_uniqueness(self, df: pd.DataFrame) -> Dict[str, float]:
        """Analyze uniqueness risk in the dataset"""
        uniqueness_risk = {}
        
        print("\n--- Uniqueness Analysis ---")
        
        # Calculate uniqueness for each column
        for col in df.columns:
            if df[col].dtype in ['object', 'int64', 'float64']:
                unique_ratio = df[col].nunique() / len(df)
                uniqueness_risk[col] = unique_ratio
                
                if unique_ratio > 0.9:
                    print(f"⚠️  High uniqueness risk in '{col}': {unique_ratio:.2%}")
                elif unique_ratio > 0.5:
                    print(f"⚠️  Medium uniqueness risk in '{col}': {unique_ratio:.2%}")
        
        # Combination uniqueness (simplified)
        if len(df) > 0:
            # Check uniqueness of combinations
            important_cols = [col for col in df.columns 
                            if df[col].dtype in ['object', 'int64', 'float64']][:3]
            
            if len(important_cols) >= 2:
                combo_df = df[important_cols].drop_duplicates()
                combo_uniqueness = len(combo_df) / len(df)
                uniqueness_risk['combination_2-3_cols'] = combo_uniqueness
                
                if combo_uniqueness > 0.8:
                    print(f"⚠️  High re-identification risk from column combinations: {combo_uniqueness:.2%}")
        
        return uniqueness_risk
    
    def _generate_recommendations(self, analysis_results: Dict) -> List[str]:
        """Generate privacy protection recommendations"""
        recommendations = []
        
        print("\n--- Privacy Recommendations ---")
        
        # PII recommendations
        if analysis_results['pii_detected']:
            recommendations.append("🔒 Remove or encrypt detected PII before model training")
            recommendations.append("🔒 Consider data anonymization techniques")
        
        # Quasi-identifier recommendations
        if analysis_results['quasi_identifiers']:
            recommendations.append("🔒 Apply k-anonymity or l-diversity to quasi-identifiers")
            recommendations.append("🔒 Consider generalization/suppression of sensitive attributes")
        
        # Uniqueness recommendations
        high_unique_cols = [col for col, ratio in analysis_results['uniqueness_risk'].items() 
                           if ratio > 0.9]
        if high_unique_cols:
            recommendations.append("🔒 Reduce granularity of highly unique columns")
            recommendations.append("🔒 Consider data aggregation or binning")
        
        # General recommendations
        recommendations.extend([
            "🔒 Implement differential privacy for model training",
            "🔒 Use secure multi-party computation for sensitive data",
            "🔒 Regular privacy audits and monitoring"
        ])
        
        for rec in recommendations:
            print(rec)
        
        return recommendations
    
    def analyze_model_outputs(self, outputs: List[str], 
                            training_data: pd.DataFrame = None) -> Dict[str, Any]:
        """
        Analyze model outputs for privacy leaks
        
        Args:
            outputs: List of model outputs to analyze
            training_data: Original training data for comparison
            
        Returns:
            Privacy risk assessment of outputs
        """
        results = {
            'pii_in_outputs': {},
            'data_leakage_risk': 0,
            'recommendations': []
        }
        
        print("\n=== MODEL OUTPUT PRIVACY ANALYSIS ===")
        
        # Combine all outputs
        combined_output = ' '.join(outputs)
        
        # Check for PII in outputs
        for pii_type, pattern in self.pii_patterns.items():
            matches = re.findall(pattern, combined_output, re.IGNORECASE)
            if matches:
                results['pii_in_outputs'][pii_type] = len(matches)
                print(f"⚠️  {pii_type} found in outputs: {len(matches)} instances")
        
        # Check for potential training data leakage
        if training_data is not None:
            leakage_score = self._check_data_leakage(outputs, training_data)
            results['data_leakage_risk'] = leakage_score
            
            if leakage_score > 0.1:
                print(f"⚠️  Potential training data leakage detected: {leakage_score:.2%}")
        
        return results
    
    def _check_data_leakage(self, outputs: List[str], 
                           training_data: pd.DataFrame) -> float:
        """Simple check for training data leakage in outputs"""
        # Convert training data to text
        training_text = []
        for col in training_data.columns:
            if training_data[col].dtype == 'object':
                training_text.extend(training_data[col].astype(str).values)
        
        training_text_set = set(training_text)
        
        # Check for exact matches
        matches = 0
        total_tokens = 0
        
        for output in outputs:
            tokens = output.split()
            total_tokens += len(tokens)
            
            for token in tokens:
                if token in training_text_set:
                    matches += 1
        
        return matches / total_tokens if total_tokens > 0 else 0
    
    def generate_privacy_report(self, df: pd.DataFrame, 
                              model_outputs: List[str] = None) -> str:
        """Generate comprehensive privacy report"""
        report = "# Privacy Risk Assessment Report\n\n"
        
        # Dataset analysis
        dataset_results = self.analyze_dataset(df)
        
        report += "## Dataset Privacy Analysis\n\n"
        
        if dataset_results['pii_detected']:
            report += "### ⚠️ PII Detected:\n"
            for col, pii_types in dataset_results['pii_detected'].items():
                report += f"- **{col}**: {', '.join(pii_types)}\n"
        else:
            report += "### ✅ No PII Detected\n"
        
        if dataset_results['quasi_identifiers']:
            report += "\n### ⚠️ Quasi-Identifiers Found:\n"
            for qi in dataset_results['quasi_identifiers']:
                report += f"- {qi}\n"
        
        report += "\n### Recommendations:\n"
        for rec in dataset_results['recommendations']:
            report += f"- {rec}\n"
        
        # Model outputs analysis
        if model_outputs:
            output_results = self.analyze_model_outputs(model_outputs, df)
            report += "\n## Model Output Privacy Analysis\n\n"
            
            if output_results['pii_in_outputs']:
                report += "### ⚠️ PII in Model Outputs:\n"
                for pii_type, count in output_results['pii_in_outputs'].items():
                    report += f"- {pii_type}: {count} instances\n"
            else:
                report += "### ✅ No PII Detected in Outputs\n"
        
        return report
