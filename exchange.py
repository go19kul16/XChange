import streamlit as st
import random
import string

# Function to generate a random 4-digit PIN
def generate_pin():
    return ''.join(random.choices(string.digits, k=4))

# Function to simulate sending a text or file
def send_file_or_text():
    choice = st.radio("Choose to send a file or text", ("File", "Text"))
    pin = generate_pin()  # Generate PIN before storing any content

    if choice == "Text":
        text_to_send = st.text_area("Enter the text you want to send:")
        if text_to_send:
            st.write(f"Your PIN is: {pin}")
            return pin, text_to_send
        else:
            return pin, None  # Return None for content if no text is provided
    elif choice == "File":
        uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "jpg", "png", "docx"])
        if uploaded_file is not None:
            st.write(f"Your PIN is: {pin}")
            return pin, uploaded_file
        else:
            return pin, None  # Return None for content if no file is uploaded

# Function to simulate receiving a text or file using the PIN
def receive_content(stored_pin, stored_content):
    pin_entered = st.text_input("Enter the PIN:")
    
    if pin_entered:
        if pin_entered == stored_pin:
            st.write("PIN Verified Successfully!")
            if isinstance(stored_content, str):  # If it's a text
                st.write("Text received:")
                st.write(stored_content)
            elif stored_content is not None:  # If it's a file
                st.write("File received:")
                st.download_button("Download the file", stored_content, file_name="received_file")
        else:
            st.error("Incorrect PIN. Please try again.")

# Main Streamlit UI
st.title("Secure File/Text Transfer App")

mode = st.radio("Choose mode", ("Send", "Receive"))

if mode == "Send":
    pin, stored_content = send_file_or_text()
    stored_pin = pin  # Store pin and content temporarily for this session (in production, store in a secure DB)

elif mode == "Receive":
    if 'stored_pin' in locals() and 'stored_content' in locals():  # Ensure these variables are available
        receive_content(stored_pin, stored_content)
    else:
        st.warning("No content is available to receive. Please first send content using the 'Send' mode.")
