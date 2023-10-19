import fitz  
def AnalyzeAuthor(pdf_path):
    def extract_author(pdf_path):
        doc = fitz.open(pdf_path)

        author = doc.metadata.get("author", None)
        
        doc.close()
        
        return author


    pdf_file_path = pdf_path

    author_name = extract_author(pdf_file_path)

    if author_name:
        #print(f'Author: {author_name}')
        return author_name
    else:
        #print('Author information not found in the PDF.')
        return 'Author information not found in the PDF.'
