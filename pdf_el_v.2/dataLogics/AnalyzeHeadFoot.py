import fitz  

def AnalyzeHeadFooter(pdf_path):

    def extract_header_footer(pdf_path):
        doc = fitz.open(pdf_path)
        header_footer_text = []

        for page_number in range(len(doc)):
            page = doc.load_page(page_number)
            page_text = page.get_text()
            header_text = ""
            footer_text = ""
            page_height = page.rect.height
            page_width = page.rect.width 

            header_height = page_height * 0.1  
            footer_height = page_height * 0.1 

            header_text = page.get_text("text", clip=(0, 0, page_width, header_height))
            footer_text = page.get_text("text", clip=(0, page_height - footer_height, page_width, page_height))

            header_footer_text.append({
                "Page Number": page_number + 1,
                "Header": header_text,
                "Footer": footer_text,
            })
            author = doc.metadata.get("author", None)

        doc.close()

        return [header_footer_text,author]

    pdf_file_path = pdf_path  

    header_footer_info = extract_header_footer(pdf_file_path)
    
    return header_footer_info

