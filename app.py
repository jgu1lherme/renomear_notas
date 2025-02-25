import os
import re
import shutil
import PyPDF2
import tkinter as tk
from tkinter import filedialog

def extract_info_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

            emitente_match = re.search(r"IDENTIFICAÇÃO DO EMITENTE\s*([A-Z0-9 \-.]+)", text)
            numero_match = re.search(r"Nº\.:\s*(\d{3}\.\d{3}\.\d{3})", text)

            if emitente_match and numero_match:
                emitente = emitente_match.group(1).strip()
                numero_nota = numero_match.group(1).strip()
                return f"{numero_nota} - {emitente}.pdf"
    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {e}")
    return None

def process_pdfs(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            new_name = extract_info_from_pdf(pdf_path)
            if new_name:
                new_path = os.path.join(output_folder, new_name)
                shutil.copy(pdf_path, new_path)
                print(f"Renomeado: {filename} -> {new_name}")

def main():
    root = tk.Tk()
    root.withdraw()
    
    input_folder = filedialog.askdirectory(title="Selecione a pasta com os PDFs")
    if not input_folder:
        print("Nenhuma pasta selecionada.")
        return
    
    output_folder = filedialog.askdirectory(title="Selecione a pasta para salvar os PDFs renomeados")
    if not output_folder:
        print("Nenhuma pasta de destino selecionada.")
        return
    
    process_pdfs(input_folder, output_folder)
    print("Processo concluído!")

if __name__ == "__main__":
    main()
