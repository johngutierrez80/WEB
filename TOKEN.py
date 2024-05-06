import mysql.connector
from tkinter import *
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime
import xlsxwriter
import random
import string
import pandas as pd
import os

import mysql.connector

def conectarBaseDeDatos():
    # Detalles de conexión
    config = {
        'host': 'localhost',
        'user': 'root',  # Nombre de usuario de la base de datos
        'password': '',  # Contraseña de la base de datos
        'database': 'Sdh',  # Nombre de la base de datos
        'charset': 'utf8'
    }

    # Crear conexión
    conn = mysql.connector.connect(**config)

    return conn

def insertarArchivo(conn, nombre_archivo, ruta_archivo, token):
    cursor = conn.cursor()
    sql = "INSERT INTO Archivos (NombreArchivo, RutaArchivo, TokenUnico) VALUES (%s, %s, %s)"
    val = (nombre_archivo, ruta_archivo, token)
    cursor.execute(sql, val)
    conn.commit()
    cursor.close()

def generar_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def generar_numero_seguridad():
    fecha_actual = datetime.datetime.now()
    fecha_formateada = fecha_actual.strftime("%Y%m%d%H%M%S")
    return fecha_formateada

def agregar_marca_agua(can, texto):
    can.setFont("Helvetica", 10)
    #can.setFillAlpha(0.3)
    can.setFillColorRGB(0, 0, 0)
    text_width = can.stringWidth(texto)
    text_height = 10
    page_width, page_height = can._pagesize
    x = (page_width - text_width) / 2
    y = text_height
    can.drawString(x, y, texto)

def agregar_numero_seguridad(pdf_entrada, pdf_salida, token):
    pdf_reader = PdfReader(pdf_entrada)
    pdf_writer = PdfWriter()
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        packet = BytesIO()
        can = canvas.Canvas(packet)
        texto = f"{token}"
        agregar_marca_agua(can, texto)
        can.save()
        packet.seek(0)
        watermark_pdf = PdfReader(packet)
        page.merge_page(watermark_pdf.pages[0])
        pdf_writer.add_page(page)
    with open(pdf_salida, 'wb') as output_file:
        pdf_writer.write(output_file)

def agregar_numero_seguridad_a_directorio(conn, directorio_entrada, directorio_salida, numero_seguridad):
    archivos_info = []
    archivos_ordenados = sorted(os.listdir(directorio_entrada))
    for filename in archivos_ordenados:
        pdf_entrada = os.path.join(directorio_entrada, filename)
        if os.path.isfile(pdf_entrada) and filename.lower().endswith(".pdf"):
            token = generar_token()
            ultimo_guion = filename.rfind("_")
            if ultimo_guion != -1:
                consecutivo = filename[ultimo_guion + 1:filename.find(".", ultimo_guion)]
                nombre_salida = os.path.splitext(filename)[0] + '.pdf'
                pdf_salida = os.path.join(directorio_salida, nombre_salida)
                agregar_numero_seguridad(pdf_entrada, pdf_salida, token)
                insertarArchivo(conn, filename, pdf_salida.replace("/", "\\"), token)
                archivo_info = {
                    'Nombre de Archivo': filename,
                    'Ruta del Archivo': pdf_salida.replace("/", "\\"),
                    'Token Único': token,
                }
                archivos_info.append(archivo_info)
            else:
                print(f"No se encontró el guión bajo en el nombre del archivo: {filename}")

    df = pd.DataFrame(archivos_info)
    excel_file = os.path.join(directorio_salida, 'tokens.xlsx')
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        for idx, link in enumerate(df['Ruta del Archivo'], start=2):
            worksheet.write_url(f'E{idx}', link, string='Abrir')

    print(f"Se han generado y almacenado los tokens únicos en '{excel_file}'.")

def seleccionar_directorio_entrada():
    directorio_entrada = filedialog.askdirectory()
    if directorio_entrada:
        entry_directorio_entrada.delete(0, END)
        entry_directorio_entrada.insert(0, directorio_entrada)

def seleccionar_directorio_salida():
    directorio_salida = filedialog.askdirectory()
    if directorio_salida:
        entry_directorio_salida.delete(0, END)
        entry_directorio_salida.insert(0, directorio_salida)

def ejecutar_programa():
    directorio_entrada = entry_directorio_entrada.get()
    directorio_salida = entry_directorio_salida.get()
    numero_seguridad = generar_numero_seguridad()
    if directorio_entrada and directorio_salida:
        conn = conectarBaseDeDatos()
        agregar_numero_seguridad_a_directorio(conn, directorio_entrada, directorio_salida, numero_seguridad)
        conn.close()
    else:
        print("Por favor, complete todos los campos.")

root = Tk()
root.title("Agregar Número de Seguridad a Archivos PDF")

label_directorio_entrada = Label(root, text="Directorio de Entrada:")
label_directorio_entrada.grid(row=0, column=0, sticky=W, padx=5, pady=5)
entry_directorio_entrada = Entry(root, width=50)
entry_directorio_entrada.grid(row=0, column=1, padx=5, pady=5)
button_seleccionar_entrada = Button(root, text="Seleccionar", command=seleccionar_directorio_entrada)
button_seleccionar_entrada.grid(row=0, column=2, padx=5, pady=5)

label_directorio_salida = Label(root, text="Directorio de Salida:")
label_directorio_salida.grid(row=1, column=0, sticky=W, padx=5, pady=5)
entry_directorio_salida = Entry(root, width=50)
entry_directorio_salida.grid(row=1, column=1, padx=5, pady=5)
button_seleccionar_salida = Button(root, text="Seleccionar", command=seleccionar_directorio_salida)
button_seleccionar_salida.grid(row=1, column=2, padx=5, pady=5)

button_ejecutar = Button(root, text="Ejecutar", command=ejecutar_programa)
button_ejecutar.grid(row=3, column=1, pady=10)

root.mainloop()