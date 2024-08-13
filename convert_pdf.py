# How to use
# 1. Install the required dependencies:
#    - Install Python packages:
#      pip install pdf2image pillow
#    - Install poppler-utils (required by pdf2image):
#      sudo apt-get install poppler-utils
# 2. Run the script:
#    - To use default settings:
#      python3 script_name.py
#    - To specify a PDF file and output folder:
#      python3 script_name.py path/to/your_pdf_file.pdf path/to/output_folder

from pdf2image import convert_from_path
import os
import sys

# Default PDF file and output folder
pdf_file = "portfolio.pdf"  # Default PDF file name
output_folder = "webpage"  # Default folder where the HTML and images will be saved

# Check for command-line arguments to override defaults
if len(sys.argv) > 1:
    pdf_file = sys.argv[1]  # First command-line argument is the PDF file
    print(f"Using provided PDF file: {pdf_file}")
else:
    print(f"No PDF file provided. Using default: {pdf_file}")

if len(sys.argv) > 2:
    output_folder = sys.argv[2]  # Second command-line argument is the output folder
    print(f"Using provided output folder: {output_folder}")
else:
    print(f"No output folder provided. Using default: {output_folder}")

# Subfolder to store the images
src_folder = os.path.join(output_folder, "src") 

# Start the conversion process
print("Starting PDF to HTML conversion...")
print(f"PDF file to convert: {pdf_file}")
print(f"Output folder: {output_folder}")

# Create the output and src folders if they don't exist
print("Creating necessary directories...")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)  # Create the output directory
    print(f"Created directory: {output_folder}")
if not os.path.exists(src_folder):
    os.makedirs(src_folder)  # Create the subdirectory for images
    print(f"Created directory: {src_folder}")

# Convert PDF to images
print("Converting PDF to images...")
try:
    # Convert each page of the PDF into an image at 300 DPI resolution
    pages = convert_from_path(pdf_file, 300)
    print(f"Successfully converted {len(pages)} pages from PDF to images.")
except Exception as e:
    # If there is an error during conversion, print the error and exit
    print(f"Error during PDF to image conversion: {e}")
    exit()

# Initialize a list to store the paths of the saved images
image_files = []
for i, page in enumerate(pages):
    # Define the filename for each image (page_1.jpg, page_2.jpg, etc.)
    image_filename = os.path.join(src_folder, f'page_{i+1}.jpg')
    try:
        # Save each page as a JPEG image in the src folder
        page.save(image_filename, 'JPEG')
        image_files.append(image_filename)
        print(f"Saved image: {image_filename}")
    except Exception as e:
        # If there is an error saving an image, print the error
        print(f"Error saving image {image_filename}: {e}")

# Begin generating the HTML file
print("Generating HTML file...")
html_content = """
<html>
<head>
<style>
    body {
        margin: 0;
        padding: 0;
        background-color: #f0f0f0;  /* Set a light background color */
    }
    img {
        display: block;
        margin: 0 auto;  /* Center images horizontally */
    }
</style>
</head>
<body>
"""

# Add each image to the HTML content
print("Adding images to the HTML content...")
for i in range(len(image_files)):
    image_file = os.path.join("src", f'page_{i+1}.jpg')
    # Add a div for each image with 100% width and a max-width of 1200px
    html_content += f'<div><img src="{image_file}" style="width:100%; max-width:1200px;"/></div>\n'
    print(f"Added image {image_file} to HTML content.")

html_content += "</body></html>"

# Define the filename for the output HTML file
html_filename = os.path.join(output_folder, "output.html")
print(f"Saving HTML file to: {html_filename}")
try:
    # Write the generated HTML content to the output file
    with open(html_filename, "w") as f:
        f.write(html_content)
    print(f"HTML file created successfully: {html_filename}")
except Exception as e:
    # If there is an error writing the HTML file, print the error
    print(f"Error writing HTML file: {e}")
