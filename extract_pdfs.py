import glob
import PyPDF2
import os

pdf_files = glob.glob('*.pdf')
for f in pdf_files:
    try:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + '\n'
        
        out_name = f.replace('.pdf', '.txt').replace('^M', '').replace('\r', '')
        with open(out_name, 'w', encoding='utf-8') as out_f:
            out_f.write(text)
        print(f"Extracted {f} to {out_name}")
    except Exception as e:
        print(f"Failed to extract {f}: {e}")
