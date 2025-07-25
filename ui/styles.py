"""
Custom CSS styles for the Ethics Toolkit Streamlit application
Provides modern, professional styling for enhanced user experience
"""

import streamlit as st

def apply_custom_styles():
    """
    Apply comprehensive custom CSS styling to the Streamlit app
    """
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --success-color: #4facfe;
        --warning-color: #fa709a;
        --error-color: #ff6b6b;
        --text-primary: #2E4057;
        --text-secondary: #666;
        --background-light: #f8f9fa;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        --border-radius: 12px;
        --transition: all 0.3s ease;
    }
    
    /* Global app styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .main > div {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom header styling */
    .main-header {
        background: var(--background-gradient);
        color: white;
        padding: 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--card-shadow);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 2px solid #e9ecef;
    }
    
    .sidebar .sidebar-content {
        padding: 1rem;
    }
    
    /* Card components */
    .metric-card {
        background: var(--background-gradient);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: var(--card-shadow);
        transition: var(--transition);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Status indicators */
    .status-card {
        padding: 1.5rem;
        border-radius: var(--border-radius);
        color: white;
        text-align: center;
        margin: 0.5rem;
        box-shadow: var(--card-shadow);
        transition: var(--transition);
    }
    
    .status-card:hover {
        transform: translateY(-2px);
    }
    
    .status-good {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    .status-error {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    }
    
    .status-neutral {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    }
    
    /* Feature highlight cards */
    .feature-highlight {
        background: var(--background-gradient);
        padding: 2rem;
        border-radius: var(--border-radius);
        color: white;
        margin: 1rem 0;
        box-shadow: var(--card-shadow);
        transition: var(--transition);
    }
    
    .feature-highlight:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
    }
    
    .feature-highlight h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .feature-highlight p {
        opacity: 0.9;
        line-height: 1.6;
    }
    
    /* Upload section */
    .upload-section {
        border: 3px dashed #cccccc;
        border-radius: var(--border-radius);
        padding: 3rem;
        text-align: center;
        background: var(--background-light);
        margin: 2rem 0;
        transition: var(--transition);
    }
    
    .upload-section:hover {
        border-color: var(--primary-color);
        background: white;
    }
    
    .upload-section h2 {
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    .upload-section p {
        color: var(--text-secondary);
        font-size: 1.1rem;
    }
    
    /* Button enhancements */
    .stButton > button {
        background: var(--background-gradient);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: var(--transition);
        box-shadow: var(--card-shadow);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: var(--transition);
        box-shadow: var(--card-shadow);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white;
        border-radius: var(--border-radius);
        padding: 0.5rem;
        box-shadow: var(--card-shadow);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: var(--transition);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--background-gradient);
        color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Data display enhancements */
    .stDataFrame {
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--card-shadow);
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: var(--border-radius);
        box-shadow: var(--card-shadow);
        transition: var(--transition);
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: var(--border-radius);
        border: none;
        box-shadow: var(--card-shadow);
    }
    
    .stAlert[data-baseweb="notification"] {
        background: white;
        border-left: 4px solid var(--primary-color);
    }
    
    /* Success messages */
    .stSuccess {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border-radius: var(--border-radius);
        padding: 1rem;
        box-shadow: var(--card-shadow);
    }
    
    /* Warning messages */
    .stWarning {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        border-radius: var(--border-radius);
        padding: 1rem;
        box-shadow: var(--card-shadow);
    }
    
    /* Error messages */
    .stError {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        border-radius: var(--border-radius);
        padding: 1rem;
        box-shadow: var(--card-shadow);
    }
    
    /* Info messages */
    .stInfo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: var(--border-radius);
        padding: 1rem;
        box-shadow: var(--card-shadow);
    }
    
    /* Code block styling */
    .stCode {
        border-radius: var(--border-radius);
        border: 1px solid #e9ecef;
        box-shadow: var(--card-shadow);
    }
    
    /* Spinner styling */
    .stSpinner {
        text-align: center;
        padding: 2rem;
    }
    
    /* Footer styling */
    .footer {
        background: var(--background-gradient);
        color: white;
        text-align: center;
        padding: 2rem;
        border-radius: var(--border-radius);
        margin-top: 3rem;
        box-shadow: var(--card-shadow);
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .feature-highlight {
            padding: 1.5rem;
        }
        
        .upload-section {
            padding: 2rem;
        }
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-up {
        animation: slideUp 0.6s ease-out;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Loading states */
    .loading-shimmer {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
    </style>
    """, unsafe_allow_html=True)

def create_status_card(status, title, color_class="status-neutral"):
    """
    Create a styled status card component
    
    Args:
        status: Status value to display
        title: Title/label for the status
        color_class: CSS class for color styling
    
    Returns:
        HTML string for the status card
    """
    return f"""
    <div class="status-card {color_class}">
        <h3 style="margin: 0; font-size: 1.8rem; font-weight: 700;">{status}</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">{title}</p>
    </div>
    """

def create_metric_card(value, label, icon="📊"):
    """
    Create a styled metric card
    
    Args:
        value: Metric value
        label: Metric label
        icon: Icon emoji
    
    Returns:
        HTML string for the metric card
    """
    return f"""
    <div class="metric-card fade-in">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
        <h3 style="margin: 0; font-size: 1.8rem; font-weight: 700;">{value}</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">{label}</p>
    </div>
    """

def create_feature_card(title, description, icon="🔧"):
    """
    Create a feature highlight card
    
    Args:
        title: Feature title
        description: Feature description
        icon: Icon emoji
    
    Returns:
        HTML string for the feature card
    """
    return f"""
    <div class="feature-highlight slide-up">
        <h3>{icon} {title}</h3>
        <p>{description}</p>
    </div>
    """

def create_progress_bar(progress, label="Progress"):
    """
    Create a custom progress bar
    
    Args:
        progress: Progress value (0-100)
        label: Progress label
    
    Returns:
        HTML string for the progress bar
    """
    return f"""
    <div style="margin: 1rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="font-weight: 500;">{label}</span>
            <span style="font-weight: 600;">{progress}%</span>
        </div>
        <div style="background: #e9ecef; border-radius: 10px; height: 8px; overflow: hidden;">
            <div style="background: var(--background-gradient); height: 100%; width: {progress}%; transition: width 0.3s ease;"></div>
        </div>
    </div>
    """
