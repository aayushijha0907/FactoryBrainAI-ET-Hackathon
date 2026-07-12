import os
import streamlit as st

# ==========================
# Configuration
# ==========================
UPLOAD_FOLDER = "uploads"
SUPPORTED_FILE_TYPES = ["pdf", "txt", "docx"]
MAX_FILE_SIZE_MB = 25


def create_upload_folder():
    """Create upload folder if it doesn't exist."""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_uploaded_file(uploaded_file):
    """Save uploaded file and return filepath."""
    filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filepath


def show_upload():
    st.header("📤 Document Upload & Processing")
    st.markdown(
        """
        Upload your industrial documents to build a powerful AI knowledge base.  
        Supported formats include **PDFs, DOCX, and TXT** files.
        """
    )

    st.divider()

    # File Uploader
    uploaded_files = st.file_uploader(
        "Drag and drop or browse your documents",
        type=SUPPORTED_FILE_TYPES,
        accept_multiple_files=True,
        help=f"Maximum file size: {MAX_FILE_SIZE_MB} MB per file",
    )

    if uploaded_files:
        st.subheader("📋 Selected Files")

        total_size = sum(file.size for file in uploaded_files) / (1024 * 1024)
        valid_files = []
        invalid_files = []

        # Display file details
        for file in uploaded_files:
            size_mb = file.size / (1024 * 1024)
            if size_mb > MAX_FILE_SIZE_MB:
                invalid_files.append(file)
                st.error(f"❌ **{file.name}** — File too large ({size_mb:.2f} MB)")
            else:
                valid_files.append(file)
                st.success(
                    f"✅ **{file.name}**  \n"
                    f"Size: `{size_mb:.2f} MB`"
                )

        # Summary
        st.info(f"**{len(valid_files)}** valid file(s) selected | Total size: `{total_size:.2f} MB`")

        if invalid_files:
            st.warning("Some files exceed the size limit and will not be processed.")

        # Process Button
        if valid_files and st.button(
            "🚀 Process & Store Documents",
            type="primary",
            use_container_width=True,
        ):
            create_upload_folder()
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            saved_files = []

            for i, file in enumerate(valid_files):
                status_text.info(f"Processing **{file.name}**... ({i+1}/{len(valid_files)})")
                
                try:
                    filepath = save_uploaded_file(file)
                    saved_files.append(filepath)
                except Exception as e:
                    st.error(f"Failed to save {file.name}: {e}")

                # Update progress
                progress_bar.progress((i + 1) / len(valid_files))
                # Small delay for better UX (optional)
                # time.sleep(0.3)

            progress_bar.progress(100)
            status_text.success("✅ All documents uploaded successfully!")

            # Final Success Message
            st.success(f"**{len(saved_files)} document(s)** have been successfully uploaded and are ready for processing.")

            # Show saved paths (collapsible)
            with st.expander("📂 View Saved File Paths", expanded=False):
                for path in saved_files:
                    st.code(path, language="text")

            st.divider()

            st.info(
                """
                **Next Steps:**
                1. Documents are parsed (text extraction + OCR if needed)  
                2. Text is chunked and embedded  
                3. Stored in ChromaDB vector database  
                4. Ready to query in **AI Chat**
                """
            )

            # Optional: Button to go to chat
            if st.button("💬 Go to AI Chat", use_container_width=True):
                st.switch_page("frontend/chat.py")  # Adjust path if needed

    else:
        st.info("👆 Upload documents to begin building your industrial knowledge base.")

    st.divider()

    # Guidelines
    st.subheader("📌 Upload Guidelines")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            - Maximum **25 MB** per file  
            - Multiple files supported  
            - Preferred: Clear, text-based PDFs
            """
        )
    with col2:
        st.markdown(
            """
            - Scanned documents will use OCR  
            - DOCX and TXT also supported  
            - Keep file names descriptive
            """
        )

    st.caption("💡 Tip: High-quality PDFs with selectable text give the best results.")