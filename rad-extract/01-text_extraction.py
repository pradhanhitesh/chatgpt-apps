# Import required packages
import glob
import PyPDF2
import pandas as pd

# Define the path where all the .pdf files are stored
path = "/path/to/your/pdf/files/*.pdf"  # Update with the correct path and wildcard

# List all the pdf files in the specified path
pdf_lists = sorted(glob.glob(path))

# Create an empty list to store extracted data (File_ID and texts)
data = []

# Iterate over each PDF file to extract subject ID, impression, and Fazekas score
for i in range(len(pdf_lists)):
    # Extract subject ID from the PDF file name
    sub_id = pdf_lists[i].split('\\')[-1].split('.pdf')[0]
    
    # Open the PDF file in read-binary mode
    pdfFileObj = open(pdf_lists[i], 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    
    # Read the first page of the PDF (assuming information is on the first page)
    pageObj = pdfReader.pages[0]
    page = pageObj.extract_text()  # Extract text from the PDF page
    
    # Clean up the extracted text (remove extra newline characters)
    page = page.replace('\n \n', ', ').replace('\n', '')
    
    # Custom extraction logic for the specific document structure
    # Extracting the "IMPRESSION" and Fazekas score based on the structure of the document
    # This part is specific to your documents and may need to be adjusted for other files
    
    impression = page[page.find("IMPRESSION"):page.find("DR M L")].replace("R E", "RE").replace("  ,  ", "").replace("ION", "ION:")
    fazekas_score = page[page.find("FAZ"):page.find("FAZ") + 11]  # Extract Fazekas score (11 characters after "FAZ")
    
    # Handle cases where "IMPRESSION" or Fazekas score is not found
    if len(impression) == 0:
        # If the regular impression extraction fails, attempt an alternative approach
        impression = page[page.find("IMPR ESSION"):page.find("DR M L")].replace("R E", "RE").replace("  ,  ", "").replace("ION", "ION:")
    
    if len(fazekas_score) == 0:
        # If Fazekas score is missing, append 'NO SCORE'
        data.append([sub_id, impression, 'NO SCORE'])
    else:
        # Append the extracted subject ID, impression, and Fazekas score to the data list
        data.append([sub_id, impression, fazekas_score])
    
    # Print progress for each subject
    print(sub_id, ':DONE')

# Save the extracted data to a CSV file
destination_path = "/path/to/save/extracted_data.csv"  # Update with the correct destination path
save_data_to_csv = pd.DataFrame(data, columns=['SubID', 'Comments', 'Fazekas']).to_csv(destination_path, index=False)
