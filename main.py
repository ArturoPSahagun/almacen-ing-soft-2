from clases import *
from submenus import *
import sys

def updateFields(cur, window):
    cur.execute('SELECT DISTINCT depto FROM producto')
    dptos = cur.fetchall()
    dptos = [i for sub in dptos for i in sub]
    dptos.insert(0, '')
    window['-DPTOINPUT-'].update(values=(dptos))
    cur.execute('SELECT DISTINCT marca FROM producto')
    marcas = cur.fetchall()
    marcas = [i for sub in marcas for i in sub]
    marcas.insert(0, '')
    window['-MARCAINPUT-'].update(values=(marcas))
    cur.execute('SELECT DISTINCT size FROM producto')
    sizes = cur.fetchall()
    sizes = [i for sub in sizes for i in sub]
    sizes.insert(0, '')
    window['-SIZEINPUT-'].update(values=(sizes))
    cur.execute('SELECT DISTINCT color FROM producto')
    colores = cur.fetchall()
    colores = [i for sub in colores for i in sub]
    colores.insert(0, '')
    window['-COLORINPUT-'].update(values=(colores))

def lookForNotifications(cur):
    cur.execute('select sku from producto where existencias < minexistencia and existencias > 0 and disponible = \'t\'')
    pocoContent = cur.fetchall()
    cur.execute('select sku from producto where existencias < 1 and disponible = \'t\'')
    ceroContent = cur.fetchall()
    for product in pocoContent:
        cur.execute('insert into notificacion(sku, fecha, tipo)'
                    'select %s, LOCALTIMESTAMP, %s'
                        'where not exists ('
                            'select 1 from notificacion where sku = %s and tipo = %s)', (product[0], 'poco', product[0], 'poco'))
    for product in ceroContent:
        cur.execute('insert into notificacion(sku, fecha, tipo)'
                    'select %s, LOCALTIMESTAMP, %s'
                        'where not exists ('
                            'select 1 from notificacion where sku = %s and tipo = %s)', (product[0], 'cero', product[0], 'cero'))

def lookForFutureES(cur):
    cur.execute('select identrada from entrada where futuro <= now() at time zone \'America/Chicago\'')
    entradas = cur.fetchall()
    for e in entradas:
        cur.execute('select sku, cantidad from mercanciaenentrada where identrada = %s', (e[0],))
        productos = cur.fetchall()
        for p in productos:
            cur.execute('update producto set existencias = existencias + %s where sku = %s', (p[1], p[0]))
        cur.execute('update entrada set fecha = futuro where identrada = %s', (e[0],))
        cur.execute('update entrada set futuro = null where identrada = %s', (e[0],))

    cur.execute('select idsalida from salida where futuro <= now() at time zone \'America/Chicago\'')
    salidas = cur.fetchall()
    for s in salidas:
        cur.execute('select sku, cantidad from mercanciaensalida where idsalida = %s', (s[0],))
        productos = cur.fetchall()
        for p in productos:
            cur.execute('update producto set existencias = existencias - %s where sku = %s', (p[1], p[0]))
        cur.execute('update salida set fecha = futuro where idsalida = %s', (s[0],))
        cur.execute('update salida set futuro = null where idsalida = %s', (s[0],))


#Conexion a la database
conn = db.connect(
    database = 'd4i0d59nudi76s',
    user = 'lhxbvkydfkbtip',
    password = 'bd17774e8cc4b1967a0b458d4a47222b2821572fc08a104906a4fac10748141c',
    host = 'ec2-54-147-93-73.compute-1.amazonaws.com',
    port = '5432'
)
conn.autocommit = True
cur = conn.cursor()
sg.ChangeLookAndFeel('LightGreen6')

user = ''
rol = ''
nombre = ''
treedata = sg.TreeData()


layout_login = [[sg.Text("Introduzca su usuario y contrase??a")],
                [sg.Text("Usuario:\t\t"), sg.Input(size=(20, 1), enable_events=True, key='-NAMEINPUT-')],
                [sg.Text("Contrase??a:\t"), sg.Input(size=(20, 1), enable_events=True, key='-PASSWORDINPUT-', password_char='???')],
                [sg.Button('Login', bind_return_key=True)],
                [sg.Text("", key='-ERRORTEXT-')]
                ]
window = sg.Window('Sistema de Almacen', layout_login)
while True:
    event, values = window.read()
    if event == "Login" :
        cur.execute('select password, nombre, rol from usuario where username = \'' + values['-NAMEINPUT-'] + '\'')
        query = cur.fetchall()
        passw = ' '
        if len(query) > 0:
            passw = query[0][0]

        if passw != values['-PASSWORDINPUT-']:
            sg.Popup('Error', 'Usuario o contrase??a incorrectos')
            window['-PASSWORDINPUT-'].Update('')
            continue
        else:
            user = values['-NAMEINPUT-']
            nombre = query[0][1]
            rol = query[0][2]
            window.close()
            break
        window.close()
        break
    if event == sg.WIN_CLOSED :
        sys.exit()
        break

consult_layout = [[sg.Text("Codigo:"), sg.Input(size=(5, 1), enable_events=True, key='-CODIGOINPUT-'),
                   sg.Text("Nombre:"), sg.Input(size=(10,1),enable_events=True, key='-NAMEINPUT-'),
                   sg.Text('Departamento:'), sg.Combo((), enable_events=True, key='-DPTOINPUT-', size=(10,1))],
                  [sg.Text('Marca:'), sg.Combo((), enable_events=True, key='-MARCAINPUT-', size=(10,1)),
                   sg.Text('Tama??o:'), sg.Combo((), enable_events=True, key='-SIZEINPUT-', size=(5,1)),
                   sg.Text('Color:'), sg.Combo((), enable_events=True, key='-COLORINPUT-', size=(10,1)),
                   sg.Button('Buscar')],
                  [sg.Tree(data=treedata,
                           text_color='black',
                           headings=['   Nombre   ', 'Dpto', 'Marca', 'Tama??o', 'Color', 'Precio', 'Exis.','Ubicacion'],
                           auto_size_columns=True,
                           justification='center',
                           num_rows=20,
                           col0_width=6,
                           key='-LISTA-',
                           enable_events=True)]]

button_layout = [[sg.Button('Entradas', size=(10, 3))],
                 [sg.Button('Salidas', size=(10, 3))],
                 [sg.Button('Altas', size=(10, 3))],
                 [sg.Button('Bajas', size=(10, 3))],
                 [sg.Button('Conteo', size=(10, 3))],
                 [sg.Button('Conteo Indivual', size=(10, 3))],
                 [sg.Button('Reporte', size=(10,3))],
                 [sg.Button('Salir', size=(10, 3))]]

menu_layout = [
                ['Usuarios',
                    ['Crear usuario', 'Editar Usuario']
                ],
                ['Productos',
                 ['Editar Producto']
                ]
              ]

layout_main =   [[sg.Menu(menu_layout, key = '-MENU-')],
                 [sg.Text("Bienvenido, " + nombre + '\t\t\t\t\t\t\t\t'), sg.Button('Notificaciones')],
                 [sg.Frame('Consultas', consult_layout), sg.Column(button_layout, key = '-BOTONERA-')]
                ]
window = sg.Window("Sistema de almacen", layout_main, finalize=True)
if rol != 'admin':
    window['-MENU-'].update(visible=False)
    if rol != 'operador':
        window['-BOTONERA-'].update(visible=False)

updateFields(cur, window)
lookForNotifications(cur)
lookForFutureES(cur)
#bucle principal
while True:
    event, values = window.read()
    if event == 'Entradas':
        Feature_entrada(conn, user).ejecutar()
        lookForNotifications(cur)
    elif event == "Altas":
        Feature_alta(conn, user).ejecutar()
        updateFields(cur, window)
    elif event == "Salidas":
        Feature_salida(conn, user).ejecutar()
        lookForNotifications(cur)
    elif event == 'Buscar' :
        cur.execute('SELECT sku, nombre, depto, marca, size, color, precio, existencias, ubicacion '
                   'from producto where disponible = True '
                   'and sku like %s'
                   'and nombre ilike %s'
                   'and depto ilike %s'
                   'and marca ilike %s'
                   'and size ilike %s'
                   'and color ilike %s',
                   ('%'+values['-CODIGOINPUT-']+'%',
                    '%'+values['-NAMEINPUT-']+'%',
                    '%'+values['-DPTOINPUT-']+'%',
                    '%'+values['-MARCAINPUT-']+'%',
                    '%'+values['-SIZEINPUT-']+'%',
                    '%'+values['-COLORINPUT-']+'%'))
        todo = cur.fetchall()
        for prod in todo:
            treedata.insert('', prod[0], prod[0], values=[prod[1], prod[2], prod[3], prod[4], prod[5], prod[6], prod[7], prod[8]])
        window['-LISTA-'].update(treedata)
        treedata = sg.TreeData()
    elif event == 'Editar Productos':
        editar_productos(conn).ejecutar()
    elif event == 'Bajas':
        Feature_Baja(conn).ejecutar()
    elif event == 'Conteo':
        Feature_conteo(conn, user).ejecutar()
    elif event == 'Reporte':
        Feature_reporte(conn,user).ejecutar()
    elif event == 'Crear usuario':
        crear_usuarios(conn).ejecutar()
    elif event == 'Editar Usuario':
        editar_usuarios(conn).ejecutar()
    elif event == 'Editar Producto':
        editar_productos(conn).ejecutar()
    elif event == "Notificaciones":
        Feature_bandeja(conn).ejecutar()
    elif event == "Conteo Indivual":
        Feature_conteo_idividual(conn, user).ejecutar()
    elif event == 'Salir':
        break
    if event == sg.WIN_CLOSED:
        break



cur.close()
conn.close()
window.close()
