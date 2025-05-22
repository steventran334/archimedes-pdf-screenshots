import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import matplotlib.pyplot as plt

st.title("PDF Graph and Table Screenshot Tool")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file is not None:
    # Extract filename (without .pdf)
    filename_base = uploaded_file.name.rsplit(".", 1)[0]

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
        table_box = (339, 1185, 1367, 1770)

        graph_img = img.crop(graph_box)
        table_img = img.crop(table_box)

        def image_to_svg(pil_img):
            buf = io.BytesIO()
            fig, ax = plt.subplots()
            ax.imshow(pil_img)
            ax.axis("off")
            fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0)
            plt.close(fig)
            return buf

        # Display and download graph
        st.image(graph_img, caption="Graph Screenshot")
        buf_graph_svg = image_to_svg(graph_img)
        st.download_button(
            label="Download Graph Screenshot",
            data=buf_graph_svg.getvalue(),
            file_name=f"{filename_base}_graph.svg",
            mime="image/svg+xml"
        )

        # Display and download table
        st.image(table_img, caption="Table Screenshot")
        buf_table_svg = image_to_svg(table_img)
        st.download_button(
            label="Download Table Screenshot",
            data=buf_table_svg.getvalue(),
            file_name=f"{filename_base}_table.svg",
            mime="image/svg+xml"
        )
    else:
        st.warning("Your PDF has less than 2 pages.")
