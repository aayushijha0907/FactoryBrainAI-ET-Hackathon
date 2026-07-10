import streamlit as st
import time

def show_home():
    # ====================== HERO SECTION ======================
    st.markdown(
        """
        <div style='text-align:center; padding: 2.5rem 1rem;'>
            <h1 style='color:#1E3A8A; font-size: 3.2rem; margin-bottom: 0.5rem; animation: fadeIn 1.5s;'>
                🏭 FactoryBrain AI
            </h1>
            <h3 style='color:#475569; margin-bottom: 1.2rem;'>
                AI-Powered Industrial Knowledge Intelligence
            </h3>
            <p style='font-size: 1.15rem; color:#64748b; max-width: 850px; margin: 0 auto;'>
                Transform scattered industrial documents into intelligent, 
                searchable, and actionable knowledge.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ====================== OVERVIEW ======================
    st.header("📖 Overview")
    st.markdown(
        """
        **FactoryBrain AI** centralizes your industrial knowledge — maintenance manuals, 
        SOPs, inspection reports, engineering drawings, and safety documents — into one 
        powerful intelligent platform.
        """
    )

    st.divider()

    # ====================== KEY FEATURES (with animation) ======================
    st.header("🚀 Key Features")
    
    features = [
        ("🤖", "AI Assistant", "Chat naturally with your entire document base"),
        ("📄", "Smart Document Processing", "Extract text, tables & insights from PDFs"),
        ("🔍", "Semantic Search", "Find information using meaning, not keywords"),
        ("🧠", "Knowledge Graph", "Visualize relationships between assets & documents"),
        ("🛠", "Maintenance Insights", "Detect recurring failures & root causes"),
        ("✅", "Compliance Analysis", "Identify regulatory and safety gaps"),
    ]

    cols = st.columns(3)
    for i, (emoji, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style='padding: 1.2rem; background:#f8fafc; border-radius: 12px; 
                            border-left: 5px solid #1E3A8A; margin-bottom: 1rem;
                            animation: fadeIn 0.8s ease {i*0.1}s both;'>
                    <h3 style='margin:0 0 0.5rem 0;'>{emoji} {title}</h3>
                    <p style='color:#475569; margin:0;'>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # ====================== HOW IT WORKS ======================
    st.header("⚙️ How It Works")
    
    steps = [
        ("1️⃣ Upload Documents", "PDFs, manuals, reports, drawings"),
        ("2️⃣ AI Processing", "Parsing, OCR, chunking & embedding"),
        ("3️⃣ Knowledge Storage", "Vector + Graph Database"),
        ("4️⃣ Intelligent Chat", "Ask questions → Get cited answers"),
    ]

    cols = st.columns(4)
    for i, (title, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(
                f"""
                <div style='text-align:center; padding:1.2rem; background:#f1f5f9; 
                            border-radius:12px; height:100%; animation: fadeIn 1s ease {i*0.15}s both;'>
                    <h2 style='margin:0; color:#1E3A8A;'>{title.split()[0]}</h2>
                    <strong>{title.split(' ', 1)[1]}</strong><br>
                    <small style='color:#64748b;'>{desc}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # ====================== METRICS ======================
    st.header("📈 Platform Snapshot")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Documents Processed", "248", "↑42")
    with col2:
        st.metric("Questions Answered", "1,394", "↑18%")
    with col3:
        st.metric("Knowledge Nodes", "8,742", "↑203")
    with col4:
        st.metric("Compliance Score", "94%", "↑3%")

    st.divider()

    # ====================== CALL TO ACTION ======================
    st.header("🚀 Get Started Today")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📤 Upload Documents", type="primary", use_container_width=True, key="upload_btn"):
            st.switch_page("pages/2_Upload_Documents.py")   # Adjust path as needed
    with c2:
        if st.button("💬 Start AI Chat", use_container_width=True, key="chat_btn"):
            st.switch_page("pages/3_AI_Chat.py")

    st.success("**Your factory's knowledge, now supercharged with AI.**")