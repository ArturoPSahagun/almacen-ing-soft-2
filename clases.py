import PySimpleGUI as sg
import psycopg2 as db
from datetime import datetime
from tkcalendar import *
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
                cur.execute('insert into salida(iduser, motivo) values(%s, %s) returning idsalida', (self.user, values['-MOTIVOINPUT-']))
                idSalida = cur.fetchall()[0][0]
                for prod in items:
                    cur.execute('insert into mercanciaEnSalida (sku, idsalida, cantidad) values(%s, %s, %s)', (prod[0], idSalida, prod[1]))
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
                cur.execute('insert into entrada(iduser, observacion) values(%s, %s) returning identrada', (self.user, values['-MOTIVOINPUT-']))
                idEntrada = cur.fetchall()[0][0]
                for prod in items:
                    cur.execute('insert into mercanciaEnEntrada (sku, identrada, cantidad) values(%s, %s, %s)', (prod[0], idEntrada, prod[1]))
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
                       [sg.Button('Registrar producto nuevo')]]


    def ejecutar(self):
        cur = self.conn.cursor()
        window = sg.Window("Altas", self.layout)
        while True:
            event, values = window.read()
            if event == 'Registrar producto nuevo':
                cur.execute('insert into producto (sku, depto, nombre, marca, size, color, precio, ubicacion, existencias)'
                            'values(%s, %s, %s, %s, %s, %s, %s, %s, 0);',
                            (values['-CODIGOINPUT-'],values['-DPTOINPUT-'],values['-NOMBREINPUT-'],values['-MARCAINPUT-'],values['-SIZEINPUT-'],
                             values['-COLORINPUT-'],values['-PRECIOINPUT-'],values['-UBICACIONINPUT-']))
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