import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd

conexion = None
# ----------------------------------------------------------------------------------------------------------------------
# 1 - CONEXIÓN A LA BBDD.
def conectar_db(usuario, contrasena):
    global conexion
    try:
        # Intentamos establecer la conexión con la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            user=usuario,
            password=contrasena,
            database="encuestas"
        )
        # Si la conexión es exitosa, mostramos un mensaje
        messagebox.showinfo("Conexión exitosa", "Conexión a la base de datos realizada.")
        return True
    except mysql.connector.Error as err:
        # Si ocurre un error en la conexión, mostramos un mensaje
        messagebox.showerror("Error", f"No se puede realizar la conexión a la BBDD: {err}")
        # Retornamos False si la conexión falla
        return False
# ----------------------------------------------------------------------------------------------------------------------
# 2 - REALIZACIÓN DE UNA CONSULTA
def realizar_query(query, filtros):
    # Verificamos si no hay una conexión activa a la base de datos
    if not conexion:
        # Si no hay conexión, mostramos un error
        messagebox.showerror("Error", "No estás conectado a la base de datos.")
        # Retornamos una lista vacía si no hay conexión
        return []

    try:
        # Intentamos ejecutar la consulta con los filtros proporcionados
        with conexion.cursor() as cursor:
            cursor.execute(query, filtros)
            # Retornamos los resultados de la consulta
            return cursor.fetchall()
    except mysql.connector.Error as err:
        # Si ocurre un error al ejecutar la consulta, mostramos el error
        messagebox.showerror("Error", f"No se puede ejecutar la consulta: {err}")
        # Retornamos una lista vacía en caso de error
        return []
# ----------------------------------------------------------------------------------------------------------------------
# 3 - ACTUALIZACIÓN DEL TREEVIEW
def actualizar_treeview(resultados):
    # Eliminamos todas las filas previas del Treeview antes de agregar nuevos datos.
    # Se itera en cada fila.
    for row in treeviewEncuesta.get_children():
        # Eliminamos cada fila del Treeview.
        treeviewEncuesta.delete(row)

    # Verificamos si hay resultados para mostrar.
    if resultados:
        # Si hay resultados, los insertamos en el Treeview.
        for fila in resultados:
            # Insertamos cada fila en el Treeview
            treeviewEncuesta.insert("", "end", values=fila)
    else:
        # Si no hay resultados, mostramos un mensaje informativo
        messagebox.showinfo("Sin resultados", "No se encontraron registros con los filtros proporcionados.")
# ----------------------------------------------------------------------------------------------------------------------
# 4 - FUNCIÓN QUE CARGA LOS DATOS DE LA BASE DE DATOS EL TREEVIEW
def encuesta():
    # Se obtienen los valores de los campos de entrada del usuario.
    edad = textoEdad.get()
    sexo = comboSexo.get()
    bebidasSemana = textoBebidasSemana.get()
    cervezasSemana = textoCervezasSemana.get()
    bebidasFinSemana = textoBebidasFinSemana.get()
    bebidasDestiladasSemana = textoBebidasDestiladasSemana.get()
    vinosSemana = textoVinoSemana.get()
    perdidasControl = textoPerdidasControl.get()
    diversionDependencia = comboDiversionDependenciaAlcohol.get()
    problemasDigestivos = comboProblemasDigestivos.get()
    tensionAlta = comboTensionAlta.get()
    dolorCabeza = comboDolorCabeza.get()

    # Convertir campos numéricos a enteros.
    edad = int(edad) if edad.isdigit() else None
    bebidasSemana = int(bebidasSemana) if bebidasSemana.isdigit() else None
    cervezasSemana = int(cervezasSemana) if cervezasSemana.isdigit() else None
    bebidasFinSemana = int(bebidasFinSemana) if bebidasFinSemana.isdigit() else None
    bebidasDestiladasSemana = int(bebidasDestiladasSemana) if bebidasDestiladasSemana.isdigit() else None
    vinosSemana = int(vinosSemana) if vinosSemana.isdigit() else None
    perdidasControl = int(perdidasControl) if perdidasControl.isdigit() else None

    # Listas para condiciones y filtros.
    condiciones = []
    filtros = []

    # Agregar condiciones a la consulta si los campos correspondientes tienen valores.
    if edad:
        condiciones.append("AND edad = %s")
        filtros.append(edad)
    if sexo:
        condiciones.append("AND Sexo = %s")
        filtros.append(sexo)
    if bebidasSemana:
        condiciones.append("AND BebidasSemana = %s")
        filtros.append(bebidasSemana)
    if cervezasSemana:
        condiciones.append("AND CervezasSemana = %s")
        filtros.append(cervezasSemana)
    if bebidasFinSemana:
        condiciones.append("AND BebidasFinSemana = %s")
        filtros.append(bebidasFinSemana)
    if bebidasDestiladasSemana:
        condiciones.append("AND BebidasDestiladasSemana = %s")
        filtros.append(bebidasDestiladasSemana)
    if vinosSemana:
        condiciones.append("AND VinosSemana = %s")
        filtros.append(vinosSemana)
    if perdidasControl:
        condiciones.append("AND PerdidasControl = %s")
        filtros.append(perdidasControl)
    if diversionDependencia:
        condiciones.append("AND DiversionDependenciaAlcohol = %s")
        filtros.append(diversionDependencia)
    if problemasDigestivos:
        condiciones.append("AND ProblemasDigestivos = %s")
        filtros.append(problemasDigestivos)
    if tensionAlta:
        condiciones.append("AND TensionAlta = %s")
        filtros.append(tensionAlta)
    if dolorCabeza:
        condiciones.append("AND DolorCabeza = %s")
        filtros.append(dolorCabeza)

    # Crear la consulta SQL inicial.
    query = ("SELECT edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, "
             "BebidasDestiladasSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, "
             "ProblemasDigestivos, TensionAlta, DolorCabeza FROM ENCUESTA WHERE 1=1")
    if condiciones:
        # Se unen todas las condiciones.
        query += " " + " ".join(condiciones)

    # Realizar la consulta y actualizar el Treeview
    resultados = realizar_query(query, filtros)
    actualizar_treeview(resultados)
# ----------------------------------------------------------------------------------------------------------------------
# 5 - MOSTRAR GRÁFICO
def mostrar_grafico():
    # Recopilación de datos desde los campos de entrada de la interfaz.
    edad = textoEdad.get()
    sexo = comboSexo.get()
    bebidas_semana = textoBebidasSemana.get()
    cervezas_semana = textoCervezasSemana.get()
    bebidas_fin_semana = textoBebidasFinSemana.get()
    bebidas_destiladas_semana = textoBebidasDestiladasSemana.get()
    vinos_semana = textoVinoSemana.get()
    perdidas_control = textoPerdidasControl.get()
    diversion_dependencia = comboDiversionDependenciaAlcohol.get()
    problemas_digestivos = comboProblemasDigestivos.get()
    tension_alta = comboTensionAlta.get()
    dolor_cabeza = comboDolorCabeza.get()

    # Listas para almacenar condiciones y los filtros.
    condiciones = []
    filtros = []

    # Agregar condiciones según los valores ingresados.
    if edad:
        condiciones.append("AND edad = %s")
        filtros.append(int(edad))
    if sexo:
        condiciones.append("AND Sexo = %s")
        filtros.append(sexo)
    if bebidas_semana:
        condiciones.append("AND BebidasSemana = %s")
        filtros.append(int(bebidas_semana))
    if cervezas_semana:
        condiciones.append("AND CervezasSemana = %s")
        filtros.append(int(cervezas_semana))
    if bebidas_fin_semana:
        condiciones.append("AND BebidasFinSemana = %s")
        filtros.append(int(bebidas_fin_semana))
    if bebidas_destiladas_semana:
        condiciones.append("AND BebidasDestiladasSemana = %s")
        filtros.append(int(bebidas_destiladas_semana))
    if vinos_semana:
        condiciones.append("AND VinosSemana = %s")
        filtros.append(int(vinos_semana))
    if perdidas_control:
        condiciones.append("AND PerdidasControl = %s")
        filtros.append(int(perdidas_control))
    if diversion_dependencia:
        condiciones.append("AND DiversionDependenciaAlcohol = %s")
        filtros.append(diversion_dependencia)
    if problemas_digestivos:
        condiciones.append("AND ProblemasDigestivos = %s")
        filtros.append(problemas_digestivos)
    if tension_alta:
        condiciones.append("AND TensionAlta = %s")
        filtros.append(tension_alta)
    if dolor_cabeza:
        condiciones.append("AND DolorCabeza = %s")
        filtros.append(dolor_cabeza)

    # Crear la consulta base para extraer los datos relevantes.
    query = "SELECT Edad, Sexo, BebidasSemana, DiversionDependenciaAlcohol FROM ENCUESTA WHERE 1=1"
    if condiciones:
        # Añadimos las condiciones a la consulta.
        query += " " + " ".join(condiciones)

    # Ejecutar la consulta para obtener los datos.
    resultados = realizar_query(query, filtros)

    if resultados:
        # Separar los datos necesarios para el gráfico, en este caso edades y bebidas.
        edades = [row[0] for row in resultados]
        bebidas = [row[2] for row in resultados]

        # Obtener el tipo de gráfico seleccionado en la interfaz.
        grafico_tipo = comboGrafico.get()

        if grafico_tipo == "Gráfico de Barras":
            # Crear un gráfico de barras
            plt.bar(edades, bebidas)
            # Ejes X e Y.
            plt.xlabel('Edad')
            plt.ylabel('Bebidas a la Semana')
            plt.title('Consumo de Bebidas por Edad') # Título.

        elif grafico_tipo == "Gráfico Circular":
            # Crear un gráfico circular basado en la diversión o dependencia.
            diversion_labels = [row[3] for row in resultados] # Lista de etiquetas de diversión/dependencia.
            # Conteo por categoría.
            diversion_counts = [diversion_labels.count(label) for label in set(diversion_labels)]
            # Se crea el gráfico.
            plt.pie(diversion_counts, labels=set(diversion_labels), autopct='%1.1f%%', startangle=90)
            plt.title('Distribución de Diversión/Dependencia') # Título del gráfico.

        elif grafico_tipo == "Gráfico de Líneas":
            # Graficar el gráfico de líneas
            # Línea azul con marcadores circulares.
            plt.plot(edades, bebidas, marker='o', linestyle='-', color='b')
            # Ejes.
            plt.xlabel('Edad')
            plt.ylabel('Bebidas a la Semana')
            plt.title('Consumo de Bebidas por Edad (Gráfico de Líneas)') #Título del gráfico.

        # Mostrar el gráfico generado.
        plt.show()
# ----------------------------------------------------------------------------------------------------------------------
# 6 - EXPORTACIÓN DE DATOS A EXCEL.
def exportar_datos():
    # Recopilación de datos desde los campos de la interfaz.
    edad = textoEdad.get()
    sexo = comboSexo.get()
    bebidas_semana = textoBebidasSemana.get()
    cervezas_semana = textoCervezasSemana.get()
    bebidas_fin_semana = textoBebidasFinSemana.get()
    bebidas_destiladas_semana = textoBebidasDestiladasSemana.get()
    vinos_semana = textoVinoSemana.get()
    perdidas_control = textoPerdidasControl.get()
    diversion_dependencia = comboDiversionDependenciaAlcohol.get()
    problemas_digestivos = comboProblemasDigestivos.get()
    tension_alta = comboTensionAlta.get()
    dolor_cabeza = comboDolorCabeza.get()

    # Lista para condiciones de consulta y valores de filtro.
    condiciones = []
    filtros = []

    # Agregar condiciones y filtros según los valores proporcionados.
    if edad:
        condiciones.append("AND edad = %s")
        filtros.append(int(edad))
    if sexo:
        condiciones.append("AND Sexo = %s")
        filtros.append(sexo)
    if bebidas_semana:
        condiciones.append("AND BebidasSemana = %s")
        filtros.append(int(bebidas_semana))
    if cervezas_semana:
        condiciones.append("AND CervezasSemana = %s")
        filtros.append(int(cervezas_semana))
    if bebidas_fin_semana:
        condiciones.append("AND BebidasFinSemana = %s")
        filtros.append(int(bebidas_fin_semana))
    if bebidas_destiladas_semana:
        condiciones.append("AND BebidasDestiladasSemana = %s")
        filtros.append(int(bebidas_destiladas_semana))
    if vinos_semana:
        condiciones.append("AND VinosSemana = %s")
        filtros.append(int(vinos_semana))
    if perdidas_control:
        condiciones.append("AND PerdidasControl = %s")
        filtros.append(int(perdidas_control))
    if diversion_dependencia:
        condiciones.append("AND DiversionDependenciaAlcohol = %s")
        filtros.append(diversion_dependencia)
    if problemas_digestivos:
        condiciones.append("AND ProblemasDigestivos = %s")
        filtros.append(problemas_digestivos)
    if tension_alta:
        condiciones.append("AND TensionAlta = %s")
        filtros.append(tension_alta)
    if dolor_cabeza:
        condiciones.append("AND DolorCabeza = %s")
        filtros.append(dolor_cabeza)

    # Consulta base para seleccionar los datos.
    query = "SELECT Edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, BebidasDestiladasSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza FROM ENCUESTA WHERE 1=1"
    if condiciones:
        query += " " + " ".join(condiciones)

    # Realizar la consulta y obtener los resultados.
    resultados = realizar_query(query, filtros)

    if resultados:
        try:
            # Crear un DataFrame de pandas con los resultados.
            df = pd.DataFrame(resultados, columns=["Edad", "Sexo", "Bebidas a la Semana", "Cervezas a la Semana", "Bebidas Fin de Semana", "Bebidas Destiladas", "Vino a la Semana", "Pérdidas de Control", "Diversión/Dependencia", "Problemas Digestivos", "Tensión Alta", "Dolores de Cabeza"])
            # Exportar los datos a un archivo Excel.
            df.to_excel("encuesta_resultados.xlsx", index=False)
            # Mostrar mensaje de éxito al usuario.
            messagebox.showinfo("Éxito", "Datos exportados a Excel.")
        except Exception as e:
            # Mostrar mensaje de error si ocurre un problema al exportar.
            messagebox.showerror("Error", f"Hubo un problema al exportar a Excel: {str(e)}")
    else:
        # Mostrar advertencia si no hay resultados para exportar.
        messagebox.showwarning("Sin resultados", "No hay datos para exportar.")
# ----------------------------------------------------------------------------------------------------------------------
# 7 - VENTANA DE CONEXIÓN PARA VALIDARLA
def mostrar_ventana_conexion():
    # Crear una ventana secundaria para la conexión.
    ventana1 = tk.Toplevel()
    ventana1.minsize(300, 300)
    ventana1.geometry("300x300")
    ventana1.title("Conexión")
    ventana1.resizable(False, False)
    ventana1.config(bg="lightblue")

    # Etiqueta y entrada para el nombre de usuario.
    labelUsuario = tk.Label(ventana1, text="Usuario")
    labelUsuario.pack(pady=3)

    textoUsuario = tk.Entry(ventana1, font=("Arial", 12), width=16)
    textoUsuario.pack(pady=3)

    # Etiqueta y entrada para la contraseña.
    labelPassword = tk.Label(ventana1, text="Contraseña")
    labelPassword.pack(pady=3)

    textoPassword = tk.Entry(ventana1, font=("Arial", 12), width=16)
    textoPassword.pack(pady=3)

    # Función que intenta conectar a la base de datos.
    def intentar_conectar():
        # Se obtienen los valores ingresados por el usuario.
        usuario = textoUsuario.get()
        contrasena = textoPassword.get()

        # Intentar conectar a la base de datos.
        if conectar_db(usuario, contrasena):
            # Si la conexión es exitosa, cerrar la ventana de conexión.
            ventana1.destroy()
            # Actualizar el estado de los botones de la interfaz principal.
            botonLogin.config(state=tk.DISABLED)
            botonEncuesta.config(state=tk.NORMAL)
            botonGrafico.config(state=tk.NORMAL)
            botonExportar.config(state=tk.NORMAL)

    # Botón para intentar conectar a la base de datos.
    botonConectar = tk.Button(ventana1, text="Conectar", command=intentar_conectar)
    botonConectar.pack(pady=10)
# ----------------------------------------------------------------------------------------------------------------------
# 8 - AGREGAR UN REGISTRO A NUESTRA BBDD.
def agregar_registro():
    # Obtener valores de los campos de entrada.
    edad = textoEdad.get()
    sexo = comboSexo.get()
    bebidasSemana = textoBebidasSemana.get()
    cervezasSemana = textoCervezasSemana.get()
    bebidasFinSemana = textoBebidasFinSemana.get()
    bebidasDestiladasSemana = textoBebidasDestiladasSemana.get()
    vinosSemana = textoVinoSemana.get()
    perdidasControl = textoPerdidasControl.get()
    diversionDependencia = comboDiversionDependenciaAlcohol.get()
    problemasDigestivos = comboProblemasDigestivos.get()
    tensionAlta = comboTensionAlta.get()
    dolorCabeza = comboDolorCabeza.get()

    # Validar datos mínimos requeridos.
    if not edad or not sexo:
        messagebox.showerror("Error", "La edad y el sexo son obligatorios.")
        return

    try:
        # Primero obtener el ID mas alto de la base de datos.
        query_max_id = "SELECT MAX(idEncuesta) FROM ENCUESTA"
        max_id_result = realizar_query(query_max_id, ())
        max_id = max_id_result[0][0] if max_id_result[0][0] is not None else 0
        # El siguiente idEncuesta será el max_id + 1
        nuevo_idEncuesta = max_id + 1
        # Consulta para insertar el nuevo registro con el nuevo ID
        query = """
        INSERT INTO ENCUESTA (idEncuesta, Edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, BebidasDestiladasSemana, 
                              VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            # ID único del nuevo registro.
            nuevo_idEncuesta,
            int(edad), sexo, int(bebidasSemana or 0), int(cervezasSemana or 0), int(bebidasFinSemana or 0),
            int(bebidasDestiladasSemana or 0), int(vinosSemana or 0), int(perdidasControl or 0),
            diversionDependencia, problemasDigestivos, tensionAlta, dolorCabeza
        )

        # Ejecutar la consulta de inserción.
        with conexion.cursor() as cursor:
            # Ejecutar la consulta con los valores especificados.
            cursor.execute(query, valores)
        # Guardar los cambios en la base de datos.
        conexion.commit()

        # Mostrar mensaje de éxito.
        messagebox.showinfo("Éxito", "Registro agregado correctamente.")
        # Refrescar el TreeView.
        encuesta()

    except mysql.connector.Error as err:
        # Manejo de errores en la inserción.
        messagebox.showerror("Error", f"No se pudo agregar el registro: {err}")
# ----------------------------------------------------------------------------------------------------------------------
# 9 - CARGAR LOS DATOS EN LOS CAMPOS RELLENABLE DE UNA ENTRADA SELECCIONADA.
def cargar_datos_modificar():
    # Obtiene el registro seleccionado mediante .selection().
    seleccionado = treeviewEncuesta.selection()
    if seleccionado:
        valores = treeviewEncuesta.item(seleccionado)["values"]
        # Cargar datos en los campos
        textoEdad.delete(0, tk.END)
        textoEdad.insert(0, valores[0])
        comboSexo.set(valores[1])
        textoBebidasSemana.delete(0, tk.END)
        textoBebidasSemana.insert(0, valores[2])
        textoCervezasSemana.delete(0, tk.END)
        textoCervezasSemana.insert(0, valores[3])
        textoBebidasFinSemana.delete(0, tk.END)
        textoBebidasFinSemana.insert(0, valores[4])
        textoBebidasDestiladasSemana.delete(0, tk.END)
        textoBebidasDestiladasSemana.insert(0, valores[5])
        textoVinoSemana.delete(0, tk.END)
        textoVinoSemana.insert(0, valores[6])
        textoPerdidasControl.delete(0, tk.END)
        textoPerdidasControl.insert(0, valores[7])
        comboDiversionDependenciaAlcohol.set(valores[8])
        comboProblemasDigestivos.set(valores[9])
        comboTensionAlta.set(valores[10])
        comboDolorCabeza.set(valores[11])
    else:
        # Mensaje de error en caso de que no se haya seleccionado ningún registro.,
        messagebox.showerror("Error", "Selecciona un registro para modificar.")
# ----------------------------------------------------------------------------------------------------------------------
# 10 - MODIFICAR UNA ENTRADA SELECCIONADA CON LOS CAMPOS DE ARRIBA.
def modificar_registro():
    # Obtiene el registro seleccionado mediante .selection().
    seleccionado = treeviewEncuesta.selection()
    # Validar si se seleccionó un registro.
    if not seleccionado:
        messagebox.showerror("Error", "Selecciona un registro para modificar.")
        return

    # Obtener los valores del registro seleccionado.
    valores = treeviewEncuesta.item(seleccionado)["values"]
    # Se asume que la primera columna es el identificador único (ID o Edad).
    edad_original = valores[0]

    try:
        # Preparar la consulta SQL para actualizar el registro.
        query = """
        UPDATE ENCUESTA SET Edad = %s, Sexo = %s, BebidasSemana = %s, CervezasSemana = %s, BebidasFinSemana = %s,
                             BebidasDestiladasSemana = %s, VinosSemana = %s, PerdidasControl = %s,
                             DiversionDependenciaAlcohol = %s, ProblemasDigestivos = %s, TensionAlta = %s,
                             DolorCabeza = %s
        WHERE Edad = %s
        """
        # Recopilar valores actualizados desde los campos del formulario.
        valores = (
            int(textoEdad.get()), comboSexo.get(), int(textoBebidasSemana.get() or 0), int(textoCervezasSemana.get() or 0),
            int(textoBebidasFinSemana.get() or 0), int(textoBebidasDestiladasSemana.get() or 0),
            int(textoVinoSemana.get() or 0), int(textoPerdidasControl.get() or 0),
            comboDiversionDependenciaAlcohol.get(), comboProblemasDigestivos.get(),
            comboTensionAlta.get(), comboDolorCabeza.get(), int(edad_original)
        )
        # Ejecutar la consulta.
        with conexion.cursor() as cursor:
            cursor.execute(query, valores)
        # Confirmar los cambios en la base de datos.
        conexion.commit()

        # Mostrar mensaje de éxito y refrescar el TreeView.
        messagebox.showinfo("Éxito", "Registro modificado correctamente.")
        encuesta()
    except mysql.connector.Error as err:
        # Manejo de errores en la operación.
        messagebox.showerror("Error", f"No se pudo modificar el registro: {err}")
# ----------------------------------------------------------------------------------------------------------------------
# 11 - ELIMINAR UNA ENTRADA DE LA BBDD QUE SE HAYA SELECCIONADO.
def eliminar_registro():
    # Obtiene el registro seleccionado mediante .selection().
    seleccionado = treeviewEncuesta.selection()
    # Validar si se seleccionó un registro.
    if not seleccionado:
        messagebox.showerror("Error", "Selecciona un registro para eliminar.")
        return
    # Confirmar la eliminación.
    confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este registro?")

    # Si el usuario confirma.
    if confirmacion:
        try:
            # Obtener los valores del registro seleccionado.
            valores = treeviewEncuesta.item(seleccionado)["values"]
            edad = valores[0]
            # Consulta SQL para eliminar el registro.
            query = "DELETE FROM ENCUESTA WHERE Edad = %s"

            # Ejecutar la consulta.
            with conexion.cursor() as cursor:
                cursor.execute(query, (edad,))
            # Confirmar los cambios en la base de datos.
            conexion.commit()

            # Mostrar mensaje de éxito y refrescar el TreeView.
            messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
            encuesta()
        except mysql.connector.Error as err:
            # Manejo de errores de la base de datos.
            messagebox.showerror("Error", f"No se pudo eliminar el registro: {err}")
# ----------------------------------------------------------------------------------------------------------------------
# 12 - LIMPIA TODOS LOS CAMPOS.
def limpiar_datos():
    # Función para limpiar todos los campos de entrada.
    textoEdad.delete(0, tk.END)
    comboSexo.set('')
    textoBebidasSemana.delete(0, tk.END)
    textoCervezasSemana.delete(0, tk.END)
    textoBebidasFinSemana.delete(0, tk.END)
    textoBebidasDestiladasSemana.delete(0, tk.END)
    textoVinoSemana.delete(0, tk.END)
    textoPerdidasControl.delete(0, tk.END)
    comboDiversionDependenciaAlcohol.set('')
    comboProblemasDigestivos.set('')
    comboTensionAlta.set('')
    comboDolorCabeza.set('')
# ----------------------------------------------------------------------------------------------------------------------

# Ventana principal
ventana = tk.Tk()
ventana.minsize(1300, 800)
ventana.geometry("1300x800")
ventana.title("Encuesta")
ventana.resizable(False, False)
ventana.config(bg="lightblue")

# Botón de login para la BBDD
botonLogin = tk.Button(ventana, text="Conectar A BBDD", command=mostrar_ventana_conexion)
botonLogin.pack(pady=3)

# Frame principal para centrar las columnas
frame_central = tk.Frame(ventana, bg="lightblue")
frame_central.pack(pady=20)

# Crear tres columnas usando Frames dentro del frame central
columna1 = tk.Frame(frame_central, bg="lightblue")
columna1.pack(side=tk.LEFT, padx=20, anchor="n")

columna2 = tk.Frame(frame_central, bg="lightblue")
columna2.pack(side=tk.LEFT, padx=20, anchor="n")

columna3 = tk.Frame(frame_central, bg="lightblue")
columna3.pack(side=tk.LEFT, padx=20, anchor="n")

# ---- Primera Columna ----
# Edad
labelEdad = tk.Label(columna1, text="Edad", bg="lightblue")
labelEdad.pack(pady=3)

textoEdad = tk.Entry(columna1, font=("Arial", 12), width=16)
textoEdad.pack(pady=3)

# Sexo
labelSexo = tk.Label(columna1, text="Sexo", bg="lightblue")
labelSexo.pack(pady=3)

comboSexo = ttk.Combobox(columna1, values=['Hombre', 'Mujer'])
comboSexo.pack(pady=3)

# Bebidas Semana
labelBebidasSemana = tk.Label(columna1, text="Bebidas a la Semana", bg="lightblue")
labelBebidasSemana.pack(pady=3)

textoBebidasSemana = tk.Entry(columna1, font=("Arial", 12), width=16)
textoBebidasSemana.pack(pady=3)

# Cervezas Semana
labelCervezasSemana = tk.Label(columna1, text="Cervezas a la Semana", bg="lightblue")
labelCervezasSemana.pack(pady=3)

textoCervezasSemana = tk.Entry(columna1, font=("Arial", 12), width=16)
textoCervezasSemana.pack(pady=3)

# ---- Segunda Columna ----
# Bebidas Fin de Semana
labelBebidasFinSemana = tk.Label(columna2, text="Bebidas en Fines de Semana", bg="lightblue")
labelBebidasFinSemana.pack(pady=3)

textoBebidasFinSemana = tk.Entry(columna2, font=("Arial", 12), width=16)
textoBebidasFinSemana.pack(pady=3)

# Bebidas Destiladas Semana
labelBebidasDestiladasSemana = tk.Label(columna2, text="Bebidas Destiladas a la Semana", bg="lightblue")
labelBebidasDestiladasSemana.pack(pady=3)

textoBebidasDestiladasSemana = tk.Entry(columna2, font=("Arial", 12), width=16)
textoBebidasDestiladasSemana.pack(pady=3)

# Vino Semana
labelVinoSemana = tk.Label(columna2, text="Vino a la Semana", bg="lightblue")
labelVinoSemana.pack(pady=3)

textoVinoSemana = tk.Entry(columna2, font=("Arial", 12), width=16)
textoVinoSemana.pack(pady=3)

# Pérdidas de Control
labelPerdidasControl = tk.Label(columna2, text="Pérdidas de Control", bg="lightblue")
labelPerdidasControl.pack(pady=3)

textoPerdidasControl = tk.Entry(columna2, font=("Arial", 12), width=16)
textoPerdidasControl.pack(pady=3)

# ---- Tercera Columna ----
# Diversión / Dependencia por el Alcohol
labelDiversionDependenciaAlcohol = tk.Label(columna3, text="Diversión / Dependencia", bg="lightblue")
labelDiversionDependenciaAlcohol.pack(pady=3)

comboDiversionDependenciaAlcohol = ttk.Combobox(columna3, values=['Sí', 'No'])
comboDiversionDependenciaAlcohol.pack(pady=3)

# Problemas Digestivos
labelProblemasDigestivos = tk.Label(columna3, text="Problemas Digestivos", bg="lightblue")
labelProblemasDigestivos.pack(pady=3)

comboProblemasDigestivos = ttk.Combobox(columna3, values=['Sí', 'No'])
comboProblemasDigestivos.pack(pady=3)

# Tensión Alta
labelTensionAlta = tk.Label(columna3, text="Tensión Alta", bg="lightblue")
labelTensionAlta.pack(pady=3)

comboTensionAlta = ttk.Combobox(columna3, values=['Sí', 'No', 'No lo sé'])
comboTensionAlta.pack(pady=3)

# Dolores de Cabeza
labelDolorCabeza = tk.Label(columna3, text="Dolores de Cabeza", bg="lightblue")
labelDolorCabeza.pack(pady=3)

comboDolorCabeza = ttk.Combobox(columna3, values=['Nunca', 'Alguna vez', 'A menudo', 'Muy a menudo'])
comboDolorCabeza.pack(pady=3)

# Frame para los botones CRUD organizados horizontalmente
frame_botones = tk.Frame(ventana, bg="lightblue")
frame_botones.pack(pady=20)

# ----------------------------------------------------------------------------------------------------------------------
# Botones CRUD
botonAgregar = tk.Button(frame_botones, text="Agregar Registro", command=agregar_registro)
botonAgregar.grid(row=0, column=0, padx=10)

botonCargarModificar = tk.Button(frame_botones, text="Cargar Datos", command=cargar_datos_modificar)
botonCargarModificar.grid(row=0, column=1, padx=10)

botonLimpiar = tk.Button(frame_botones, text="Limpiar Datos", command=limpiar_datos)
botonLimpiar.grid(row=0, column=2, padx=10)

botonModificar = tk.Button(frame_botones, text="Modificar Registro", command=modificar_registro)
botonModificar.grid(row=0, column=3, padx=10)

botonEliminar = tk.Button(frame_botones, text="Eliminar Registro", command=eliminar_registro)
botonEliminar.grid(row=0, column=4, padx=10)
# ----------------------------------------------------------------------------------------------------------------------

# Otros botones debajo de los CRUD
botonEncuesta = tk.Button(frame_botones, text="Ver Resultados", command=encuesta, state=tk.DISABLED)
botonEncuesta.grid(row=1, column=0, columnspan=2, pady=10)

comboGrafico = ttk.Combobox(frame_botones, values=['Gráfico de Barras', 'Gráfico Circular', 'Gráfico de Líneas'])
comboGrafico.grid(row=1, column=2, pady=10)

botonGrafico = tk.Button(frame_botones, text="Mostrar Gráfico", command=mostrar_grafico, state=tk.DISABLED)
botonGrafico.grid(row=1, column=3, pady=10)

botonExportar = tk.Button(frame_botones, text="Exportar a Excel", command=exportar_datos, state=tk.DISABLED)
botonExportar.grid(row=2, column=0, columnspan=4, pady=10)

labelLeyenda = tk.Label(frame_botones, text="[7] = A la semana", bg="lightblue")
labelLeyenda.grid(row=3, column=0, columnspan=4, pady=3)

# Treeview para resultados
treeviewEncuesta = ttk.Treeview(ventana, columns=("Edad", "Sexo", "Bebidas a la Semana", "Cervezas a la Semana", "Bebidas Fin de Semana", "Bebidas Destiladas", "Vinos Semana", "Pérdidas de Control", "Diversión/Dependencia", "Problemas Digestivos", "Tensión Alta", "Dolores de Cabeza"), show="headings")
treeviewEncuesta.pack(fill=tk.BOTH, expand=True)

# Encabezados y configuración de columnas
treeviewEncuesta.heading("Edad", text="Edad")
treeviewEncuesta.heading("Sexo", text="Sexo")
treeviewEncuesta.heading("Bebidas a la Semana", text="Bebidas [7]")
treeviewEncuesta.heading("Cervezas a la Semana", text="Cervezas [7]")
treeviewEncuesta.heading("Bebidas Fin de Semana", text="Bebidas fin de semana")
treeviewEncuesta.heading("Bebidas Destiladas", text="Bebidas Destiladas [7]")
treeviewEncuesta.heading("Vinos Semana", text="Vino [7]")
treeviewEncuesta.heading("Pérdidas de Control", text="Pérdidas de Control")
treeviewEncuesta.heading("Diversión/Dependencia", text="Diversión/Dependencia")
treeviewEncuesta.heading("Problemas Digestivos", text="Problemas Digestivos")
treeviewEncuesta.heading("Tensión Alta", text="Tensión Alta")
treeviewEncuesta.heading("Dolores de Cabeza", text="Dolores de Cabeza")

# Configuración de ancho de columnas
treeviewEncuesta.column("Edad", width=45, anchor="center")
treeviewEncuesta.column("Sexo", width=45, anchor="center")
treeviewEncuesta.column("Bebidas a la Semana", width=75, anchor="center")
treeviewEncuesta.column("Cervezas a la Semana", width=80, anchor="center")
treeviewEncuesta.column("Bebidas Fin de Semana", width=130, anchor="center")
treeviewEncuesta.column("Bebidas Destiladas", width=130, anchor="center")
treeviewEncuesta.column("Vinos Semana", width=55, anchor="center")
treeviewEncuesta.column("Pérdidas de Control", width=120, anchor="center")
treeviewEncuesta.column("Diversión/Dependencia", width=140, anchor="center")
treeviewEncuesta.column("Problemas Digestivos", width=130, anchor="center")
treeviewEncuesta.column("Tensión Alta", width=75, anchor="center")
treeviewEncuesta.column("Dolores de Cabeza", width=100, anchor="center")

# Mostrar la ventana.
ventana.mainloop()