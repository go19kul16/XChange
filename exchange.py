import streamlit as st
import random
import string
import os
import zipfile
import io
import pygments
from pygments import lexers
from pygments import formatters

# Set up a directory for storing content (in a production environment, you'd use a cloud service)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
            # Store the text content in a file with the PIN as the filename
            with open(os.path.join(UPLOAD_FOLDER, f"{pin}.txt"), 'w') as f:
                f.write(text_to_send)
            return pin
    elif choice == "File":
        uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "jpg", "png", "docx", "zip"])
        if uploaded_file is not None:
            st.write(f"Your PIN is: {pin}")
            
            # Check if the uploaded file is a ZIP file
            if uploaded_file.name.endswith(".zip"):
                # Extract the ZIP file's contents
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    zip_ref.extractall(os.path.join(UPLOAD_FOLDER, pin))  # Extract to a directory named with the PIN
                st.success(f"ZIP file uploaded and extracted with PIN: {pin}")
            else:
                # Save the file with the PIN as the filename for other file types
                with open(os.path.join(UPLOAD_FOLDER, f"{pin}_{uploaded_file.name}"), 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"File uploaded with PIN: {pin}")

            return pin
    return None

# Function to receive content using the PIN
def receive_content():
    pin_entered = st.text_input("Enter the PIN to receive the content:")

    if pin_entered:
        # Check if the uploaded content is a text file first
        text_file_path = os.path.join(UPLOAD_FOLDER, f"{pin_entered}.txt")
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r') as f:
                content = f.read()
            st.write("Text received:")
            st.write(content)
        else:
            # If it's a directory containing extracted ZIP contents, list them
            zip_folder_path = os.path.join(UPLOAD_FOLDER, pin_entered)
            if os.path.exists(zip_folder_path):
                st.write(f"Contents of ZIP file uploaded with PIN {pin_entered}:")
                for file_name in os.listdir(zip_folder_path):
                    st.write(f"- {file_name}")
                    file_path = os.path.join(zip_folder_path, file_name)
                    with open(file_path, 'rb') as f:
                        st.download_button(label=f"Download {file_name}", data=f, file_name=file_name)
            else:
                # If it's a regular file, allow downloading the file
                for file in os.listdir(UPLOAD_FOLDER):
                    if pin_entered in file:
                        st.write(f"File received: {file}")
                        with open(os.path.join(UPLOAD_FOLDER, file), 'rb') as f:
                            st.download_button(label="Download the file", data=f, file_name=file)
                        break
                else:
                    st.error("Incorrect PIN. Please try again.")

# New page for transferring code
def transfer_code_page():
    st.title("Transfer Code")

    code_to_send = st.text_area("Enter your code here (or upload a file):")

    if code_to_send:
        # Detect language based on the code
        try:
            # Try to automatically detect the language using pygments
            lexer = lexers.guess_lexer_for_filename("example.py", code_to_send)
            formatter = formatters.HtmlFormatter(linenos=True, full=True)
            formatted_code = pygments.highlight(code_to_send, lexer, formatter)

            st.markdown("### Your beautified code:")
            st.markdown(f"<pre>{formatted_code}</pre>", unsafe_allow_html=True)

            # Provide a button to download the beautified code as a file
            pin = generate_pin()
            with open(os.path.join(UPLOAD_FOLDER, f"{pin}_code.py"), "w") as f:
                f.write(code_to_send)
            st.download_button(label="Download Beautified Code", data=formatted_code, file_name=f"{pin}_code.html")
            st.success(f"Code formatted and saved with PIN: {pin}")
        except Exception as e:
            st.error(f"Error formatting code: {e}")

# Main Streamlit UI
st.sidebar.title("Menu")
page = st.sidebar.selectbox("Choose a page", ["Transfer Content", "Transfer Code"])

if page == "Transfer Content":
    # Create two columns: one for sending, one for receiving
    col1, col2 = st.columns(2)

    # **Sender Column (col1)**:
    with col1:
        st.header("Send Content")
        pin = send_file_or_text()
        if pin:
            st.success(f"Your PIN is: {pin}")  # Inform the user about the PIN for sending

    # **Receiver Column (col2)**:
    with col2:
        st.header("Receive Content")
        receive_content()

elif page == "Transfer Code":
    transfer_code_page()
