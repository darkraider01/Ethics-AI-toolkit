import os
import sys
import json
from datetime import datetime

# Fix import path BEFORE any other imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Now these imports should work
from pipeline import EthicsToolkitPipeline
from styles import (
    apply_custom_styles,
    create_status_card,
    create_metric_card,
)

# ------------------------------------------------------------------ #
# Streamlit page configuration & global styles
# ------------------------------------------------------------------ #
st.set_page_config(
    page_title="Ethics Toolkit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_custom_styles()

# ------------------------------------------------------------------ #
# Header
# ------------------------------------------------------------------ #
st.markdown(
    """
<div class="main-header">
    <h1>🛡️ Ethics Toolkit</h1>
    <p>Comprehensive AI Ethics Auditing Platform</p>
</div>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# Sidebar – data & settings
# ------------------------------------------------------------------ #
with st.sidebar:
    st.markdown("## 📁 Upload Dataset")
    csv_file = st.file_uploader("Choose CSV", type="csv")

    if csv_file:
        data = pd.read_csv(csv_file)
        st.success(f"Loaded **{data.shape[0]}** rows × **{data.shape[1]}** columns")

        st.markdown("## 🔧 Configure Columns")
        label_col = st.selectbox("Label column", data.columns)
        protected_cols = st.multiselect(
            "Protected attributes", [c for c in data.columns if c != label_col]
        )

        st.markdown("## 🧠 Hallucination Prompts (optional)")
        enable_hall = st.checkbox("Enable", value=True)
        prompt_input = st.text_area(
            "Prompts (one per line)",
            "What factors determine approval?\nHow does income affect decisions?",
        )
        prompts = [p.strip() for p in prompt_input.split("\n") if p.strip()] if enable_hall else []

        run_btn = st.button("🚀 Run Ethics Audit", type="primary")
    else:
        data, label_col, protected_cols, prompts, run_btn = None, None, None, None, False

# ------------------------------------------------------------------ #
# Run audit
# ------------------------------------------------------------------ #
if run_btn and data is not None:
    with st.spinner("Running comprehensive ethics audit..."):
        try:
            # Basic train-and-audit loop
            feature_cols = [c for c in data.columns if c not in [label_col] + protected_cols]
            if len(feature_cols) == 0:
                st.error("❌ No feature columns available")
                st.stop()
                
            X = data[feature_cols]
            y = data[label_col]
            
            # Ensure label column is numeric
            if y.dtype == 'object':
                unique_labels = y.unique()
                if len(unique_labels) == 2:
                    # Map to 0 and 1
                    mapping = {unique_labels[0]: 0, unique_labels[1]: 1}
                    y = y.map(mapping)
                else:
                    st.error("❌ Label column has more than two unique string values. Cannot perform binary classification.")
                    st.stop()

            # Convert categorical features to numerical using one-hot encoding
            X = pd.get_dummies(X, drop_first=True)

            model = LogisticRegression(max_iter=1000, random_state=42)
            model.fit(X, y)

            pipeline = EthicsToolkitPipeline(enable_models=True)
            results = pipeline.run_full_audit(
                dataset=data,
                X_processed=X,
                y_processed=y,
                label_column=label_col,
                protected_attributes=protected_cols,
                model=model,
                test_prompts=prompts,
                reference_facts={},
            )
            st.session_state["audit"] = results
            st.session_state["compliance"] = pipeline.generate_compliance_score()
        except Exception as e:
            st.error(f"❌ Audit failed: {str(e)}")
            st.stop()

# ------------------------------------------------------------------ #
# Display results
# ------------------------------------------------------------------ #
if "audit" in st.session_state:
    audit = st.session_state["audit"]
    score = st.session_state["compliance"]
    summ = audit["summary"]

    st.markdown("## 📊 Audit Overview")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        status_class = "status-good" if summ["overall_status"] == "PASSED" else "status-error"
        status_text = "✅ PASSED" if summ["overall_status"] == "PASSED" else "❌ FAILED"
        st.markdown(
            create_status_card(status_text, "Overall Status", status_class),
            unsafe_allow_html=True,
        )
    
    with c2:
        risk_colors = {"LOW": "status-good", "MEDIUM": "status-warning", "HIGH": "status-error"}
        risk_class = risk_colors.get(summ["risk_level"], "status-neutral")
        st.markdown(
            create_status_card(summ["risk_level"], "Risk Level", risk_class),
            unsafe_allow_html=True,
        )
    
    with c3:
        st.markdown(
            create_metric_card(len(summ["issues_found"]), "Issues Found", "⚠️"),
            unsafe_allow_html=True,
        )
    
    with c4:
        st.markdown(
            create_metric_card(f"{score:.0f}%", "Compliance Score", "📈"),
            unsafe_allow_html=True,
        )

    # Tabs for detailed results
    tab_sum, tab_bias, tab_expl, tab_priv, tab_hall = st.tabs(
        ["📊 Summary", "⚖️ Bias", "🔍 Explainability", "🔒 Privacy", "🧠 Hallucination"]
    )

    with tab_sum:
        st.subheader("🎯 Key Findings")
        if summ["issues_found"]:
            for issue in summ["issues_found"]:
                st.warning(f"⚠️ {issue}")
        else:
            st.success("✅ No critical issues detected!")

        st.subheader("💡 Recommendations")
        for rec in summ["recommendations"]:
            st.info(f"• {rec}")

    with tab_bias:
        st.subheader("⚖️ Bias & Fairness Analysis")
        bias = audit["bias_analysis"]
        if "error" in bias:
            st.error(f"❌ {bias['error']}")
        else:
            for k, v in bias.items():
                if isinstance(v, pd.DataFrame):
                    st.write(f"**{k}**")
                    st.dataframe(v, use_container_width=True)

    with tab_expl:
        st.subheader("🔍 Model Explainability")
        expl = audit["explainability_analysis"]
        if "error" in expl:
            st.error(f"❌ {expl['error']}")
        else:
            st.write("**Sample Explanation:**")
            st.code(expl.get("local_example", "No explanation available"))

    with tab_priv:
        st.subheader("🔒 Privacy Analysis")
        priv = audit["privacy_analysis"]
        if priv.get("pii_detected"):
            st.warning("⚠️ PII detected:")
            for col, details in priv["pii_detected"].items():
                st.write(f"- **{col}**: {', '.join(details)}")
        else:
            st.success("✅ No PII detected")

    with tab_hall:
        st.subheader("🧠 Hallucination Detection")
        hall = audit["hallucination_analysis"]
        if hall.get("skipped"):
            st.info("ℹ️ Hallucination test skipped")
        elif hall.get("error"):
            st.error(f"❌ {hall['error']}")
        else:
            hs = hall.get("summary", {})
            if hs:
                st.write(f"**Hallucination Rate:** {hs.get('hallucination_rate', 0):.1%}")
                st.write(f"**Overall Quality:** {hs.get('overall_quality', 'Unknown')}")
                if 'average_consistency' in hs:
                    st.write(f"**Average Consistency:** {hs['average_consistency']:.3f}")
                    st.write(f"**Is Inconsistent:** {hs['is_inconsistent']}")
            
            if hall.get('individual_analyses'):
                st.subheader("Individual Analyses:")
                for i, analysis in enumerate(hall['individual_analyses']):
                    status = "🚨 POTENTIAL HALLUCINATION" if analysis['is_hallucination'] else "✅ FACTUAL"
                    st.write(f"**Prompt {i+1}:** {analysis['prompt']}")
                    st.write(f"**Generated:** {analysis['response']}")
                    st.write(f"**Reference:** {analysis.get('reference', 'N/A')}")
                    st.write(f"**Similarity Score:** {analysis['similarity_score']:.3f}")
                    st.write(f"**Status:** {status}")
                    st.markdown("---")

    # ------------------------------------------------------------------ #
    # Downloads
    # ------------------------------------------------------------------ #
    st.markdown("---")
    st.markdown("### 📥 Export Reports")
    col1, col2 = st.columns(2)

    with col1:
        # JSON download
        json_data = json.dumps(audit, indent=2, default=str).encode()
        st.download_button(
            label="📄 Download JSON Report",
            data=json_data,
            file_name=f"ethics_audit_{datetime.now():%Y%m%d_%H%M%S}.json",
            mime="application/json",
        )

    with col2:
        # Markdown summary
        md_summary = f"""# Ethics Audit Summary
**Status:** {summ['overall_status']}
**Risk Level:** {summ['risk_level']}
**Issues Found:** {len(summ['issues_found'])}
**Compliance Score:** {score:.0f}%
**Generated:** {datetime.now():%Y-%m-%d %H:%M:%S}

## Issues Identified
{chr(10).join(f'- {issue}' for issue in summ['issues_found']) if summ['issues_found'] else '- No critical issues detected'}

## Recommendations
{chr(10).join(f'- {rec}' for rec in summ['recommendations'])}
"""
        st.download_button(
            label="📝 Download Markdown Report",
            data=md_summary,
            file_name=f"ethics_audit_{datetime.now():%Y%m%d_%H%M%S}.md",
            mime="text/markdown",
        )

# Footer
st.markdown("""
---
<div class="footer">
    <p>Ethics Toolkit v1.0 | Built for Responsible AI Development</p>
</div>
""", unsafe_allow_html=True)
