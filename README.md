# Encuesta de Consumo de Alcohol

Este proyecto consiste en una aplicación de encuesta para recopilar información sobre el consumo de alcohol, sus efectos y otros hábitos relacionados. La interfaz gráfica está construida con Tkinter en Python.

## Requisitos

- Python 3.x
- Tkinter (viene incluido con Python)
- openpyxl (para exportar datos a Excel)

## Funcionalidades

- Conectar a una base de datos (simulado mediante un botón).
- Ingreso de datos en campos como edad, sexo, consumo de bebidas alcohólicas, etc.
- Realización de operaciones CRUD (Crear, Leer, Actualizar, Eliminar).
- Visualización de los resultados en un `Treeview`.
- Generación de gráficos (barras, circular, líneas).
- Exportación de datos a un archivo Excel.

## Instrucciones de uso

1. Clona o descarga el repositorio.
2. Instala los requerimientos necesarios.
3. Ejecuta el archivo `main.py`.
4. Completa los campos en la interfaz y realiza las acciones que necesites (agregar, cargar, modificar, eliminar registros).
5. Puedes visualizar los resultados de las encuestas y exportarlos a Excel o generar gráficos.

## Funciones principales

- **Conectar a BBDD**: Simula la conexión a una base de datos.
- **Agregar Registro**: Añade un nuevo registro a la encuesta.
- **Cargar Datos**: Permite cargar y modificar datos existentes.
- **Limpiar Datos**: Limpia los campos de entrada.
- **Modificar Registro**: Modifica un registro existente.
- **Eliminar Registro**: Elimina un registro de la encuesta.
- **Ver Resultados**: Muestra los resultados de las encuestas en una tabla.
- **Mostrar Gráfico**: Genera un gráfico con los resultados de la encuesta.
- **Exportar a Excel**: Exporta los datos de la encuesta a un archivo Excel.

## Instalación

Para instalar los requerimientos necesarios, usa el siguiente comando:

```bash
pip install openpyxl
