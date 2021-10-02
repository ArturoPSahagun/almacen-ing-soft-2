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


