import streamlit as st
import llm_engine

st.set_page_config(page_title="AI Debate Partner", page_icon="🗣️", layout="wide")

# --- Initial State Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "assessment_profile" not in st.session_state:
    st.session_state.assessment_profile = "No profile established yet."
if "topic" not in st.session_state:
    st.session_state.topic = "Is artificial intelligence a net positive for humanity?"
if "persona" not in st.session_state:
    st.session_state.persona = "Opponent"

# --- Sidebar Configuration ---
with st.sidebar:
    st.title("Debate Settings")
    
    new_topic = st.text_input("Debate Topic:", value=st.session_state.topic)
    new_persona = st.selectbox("Persona:", ["Opponent", "Coach"], index=0 if st.session_state.persona == "Opponent" else 1)
    
    # Reset chat if topic or persona changes significantly
    if new_topic != st.session_state.topic or new_persona != st.session_state.persona:
        if st.button("Apply & Reset Debate"):
            st.session_state.topic = new_topic
            st.session_state.persona = new_persona
            st.session_state.messages = []
            st.session_state.assessment_profile = "No profile established yet."
            st.rerun()
            
    st.divider()
    st.subheader("Your Hidden Profile")
    st.caption("The AI continuously assesses your logic and knowledge depth to adapt its responses.")
    with st.expander("View Current Assessment"):
        st.write(st.session_state.assessment_profile)
        
    st.divider()
    st.warning("Note: You need a `.env` file with `GEMINI_API_KEY` to run this app.")

# --- Main Interface ---
st.title("🗣️ AI Debate Partner")

# Display welcome message if empty
if not st.session_state.messages:
    if st.session_state.persona == "Opponent":
        st.info(f"**Opponent Mode:** Defend your position on '{st.session_state.topic}'. I will challenge your arguments and find logical flaws. Start by stating your opening argument.")
    else:
        st.info(f"**Coach Mode:** Let's build a strong argument for '{st.session_state.topic}'. State your current thoughts, and I will help you refine them.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Enter your argument here..."):
    # 1. Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Silently update assessment profile
    with st.spinner("Analyzing your argument..."):
        new_profile = llm_engine.generate_assessment(
            st.session_state.assessment_profile, 
            prompt
        )
        st.session_state.assessment_profile = new_profile

    # 3. Generate and display response
    with st.chat_message("assistant"):
        with st.spinner("Formulating response..."):
            response_text = llm_engine.generate_debate_response(
                persona=st.session_state.persona,
                topic=st.session_state.topic,
                assessment_profile=st.session_state.assessment_profile,
                chat_history=st.session_state.messages[:-1], # Exclude the latest user message from history
                latest_input=prompt
            )
            st.markdown(response_text)
            
    # Add response to state
    st.session_state.messages.append({"role": "assistant", "content": response_text})
