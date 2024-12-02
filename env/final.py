import streamlit as st
import os
from PIL import Image
import shutil
from main import encode, decode, convert_all_bin_to_jpg

def ascii_key_to_binary(key):
    return ''.join(format(ord(char), '08b') for char in key)

# Helper function to clear temporary folders
def clear_temp_folders():
    for folder in ["temp", "recovered_files", "recovered"]:
        shutil.rmtree(folder, ignore_errors=True)
        os.makedirs(folder, exist_ok=True)

# Inject CSS for styling
def inject_css():
    st.markdown("""
    <style>
        /* General Body Styling */
        body {
            background: linear-gradient(90deg, #f3f4f6, #e3e4e6);
            font-family: 'Arial', sans-serif;
        }

        /* Header Styling */
        h1 {
            color: #4a90e2;
            text-align: center;
            padding: 10px;
            border-bottom: 2px solid #4a90e2;
            margin-bottom: 20px;
        }

        /* Tabs Styling */
        .stTabs [role="tablist"] {
            border-bottom: 2px solid #4a90e2;
            margin-bottom: 10px;
        }

        /* File Uploader and Buttons */
        .stFileUploader {
            border: 2px dashed #4a90e2;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }

        button {
            background-color: #4a90e2;
            color: white;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            cursor: pointer;
        }
        
        button:hover {
            background-color: #357abd;
        }

        /* Footer */
        .footer {
            text-align: center;
            color: #888;
            font-size: 14px;
            padding: 10px;
            margin-top: 20px;
            border-top: 1px solid #ddd;
        }

        /* Rounded Containers */
        .rounded-container {
            background: white;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# Set up the Streamlit app
st.set_page_config(page_title="File to GIF Encoder/Decoder", layout="centered")
inject_css()  # Inject the CSS

st.title("HYBRID CRYPTOSYSTEM TO SECURE FILE IN GIF")

# Tabs for Encode and Decode
tab1, tab2 = st.tabs(["Encode", "Decode"])

# Encode Tab
with tab1:
    st.markdown('<div class="rounded-container">', unsafe_allow_html=True)
    st.header("Encode a File into GIF")
    uploaded_file = st.file_uploader("Upload a file to encode", type=["txt", "jpg", "png", "mp3", "bin", "m4a"])

    resolution = st.selectbox(
        "Select GIF Resolution",
        options=["4K (3840x2160)", "HD (1920x1080)"],
        index=1
    )

    res_map = {
        "4K (3840x2160)": (3840, 2160),
        "HD (1920x1080)": (1920, 1080)
    }
    res = res_map[resolution]

    key = st.text_input("Enter Vigenère Cipher Key (ASCII):", value="key")
    binary_key = ascii_key_to_binary(key)

    if st.button("Encode"):
        if uploaded_file is not None:
            clear_temp_folders()
            input_file_path = os.path.join("temp", uploaded_file.name)
            with open(input_file_path, "wb") as f:
                f.write(uploaded_file.read())
            
            st.write("Encoding in progress...")
            try:
                gif_path = encode(input_file_path, binary_key, res)
                st.success("Encoding completed!")
                st.image(gif_path, caption="Encoded GIF")
                st.download_button("Download Encoded GIF", data=open(gif_path, "rb"), file_name=os.path.basename(gif_path))
            except Exception as e:
                st.error(f"Error during encoding: {e}")
        else:
            st.warning("Please upload a file to encode.")
    st.markdown('</div>', unsafe_allow_html=True)

# Decode Tab
with tab2:
    st.markdown('<div class="rounded-container">', unsafe_allow_html=True)
    st.header("Decode a GIF into its Original File")
    uploaded_gif = st.file_uploader("Upload a GIF to decode", type=["gif"])

    key = st.text_input("Enter Vigenère Cipher Key (ASCII):", value="secret")
    binary_key = ascii_key_to_binary(key)

    if st.button("Decode"):
        if uploaded_gif is not None:
            clear_temp_folders()
            gif_path = os.path.join("temp", uploaded_gif.name)
            with open(gif_path, "wb") as f:
                f.write(uploaded_gif.read())

            st.write("Decoding in progress...")
            try:
                decode(gif_path, binary_key=binary_key)
                st.success("Decoding completed!")
                st.write("Recovered files:")

                # Display and provide download links for recovered files
                recovered_files = os.listdir("recovered_files")
                if recovered_files:
                    for recovered_file in recovered_files:
                        file_path = os.path.join("recovered_files", recovered_file)
                        if recovered_file.endswith(".jpg") or recovered_file.endswith(".png"):
                            st.image(file_path, caption=recovered_file)
                        st.download_button(
                            f"Download {recovered_file}",
                            data=open(file_path, "rb"),
                            file_name=recovered_file
                        )
                else:
                    st.warning("No recovered files found.")
            except Exception as e:
                st.error(f"Error during decoding: {e}")
        else:
            st.warning("Please upload a GIF to decode.")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">This app encodes and decodes files into GIFs using advanced cryptographic techniques.</div>', unsafe_allow_html=True)
