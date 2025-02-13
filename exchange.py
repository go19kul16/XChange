import streamlit as st
import random
import string

# Function to generate a random 4-digit PIN
def generate_pin():
    return ''.join(random.choices(string.digits, k=4))

# Function to simulate sending a text or file
def send_file_or_text():
    choice = st.radio("Choose to send a file or text", ("File", "Text"))
    
    if choice == "Text":
        text_to_send = st.text_area("Enter the text you want to send:")
        if text_to_send:
            pin = generate_pin()
            st.write(f"Your PIN is: {pin}")
            # Store text and pin (This can be stored in a temporary file or database for production)
            return pin, text_to_send
    elif choice == "File":
        uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "jpg", "png", "docx"])
        if uploaded_file is not None:
            pin = generate_pin()
            st.write(f"Your PIN is: {pin}")
            # Store file and pin (This can be saved in a temporary file or database for production)
            return pin, uploaded_file

# Function to simulate receiving a text or file using the PIN
def receive_content():
    pin_entered = st.text_input("Enter the PIN:")
    
    if pin_entered:
        # In a real application, you would check the entered PIN against stored values
        if pin_entered == stored_pin:
            st.write("PIN Verified Successfully!")
            if isinstance(stored_content, str):  # If it's a text
                st.write("Text received:")
                st.write(stored_content)
            else:  # If it's a file
                st.write("File received:")
                st.download_button("Download the file", stored_content, file_name="received_file")

# Main Streamlit UI
st.title("Secure File/Text Transfer App")

mode = st.radio("Choose mode", ("Send", "Receive"))

if mode == "Send":
    pin, stored_content = send_file_or_text()
    stored_pin = pin  # Store pin and content temporarily for this session (in production, store in a secure DB)
    
elif mode == "Receive":
    receive_content()
