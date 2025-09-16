import tkinter as tk
import sqlite3
import csv
from tkinter import filedialog, messagebox, ttk, StringVar, OptionMenu

conn=sqlite3.connect(':memory:')

cur=conn.cursor()
qry='''
CREATE TABLE Book (
id INTEGER PRIMARY KEY AUTOINCREMENT,
isbn TEXT (200),
title TEXT(200),
author TEXT(200),
year INTEGER,
publisher TEXT(200)
);
'''
try:
   cur.execute(qry)
   print ('Table created successfully')
except:
   print ('error in creating table')

class Book:
    def __init__(self, isbn, titulo, autor, año, editorial):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.año = año
        self.editorial = editorial

    def show(self):
        return f"Titulo: {self.titulo}. Autor: {self.autor}"

    def __str__(self):
        return self.show()

app = tk.Tk()

def hay_datos():
    libros = cur.execute("SELECT * FROM BOOK").fetchall()
    if(len(libros) > 0):
        return True
    else:
        return False

def guardar_csv():

    if(hay_datos()):
        return messagebox.showerror("Error", "Ya hay datos cargados")

    file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
    
    list = []

    with open(file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        lector = csv.reader(csv_file, delimiter=';')
        next(lector)
        for fila in lector:
            if(fila[3].isdigit()):
                fila[3] = int(fila[3])
            else:
                fila[3] = 0    
            list.append(fila)

    insert = '''
    INSERT INTO BOOK(isbn,title,author,year,publisher) VALUES (?,?,?,?,?)
    '''

    try:
        cur.executemany(insert, list)
        print ('Datos guardados correctamente')
        conn.commit()

        total = cur.execute("SELECT COUNT(*) FROM BOOK").fetchone()[0]
        print(total)
        messagebox.showinfo("Total", f"Total de libros cargados: {total}")

    except:
        print ('error insertando datos')

def salir():
    conn.close()
    app.destroy()

def listar_completo():
    if(hay_datos() == False):
        return messagebox.showerror("Error", "No hay datos cargados")
    libros = cur.execute("SELECT * FROM BOOK").fetchall()
    ventana_libros = tk.Toplevel(app)
    ventana_libros.title("Todos los libros")
    ventana_libros.geometry("400x400")
    y_scrollbar = ttk.Scrollbar(ventana_libros, orient=tk.VERTICAL)
    x_scrollbar = ttk.Scrollbar(ventana_libros, orient=tk.HORIZONTAL)
    listbox = tk.Listbox(ventana_libros, 
                         yscrollcommand=y_scrollbar,
                         xscrollcommand=x_scrollbar,
                         width=200, height=100)
    y_scrollbar.config(command=listbox.yview)
    x_scrollbar.config(command=listbox.xview)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    listbox.pack()
    listbox.insert(tk.END, "isbn, título, autor, año")
    for libro in libros:
        listbox.insert(tk.END, f"{libro[1]},{libro[2]},{libro[3]},{libro[4]}")

def seleccion():
    if(hay_datos() == False):
        return messagebox.showerror("Error", "No hay datos cargados")
    ventana_seleccion_ordenacion = tk.Toplevel(app)
    ventana_seleccion_ordenacion.title("Que ordenación quieres seguir?")
    ventana_seleccion_ordenacion.geometry("300x300")
    opcion_seleccionada = tk.StringVar(value="year")
    r_año = tk.Radiobutton(ventana_seleccion_ordenacion, text="Año", variable=opcion_seleccionada, value="year")
    r_isbn = tk.Radiobutton(ventana_seleccion_ordenacion, text="ISBN", variable=opcion_seleccionada, value="isbn")
    r_año.pack()
    r_isbn.pack()
    print(opcion_seleccionada.get())
    ttk.Button(ventana_seleccion_ordenacion, text="Listar", command=lambda: lista_ordenada(ventana_seleccion_ordenacion, opcion_seleccionada.get())).pack()

def lista_ordenada(ventana, opcion):
    libros = cur.execute(f"SELECT * FROM BOOK ORDER BY {opcion}").fetchall()
    ventana_libros_ordenados = tk.Toplevel(ventana)
    ventana_libros_ordenados.title("Libros ordenador")
    ventana_libros_ordenados.geometry("400x400")
    y_scrollbar = ttk.Scrollbar(ventana_libros_ordenados, orient=tk.VERTICAL)
    x_scrollbar = ttk.Scrollbar(ventana_libros_ordenados, orient=tk.HORIZONTAL)
    listbox = tk.Listbox(ventana_libros_ordenados, 
                         yscrollcommand=y_scrollbar,
                         xscrollcommand=x_scrollbar,
                         width=200, height=100)
    y_scrollbar.config(command=listbox.yview)
    x_scrollbar.config(command=listbox.xview)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    listbox.pack()
    listbox.insert(tk.END, "isbn, título, autor, año")
    for libro in libros:
        listbox.insert(tk.END, f"{libro[1]},{libro[2]},{libro[3]},{libro[4]}")

def buscar_titulo():
    if(hay_datos() == False):
        return messagebox.showerror("Error", "No hay datos cargados")
    ventana_seleccion_titulo = tk.Toplevel(app)
    ventana_seleccion_titulo.title("Que palabra quieres buscar")
    ventana_seleccion_titulo.geometry("300x300")
    titulo = tk.Entry(ventana_seleccion_titulo)
    titulo.pack()
    print(titulo.get())
    ttk.Button(ventana_seleccion_titulo, text="Listar", command=lambda: filta_por_titulo(ventana_seleccion_titulo, titulo.get())).pack()

def filta_por_titulo(ventana, titulo):
    libros = cur.execute(f"SELECT * FROM BOOK WHERE TITLE LIKE '%{titulo}%'").fetchall()
    ventana_libros_ordenados = tk.Toplevel(ventana)
    ventana_libros_ordenados.title("Libros ordenador")
    ventana_libros_ordenados.geometry("400x400")
    y_scrollbar = ttk.Scrollbar(ventana_libros_ordenados, orient=tk.VERTICAL)
    x_scrollbar = ttk.Scrollbar(ventana_libros_ordenados, orient=tk.HORIZONTAL)
    listbox = tk.Listbox(ventana_libros_ordenados, 
                         yscrollcommand=y_scrollbar,
                         xscrollcommand=x_scrollbar,
                         width=200, height=100)
    y_scrollbar.config(command=listbox.yview)
    x_scrollbar.config(command=listbox.xview)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    listbox.pack()
    listbox.insert(tk.END, "isbn, título, autor, año")
    for libro in libros:
        listbox.insert(tk.END, f"{libro[1]},{libro[2]},{libro[3]},{libro[4]},{libro[5]}")

def buscar_editorial():
    if(hay_datos() == False):
        return messagebox.showerror("Error", "No hay datos cargados")
    editoriales = [fila[0] for fila in cur.execute("SELECT DISTINCT publisher FROM BOOK").fetchall()]
    print(editoriales)
    ventana_seleccion_editorial = tk.Toplevel(app)
    ventana_seleccion_editorial.title("Que editorial quieres buscar")
    ventana_seleccion_editorial.geometry("300x300")
    editorial_seleccionada = StringVar(ventana_seleccion_editorial, editoriales[0])
    editorial_dropdown = OptionMenu(ventana_seleccion_editorial, editorial_seleccionada, *editoriales)
    editorial_dropdown.pack()
    ttk.Button(ventana_seleccion_editorial, text="Listar", command=lambda: filta_por_editorial(ventana_seleccion_editorial, editorial_seleccionada.get())).pack()

def filta_por_editorial(ventana, editorial):
    libros = cur.execute(f"SELECT * FROM BOOK WHERE PUBLISHER= ?", (f"{editorial}",)).fetchall()
    ventana_libros_ordenados = tk.Toplevel(ventana)
    ventana_libros_ordenados.title("Libros ordenador")
    ventana_libros_ordenados.geometry("400x400")
    y_scrollbar = ttk.Scrollbar(ventana_libros_ordenados, orient=tk.VERTICAL)
    x_scrollbar = ttk.Scrollbar(ventana_libros_ordenados, orient=tk.HORIZONTAL)
    listbox = tk.Listbox(ventana_libros_ordenados, 
                         yscrollcommand=y_scrollbar,
                         xscrollcommand=x_scrollbar,
                         width=200, height=100)
    y_scrollbar.config(command=listbox.yview)
    x_scrollbar.config(command=listbox.xview)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    listbox.pack()
    listbox.insert(tk.END, "título, autor, año")
    for libro in libros:
        listbox.insert(tk.END, f"{libro[2]},{libro[3]},{libro[4]},{libro[5]}")

app.title('Datos de libros')

app.geometry('600x400')

barra_menu = tk.Menu(app)
app.config(menu=barra_menu)

#Menu datos
menu_datos = tk.Menu(barra_menu, tearoff=0)
menu_datos.add_command(label="Cargar", command=guardar_csv)
menu_datos.add_command(label="Salir", command=salir)
barra_menu.add_cascade(label="Datos", menu=menu_datos)

#Menu listado
menu_datos = tk.Menu(barra_menu, tearoff=0)
menu_datos.add_command(label="Completo", command=listar_completo)
menu_datos.add_command(label="Ordenado", command=seleccion)
barra_menu.add_cascade(label="Listar", menu=menu_datos)

#Menu buscar
menu_datos = tk.Menu(barra_menu, tearoff=0)
menu_datos.add_command(label="Título", command=buscar_titulo)
menu_datos.add_command(label="Editorial", command=buscar_editorial)
barra_menu.add_cascade(label="Buscar", menu=menu_datos)


app.mainloop()