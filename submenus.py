import PySimpleGUI as sg
import psycopg2 as db

class crear_usuarios:
    layout = [[]]

    def __init__(self, conn):
        self.conn = conn
        self.layout = [[sg.Text("Username: "), sg.Input(size=(10, 1), key='-CODIGOINPUT-')],
                       [sg.Text("Password: "), sg.Input(size=(20, 1), key='-PASSWORDINPUT-')],
                       [sg.Text("Nombre:\t  "), sg.Input(size=(20, 1), key='-NOMBREINPUT-')],
                       [sg.Text("Turno:\t  "), sg.Input(size=(20, 1), key='-TURNOINPUT-')],
                       [sg.Text("Rol:\t  "),  sg.Combo(('Admin', 'Operador', 'Esclavo'), key='-ROLINPUT-')],
                       [sg.Button('Crear')]
                       ]

    def ejecutar(self):
        cur = self.conn.cursor()
        window = sg.Window("Crear usuario", self.layout)
        while True:
            event, values = window.read()
            if event == 'Crear':
                cur.execute('INSERT INTO usuario '
                            'VALUES(%s, %s, %s, %s, %s)',
                            (values['-CODIGOINPUT-'],
                             values['-PASSWORDINPUT-'],
                             values['-NOMBREINPUT-'],
                             values['-TURNOINPUT-'],
                             values['-ROLINPUT-'],))
                break
            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()

class editar_usuarios:
    layout = [[]]

    def __init__(self, conn):
        self.conn = conn
        self.layout=[[sg.Text("Ingrese username del usuario a editar: "), sg.Input(size=(10, 1), key='-CODIGOINPUT-'), sg.Button('Buscar')],
                     [sg.Text("Password: "), sg.Input(size=(20, 1), key='-PASSWORDINPUT-')],
                     [sg.Text("Nombre:\t  "), sg.Input(size=(20, 1), key='-NOMBREINPUT-')],
                     [sg.Text("Turno:\t  "), sg.Input(size=(20, 1), key='-TURNOINPUT-')],
                     [sg.Text("Rol:\t  "),  sg.Combo(('Admin', 'Operador', 'Esclavo'), key='-ROLINPUT-')],
                     [sg.Button('Actualizar')]
                     ]


    def ejecutar(self):
        cur = self.conn.cursor()
        window = sg.Window("Editar usuario", self.layout)
        while True:
            event, values = window.read()
            if  event == 'Buscar':
                cur.execute('select * from usuario where username = %s', (values['-CODIGOINPUT-'],))
                usuarios = cur.fetchall()
                if len(usuarios) > 0:
                    window['-PASSWORDINPUT-'].update(usuarios[0][1])
                    window['-NOMBREINPUT-'].update(usuarios[0][2])
                    window['-TURNOINPUT-'].update(usuarios[0][3])
                    window['-ROLINPUT-'].update(usuarios[0][4])

            elif event == 'Actualizar':
                cur.execute('UPDATE usuario '
                            'SET password = %s, '
                            'nombre = %s, '
                            'turno = %s,'
                            'rol = %s'
                            'WHERE username = %s',
                            (values['-PASSWORDINPUT-'],
                             values['-NOMBREINPUT-'],
                             values['-TURNOINPUT-'],
                             values['-ROLINPUT-'],
                             values['-CODIGOINPUT-'], ))
                break
            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()

class editar_productos:
    layout = [[]]
    def __init__(self, conn):
        self.conn = conn
        self.layout=[[sg.Text("Ingrese codigo del producto a editar: "), sg.Input(size=(10, 1), key='-CODIGOINPUT-'), sg.Button('Buscar')],
                     [sg.Text("Departamento:\t "), sg.Input(size=(20, 1), key='-DPTOINPUT-')],
                     [sg.Text("Nombre:\t "), sg.Input(size=(20, 1), key='-NOMBREINPUT-')],
                     [sg.Text("Marca:\t "), sg.Input(size=(20, 1), key='-MARCAINPUT-')],
                     [sg.Text("Tamaño:\t "), sg.Input(size=(20, 1), key='-SIZEINPUT-')],
                     [sg.Text("Color:\t "), sg.Input(size=(20, 1), key='-COLORINPUT-')],
                     [sg.Text("Precio:\t "), sg.Input(size=(20, 1), key='-PRECIOINPUT-')],
                     [sg.Text("Ubicacion:\t "), sg.Input(size=(20, 1), key='-UBICACIONINPUT-')],
                     [sg.Text("Disponible:\t "), sg.Combo(('t', 'f'), key='-DISPONIBLEINPUT-')],
                     [sg.Text("Minima Existencia:\t"), sg.Input(size=(20, 1), key='-MINEXISTENCIAINPUT-')],
                     [sg.Button('Actualizar')]
                     ]

    def ejecutar(self):
        cur = self.conn.cursor()
        window = sg.Window('Editar Productos',self.layout)
        while True:
            event, values = window.read()
            if event == 'Buscar':
                cur.execute('select * from producto where sku = %s', (values['-CODIGOINPUT-'],))
                prod = cur.fetchall()
                if len(prod) > 0:
                    window['-DPTOINPUT-'].update(prod[0][7])
                    window['-NOMBREINPUT-'].update(prod[0][2])
                    window['-MARCAINPUT-'].update(prod[0][3])
                    window['-SIZEINPUT-'].update(prod[0][4])
                    window['-COLORINPUT-'].update(prod[0][5])
                    window['-PRECIOINPUT-'].update(prod[0][6])
                    window['-UBICACIONINPUT-'].update(prod[0][1])
                    window['-DISPONIBLEINPUT-'].update(prod[0][9])
                    window['-MINEXISTENCIAINPUT-'].update(prod[0][10])

            elif event == 'Actualizar':
                cur.execute('UPDATE producto '
                            'SET depto = %s, '
                            'nombre = %s, '
                            'marca = %s,'
                            'size = %s,'
                            'color = %s,'
                            'precio = %s,'
                            'ubicacion = %s,'
                            'disponible = %s,'
                            'minexistencia = %s'
                            'WHERE sku = %s',
                            (values['-DPTOINPUT-'],
                             values['-NOMBREINPUT-'],
                             values['-MARCAINPUT-'],
                             values['-SIZEINPUT-'],
                             values['-COLORINPUT-'],
                             values['-PRECIOINPUT-'],
                             values['-UBICACIONINPUT-'],
                             values['-DISPONIBLEINPUT-'],
                             values['-MINEXISTENCIAINPUT-'],
                             values['-CODIGOINPUT-'],))
                break

            if event == sg.WIN_CLOSED:
                break
        cur.close()
        window.close()