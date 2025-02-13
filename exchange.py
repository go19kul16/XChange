import streamlit as st
import random
import string

# This dictionary will store content temporarily (in a real-world scenario, you'd use a database or file system)
storage = {}

# Function to generate a random 4-digit PIN
def generate_pin():
    return ''.join(random.choices(string.digits, k=4))

# Function to send text or file
def send_file_or_text():
    choice = st.radio("Choose to send a file or text", ("File", "Text"))
    pin = generate_pin()  # Generate PIN before storing any content

    if choice == "Text":
        text_to_send = st.text_area("Enter the text you want to send:")
        if text_to_send:
            st.write(f"Your PIN is: {pin}")
            # Store the text content in storage with the PIN as key
            storage[pin] = text_to_send
            return pin
    elif choice == "File":
        uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "jpg", "png", "docx"])
        if uploaded_file is not None:
            st.write(f"Your PIN is: {pin}")
            # Store the file content in storage with the PIN as key
            storage[pin] = uploaded_file
            return pin
    return None

# Function to receive content using the PIN
def receive_content():
    pin_entered = st.text_input("Enter the PIN to receive the content:")
    
    if pin_entered:
        if pin_entered in storage:
            st.write("PIN Verified Successfully!")
            content = storage[pin_entered]
            # Check if the content is text or file
            if isinstance(content, str):  # If it's text
                st.write("Text received:")
                st.write(content)
            else:  # If it's a file
                st.write("File received:")
                st.download_button("Download the file", content, file_name="received_file")
        else:
            st.error("Incorrect PIN. Please try again.")

# Main Streamlit UI
st.title("Secure File/Text Transfer App")

mode = st.radio("Choose mode", ("Send", "Receive"))

if mode == "Send":
    pin = send_file_or_text()
    if pin:
        st.success(f"Your PIN is: {pin}")  # Inform the user about the PIN for sending

elif mode == "Receive":
    receive_content()

