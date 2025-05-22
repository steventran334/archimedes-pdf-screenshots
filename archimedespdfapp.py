import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.title("PDF Graph and Table Screenshot Tool")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    st.write(f"Number of pages: {doc.page_count}")

    if doc.page_count >= 2:
        page = doc[1]  # Page 2 (0-indexed)
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        st.subheader("Cropped Graph and Table from Page 2")

        # Final crop boxes
        graph_box = (120, 370, 1590, 1035)
        table_box = (340, 1185, 1500, 1790)

        graph_img = img.crop(graph_box)
        table_img = img.crop(table_box)

        # Show and download Graph
        st.image(graph_img, caption="Graph Screenshot")
        buf_graph = io.BytesIO()
        graph_img.save(buf_graph, format="PNG")
        st.download_button(
            label="Download Graph Screenshot",
            data=buf_graph.getvalue(),
            file_name="graph_screenshot.png",
            mime="image/png"
        )

        # Show and download Table
        st.image(table_img, caption="Table Screenshot")
        buf_table = io.BytesIO()
        table_img.save(buf_table, format="PNG")
        st.download_button(
            label="Download Table Screenshot",
            data=buf_table.getvalue(),
            file_name="table_screenshot.png",
            mime="image/png"
        )
    else:
        st.warning("Your PDF has less than 2 pages.")
