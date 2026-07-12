import streamlit as st
import time
from typing import Optional

# =====================================
# Mock AI Response (Replace with real backend later)
# =====================================
def get_ai_response(question: str) -> str:
    """Mock AI response. Replace with actual RAG + LLM call."""
    responses = {
        "pump": "Pump A was last serviced on June 12, 2026. The maintenance report is available in the uploaded documents.",
        "boiler": "Safety procedures for Boiler 3 include pressure testing every 6 months and annual certification.",
        "compressor": "Standard maintenance for Compressor X involves oil change, filter replacement, and vibration analysis.",
    }
    
    lower_q = question.lower()
    
    if any(word in lower_q for word in ["pump", "a"]):
        answer = responses["pump"]
    elif "boiler" in lower_q:
        answer = responses["boiler"]
    elif "compressor" in lower_q:
        answer = responses["compressor"]
    else:
        answer = (
            f"Based on your uploaded documents, here's what I found regarding **{question}**.\n\n"
            "This is a simulated response. When fully connected to the backend, "
            "FactoryBrain AI will retrieve relevant document chunks and provide "
            "citation-backed answers."
        )
    
    return answer


def show_chat():
    st.header("💬 AI Industrial Assistant")
    st.caption("Ask questions about your uploaded factory documents")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    prompt = st.chat_input("Ask about maintenance, safety, procedures, or equipment...")

    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching knowledge base..."):
                time.sleep(1.2)  # Simulate retrieval time
                
                response = get_ai_response(prompt)
                
                # Simulate typing effect
                message_placeholder = st.empty()
                full_response = ""
                
                for chunk in response.split():
                    full_response += chunk + " "
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.03)
                
                message_placeholder.markdown(response)

        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})

    st.divider()

    # Sidebar / Helper Section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        with st.expander("💡 Example Questions", expanded=False):
            examples = [
                "When was Pump A last serviced?",
                "Show safety procedures for Boiler 3",
                "What are the maintenance steps for Compressor X?",
                "Find inspection reports mentioning leakage",
                "What is the torque specification for Valve V12?",
            ]
            for ex in examples:
                st.markdown(f"• `{ex}`")

    with col2:
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # Footer info
    st.caption(
        "FactoryBrain AI • Responses are generated from your uploaded documents • "
        "Citations will be added after backend integration"
    )