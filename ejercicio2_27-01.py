import sqlite3
import sys

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

def baseDatos():
    conexion=sqlite3.connect("../databases/tareas.db")
    cursor=conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tarea TEXT NOT NULL)
    """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareasAcabadas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarea TEXT NOT NULL)
        """)

class ListaTareas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación Tareas")
        self.setGeometry(100, 100, 500, 500)
        self.setStyleSheet("background-color:#444444")

        # Centrar la ventana correctamente
        self.centrarVentana()

        # Crear el widget central y su layout principal
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layoutPrincipal = QHBoxLayout()
        self.centralWidget.setLayout(self.layoutPrincipal)
        self.layoutPrincipal.setContentsMargins(0, 10, 0, 10)

        # Layouts izquierdo y derecho
        self.layoutIzquierdo = QVBoxLayout()
        self.layoutDerecho = QVBoxLayout()
        self.layoutDerecho.setContentsMargins(0,0,0,0)
        self.layoutIzquierdo.setContentsMargins(0, 0, 0, 0)
        self.layoutPrincipal.addLayout(self.layoutIzquierdo)
        self.layoutPrincipal.addLayout(self.layoutDerecho)

        # Crear el menú superior
        self.menuBar = self.menuBar()
        self.menuBar.setStyleSheet("background-color: #B0B0B0")
        self.menu = self.menuBar.addMenu("Menú")
        self.menu.setStyleSheet("background-color:white")

        # Opciones del menú
        self.accionNuevaTarea = QAction("Nueva tarea", self)
        self.accionNuevaTarea.setShortcut(QKeySequence("Ctrl+Q"))
        self.accionNuevaTarea.triggered.connect(self.nuevaTarea)
        self.menu.addAction(self.accionNuevaTarea)

        self.accionEditarTarea = QAction("Editar tarea", self)
        self.accionEditarTarea.setShortcut(QKeySequence("Ctrl+W"))
        self.accionEditarTarea.triggered.connect(self.editarTarea)
        self.menu.addAction(self.accionEditarTarea)

        self.accionEliminarTarea = QAction("Eliminar tarea", self)
        self.accionEliminarTarea.setShortcut(QKeySequence("Ctrl+E"))
        self.accionEliminarTarea.triggered.connect(self.eliminarTareas)
        self.menu.addAction(self.accionEliminarTarea)

        # MENU CONTEXTUAL
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)



        #TITULO TAREAS DERECHO
        lblTareasPendientes=QLabel("PENDIENTES")
        lblTareasPendientes.setStyleSheet("background-color: #444444; font-size:28px;color: black; font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
        lblTareasPendientes.setContentsMargins(0,0,0,0)
        lblTareasPendientes.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutDerecho.addWidget(lblTareasPendientes)
        # TITULO TAREAS Izquierdo
        lblTareasAcabadas = QLabel("ACABADAS")
        lblTareasAcabadas.setStyleSheet("background-color: #444444; font-size:28px;color: black; font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
        lblTareasAcabadas.setContentsMargins(0, 0, 0, 0)
        lblTareasAcabadas.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layoutIzquierdo.addWidget(lblTareasAcabadas)
        # SCROLL AREA para el contenedor de tareas pendientes
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)  # Permitir que se expanda dinámicamente
        self.layoutDerecho.addWidget(self.scrollArea)

        # CONTENEDOR TAREAS DERECHO (dentro del scroll)
        self.contenedorDerecho = QWidget()
        self.layoutContenedorDerecho = QVBoxLayout()
        self.contenedorDerecho.setLayout(self.layoutContenedorDerecho)
        self.scrollArea.setWidget(self.contenedorDerecho)  # El scroll contiene este widget

        # Ajustar tamaño dinámico
        self.contenedorDerecho.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.contenedorDerecho.setStyleSheet("background-color:white;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);")

        # SCROLL AREA para el contenedor de tareas acabadas
        self.scrollAreaIzq = QScrollArea()
        self.scrollAreaIzq.setWidgetResizable(True)  # Permitir que se expanda dinámicamente
        self.layoutIzquierdo.addWidget(self.scrollAreaIzq)

        # CONTENEDOR TAREAS DERECHO (dentro del scroll)
        self.contenedorIzquierdo = QWidget()
        self.layoutContenedorIzquierdo = QVBoxLayout()
        self.contenedorIzquierdo.setLayout(self.layoutContenedorIzquierdo)
        self.scrollAreaIzq.setWidget(self.contenedorIzquierdo)  # El scroll contiene este widget

        # Ajustar tamaño dinámico
        self.contenedorIzquierdo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.contenedorIzquierdo.setStyleSheet(
            "background-color:white;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);")
        #BOTON AGREGAR TAREA
        btnAgregarTarea=QPushButton()
        btnAgregarTarea.setText("Agregar tarea")
        btnAgregarTarea.setStyleSheet("background-color:#B0B0B0;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
        btnAgregarTarea.clicked.connect(self.nuevaTarea)
        self.layoutDerecho.addWidget(btnAgregarTarea)
        # BOTON ELIMINAR TAREAS
        btnBorrarTareas = QPushButton()
        btnBorrarTareas.setText("Eliminar tareas")
        btnBorrarTareas.setStyleSheet(
            "background-color:#B0B0B0;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
        btnBorrarTareas.clicked.connect(self.eliminarTareas)
        self.layoutDerecho.addWidget(btnBorrarTareas)
        # BOTON EDITAR TAREA
        btnEditarTarea = QPushButton()
        btnEditarTarea.setText("Finalizar tarea")
        btnEditarTarea.setStyleSheet(
            "background-color:#B0B0B0;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
        btnEditarTarea.clicked.connect(self.editarTarea)
        self.layoutIzquierdo.addWidget(btnEditarTarea)
        #BOTON ACTUALIZAR TAREAS
        btnActualizarTareas = QPushButton()
        btnActualizarTareas.setText("Actualizar tareas")
        btnActualizarTareas.setStyleSheet(
            "background-color:#B0B0B0;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
        btnActualizarTareas.clicked.connect(self.devolverTareas)
        btnActualizarTareas.clicked.connect(self.devolverTareasAcabadas)
        self.layoutIzquierdo.addWidget(btnActualizarTareas)
    def asignarTarea(self):
        self.dialogoAsignar = DialogoAsignarTarea()
        self.dialogoAsignar.show()
        self.centrarVentana()
    def show_context_menu(self, position):
        context_menu = QMenu()
        context_action = QAction("Asignar tarea", self)
        context_action.setShortcut(QKeySequence("Ctrl+t"))
        context_action.triggered.connect(self.asignarTarea)
        context_menu.addAction(context_action)
        context_menu.exec(self.mapToGlobal(position))

    def nuevaTarea(self):
        self.dialogoAgregar=DialogoAgregar()
        self.dialogoAgregar.show()
        self.centrarVentana()

    def editarTarea(self):
        self.dialogoEditar=DialogoEditar()
        self.dialogoEditar.show()
        self.centrarVentana()

    def devolverTareas(self):

        conexion = sqlite3.connect("../databases/tareas.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT tarea FROM tareas")
        listaTareas = cursor.fetchall()
        self.limpiarLayout(self.layoutContenedorDerecho)
        for i in listaTareas:
            lblLista=QLabel(i[0])
            lblLista.setFixedSize(220,80)
            lblLista.setStyleSheet("background-color:#B0B0B0;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
            lblLista.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layoutContenedorDerecho.addWidget(lblLista)

        print(listaTareas)
        conexion.close()

    def devolverTareasAcabadas(self):

        conexion = sqlite3.connect("../databases/tareas.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT tarea FROM tareasAcabadas")
        listaTareas = cursor.fetchall()
        self.limpiarLayout(self.layoutContenedorIzquierdo)
        for i in listaTareas:
            lblLista = QLabel(i[0])
            lblLista.setFixedSize(220, 80)
            lblLista.setStyleSheet(
                "background-color:#B0B0B0;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
            lblLista.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layoutContenedorIzquierdo.addWidget(lblLista)

        print("Tareas acabadas : ",listaTareas)
        conexion.close()

    def limpiarLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def eliminarTareas(self):
        conexion = sqlite3.connect("../databases/tareas.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM tareas")
        cursor.execute("DELETE FROM tareasAcabadas")
        conexion.commit()
        conexion.close()
        self.devolverTareas()
        self.devolverTareasAcabadas()
        QMessageBox.information(self, "Tareas eliminadas", f"Tareas eliminadas finalizada correctamente")

    def centrarVentana(self):
        screen = QApplication.primaryScreen().availableGeometry()
        ventana = self.frameGeometry()
        ventana.moveCenter(screen.center())
        self.move(ventana.topLeft())

class DialogoAgregar(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100,100,300,300)
        self.centrarVentana()
        self.setStyleSheet("background-color:#444444")
        self.setWindowTitle("Agregar tarea")
        self.layoutPrincipal=QVBoxLayout()
        self.setLayout(self.layoutPrincipal)
        # LABEL TITULO
        lblTitulo = QLabel("TAREA")
        lblTitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lblTitulo.setStyleSheet(
            "background-color: #444444; font-size:28px;color: black; font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
        self.layoutPrincipal.addWidget(lblTitulo)
        #EDIT CONTACTO
        self.editTarea=QLineEdit()
        self.editTarea.setPlaceholderText("Introduzca el nombre")
        self.editTarea.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.editTarea.setStyleSheet(
            "background-color:white;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);")
        self.layoutPrincipal.addWidget(self.editTarea)
        #BOTON AGREGAR
        self.btnAgregar=QPushButton("Agregar")
        self.btnAgregar.clicked.connect(self.agregarTarea)
        self.btnAgregar.setStyleSheet("background-color:#B0B0B0;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
        self.layoutPrincipal.addWidget(self.btnAgregar)
        self.ventanaPrincipal=parent
    def agregarTarea(self):
        conexion=sqlite3.connect("../databases/tareas.db")
        cursor=conexion.cursor()
        tarea=self.editTarea.text()
        cursor.execute("INSERT INTO tareas(tarea)VALUES (?)",(tarea,))
        self.editTarea.clear()
        conexion.commit()
        conexion.close()
        QMessageBox.information(self,"Tarea agregada",f"Tarea {tarea} agregada correctamente")
        self.close()

    def centrarVentana(self):
        screen = QApplication.primaryScreen().availableGeometry()
        ventana = self.frameGeometry()
        ventana.moveCenter(screen.center())
        self.move(ventana.topLeft())
class DialogoAsignarTarea(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,300,300)
        self.centrarVentana()
        self.setStyleSheet("background-color:#444444")
        self.setWindowTitle("Editar tarea")
        self.layoutPrincipal=QVBoxLayout()
        self.setLayout(self.layoutPrincipal)
        # LABEL TITULO
        lblTitulo = QLabel("TAREA ASIGNADA")
        lblTitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lblTitulo.setStyleSheet(
            "background-color: #444444; font-size:28px;color: black; font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
        self.layoutPrincipal.addWidget(lblTitulo)
        #EDIT TAREA
        self.editTarea=QLineEdit()
        self.editTarea.setPlaceholderText("Introduzca la tarea")
        self.editTarea.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.editTarea.setStyleSheet(
            "background-color:white;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);")
        self.layoutPrincipal.addWidget(self.editTarea)
        #EDIT USUARIO
        self.editUsuario = QLineEdit()
        self.editUsuario.setPlaceholderText("Introduzca el usuario")
        self.editUsuario.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.editUsuario.setStyleSheet(
            "background-color:white;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);")
        self.layoutPrincipal.addWidget(self.editUsuario)
        #BOTON AGREGAR
        self.btnEditar=QPushButton("Editar")
        self.btnEditar.clicked.connect(self.agregarTareaUsuario)
        self.btnEditar.setStyleSheet("background-color:#B0B0B0;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
        self.layoutPrincipal.addWidget(self.btnEditar)
    def agregarTareaUsuario(self):
        conexion = sqlite3.connect("../databases/tareas.db")
        cursor = conexion.cursor()
        tarea = self.editTarea.text() +"("+ self.editUsuario.text()+")"
        cursor.execute("INSERT INTO tareas(tarea)VALUES (?)", (tarea,))
        self.editTarea.clear()
        conexion.commit()
        conexion.close()
        QMessageBox.information(self, "Tarea agregada", f"Tarea {tarea} agregada correctamente")
        self.close()
    def centrarVentana(self):
        screen = QApplication.primaryScreen().availableGeometry()
        ventana = self.frameGeometry()
        ventana.moveCenter(screen.center())
        self.move(ventana.topLeft())


class DialogoEditar(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,300,300)
        self.centrarVentana()
        self.setStyleSheet("background-color:#444444")
        self.setWindowTitle("Editar tarea")
        self.layoutPrincipal=QVBoxLayout()
        self.setLayout(self.layoutPrincipal)
        # LABEL TITULO
        lblTitulo = QLabel("TAREA")
        lblTitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lblTitulo.setStyleSheet(
            "background-color: #444444; font-size:28px;color: black; font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
        self.layoutPrincipal.addWidget(lblTitulo)
        #EDIT CONTACTO
        self.editTarea=QLineEdit()
        self.editTarea.setPlaceholderText("Introduzca la tarea")
        self.editTarea.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.editTarea.setStyleSheet(
            "background-color:white;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);")
        self.layoutPrincipal.addWidget(self.editTarea)
        #BOTON AGREGAR
        self.btnEditar=QPushButton("Editar")
        self.btnEditar.clicked.connect(self.editarTarea)
        self.btnEditar.setStyleSheet("background-color:#B0B0B0;font-size:14px;border-radius: 10px;padding: 20px;margin: 10px;box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);font-family: 'Comic Sans MS', sans-serif; font-weight: bold;")
        self.layoutPrincipal.addWidget(self.btnEditar)
    def editarTarea(self):
        tarea = self.editTarea.text()

        try:
            conexion=sqlite3.connect("../databases/tareas.db")
            cursor=conexion.cursor()

            cursor.execute("SELECT tarea FROM tareas WHERE tarea=?",(tarea,))

            tarea_encontrada=cursor.fetchone()
            if tarea_encontrada:
                # Insertar la tarea en tareasAcabadas
                cursor.execute("INSERT INTO tareasAcabadas(tarea) VALUES(?)", (tarea_encontrada[0],))

                # Eliminar la tarea de la tabla tareas
                cursor.execute("DELETE FROM tareas WHERE tarea=?", (tarea_encontrada[0],))

                # Confirmar cambios
                conexion.commit()
                print("Tarea movida a tareasAcabadas correctamente")

            else:
                print("Tarea no encontrada")
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")

        QMessageBox.information(self,"Tarea finalizada",f"Tarea {tarea} finalizada correctamente")
        self.close()

    def centrarVentana(self):
        screen = QApplication.primaryScreen().availableGeometry()
        ventana = self.frameGeometry()
        ventana.moveCenter(screen.center())
        self.move(ventana.topLeft())

if __name__=="__main__":
    baseDatos()
    app=QApplication([])
    ventana=ListaTareas()
    ventana.show()
    sys.exit(app.exec())