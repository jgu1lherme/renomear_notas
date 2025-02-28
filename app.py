import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog
import PyPDF2


def extract_info_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = "\n".join(
                page.extract_text() for page in reader.pages if page.extract_text()
            )

            emitente_match = re.search(
                r"IDENTIFICAÇÃO DO EMITENTE\s*([\wÀ-ÿ\-.,& ]+)", text, re.MULTILINE
            )
            numero_match = re.search(r"Nº\.:\s*(\d{3}\.\d{3}\.\d{3})", text)

            if emitente_match and numero_match:
                emitente = emitente_match.group(1).strip()
                numero_nota = numero_match.group(1).strip()
                return f"{numero_nota} - {emitente}.pdf"
    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {e}")
    return None


def process_selected_pdfs(pdf_files, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for pdf_path in pdf_files:
        new_name = extract_info_from_pdf(pdf_path)

        if new_name:
            new_path = os.path.join(output_folder, new_name)

            if os.path.abspath(pdf_path) != os.path.abspath(new_path):
                shutil.copy(pdf_path, new_path)
                print(f"Renomeado: {os.path.basename(pdf_path)} -> {new_name}")
            else:
                print(f"O arquivo '{new_name}' já está no destino e não foi copiado.")


def main():
    root = tk.Tk()
    root.withdraw()

    pdf_files = filedialog.askopenfilenames(
        title="Selecione os PDFs para renomear", filetypes=[("Arquivos PDF", "*.pdf")]
    )

    if not pdf_files:
        print("Nenhum arquivo selecionado.")
        return

    output_folder = filedialog.askdirectory(
        title="Selecione a pasta para salvar os PDFs renomeados"
    )
    if not output_folder:
        print("Nenhuma pasta de destino selecionada.")
        return

    process_selected_pdfs(pdf_files, output_folder)
    print("Processo concluído!")


if __name__ == "__main__":
    main()
