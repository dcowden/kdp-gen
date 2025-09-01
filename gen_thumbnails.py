# Path to save thumbnails
import os
import fitz  # pip install PyMuPDF

# Path containing PDFs
pdf_folder = r"C:\Users\davec\gitwork\kdp-gen\output"
# Path to save thumbnails
thumb_folder = os.path.join(pdf_folder, "thumbnails")
os.makedirs(thumb_folder, exist_ok=True)

# Loop over all PDF files in the folder
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, filename)
        print(f"Processing {filename}...")

        # Open PDF
        doc = fitz.open(pdf_path)
        if len(doc) > 0:
            page = doc[0]  # first page
            # Create thumbnail by scaling down
            zoom = 0.4  # 20% of original size
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            thumb_path = os.path.join(thumb_folder, os.path.splitext(filename)[0] + ".png")
            pix.save(thumb_path)
            print(f"Saved thumbnail: {thumb_path}")

print("Done!")

