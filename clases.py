import PySimpleGUI as sg
import psycopg2 as db
from datetime import datetime
from tkcalendar import *
from tkinter import *
import smtplib, ssl
import sys

class Feature_salida:
    layout = [[]]
    fecha = ''
    folio = ''


    def __init__(self, conn, user):
        self.conn = conn
        self.user = user
        cur = conn.cursor()
        self.fecha = datetime.today().strftime("%d/%m/%Y")
        cur.execute('select idSalida from salida')
        self.folio=len(cur.fetchall())+1
        self.layout= [
                 [sg.Text("Fecha: "), sg.Text(self.fecha, text_color='black', background_color='lightgray'), sg.Text("\t\tFolio: ",), sg.Text(self.folio, text_color='black', background_color='lightgray')],
                 [sg.Text('')],
                 [sg.Frame('Codigo',[[sg.Input(size=(10, 1), key='-CODIGOINPUT-')]]), sg.Frame('Cantidad', [[sg.Input(size=(10, 1), key='-CANTIDADINPUT-')]]), sg.Button("Registrar")],
                 [sg.Button('Salida a futuro'), sg.Input(size=(10, 1), key='-FUTUROINPUT-', disabled=True, text_color='black' )],
                 #[sg.Text("Codigo:"), sg.Input(size=(10, 1), enable_events=True, key='-CODIGOINPUT-'),
                 # sg.Text("Cantidad: "), sg.Input(size=(10, 1), enable_events=True, key='-CANTIDADINPUT-'), sg.Button('Registrar')],
                 [sg.Tree(data=sg.TreeData(),
                          text_color='black',
                          headings=['SKU','     Nombre     ','Cant'],
                          auto_size_columns=True,
                          justification='center',
                          num_rows=5,
                          col0_width=4,

                          def_col_width=20,
                          key='-TREE-',
                          enable_events=True)],
                 [sg.Frame('Motivo',[[sg.Input(size=(40,3), key=('-MOTIVOINPUT-'))]],)],
                 [sg.Button('Terminar')]]

    def ejecutar(self):
        cur = self.conn.cursor()
        nombre=''
        data = sg.TreeData()
        items = [()]
        items.pop(0)
        window = sg.Window("Salidas", self.layout)
        while True:
            event, values = window.read()

            if event=='Salida a futuro': #Funcion para mostrar calendario
                root = Tk() 
                root.geometry("400x400")  
                cal = Calendar(root, selectmode="day",firstweekday="monday",
                            day=int(datetime.now().strftime("%d")),
                            month=int(datetime.now().strftime("%m")), 
                            year=int(datetime.now().strftime("%Y")),
                            disabledforeground="green",
                            bordercolor="green",
                            background="green",
                            normalbackground="lightgreen",
                            weekendbackground="darkgreen",
                            weekendforeground ="black" ,
                            disabledbackground="green",
                            date_pattern = "y-mm-dd")
                cal.pack(padx=10,pady = 20) 
                def grad_date(): 
                    date.config(text = "La fecha seleccionada es: " + cal.get_date())
                    window['-FUTUROINPUT-'].Update(cal.get_date())
                def borrar_date():
                    window['-FUTUROINPUT-'].Update('')
                Button(root, text = "Fijar Fecha",
                    command = grad_date).pack(pady = 20)
                Button(root, text="Borrar Fecha",
                       command=borrar_date).pack(pady=20)
                date = Label(root, text = "") 
                date.pack(pady = 20)

                #Termina funcion del calendario


            if event == 'Registrar':
                cur.execute('select nombre from producto where sku=\''+values['-CODIGOINPUT-']+'\' AND disponible = True')
                nombre = cur.fetchall()
                if(len(nombre) == 0):
                    sg.popup('Error', "Ese codigo no existe en la base de datos\nSi es un producto nuevo registrelo en el apartado de altas", )
                else:
                    items.append((values['-CODIGOINPUT-'], values['-CANTIDADINPUT-']))
                    data.insert('', values['-CODIGOINPUT-'], '#' + str(len(items)), values=[values['-CODIGOINPUT-'], nombre[0][0], values['-CANTIDADINPUT-']])
                    window['-TREE-'].update(data)
                    window['-CODIGOINPUT-'].update('')
                    window['-CANTIDADINPUT-'].update('')
            if event == 'Terminar':
                if values['-FUTUROINPUT-'] == '':
                    cur.execute('insert into salida(iduser, motivo) values(%s, %s) returning idsalida', (self.user, values['-MOTIVOINPUT-']))
                else:
                    cur.execute('insert into salida(iduser, motivo, futuro) values(%s, %s, %s) returning idsalida', (self.user, values['-MOTIVOINPUT-'], values['-FUTUROINPUT-']))

                idSalida = cur.fetchall()[0][0]
                for prod in items:
                    cur.execute('insert into mercanciaEnSalida (sku, idsalida, cantidad) values(%s, %s, %s)', (prod[0], idSalida, prod[1]))
                    if values['-FUTUROINPUT-'] == '':
                        cur.execute('update producto set existencias = existencias - %s where sku = %s', (prod[1], prod[0]))
                break
            if event == sg.WIN_CLOSED:
               break
        cur.close()
        window.close()

class Feature_entrada:
    layout = [[]]
    fecha = ''
    folio = ''

    def __init__(self, conn, user):
        self.conn = conn
        self.user = user
        cur = conn.cursor()
        self.fecha = datetime.today().strftime("%d/%m/%Y")
        cur.execute('select idEntrada from entrada')
        self.folio=len(cur.fetchall())+1
        self.layout= [
                 [sg.Text("Fecha: "), sg.Text(self.fecha, text_color='black', background_color='lightgray'), sg.Text("\t\tFolio: ",), sg.Text(self.folio, text_color='black', background_color='lightgray')],
                 [sg.Text('')],
                 [sg.Frame('Codigo',[[sg.Input(size=(10, 1), key='-CODIGOINPUT-')]]), sg.Frame('Cantidad', [[sg.Input(size=(10, 1), key='-CANTIDADINPUT-')]]), sg.Button("Registrar")],
                 [sg.Button('Entrada a futuro'), sg.Input(size=(10, 1), key='-FUTUROINPUT-',  disabled=True, text_color='black' )],
                 #[sg.Text("Codigo:"), sg.Input(size=(10, 1), enable_events=True, key='-CODIGOINPUT-'),
                 # sg.Text("Cantidad: "), sg.Input(size=(10, 1), enable_events=True, key='-CANTIDADINPUT-'), sg.Button('Registrar')],
                 [sg.Tree(data = sg.TreeData(),
                          text_color='black',
                          headings=['SKU','     Nombre     ','Cant'],
                          auto_size_columns=True,
                          justification='center',
                          num_rows=5,
                          col0_width=4,

                          def_col_width=20,
                          key='-TREE-',
                          enable_events=True)],
                 [sg.Frame('Observación',[[sg.Input(size=(40,3), key=('-MOTIVOINPUT-'))]],)],
                 [sg.Button('Terminar')]]

    def ejecutar(self):
        cur = self.conn.cursor()
        nombre=''
        data = sg.TreeData()
        items = [()]
        items.pop(0)
        window = sg.Window("Entradas", self.layout)
        while True:
            event, values = window.read()


            if event=='Entrada a futuro': #Funcion para mostrar calendario
                root = Tk() 
                root.geometry("400x400")  
                cal = Calendar(root, selectmode="day",firstweekday="monday",
                            day=int(datetime.now().strftime("%d")),
                            month=int(datetime.now().strftime("%m")), 
                            year=int(datetime.now().strftime("%Y")),
                            disabledforeground="green",
                            bordercolor="green",
                            background="green",
                            normalbackground="lightgreen",
                            weekendbackground="darkgreen",
                            weekendforeground ="black" ,
                            disabledbackground="green",
                            date_pattern = "y-mm-dd")
                cal.pack(padx=10,pady = 20) 
                def grad_date(): 
                    date.config(text = "Selected Date is: " + cal.get_date())
                    window['-FUTUROINPUT-'].Update(cal.get_date())
                def borrar_date():
                    window['-FUTUROINPUT-'].Update('')
                Button(root, text="Fijar Fecha",
                       command=grad_date).pack(pady=20)
                Button(root, text="Borrar Fecha",
                       command=borrar_date).pack(pady=20)
                date = Label(root, text = "") 
                date.pack(pady = 20) 
                #Termina funcion del calendario


            if event == 'Registrar':
                cur.execute('select nombre from producto where sku=\''+values['-CODIGOINPUT-']+'\' AND disponible = True')
                nombre = cur.fetchall()
                if(len(nombre) == 0):
                    sg.popup('Error', "Ese codigo no existe en la base de datos\nSi es un producto nuevo registrelo en el apartado de altas", )
                else:
                    items.append((values['-CODIGOINPUT-'], values['-CANTIDADINPUT-']))
                    data.insert('', values['-CODIGOINPUT-'], '#' + str(len(items)), values=[values['-CODIGOINPUT-'], nombre[0][0], values['-CANTIDADINPUT-']])
                    window['-TREE-'].update(data)
                    window['-CODIGOINPUT-'].update('')
                    window['-CANTIDADINPUT-'].update('')
            if event == 'Terminar':
                if values['-FUTUROINPUT-'] == '':
                    cur.execute('insert into entrada(iduser, observacion) values(%s, %s) returning identrada',(self.user, values['-MOTIVOINPUT-']))
                else:
                    cur.execute('insert into entrada(iduser, observacion, futuro) values(%s, %s, %s) returning identrada', (self.user, values['-MOTIVOINPUT-'], values['-FUTUROINPUT-']))
                idEntrada = cur.fetchall()[0][0]
                for prod in items:
                    cur.execute('insert into mercanciaEnEntrada (sku, identrada, cantidad) values(%s, %s, %s)', (prod[0], idEntrada, prod[1]))
                    if values['-FUTUROINPUT-'] == '':
                        cur.execute('update producto set existencias = existencias + %s where sku = %s', (prod[1], prod[0]))
                break
            if event == sg.WIN_CLOSED:
               break
        cur.close()
        window.close()

class Feature_alta:
    layout = [[]]

    def __init__(self, conn, user):
        self.conn = conn
        self.user = user
        self.layout = [[sg.Text("Codigo:\t\t"), sg.Input(size=(20, 1), enable_events=True, key='-CODIGOINPUT-')],
                       [sg.Text("Departamento:\t"), sg.Input(size=(20, 1), enable_events=True, key='-DPTOINPUT-')],
                       [sg.Text("Nombre:\t\t"), sg.Input(size=(20, 1), enable_events=True, key='-NOMBREINPUT-')],
                       [sg.Text("Marca:\t\t"), sg.Input(size=(20, 1), enable_events=True, key='-MARCAINPUT-')],
                       [sg.Text("Tamaño:\t\t"), sg.Input(size=(20, 1), enable_events=True, key='-SIZEINPUT-')],
                       [sg.Text("Color:\t\t"), sg.Input(size=(20, 1), enable_events=True, key='-COLORINPUT-')],
                       [sg.Text("Precio:\t\t"), sg.Input(size=(20, 1), enable_events=True, key='-PRECIOINPUT-')],
                       [sg.Text("Ubicacion:\t"), sg.Input(size=(20, 1), enable_events=True, key='-UBICACIONINPUT-')],
                       [sg.Text("Minima Existencia:\t"), sg.Input(size=(20, 1), enable_events=True, key='-MINEXISTENCIAINPUT-')],
                       [sg.Button('Registrar producto nuevo')]]


    def ejecutar(self):
        cur = self.conn.cursor()
        window = sg.Window("Altas", self.layout)
        while True:
            event, values = window.read()
            if event == 'Registrar producto nuevo':
                cur.execute('insert into producto (sku, depto, nombre, marca, size, color, precio, ubicacion, minexistencia, existencias)'
                            'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, 0);',
                            (values['-CODIGOINPUT-'],values['-DPTOINPUT-'],values['-NOMBREINPUT-'],values['-MARCAINPUT-'],values['-SIZEINPUT-'],
                             values['-COLORINPUT-'],values['-PRECIOINPUT-'],values['-UBICACIONINPUT-'],values['-MINEXISTENCIAINPUT-']))
                self.conn.commit()
                sg.popup("Éxito", "El producto " + values['-NOMBREINPUT-'] + " se ha registrado correctamente.")
                break
            if event == sg.WIN_CLOSED:
               break
        cur.close()
        window.close()

class Feature_Baja:
    layout = [[]]

    def __init__(self, conn):
        self.conn = conn
        self.layout = [[sg.Text("Ingrese SKU del producto a eliminar: "), sg.Input(size=(10, 1), key='-CODIGOINPUT-', enable_events=True)],
                       [sg.Text(' ', key='-CONDENADO-', size=(50, 1), background_color='lightgray')],
                       [sg.Button('Eliminar'), sg.Button('Cancelar')]
                       ]

    def ejecutar(self):
        cur = self.conn.cursor()
        window = sg.Window("Eliminar usuario", self.layout)
        while True:
            event, values = window.read()
            if values['-CODIGOINPUT-'] != '':
                cur.execute('select nombre, marca, color from producto where sku = %s and disponible = \'t\'', (values['-CODIGOINPUT-'],))
                cond = cur.fetchall()
                if len(cond) > 0:
                    window['-CONDENADO-'].update(cond[0][0] + ' ' + cond[0][2] + ' marca ' + cond[0][1])
            if event == 'Eliminar':
                cur.execute('update producto set disponible = \'f\' where sku = %s', (values['-CODIGOINPUT-'],))
                break
            if event == 'Cancelar':
                break
            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()

class Feature_reporte:
    layout = [[]]
    fecha = ''
    fechaINI = ''

    def __init__(self, conn, user):
        self.conn = conn
        self.user = user
        cur = conn.cursor()
        self.fecha = datetime.today().strftime("%d/%m/%Y")

        self.layout=[
            [sg.Text("Fecha de hoy: "), sg.Text(self.fecha, text_color='black', background_color='lightgray'),],
            [sg.Text('')],
            [sg.Text("Generar reportes generales")],
            [sg.Text('')],
            [sg.Button('Fecha inicial'), sg.Input(size=(10, 1), key='-INICIAL-', disabled=True, text_color='black' )],
            [sg.Button('Fecha final'), sg.Input(size=(10, 1), key='-FINAL-',  disabled=True, text_color='black' )],
            [sg.Text('Email: '), sg.Input(size=(20, 1), key='-EMAILINPUT-')],
            [sg.Button('Confirmar')]]

    def ejecutar(self):
        cur=self.conn.cursor()
        items = [()]
        items.pop(0)
        window=sg.Window("Reporte",self.layout)
        while True:
            event,values=window.read()      
            
            
            if event == 'Fecha inicial':  #Funcion para mostrar calendario
                root = Tk() 
                root.geometry("400x400")  
                cal = Calendar(root, selectmode="day",firstweekday="monday",
                            day=int(datetime.now().strftime("%d")),
                            month=int(datetime.now().strftime("%m")), 
                            year=int(datetime.now().strftime("%Y")),
                            disabledforeground="green",
                            bordercolor="green",
                            background="green",
                            normalbackground="lightgreen",
                            weekendbackground="darkgreen",
                            weekendforeground ="black" ,
                            disabledbackground="green",
                            date_pattern = "y-mm-dd")
                cal.pack(padx=10,pady = 20) 

                def grad_date():
                    date.config(text = "Fecha seleccionada: " + cal.get_date())
                    window['-INICIAL-'].Update(cal.get_date())
                Button(root, text="Fijar Fecha",
                       command=grad_date).pack(pady=20)

                date = Label(root, text = "") 
                date.pack(pady = 20) 
                #Termina funcion del calendario
            
            
            if event == 'Fecha final': #Funcion para mostrar calendario
                root = Tk() 
                root.geometry("400x400")  
                cal = Calendar(root, selectmode="day",firstweekday="monday",
                            day=int(datetime.now().strftime("%d")),
                            month=int(datetime.now().strftime("%m")), 
                            year=int(datetime.now().strftime("%Y")),
                            disabledforeground="green",
                            bordercolor="green",
                            background="green",
                            normalbackground="lightgreen",
                            weekendbackground="darkgreen",
                            weekendforeground ="black" ,
                            disabledbackground="green",
                            date_pattern = "y-mm-dd")
                cal.pack(padx=10,pady = 20)

                def grad_date():
                    date.config(text="Fecha seleccionada: " + cal.get_date())
                    window['-FINAL-'].Update(cal.get_date())
                Button(root, text="Fijar Fecha",
                       command=grad_date).pack(pady=20)
                date = Label(root, text = "") 
                date.pack(pady = 20) 
                #Termina funcion del calendario
            if event == sg.WIN_CLOSED:
                break
            if event == 'Confirmar':
                cur.execute("select * from producto")
                estado_actual = cur.fetchall()
                cur.execute('select * from entrada where fecha > %s and fecha < %s', (values['-INICIAL-'], values['-FINAL-']))
                entradas = cur.fetchall()
                cur.execute('select * from salida where fecha > %s and fecha < %s', (values['-INICIAL-'], values['-FINAL-']))
                salidas = cur.fetchall()
                filename = datetime.now().strftime("%d-%b-%Y-%H:%M:%S") + ".txt"
                with open(filename, "x") as reportefile:
                    reportefile.write('REPORTE DEL SISTEMA DE ALMACEN DE UNA TIENDA DEPARTAMENTAL\n\n\n')
                    reportefile.write("------------ESTADO ACTUAL DE LA BASE DE DATOS--------------\n\n")
                    for row in estado_actual:
                        reportefile.write('Codigo: ' + row[0] + '\t\t\tExistencias: ' + str(row[9]) + '\n')
                        reportefile.write('Descripcion: ' + row[2] + ' ' + row[4] + ' marca ' + row[3] + ' color ' + row[5] + '\n')
                        reportefile.write('Departamento: ' + row[7] + '\tPrecio: ' + str(row[6]) + '\tUbicación: ' + row[1] + '\n\n')
                    reportefile.write("\n\n\nMOVIMIENTOS REGISTRADOS DEL DIA " + values['-INICIAL-'] + ' AL DIA ' + values['-FINAL-'])
                    reportefile.write("\n\n------------------------ENTRADAS--------------------------\n")
                    for row in entradas:
                        reportefile.write('Fecha: ' + str(row[2]) + '\t\tResponsable: ' + row[1] + '\n')
                        reportefile.write('Observacion: ' + row[3] +  '\nProductos:\n')
                        cur.execute('select mercanciaenentrada.sku, nombre, cantidad from mercanciaenentrada inner join producto on mercanciaenentrada.sku = producto.sku where identrada = %s', (row[0],))
                        productos = cur.fetchall()
                        for p in productos:
                            reportefile.write('SKU: ' + str(p[0]) + ' Nombre: ' + p[1] + '\tCantidad: ' + str(p[2]) + '\n')
                        reportefile.write('\n\n\n')
                    reportefile.write("\n\n------------------------SALIDAS--------------------------\n")
                    for row in salidas:
                        reportefile.write('Fecha: ' + str(row[2]) + '\t\tResponsable: ' + row[1] + '\n')
                        reportefile.write('Motivo: ' + row[3] +  '\nProductos:\n')
                        cur.execute('select mercanciaensalida.sku, nombre, cantidad from mercanciaensalida inner join producto on mercanciaensalida.sku = producto.sku where idsalida = %s', (row[0],))
                        productos = cur.fetchall()
                        for p in productos:
                            reportefile.write('SKU: ' + str(p[0]) + ' Nombre: ' + p[1] + '\tCantidad: ' + str(p[2]) + '\n')
                        reportefile.write('\n\n\n')

                if values['-EMAILINPUT-'] != '':
                    port = 465
                    smtp_server = "smtp.gmail.com"
                    sender_email = "almacenpy.ingsoft2@gmail.com"  # Enter your address
                    receiver_email = values['-EMAILINPUT-']  # Enter receiver address
                    password = 'muladhara'
                    with open(filename, "r") as myfile:
                        message = myfile.read().encode('utf-8')
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, message)
                break
        cur.close()
        window.close()


class Feature_conteo:
    layout = [[]]
    def __init__(self, conn, user):
        self.conn = conn
        self.user = user
        cur = conn.cursor
        self.layout= [
                 [sg.Frame('Codigo',[[sg.Input(size=(10, 1), key='-CODIGOINPUT-')]]), sg.Frame('Cantidad', [[sg.Input(size=(10, 1), key='-CANTIDADINPUT-')]]), sg.Button("Registrar")],
                 [sg.Tree(data = sg.TreeData(),
                          text_color='black',
                          headings=['SKU','     Nombre     ','Cant'],
                          auto_size_columns=True,
                          justification='center',
                          num_rows=5,
                          col0_width=4,

                          def_col_width=20,
                          key='-TREE-',
                          enable_events=True)],
                 [sg.Button('Terminar')]]

    def ejecutar(self):
        cur = self.conn.cursor()
        nombre = ''
        data = sg.TreeData()
        items = [()]
        items.pop(0)
        window = sg.Window("Conteo", self.layout)
        while True:
            event, values = window.read()
            if event == 'Registrar':
                cur.execute(
                    'select nombre from producto where sku=\'' + values['-CODIGOINPUT-'] + '\' AND disponible = True')
                nombre = cur.fetchall()
                if (len(nombre) == 0):
                    sg.popup('Error',
                             "Ese codigo no existe en la base de datos\nSi es un producto nuevo registrelo en el apartado de altas", )
                else:
                    items.append((values['-CODIGOINPUT-'], values['-CANTIDADINPUT-']))
                    data.insert('', values['-CODIGOINPUT-'], '#' + str(len(items)),
                                values=[values['-CODIGOINPUT-'], nombre[0][0], values['-CANTIDADINPUT-']])
                    window['-TREE-'].update(data)
                    window['-CODIGOINPUT-'].update('')
                    window['-CANTIDADINPUT-'].update('')
            if event == 'Terminar':
                cur.execute('alter table producto add column temporal int default (0);')
                cur.execute('alter table producto add column diferencia int;')
                for prod in items:
                    cur.execute('update producto set temporal = %s where sku = %s', (prod[1], prod[0]))
                cur.execute('update producto set diferencia = temporal - existencias;')
                cur.execute('select sku, diferencia, nombre, marca, size, color, precio from producto;')
                resultados = cur.fetchall()
                diftotal = 0.0
                dif = 0.0
                with open('Conteo-' + datetime.today().strftime("%d-%b-%Y-%H:%M:%S") + ".txt", "x") as reportefile:
                    reportefile.write('---RESULTADOS DEL CONTEO DE EXISTENCIAS CON FECHA: ' + datetime.today().strftime("%d/%m/%Y") + '---\n\n')
                    reportefile.write('SKU\tDescripcion\t\tDiferencias\tTotal $\n')
                    for row in resultados:
                        descripcion = row[2][:10] + row[3][:4] + row[4] + row[5][:4]
                        dif = row[6] * row[1]
                        diftotal = float(diftotal) + float(dif)
                        reportefile.write(row[0] + '\t' + descripcion + '\t' + str(row[1]) + '\t\t' + str(dif) + '\n')
                    reportefile.write('\n\nDiferencia total en $: ' + str(diftotal))
                break

            if event == sg.WIN_CLOSED:
                break
        cur.execute('alter table producto drop column diferencia;')
        cur.execute('alter table producto drop column existencias;')
        cur.execute('alter table producto rename column temporal to existencias;')
        cur.execute('alter table producto rename column disponible to disp;')
        cur.execute('alter table producto add column disponible bool default (\'t\');')
        cur.execute('update producto set disponible = disp;')
        cur.execute('alter table producto drop column disp;')
        cur.close()
        window.close()

class Feature_bandeja:
    layout = [[]]
    def __init__(self, conn):
        self.conn = conn
        self.data = sg.TreeData()
        self.layout = [[sg.Text('Una vez resuelto el problema, seleccione la alerta correspondiente y haga clic en \"Descartar\"')],
            [sg.Tree(data = sg.TreeData(),
                     text_color='black',
                     headings=['Fecha/Hora'],
                     justification='center',
                     num_rows=10,
                     key='-NOTIFTREE-',
                     enable_events=True,
                     col0_width=60,
                     )],
            [sg.Button('Descartar')]]

    def ejecutar(self):
        cur = self.conn.cursor()
        window = sg.Window("Notificaciones", self.layout, finalize=True, location=(1600,0))
        self.getNotificaiones()
        window['-NOTIFTREE-'].update(self.data)
        self.data = sg.TreeData()
        while True:
            event, values = window.read()
            if event =='Descartar':
                cur.execute('delete from notificacion where sku = %s', window['-NOTIFTREE-'].SelectedRows)
                self.getNotificaiones()
                window['-NOTIFTREE-'].update(self.data)
                self.data = sg.TreeData()
            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()

    def getNotificaiones(self):
        cur = self.conn.cursor()
        cur.execute('select notificacion.sku, nombre, marca, size, color, fecha, tipo '
                    'from notificacion '
                    'inner join producto on notificacion.sku = producto.sku')
        contenido = cur.fetchall()
        for producto in contenido:
            if producto[6] == 'poco':
                self.data.insert('', producto[0],
                            '¡ඞAGUASඞ! El producto \"' + producto[0] + ' ' + producto[1] + ' ' + producto[2] + ' ' +
                            producto[3] + ' ' + producto[4] + '\" casi se agota (⚆ᗝ⚆)', values=[producto[5]])
            else:
                self.data.insert('', producto[0],
                            '¡👁J👁! El producto \"' + producto[0] + ' ' + producto[1] + ' ' + producto[2] + ' ' +
                            producto[3] + ' ' + producto[4] + '\" ya se acabo ʕ ͡° ʖ̯ ͡°ʔ', values=[producto[5]])
        cur.close()


















