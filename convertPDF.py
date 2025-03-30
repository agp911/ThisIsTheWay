import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Button, Label, Entry
import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import shutil

def convert_to_pdf(file_path, output_directory):
    try:
        output_file = os.path.join(output_directory, "converted.pdf")
        reader = PdfReader(file_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        with open(output_file, "wb") as output:
            writer.write(output)
        return output_file
    except Exception as e:
        return f"Error: {str(e)}"

def merge_pdfs(files, output_directory):
    merger = PdfMerger()
    try:
        for file in files:
            merger.append(file)
        output_file = os.path.join(output_directory, "merged.pdf")
        merger.write(output_file)
        merger.close()
        return output_file
    except Exception as e:
        return f"Error: {str(e)}"

def create_interface():
    # Crear ventana principal
    app = tk.Tk()
    app.title("ConvertPDF")
    app.geometry("500x300")
    app.resizable(False, False)
    
    # Título
    title = Label(app, text="ConvertPDF", font=("Helvetica", 16))
    title.pack(pady=10)
    
    # Seleccionar archivo
    def select_file():
        file_path = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
        if file_path:
            entry_file_path.delete(0, tk.END)
            entry_file_path.insert(0, file_path)
    
    Label(app, text="Archivo para convertir o unificar:").pack(pady=5)
    entry_file_path = Entry(app, width=50)
    entry_file_path.pack(pady=5)
    Button(app, text="Seleccionar archivo", command=select_file).pack(pady=5)

    # Seleccionar carpeta de destino
    def select_directory():
        directory = filedialog.askdirectory()
        if directory:
            entry_directory_path.delete(0, tk.END)
            entry_directory_path.insert(0, directory)
    
    Label(app, text="Directorio de destino:").pack(pady=5)
    entry_directory_path = Entry(app, width=50)
    entry_directory_path.pack(pady=5)
    Button(app, text="Seleccionar carpeta", command=select_directory).pack(pady=5)
    
    # Botones para convertir y unificar
    def handle_convert():
        file_path = entry_file_path.get()
        directory = entry_directory_path.get()
        if not file_path or not directory:
            messagebox.showerror("Error", "Por favor selecciona un archivo y un directorio.")
            return
        
        output = convert_to_pdf(file_path, directory)
        if "Error" in output:
            messagebox.showerror("Error", output)
        else:
            messagebox.showinfo("Éxito", f"Archivo convertido: {output}")
    
    def handle_merge():
        file_paths = filedialog.askopenfilenames(filetypes=[("Archivos PDF", "*.pdf")])
        directory = entry_directory_path.get()
        if not file_paths or not directory:
            messagebox.showerror("Error", "Por favor selecciona archivos y un directorio.")
            return
        
        output = merge_pdfs(file_paths, directory)
        if "Error" in output:
            messagebox.showerror("Error", output)
        else:
            messagebox.showinfo("Éxito", f"Archivos unificados: {output}")
    
    Button(app, text="Convertir a PDF", command=handle_convert).pack(pady=5)
    Button(app, text="Unificar PDFs", command=handle_merge).pack(pady=5)
    
    # Ejecución de la aplicación
    app.mainloop()

# Lanzar interfaz
create_interface()