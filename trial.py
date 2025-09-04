import pandas as pd 
import pickle
import streamlit as st 
import numpy as np

# Configure page
st.set_page_config(
    page_title="Laptop Price Predictor",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load models and data
@st.cache_data
def load_data():
    pipe = pickle.load(open('pipe.pkl', 'rb'))
    df = pickle.load(open('lapidata.pkl', 'rb'))
    return pipe, df

pipe, df = load_data()

# Initialize dark mode in session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Dark/Light mode toggle function
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Dynamic CSS based on theme
def get_theme_css(dark_mode):
    if dark_mode:
        # Dark theme colors
        bg_color = "#1e1e1e"
        card_bg = "#2d2d2d"
        text_primary = "#ffffff"
        text_secondary = "#b0b0b0"
        border_color = "#404040"
        accent_color = "#4a9eff"
        accent_hover = "#357abd"
        success_bg = "#1a4a3a"
        success_text = "#4ade80"
        success_border = "#2d5a3d"
        info_bg = "#2d3748"
        input_bg = "#374151"
        input_border = "#4b5563"
        shadow = "rgba(0,0,0,0.3)"
        hover_shadow = "rgba(0,0,0,0.4)"
    else:
        # Light theme colors
        bg_color = "#f1f3f4"
        card_bg = "#ffffff"
        text_primary = "#2c3e50"
        text_secondary = "#6c757d"
        border_color = "#e9ecef"
        accent_color = "#007bff"
        accent_hover = "#0056b3"
        success_bg = "#d4edda"
        success_text = "#155724"
        success_border = "#c3e6cb"
        info_bg = "#f8f9fa"
        input_bg = "#ffffff"
        input_border = "#ced4da"
        shadow = "rgba(0,0,0,0.08)"
        hover_shadow = "rgba(0,0,0,0.12)"

    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        
        .stApp {{
            background-color: {bg_color};
            font-family: 'Inter', sans-serif;
            color: {text_primary};
        }}
        
        .main {{
            padding: 1rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .theme-toggle {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 50px;
            padding: 0.5rem 1rem;
            cursor: pointer;
            box-shadow: 0 2px 8px {shadow};
            z-index: 1000;
            font-size: 1.1rem;
            color: {text_primary};
            transition: all 0.2s ease;
        }}
        
        .theme-toggle:hover {{
            box-shadow: 0 4px 12px {hover_shadow};
            transform: translateY(-1px);
        }}
        
        .main-header {{
            background: {card_bg};
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px {shadow};
            border: 1px solid {border_color};
        }}
        
        .main-title {{
            font-size: 2.5rem;
            font-weight: 600;
            color: {text_primary};
            text-align: center;
            margin: 0;
        }}
        
        .subtitle {{
            font-size: 1.1rem;
            color: {text_secondary};
            text-align: center;
            margin-top: 0.5rem;
            font-weight: 400;
        }}
        
        .spec-section {{
            background: {card_bg};
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px {shadow};
            border: 1px solid {border_color};
            transition: all 0.2s ease;
        }}
        
        .spec-section:hover {{
            box-shadow: 0 4px 12px {hover_shadow};
        }}
        
        .section-title {{
            font-size: 1.2rem;
            font-weight: 500;
            color: {text_primary};
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {info_bg};
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .predict-btn {{
            background: {accent_color};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.8rem 2rem;
            font-size: 1.1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            width: 100%;
            margin: 1.5rem 0;
        }}
        
        .predict-btn:hover {{
            background: {accent_hover};
            transform: translateY(-1px);
        }}
        
        .price-result {{
            background: {success_bg};
            color: {success_text};
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
            margin: 1rem 0;
            border: 1px solid {success_border};
            animation: fadeIn 0.3s ease;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .price-amount {{
            font-size: 2.2rem;
            font-weight: 600;
            margin: 0.5rem 0;
        }}
        
        .info-panel {{
            background: {card_bg};
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px {shadow};
            border: 1px solid {border_color};
        }}
        
        .info-item {{
            background: {info_bg};
            border-radius: 6px;
            padding: 1rem;
            margin: 0.8rem 0;
            border-left: 3px solid {accent_color};
            color: {text_primary};
        }}
        
        .spec-summary {{
            background: {info_bg};
            border-radius: 6px;
            padding: 1rem;
            margin: 0.5rem 0;
            font-size: 0.9rem;
            color: {text_primary};
        }}
        
        .stSelectbox > div > div {{
            background-color: {input_bg} !important;
            border-radius: 6px !important;
            border: 1px solid {input_border} !important;
            transition: border-color 0.2s ease;
            color: {text_primary} !important;
        }}
        
        .stSelectbox > div > div:focus-within {{
            border-color: {accent_color} !important;
            box-shadow: 0 0 0 2px rgba(74,158,255,0.1) !important;
        }}
        
        .stSelectbox label {{
            color: {text_primary} !important;
        }}
        
        .stNumberInput > div > div > input {{
            background-color: {input_bg} !important;
            border-radius: 6px !important;
            border: 1px solid {input_border} !important;
            transition: border-color 0.2s ease;
            color: {text_primary} !important;
        }}
        
        .stNumberInput > div > div > input:focus {{
            border-color: {accent_color} !important;
            box-shadow: 0 0 0 2px rgba(74,158,255,0.1) !important;
        }}
        
        .stNumberInput label {{
            color: {text_primary} !important;
        }}
        
        .stButton > button {{
            background: {accent_color} !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.8rem 2rem !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }}
        
        .stButton > button:hover {{
            background: {accent_hover} !important;
            transform: translateY(-1px) !important;
        }}
        
        .warning-box {{
            background: #fff3cd;
            color: #856404;
            padding: 1rem;
            border-radius: 6px;
            border: 1px solid #ffeaa7;
            margin: 1rem 0;
        }}
        
        /* Custom scrollbar for dark mode */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {info_bg};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {border_color};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {text_secondary};
        }}
    </style>
    """

# Apply theme CSS
st.markdown(get_theme_css(st.session_state.dark_mode), unsafe_allow_html=True)

# Theme toggle button
theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
theme_text = "Dark Mode" if not st.session_state.dark_mode else "Light Mode"

# Create columns for header with theme toggle
header_col1, header_col2 = st.columns([4, 1])

with header_col2:
    if st.button(f"{theme_icon} {theme_text}", key="theme_toggle"):
        toggle_theme()
        st.rerun()

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">💻 Laptop Price Predictor</h1>
    <p class="subtitle">Get accurate price estimates based on laptop specifications</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([2.5, 1.5])

with col1:
    # Basic Info Section
    st.markdown('<div class="spec-section"><h3 class="section-title">🏢 Basic Information</h3></div>', unsafe_allow_html=True)
    
    basic_col1, basic_col2 = st.columns(2)
    with basic_col1:
        company = st.selectbox('🏷️ Brand', df['Company'].unique())
        ram = st.selectbox('🧠 RAM (GB)', [2,4,6,8,12,16,24,32,64], index=3)
    
    with basic_col2:
        type_laptop = st.selectbox('💼 Type', df['TypeName'].unique())
        weight = st.number_input('⚖️ Weight (kg)', min_value=0.5, max_value=5.0, value=2.0, step=0.1)

    # Display Section
    st.markdown('<div class="spec-section"><h3 class="section-title">🖥️ Display & Features</h3></div>', unsafe_allow_html=True)
    
    display_col1, display_col2 = st.columns(2)
    with display_col1:
        screen_size = st.number_input('📏 Screen Size (inches)', min_value=10.0, max_value=20.0, value=15.6, step=0.1)
        resolution = st.selectbox('🎯 Resolution', 
            ['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])
    
    with display_col2:
        if company != 'Apple':
            touchscreen = st.selectbox('👆 Touch Screen', ['No','Yes'])
        else:
            touchscreen = st.selectbox('👆 Touch Screen', ['No'])
        ips = st.selectbox('🌈 IPS Panel', ['No','Yes'])

    # Performance Section
    st.markdown('<div class="spec-section"><h3 class="section-title">⚡ Performance</h3></div>', unsafe_allow_html=True)
    
    perf_col1, perf_col2 = st.columns(2)
    with perf_col1:
        cpu = st.selectbox('🔧 CPU', df['cpu_brand'].unique())
        ssd = st.selectbox('💾 SSD (GB)', [0,128,256,512,1024,2048], index=2)
    
    with perf_col2:
        gpu = st.selectbox('🎮 GPU', df['GpuBrand'].unique())
        hardDrive = st.selectbox('💿 HDD (GB)', [0,128,256,512,1024,2048])

    # OS Section
    st.markdown('<div class="spec-section"><h3 class="section-title">💻 Operating System</h3></div>', unsafe_allow_html=True)
    
    if company != 'Apple':
        os_for_win = df['os'].unique().tolist()[1:]
        os = st.selectbox('🖥️ Operating System', os_for_win)
    else:
        os = st.selectbox('🖥️ Operating System', ['Mac'])

    # Predict Button
    predict_clicked = st.button('🔮 Predict Price', key='predict', help='Click to get price prediction')

with col2:
    # Info Panel
    st.markdown("""
    <div class="info-panel">
        <h3 class="section-title">ℹ️ How It Works</h3>
        <div class="info-item">
            <strong>🤖 Machine Learning Model</strong><br>
            Uses advanced algorithms trained on real market data
        </div>
        <div class="info-item">
            <strong>📊 Accurate Predictions</strong><br>
            Based on thousands of laptop configurations and prices
        </div>
        <div class="info-item">
            <strong>⚡ Instant Results</strong><br>
            Get price estimates in seconds
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Current Selection Summary
    st.markdown("""
    <div class="info-panel">
        <h3 class="section-title">📝 Your Selection</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="spec-summary">
        <strong>🏷️ Brand:</strong> {company}<br>
        <strong>💼 Type:</strong> {type_laptop}<br>
        <strong>🧠 RAM:</strong> {ram} GB<br>
        <strong>💾 Storage:</strong> {ssd} GB SSD + {hardDrive} GB HDD<br>
        <strong>🖥️ Screen:</strong> {screen_size}" {resolution}<br>
        <strong>🔧 CPU:</strong> {cpu}<br>
        <strong>🎮 GPU:</strong> {gpu}<br>
        <strong>💻 OS:</strong> {os}
    </div>
    """, unsafe_allow_html=True)

# Prediction Logic
if predict_clicked:
    touchscreen_val = 1 if touchscreen == 'Yes' else 0
    ips_val = 1 if ips == 'Yes' else 0
    
    # Calculate PPI
    x_res = int(resolution.split('x')[0])
    y_res = int(resolution.split('x')[1])
    ppi = ((x_res**2 + y_res**2)**0.5) / screen_size
    
    # Create prediction query
    query = np.array([company, type_laptop, ram, weight, touchscreen_val, ips_val, ppi, cpu, ssd, hardDrive, gpu, os])
    query = query.reshape(1, -1)
    
    try:
        prediction = pipe.predict(query)[0]
        predicted_price = round(np.exp(prediction))
        
        # Display result
        st.markdown(f"""
        <div class="price-result">
            <div>💰 Estimated Price</div>
            <div class="price-amount">₹{predicted_price:,}</div>
            <div>Based on current market analysis</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Price range
        lower_range = int(predicted_price * 0.9)
        upper_range = int(predicted_price * 1.1)
        
        st.info(f"📊 **Price Range:** ₹{lower_range:,} - ₹{upper_range:,}")
        st.success("✅ Prediction completed successfully!")
        
    except Exception as e:
        st.error(f"❌ Prediction failed: {str(e)}")
        st.info("💡 Please check your inputs and try again.")

# Simple footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: var(--text-secondary); border-top: 1px solid var(--border-color); margin-top: 2rem;">
    <p>💻 Laptop Price Predictor | Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)