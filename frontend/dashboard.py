import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

def show_dashboard():
    # ====================== HEADER ======================
    st.markdown(
        """
        <h1 style='text-align:center; color:#1E3A8A; margin-bottom:0.5rem;'>
            📊 Factory Intelligence Dashboard
        </h1>
        <p style='text-align:center; color:#64748b; font-size:1.1rem;'>
            Real-time insights into your industrial knowledge base
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ====================== KPI METRICS ======================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📄 Documents",
            value="248",
            delta="+42 this week",
            delta_color="normal"
        )

    with col2:
        st.metric(
            label="📑 Pages Processed",
            value="8,742",
            delta="+1,203",
            delta_color="normal"
        )

    with col3:
        st.metric(
            label="💬 AI Queries",
            value="1,394",
            delta="+187 today",
            delta_color="normal"
        )

    with col4:
        st.metric(
            label="🧠 Knowledge Nodes",
            value="12,459",
            delta="+892",
            delta_color="normal"
        )

    st.divider()

    # ====================== HEALTH & ALERTS ======================
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.success(
            """
            **✅ Compliance Score**  
            **95.8%**  
            *Excellent*
            """
        )
    
    with c2:
        st.warning(
            """
            **⚠️ Active Alerts**  
            **4**  
            Maintenance Required
            """
        )
    
    with c3:
        st.error(
            """
            **🚨 Critical Issues**  
            **1**  
            Immediate Action Needed
            """
        )

    st.divider()

    # ====================== CHARTS ======================
    tab1, tab2, tab3 = st.tabs(["📈 Activity Trend", "📊 Document Types", "🔄 Processing Status"])

    with tab1:
        # Mock activity trend
        dates = pd.date_range(end=datetime.now(), periods=7)
        activity = [45, 67, 82, 54, 91, 73, 88]
        
        fig = px.line(
            x=dates, y=activity,
            markers=True,
            title="Daily AI Queries & Document Activity",
            labels={"x": "Date", "y": "Activity Count"}
        )
        fig.update_layout(height=380)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        doc_types = pd.DataFrame({
            "Type": ["PDF Manuals", "SOPs", "Inspection Reports", "Safety Docs", "Drawings"],
            "Count": [87, 64, 42, 31, 24]
        })
        fig2 = px.pie(doc_types, names="Type", values="Count", title="Document Distribution")
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        status_data = pd.DataFrame({
            "Status": ["Processed", "Processing", "Pending"],
            "Documents": [214, 18, 16]
        })
        st.bar_chart(status_data.set_index("Status"), use_container_width=True)

    st.divider()

    # ====================== RECENT DOCUMENTS ======================
    st.subheader("📂 Recently Uploaded Documents")
    
    recent_docs = pd.DataFrame({
        "Document Name": [
            "Pump_Maintenance_Manual_v2.pdf",
            "Boiler_Safety_Protocol_2026.pdf",
            "Compressor_Inspection_Report_Q2.pdf",
            "Valve_Assembly_Guidelines.pdf"
        ],
        "Status": ["✅ Processed", "✅ Processed", "⏳ Processing", "✅ Processed"],
        "Pages": [142, 89, 67, 54],
        "Uploaded": ["2 hours ago", "Yesterday", "Today", "3 days ago"]
    })
    
    st.dataframe(
        recent_docs,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.TextColumn("Status"),
            "Uploaded": st.column_config.TextColumn("Uploaded")
        }
    )

    st.divider()

    # ====================== QUICK ACTIONS ======================
    st.subheader("🚀 Quick Actions")
    
    ca1, ca2, ca3, ca4 = st.columns(4)
    
    with ca1:
        if st.button("📤 Upload New Documents", use_container_width=True, type="primary"):
            st.switch_page("frontend/upload.py")
    
    with ca2:
        if st.button("💬 Ask AI Assistant", use_container_width=True):
            st.switch_page("frontend/chat.py")
    
    with ca3:
        if st.button("🕸 Explore Knowledge Graph", use_container_width=True):
            st.switch_page("frontend/graph.py")
    
    with ca4:
        if st.button("📋 Generate Report", use_container_width=True):
            st.success("📄 Report generation started... (Demo)")

    st.divider()

    # Footer
    st.markdown(
        f"""
        <div style='text-align:center; color:#64748b; font-size:0.9rem;'>
            FactoryBrain AI • Live Dashboard • Last updated: 
            {datetime.now().strftime('%d %b %Y, %I:%M %p')}
        </div>
        """,
        unsafe_allow_html=True
    )
