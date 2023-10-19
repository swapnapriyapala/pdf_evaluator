

import fitz
import os



image_data_hub={}

# Output directory where images will be saved
output_dir = 'static/{username}/'
def image_analysis(pdf_path,output_dir):
    os.makedirs(output_dir, exist_ok=True)

    pdf_document = fitz.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        xrefs = page.get_images(full=True)

        for img_index, xref in enumerate(xrefs):
            image_data = pdf_document.extract_image(xref[0])  # Extract the image data

            # Get image properties from the image_data dictionary
            width = image_data['width']
            height = image_data['height']
            color_space = image_data['colorspace']
            bits_per_component = image_data['bpc']

            # Save the image to the output directory
            image_filename = os.path.join(output_dir, f'page{page_num + 1}_img{img_index + 1}.png')
            with open(image_filename, 'wb') as img_file:
                img_file.write(image_data['image'])

            image_name= f'page{page_num + 1}_img{img_index + 1}.png'  
            page_number=f'{page_num + 1}'
            image_data_hub[f'{image_name}'] = {'Image Name':image_name.upper(),'Page Number':page_number,'width': width,'Height':height,'Color Space':color_space}

    pdf_document.close()

    #print("Images have been extracted, saved, and styles printed to the output directory.")
    return image_data_hub
