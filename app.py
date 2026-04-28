import streamlit as st
from auth import show_auth
import random
import time
import cv2
import matplotlib.pyplot as plt
import json
from streamlit_lottie import st_lottie

import json

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# -------- SESSION INIT --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------- LOGIN GATE --------
if not st.session_state.logged_in:
    show_auth()
    st.stop()   # 🔥 stops app until login

# -------- MAIN APP --------
st.sidebar.title("🤖 Automorphic")

# Logout button
if st.sidebar.button("Logout", key="logout_btn"):
    st.session_state.logged_in = False
    st.rerun()

page = st.sidebar.selectbox("Navigation", ["Home","Live Sensor Data","Simulation Mode","Documentation","About","Help / Support"])


if page == "Home":

    import streamlit as st

    # ---- GLOBAL STYLE ----
    st.markdown("""
    <style>
    .hero-title {
        text-align: center;
        font-size: 48px;
        font-weight: 700;
        background: linear-gradient(90deg, #22c55e, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-sub {
        text-align: center;
        font-size: 18px;
        color: #9ca3af;
    }
    .card {
        background-color: #111827;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---- HERO ----
    st.markdown('<div class="hero-title">Automorphic</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Intelligent Metal Forming • Powered by IoT + AI</div>', unsafe_allow_html=True)

    st.markdown("")

    st.markdown("""
    <div style='text-align:center; font-size:16px; max-width:700px; margin:auto; line-height:1.6'>
    A next-generation smart manufacturing system that combines real-time sensor data, 
    predictive intelligence, and visual validation to achieve precision metal forming 
    with minimal error and maximum efficiency.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ---- HIGHLIGHTS ----
    st.markdown("### ⚡ Why Automorphic Stands Out")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        📡 <h4>Real-Time Monitoring</h4>
        Continuous sensor tracking ensures live industrial visibility
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        🧠 <h4>Predictive Intelligence</h4>
        AI-driven models optimize force & temperature dynamically
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        🎯 <h4>Precision Control</h4>
        Minimizes springback and improves forming accuracy
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ---- PROBLEM VS SOLUTION ----
    st.markdown("### 🔍 From Problem → Solution")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.error("""
        ❌ **Traditional Manufacturing**
        - Unpredictable springback  
        - Manual adjustments  
        - High material waste  
        - Inconsistent output  
        """)

    with col2:
        st.success("""
        ✅ **With Automorphic**
        - Data-driven predictions  
        - Automated optimization  
        - Reduced waste  
        - Consistent precision  
        """)

    st.markdown("---")

    # ---- SYSTEM FLOW ----
    st.markdown("### 🔄 Intelligent Workflow")

    st.markdown("""
    ```text
    Sensors → Data Stream → AI Prediction → Metal Forming → Vision Feedback → Continuous Optimization
    ```
    """)

    st.markdown("---")

    # ---- CORE MODULES ----
    st.markdown("### 🧩 Core System Modules")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("""
        📡 **Sensor Layer**
        - Temperature  
        - Thickness  
        - Material detection  
        """)

    with c2:
        st.info("""
        🧠 **AI Engine**
        - Force prediction  
        - Temperature optimization  
        """)

    with c3:
        st.info("""
        🎥 **Vision System**
        - Curvature detection  
        - Springback analysis  
        """)

    st.markdown("---")

    # ---- IMPACT ----
    st.markdown("### 📈 Impact")

    i1, i2, i3 = st.columns(3)

    with i1:
        st.success("⚡ Faster Production")

    with i2:
        st.success("♻️ Reduced Waste")

    with i3:
        st.success("🎯 Higher Accuracy")

    st.markdown("---")

    # ---- CALL TO ACTION ----
    st.markdown("### 🚀 Explore the System")

    st.info("""
    👉 Navigate using the sidebar to:
    - View **Live IoT Dashboard**  
    - Run **Simulation Mode**  
    - Explore **Analytics & Insights**  
    """)

    st.markdown("---")

    # ---- FOOTER ----
    st.markdown("""
    <p style='text-align:center; color:#6b7280; font-size:13px;'>
    Automorphic • Intelligent Manufacturing Platform
    </p>
    """, unsafe_allow_html=True)
        
elif page == "Live Sensor Data":

    import boto3
    from streamlit_autorefresh import st_autorefresh
    from decimal import Decimal

    st.title("📡 Live IoT Sensor Dashboard")
    st.caption("Real-time industrial sensor monitoring (AWS IoT + DynamoDB)")

    # 🔄 Auto refresh every 2 sec
    st_autorefresh(interval=2000, key="iot_refresh")

    st.markdown("---")

    # # 🔐 Load AWS secrets
    # aws_access_key = st.secrets["AWS_ACCESS_KEY_ID"]
    # aws_secret_key = st.secrets["AWS_SECRET_ACCESS_KEY"]
    # region = st.secrets["AWS_REGION"]
    # table_name = st.secrets["TABLE_NAME"]
    
    import os

    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION")
    table_name = os.getenv("TABLE_NAME")

    # 🔧 Convert Decimal → float
    def convert_decimal(obj):
        if isinstance(obj, list):
            return [convert_decimal(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: convert_decimal(v) for k, v in obj.items()}
        elif isinstance(obj, Decimal):
            return float(obj)
        return obj

    # 🔗 Connect to DynamoDB
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    table = dynamodb.Table(table_name)

    # 📥 Fetch data
    try:
        response = table.get_item(
            Key={"machine_id": "SMART_BENCH_01"}
        )
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
        st.stop()

    # 📊 DISPLAY
    if "Item" in response:

        data = convert_decimal(response["Item"])

        st.subheader("📊 Live Sensor Metrics")

        # ✅ 3 COLUMN LAYOUT (cleaner now)
        col1, col2, col3 = st.columns(3)

        col1.metric("🌡 Temperature", f"{data.get('temperature', 0):.1f} °C")
        col2.metric("📏 Thickness", f"{data.get('thickness_mm', 0):.2f} mm")
        col3.metric("⚖ Density", f"{data.get('density', 0):.2f}")

        st.markdown("---")

        # 🟢 SYSTEM STATUS
        st.subheader("🟢 System Status")

        temp = data.get("temperature", 0)

        if temp > 70:
            st.warning("⚠️ High Temperature - Monitor system")
        elif temp < 30:
            st.info("ℹ️ Low Temperature - Stable")
        else:
            st.success("✅ System Operating Normally")

        st.markdown("---")

        # 🧠 ML INSIGHTS (OPTIONAL CLEAN SECTION)
        with st.expander("🧠 AI Insights & Predictions"):

            angle = st.slider("🎯 Target Angle", 0, 180, 90)

            thickness = data.get("thickness_mm", 0)
            young_modulus = data.get("youngs_modulus", 180)
            temperature = data.get("temperature", 0)

            base_force = thickness * young_modulus * angle * 0.5
            temp_factor = max(0.5, 1 - (temperature / 200))

            predicted_force = round(base_force * temp_factor, 2)
            optimal_temp = round(temperature + (angle / 10) + (thickness * 2), 2)

            c1, c2 = st.columns(2)
            c1.metric("💪 Predicted Force", f"{predicted_force} N")
            c2.metric("🔥 Optimal Temp", f"{optimal_temp} °C")

    else:
        st.warning("⚠️ No live data found in DynamoDB")     

elif page == "Simulation Mode":
         # ---- LOAD LOTTIE ----
    lottie_analysis = load_lottiefile("analysis.json")

        # ---- CENTERED ANIMATION ----
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
            st_lottie(lottie_analysis, height=550)
    import streamlit as st

    # ---- HEADER ----
    st.markdown("## 🧪 Simulation Studio")
    st.caption("Experiment with different materials and predict forming conditions")

    st.markdown("---")

    # ---- MATERIAL DATABASE ----
    material_db = {
        "Mild Steel": {"young_modulus": 200, "factor": 1.2},
        "Aluminum 6061": {"young_modulus": 69, "factor": 0.8},
        "Stainless Steel 304": {"young_modulus": 193, "factor": 1.0},
        "Copper": {"young_modulus": 117, "factor": 1.3},
        "Titanium Grade 2": {"young_modulus": 105, "factor": 0.8},
        "Brass": {"young_modulus": 100, "factor": 1.0},
    }

    # ---- INPUT SECTION ----
    st.markdown("### ⚙️ Input Parameters")

    col1, col2 = st.columns(2)

    with col1:
        metal = st.selectbox("🔩 Metal Type", list(material_db.keys()))

        # auto-fill Young's modulus (editable)
        default_young = material_db[metal]["young_modulus"]
        young_modulus = st.number_input(
            "⚙️ Young’s Modulus (GPa)",
            50.0, 300.0,
            float(default_young)
        )

        thickness = st.number_input("📏 Thickness (mm)", 0.1, 10.0, 2.0)

    with col2:
        temperature = st.number_input("🌡 Temperature (°C)", 0.0, 200.0, 30.0)
        angle = st.slider("🎯 Target Angle (degrees)", 0, 180, 90)

    st.markdown("---")

    # ---- RUN BUTTON ----
    run_sim = st.button("🚀 Run Simulation")

    if run_sim:

        # ---- MATERIAL FACTOR ----
        material_factor = material_db[metal]["factor"]

        # ---- CALCULATION LOGIC ----
        base_force = thickness * young_modulus * angle * 0.5 * material_factor
        temp_factor = max(0.5, 1 - (temperature / 200))
        predicted_force = round(base_force * temp_factor, 2)

        optimal_temp = round(
            temperature + (angle / 10) + (thickness * 2), 2
        )

        # ---- OUTPUT SECTION ----
        st.markdown("### 📊 Simulation Results")

        out1, out2 = st.columns(2)

        with out1:
            st.success(f"💪 Required Force\n\n### {predicted_force} N")

        with out2:
            st.success(f"🔥 Optimal Temperature\n\n### {optimal_temp} °C")

        st.markdown("---")

        # ---- MATERIAL INSIGHT ----
        st.markdown("### 🧠 Material Insight")

        st.info(f"""
        **Selected Material:** {metal}

        - Higher stiffness increases required force  
        - Material factor applied: **{material_factor}**  
        - Temperature reduces resistance due to softening  

        This simulation helps estimate forming conditions before real-world execution.
        """)

    else:
        st.warning("👆 Select parameters and click **Run Simulation**")
        
elif page == "Documentation":
         # ---- LOAD LOTTIE ----
    lottie_analysis = load_lottiefile("Documentation.json")

        # ---- CENTERED ANIMATION ----
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
            st_lottie(lottie_analysis, height=550)

    import streamlit as st

    # ---- HEADER ----
    st.markdown("## 📘 Automorphic System Documentation")
    st.caption("Smart IoT-based metal forming intelligence platform")

    st.markdown("---")

    # ---- HERO SECTION ----
    st.markdown("### 🚀 What is Automorphic?")

    st.info("""
    **Automorphic** is a smart industrial system that combines **IoT, Machine Learning, and Computer Vision**
    to optimize metal sheet forming in manufacturing.

    It reduces **springback error**, improves **precision**, and enables **data-driven decision making**.
    """)

    st.markdown("---")

    # ---- CORE MODULES ----
    st.markdown("### 🧩 Core System Modules")

    col1, col2 = st.columns(2)

    with col1:
        st.success("""
        📡 **IoT Sensor Layer**

        - Temperature Monitoring  
        - Thickness Detection  
        - Material Identification  
        - Mechanical Properties Capture  
        """)

        st.success("""
        🎥 **Vision System**

        - Captures formed sheet  
        - Detects curvature  
        - Measures springback deviation  
        """)

    with col2:
        st.success("""
        🧠 **Prediction Engine**

        - Estimates required force  
        - Suggests optimal temperature  
        - Minimizes deformation error  
        """)

        st.success("""
        📊 **Analytics & Simulation**

        - Real-time dashboard  
        - Historical insights  
        - Virtual testing environment  
        """)

    st.markdown("---")

    # ---- SYSTEM FLOW ----
    st.markdown("### 🔄 System Workflow")

    st.markdown("""
    ```text
    Sensors → Cloud → Prediction Engine → Metal Forming → Camera Feedback → Optimization Loop
    ```
    """)

    st.markdown("""
    1. 📡 Sensors capture real-time industrial parameters  
    2. ☁️ Data is transmitted to the cloud  
    3. 🧠 Prediction engine computes optimal parameters  
    4. ⚙️ Forming process is executed  
    5. 🎥 Vision system evaluates output  
    6. 🔁 Feedback loop improves future predictions  
    """)

    st.markdown("---")

    # ---- TECH STACK ----
    st.markdown("### 🛠 Technology Stack")

    t1, t2, t3 = st.columns(3)

    with t1:
        st.info("""
        **Frontend**
        - Streamlit  
        - Interactive UI  
        """)

    with t2:
        st.info("""
        **Backend**
        - Python  
        - Firebase (Firestore)  
        """)

    with t3:
        st.info("""
        **Core Tech**
        - Machine Learning  
        - OpenCV  
        - Data Analytics  
        """)

    st.markdown("---")

    # ---- FEATURES ----
    st.markdown("### ✨ Key Capabilities")

    f1, f2, f3 = st.columns(3)

    with f1:
        st.success("📡 Real-time IoT Monitoring")

    with f2:
        st.success("🧠 Intelligent Prediction System")

    with f3:
        st.success("🧪 Simulation & Testing Mode")

    st.markdown("---")

    # ---- VALUE PROPOSITION ----
    st.markdown("### 💡 Why Automorphic?")

    st.warning("""
    - Reduces **material waste**  
    - Improves **forming accuracy**  
    - Enables **predictive manufacturing**  
    - Minimizes **manual intervention**  
    """)

    st.markdown("---")

    # ---- FUTURE ROADMAP ----
    st.markdown("### 🚀 Future Roadmap")

    roadmap1, roadmap2 = st.columns(2)

    with roadmap1:
        st.write("""
        - Industrial IoT hardware integration  
        - Cloud deployment (scalable infra)  
        - Advanced ML models (Neural Networks)  
        """)

    with roadmap2:
        st.write("""
        - Real-time video analytics  
        - Digital twin simulation  
        - Integration with factory control systems  
        """)

    st.markdown("---")

    # ---- FOOTER ----
    st.markdown("""
    ### ✅ Final Note

    Automorphic is designed as a **next-generation smart manufacturing assistant**  
    that bridges the gap between **data, prediction, and physical execution**.
    """)
    
elif page == "About":
         # ---- LOAD LOTTIE ----
    lottie_analysis = load_lottiefile("about.json")

        # ---- CENTERED ANIMATION ----
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
            st_lottie(lottie_analysis, height=550)
    import streamlit as st

    # ---- HEADER ----
    st.markdown("## 🚀 About Automorphic")
    st.caption("Smart IoT-based metal forming intelligence platform")

    st.markdown("---")

    # ---- HERO SECTION ----
    st.markdown("### 💡 The Idea")

    st.info("""
    **Automorphic** is a next-generation smart manufacturing system designed to improve 
    precision in metal sheet forming using **IoT, Machine Learning, and Computer Vision**.

    It transforms traditional processes into **data-driven, intelligent workflows**.
    """)

    st.markdown("---")

    # ---- CORE VALUE ----
    st.markdown("### 🎯 What Problem Are We Solving?")

    st.warning("""
    In metal forming, the **springback effect** causes materials to partially return 
    to their original shape after deformation, leading to inaccuracies and waste.

    Automorphic minimizes this problem using predictive intelligence and real-time validation.
    """)

    st.markdown("---")

    # ---- HOW IT WORKS ----
    st.markdown("### ⚙️ How Automorphic Works")

    col1, col2 = st.columns(2)

    with col1:
        st.success("""
        📡 **IoT Data Collection**
        - Temperature  
        - Thickness  
        - Material properties  
        """)

        st.success("""
        🧠 **Prediction Engine**
        - Calculates optimal force  
        - Suggests ideal temperature  
        """)

    with col2:
        st.success("""
        🎥 **Vision Feedback**
        - Detects final curvature  
        - Measures springback  
        """)

        st.success("""
        📊 **Optimization Loop**
        - Improves future predictions  
        - Reduces error over time  
        """)

    st.markdown("---")

    # ---- IMPACT ----
    st.markdown("### 📈 Impact & Benefits")

    b1, b2, b3 = st.columns(3)

    with b1:
        st.success("✔️ Higher Precision")

    with b2:
        st.success("♻️ Reduced Waste")

    with b3:
        st.success("⚡ Faster Production")

    st.markdown("---")

    # ---- TEAM ----
    st.markdown("### 👥 Team Behind Automorphic")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Aditya Sarkar**  
        *Team SPOC*
        """)

        st.markdown("""
        **Toshikka G**  
        *Team Reviewer*
        """)

    with col2:
        st.markdown("""
        **Team Members**
        - Atul Atul  
        - Anagha Giri  
        - V Nisha  
        - Sanjay Gadde  
        """)

    st.markdown("---")

    # ---- FOOTER ----
    st.success("🚀 Developed under TCS ILP — focused on AI, IoT & Smart Manufacturing")
    
elif page == "Help / Support":
         # ---- LOAD LOTTIE ----
    lottie_analysis = load_lottiefile("call-center.json")

        # ---- CENTERED ANIMATION ----
    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
            st_lottie(lottie_analysis, height=550)
    import streamlit as st

    # ---- HEADER ----
    st.markdown("## 🆘 Help & User Guide")
    st.caption("Quick guide to using Automorphic effectively")

    st.markdown("---")

    # ---- QUICK START ----
    st.markdown("### ⚡ Quick Start")

    st.info("""
    1. Navigate through different modules from the sidebar  
    2. View real-time data in the **Live Dashboard**  
    3. Use **Simulation Mode** to test scenarios  
    4. Explore insights and predictions  
    """)

    st.markdown("---")

    # ---- FEATURES GUIDE ----
    st.markdown("### 🧭 Feature Guide")

    f1, f2 = st.columns(2)

    with f1:
        st.success("""
        📡 **Live Sensor Dashboard**
        - Displays real-time IoT data  
        - Auto-refresh updates  
        - Shows key metrics  
        """)

        st.success("""
        🧠 **AI Insights**
        - Predicts force & temperature  
        - Based on current inputs  
        """)

    with f2:
        st.success("""
        ⚙️ **Simulation Mode**
        - Manual input testing  
        - Try different materials & angles  
        """)

        st.success("""
        📊 **Analytics**
        - Visual trends  
        - Helps decision-making  
        """)

    st.markdown("---")

    # ---- HOW TO USE ----
    st.markdown("### 🧪 How to Use Simulation")

    st.write("""
    - Select **metal type**  
    - Enter temperature, thickness, and properties  
    - Adjust target angle  
    - Click **Run Simulation**  
    - View predicted force & optimal temperature  
    """)

    st.markdown("---")

    # ---- TROUBLESHOOT ----
    st.markdown("### 🛠 Troubleshooting")

    t1, t2 = st.columns(2)

    with t1:
        st.warning("""
        - Dashboard not updating → Check data sender  
        - No data visible → Ensure Firestore is running  
        """)

    with t2:
        st.warning("""
        - Camera not working → Check permissions  
        - UI stuck → Refresh the page  
        """)

    st.markdown("---")

    # ---- SUPPORT ----
    st.markdown("### 📞 Need Help?")

    st.info("""
    📧 Email: adi.sarkar2004@gmail.com  
    📱 Phone: +91 8989028700  
    """)

    st.success("✅ You're all set to explore Automorphic!")