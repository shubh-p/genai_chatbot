import streamlit as st
from core.chatbot_core_gemini import generate_response

# Streamlit app
st.title("GitLab Handbook Chatbot")

# Initialize `history` in `st.session_state` if it doesn't exist
if 'history' not in st.session_state:
    st.session_state.history = []

user_query = st.text_input("Ask a question about GitLab:")
if st.button("Submit"):
    if user_query:
        # Generate response and store the interaction in session state
        response = generate_response(user_query)
        st.session_state.history.append({"user": user_query, "response": response})
        
        # Display chat history
        for interaction in st.session_state.history:
            st.write(f"**You:** {interaction['user']}")
            st.write(f"**Bot:** {interaction['response']}")
    else:
        st.write("Please enter a question.")
