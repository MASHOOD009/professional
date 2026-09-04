import streamlit as st
import pandas as pd
from datetime import datetime

from cyber_attack_detection import (
    predict_attack,
    accuracy
)

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="CyberGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================
# CUSTOM UI DESIGN
# ==========================================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================

st.markdown(
    '<div class="main-title">🛡️ CyberGuard AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Cyber Attack Detection and Network Monitoring System'
    '</div>',
    unsafe_allow_html=True
)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("🛡️ CyberGuard AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🔍 Attack Detection",
        "📊 Dashboard",
        "📜 Prediction History",
        "ℹ️ About Project"
    ]
)

# ==========================================
# ATTACK DETECTION PAGE
# ==========================================

if page == "🔍 Attack Detection":

    st.header("🔍 Network Activity Analysis")

    st.write(
        "Enter network traffic information below and let the "
        "Machine Learning model analyze the activity."
    )

    col1, col2 = st.columns(2)

    with col1:

        packet_size = st.number_input(
            "📦 Packet Size",
            min_value=0,
            value=500
        )

        connection_duration = st.number_input(
            "⏱️ Connection Duration",
            min_value=0,
            value=100
        )

    with col2:

        failed_login_attempts = st.number_input(
            "🔐 Failed Login Attempts",
            min_value=0,
            value=0
        )

        number_of_packets = st.number_input(
            "📡 Number of Packets",
            min_value=0,
            value=100
        )

    st.divider()

    if st.button(
        "🚀 Analyze Network Activity",
        use_container_width=True
    ):

        prediction = predict_attack(
            packet_size,
            connection_duration,
            failed_login_attempts,
            number_of_packets
        )

        st.subheader("Analysis Result")

        if prediction == 1:

            st.error("🚨 CYBER ATTACK DETECTED!")

            st.warning(
                "⚠️ The network activity contains suspicious patterns."
            )

        else:

            st.success("✅ NORMAL NETWORK TRAFFIC")

            st.info(
                "The network activity appears normal."
            )

        # Prediction information

        prediction_data = {
            "Date & Time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "Packet Size": packet_size,
            "Connection Duration": connection_duration,
            "Failed Login Attempts": failed_login_attempts,
            "Number of Packets": number_of_packets,
            "Result": (
                "Cyber Attack"
                if prediction == 1
                else "Normal Traffic"
            )
        }

        st.session_state["latest_prediction"] = prediction_data

# ==========================================
# DASHBOARD PAGE
# ==========================================

elif page == "📊 Dashboard":

    st.header("📊 Security Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🤖 ML Model",
        "Random Forest"
    )

    col2.metric(
        "🎯 Model Accuracy",
        f"{accuracy * 100:.2f}%"
    )

    col3.metric(
        "🛡️ System Status",
        "Active"
    )

    st.divider()

    st.subheader("System Overview")

    st.info(
        "This dashboard will display prediction statistics "
        "and attack detection information."
    )

    if "latest_prediction" in st.session_state:

        st.subheader("Latest Prediction")

        latest = pd.DataFrame(
            [st.session_state["latest_prediction"]]
        )

        st.dataframe(
            latest,
            use_container_width=True
        )

# ==========================================
# PREDICTION HISTORY PAGE
# ==========================================

elif page == "📜 Prediction History":

    st.header("📜 Prediction History")

    st.write(
        "All predictions will be stored and retrieved from MySQL."
    )

    st.info(
        "The MySQL database connection will be added next."
    )

# ==========================================
# ABOUT PAGE
# ==========================================

elif page == "ℹ️ About Project":

    st.header("ℹ️ About CyberGuard AI")

    st.write("""
    **CyberGuard AI** is a Data Science and Machine Learning
    project designed to analyze network traffic and detect
    possible cyber attacks.
    """)

    st.subheader("Technologies Used")

    st.write("""
    - 🐍 Python
    - 📊 Pandas
    - 🤖 Scikit-learn
    - 🌲 Random Forest Classifier
    - 🌐 Streamlit
    - 🗄️ MySQL
    """)

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "🛡️ CyberGuard AI | Cyber Attack Detection and Monitoring System"
)