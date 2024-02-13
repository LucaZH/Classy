import fitz

def save_text_to_files(pdf_path, start_page, pages_per_file, types_doc,pdf_name):
    doc = fitz.open(pdf_path)
    
    for i in range(start_page - 1, doc.page_count, pages_per_file):
        text = ""
        for j in range(pages_per_file):
            if i + j < doc.page_count:
                page = doc[i + j]
                text += page.get_text()
        
        with open(f'./data/{types_doc}/{pdf_name}_{i + 1}_to_{i + pages_per_file}.txt', 'w', encoding='utf-8') as text_file:
            text_file.write(text)

    doc.close()