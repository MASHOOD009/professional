import streamlit as st
import pandas as pd

from cyber_attack_detection import (
    predict_attack,
    save_prediction,
    get_prediction_history
)

# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="CyberGuard AI",
    page_icon="🛡️",
    layout="wide"
)

# ==============================
# CUSTOM CSS
# ==============================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.stButton > button {
    width: 100%;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==============================
# SIDEBAR
# ==============================

st.sidebar.title("🛡️ CyberGuard AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🚨 Attack Detection",
        "📊 Dashboard",
        "📜 Prediction History",
        "ℹ️ About Project"
    ]
)


# ==============================
# ATTACK DETECTION PAGE
# ==============================

if page == "🚨 Attack Detection":

    st.title("🛡️ CyberGuard AI")

    st.subheader("Cyber Attack Detection and Network Monitoring System")

    st.divider()

    st.header("🔍 Network Activity Analysis")

    st.write(
        "Enter network traffic information below and let the "
        "Machine Learning model analyze the activity."
    )

    col1, col2 = st.columns(2)

    with col1:
        packet_size = st.number_input(
            "📦 Packet Size",
            min_value=0.0,
            value=500.0
        )

        connection_duration = st.number_input(
            "⏱️ Connection Duration",
            min_value=0.0,
            value=100.0
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

    if st.button("🚀 Analyze Network Activity"):

        with st.spinner("Analyzing network activity..."):

            result = predict_attack(
                packet_size,
                connection_duration,
                failed_login_attempts,
                number_of_packets
            )

        prediction = result["prediction"]
        attack_type = result["attack_type"]
        confidence = result["confidence"]

        # SAVE TO MYSQL
        save_prediction(
            packet_size,
            connection_duration,
            failed_login_attempts,
            number_of_packets,
            prediction,
            attack_type,
            confidence
        )

        st.divider()

        st.header("📋 Analysis Result")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Prediction",
                prediction
            )

        with col2:
            st.metric(
                "Attack Type",
                attack_type
            )

        with col3:
            st.metric(
                "Confidence",
                f"{confidence:.2f}%"
            )

        # ALERT MESSAGE
        if prediction.lower() in ["attack", "malicious", "dos attack"]:

            st.error(
                f"⚠️ SECURITY ALERT: {attack_type} detected!"
            )

        else:

            st.success(
                "✅ Network activity appears to be safe."
            )


# ==============================
# DASHBOARD PAGE
# ==============================

elif page == "📊 Dashboard":

    st.title("📊 Cyber Security Dashboard")

    try:

        data = get_prediction_history()

        if data is not None and len(data) > 0:

            df = pd.DataFrame(data)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Total Records",
                    len(df)
                )

            with col2:
                attacks = len(
                    df[df["prediction"].str.lower() != "normal"]
                )

                st.metric(
                    "Total Attacks",
                    attacks
                )

            with col3:
                normal = len(df) - attacks

                st.metric(
                    "Normal Traffic",
                    normal
                )

            st.divider()

            st.subheader("📈 Recent Network Activity")

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info(
                "No prediction data available yet."
            )

    except Exception as e:

        st.warning(
            "Unable to load dashboard data."
        )


# ==============================
# PREDICTION HISTORY
# ==============================

elif page == "📜 Prediction History":

    st.title("📜 Prediction History")

    try:

        data = get_prediction_history()

        if data is not None and len(data) > 0:

            df = pd.DataFrame(data)

            st.dataframe(
                df,
                use_container_width=True
            )

        else:

            st.info(
                "No prediction history found."
            )

    except Exception as e:

        st.error(
            f"Database error: {e}"
        )


# ==============================
# ABOUT PROJECT
# ==============================

elif page == "ℹ️ About Project":

    st.title("ℹ️ About CyberGuard AI")

    st.write("""
    **CyberGuard AI** is a Cyber Attack Detection and Network
    Monitoring System.

    The system uses Machine Learning to analyze network activity
    and identify potentially malicious traffic.
    """)

    st.subheader("🛠️ Technologies Used")

    st.write("""
    - Python
    - Streamlit
    - Machine Learning
    - Scikit-learn
    - Pandas
    - NumPy
    - MySQL
    """)


# ==============================
# FOOTER
# ==============================

st.divider()

st.caption(
    "🛡️ CyberGuard AI | Cyber Attack Detection and Monitoring System"
)