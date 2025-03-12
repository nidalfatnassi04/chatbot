import streamlit as st
import pandas as pd
from openai import OpenAI


data = {
        "sku": ["12345", "67890", "11223", "44556", "78901"],
        "description": [
            "Product A - High quality",
            "Product B - Best seller",
            "Product C - New arrival",
            "Product D - Limited edition",
            "Product E - Discounted"
        ]
    }

# Define your OpenAI API key (you should keep this private).
openai_api_key = "your-openai-api-key"  # Replace with your actual API key
client = OpenAI(api_key=openai_api_key)

# Create a session state variable to store the chat messages.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add a page selection dropdown (or radio buttons).
page = st.selectbox("Select a Page", ["Home", "Chatbot", "Visualizza dati"])

# Home Page
if page == "Home":
    st.title("Welcome to My Streamlit App")
    st.write("This app has multiple pages. Use the dropdown above to navigate.")
    
# Chatbot Page
elif page == "Chatbot":
    # Show title and description for Chatbot page.
    st.title("💬 Chatbot")
    st.write(
        "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
        "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
    )
    
    # Display existing chat messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Create chat input field for user to enter a message.
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate a response using OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream=True,
        )

        # Stream the response to the chat.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

# About Page
elif page == "Visualizza dati":
    st.title("Qui potrai visulizzare i tuoi dati in tabella")
    
 
    # Create a DataFrame
    df = pd.DataFrame(data)

    # Display the dataframe with specific columns
    st.dataframe(df[["sku", "description"]])

