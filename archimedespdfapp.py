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

    # Display both pages as images
    page_images = []
    for page_num in range(doc.page_count):
        page = doc[page_num]
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        page_images.append(img)
        st.image(img, caption=f"Page {page_num+1}", use_column_width=True)

    # Crop graph and table from page 2
    if doc.page_count >= 2:
        st.subheader("Cropped Graph and Table from Page 2")

        # Use your provided coordinates
        graph_left = 33.65
        graph_top = 33.82
        graph_right = graph_left + 549.67
        graph_bottom = graph_top + 369.82
        graph_box = (graph_left, graph_top, graph_right, graph_bottom)

        table_left = 116.81
        table_top = 400.68
        table_right = table_left + 380.9
        table_bottom = table_top + 241.51
        table_box = (table_left, table_top, table_right, table_bottom)

        page2_img = page_images[1]

        graph_img = page2_img.crop(graph_box)
        table_img = page2_img.crop(table_box)

        st.image(graph_img, caption="Graph Screenshot")
        buf_graph = io.BytesIO()
        graph_img.save(buf_graph, format="PNG")
        st.download_button(
            label="Download Graph Screenshot",
            data=buf_graph.getvalue(),
            file_name="graph_screenshot.png",
            mime="image/png"
        )

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
