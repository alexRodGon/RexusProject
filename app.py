from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import re
import MySQLdb

app = Flask(__name__)
app.secret_key = 'alex'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'projecte'

mysql = MySQL(app)

@app.before_request
def before_request():
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT nomUsuari, cognomUsuari FROM usuari WHERE usernameUsuari = %s", (username,))
        user_data = cur.fetchone()
        if user_data:
            data = {'nombre': user_data[0], 'apellido': user_data[1]}
            session['data'] = data
    else:
        session['data'] = None

@app.route('/')
def index():
    data = session.get('data')
    # data = {}
    return render_template('index.html', data=data)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/notes')
@login_required
def mostrar_notes():
    data = {}
    dataN = {}
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT idNota, titolNota, contingutNota, dataM, idUsuari FROM nota WHERE idUsuari = %s ORDER BY dataM DESC"
        cursor.execute(sql, (session['user_id'],))

        notes = cursor.fetchall()
        # data['notes'] = notes
        # data['session'] = session.get('data')


        dataN = notes
        data = session.get('data')
       
        return render_template('notes.html', data=data, dataN=dataN)
    except Exception as ex:
        print(ex)
        data['missatge'] = 'Error: ' + str(ex)
    return jsonify(data)

@app.route('/notes/delete/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    data = {}
    try:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM nota WHERE idNota = %s AND idUsuari = %s"
        cursor.execute(sql, (note_id, session['user_id']))
        mysql.connection.commit()
        data['success'] = True
        return redirect(url_for('mostrar_notes'))
    except Exception as ex:
        print(ex)
        data['success'] = False
        data['message'] = str(ex)
    return jsonify(data)

@app.route('/afegirNota')
def new_note():
    data = session.get('data')
    return render_template('afegirNota.html', data=data)

@app.route('/add_note', methods=['POST'])
def agregar_nota():
    if request.method == 'POST':
        titol = request.form['titol']
        contingut = request.form['contingut']
        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO nota (titolNota, contingutNota, idUsuari) VALUES (%s, %s, %s)"

            cursor.execute(sql, (titol, contingut, session['user_id']))
            mysql.connection.commit()
            data = session.get('data')
            print(data)
            return redirect(url_for('mostrar_notes', data=data))
        except Exception as ex:
            print(ex)
            return "Error: " + str(ex)
    else:
        return "Método no permitido"

@app.route('/editarNota/<int:note_id>', methods=['GET', 'POST'])
def editarNota(note_id):
    data = {}
    if request.method == 'POST':
        # print(session['user_id'])
        titol = request.form['titol']
        contingut = request.form['contingut']
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE nota SET titolNota = %s, contingutNota = %s WHERE idNota = %s AND idUsuari = %s"
            cursor.execute(sql, (titol, contingut, note_id, session['user_id']))
            mysql.connection.commit()
            data = session.get('data')
            # print(data)
            # print(session['user_id'])
            return redirect(url_for('mostrar_notes', data=data))
        except Exception as ex:
            print(ex)
            return "Error: " + str(ex)
    else:
        nota = obtener_nota_por_id(note_id)
        data = session.get('data')
        return render_template('editarNota.html', nota=nota, data=data)


def obtener_nota_por_id(note_id):
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT idNota, titolNota, contingutNota, idUsuari FROM nota WHERE idNota = %s AND idUsuari = %s"
        cursor.execute(sql, (note_id, session['user_id']))
        nota = cursor.fetchone()
        #print(nota)
        #print(session['user_id'])
        return nota
    except Exception as ex:
        print(ex)
        return None

@app.route('/grups')
@login_required
def mostrar_grups():
    try:
        data = session.get('data', {})
        grupos = {}

        conexion = mysql.connection
        cursor = conexion.cursor()

        sql = "SELECT usuari.nomUsuari, usuari.cognomUsuari, grup.nomGrup, grup.descripcioGrup, grup.idGrup, (SELECT GROUP_CONCAT(usuari.idUsuari, ' ', usuari.nomUsuari, ' ', usuari.cognomUsuari) FROM usuari JOIN membresgrup ON usuari.idUsuari = membresgrup.idUsuari WHERE membresgrup.idGrup = grup.idGrup) AS integrantes FROM usuari JOIN membresgrup ON usuari.idUsuari = membresgrup.idUsuari JOIN grup ON membresgrup.idGrup = grup.idGrup WHERE usuari.idUsuari = %s;"
        cursor.execute(sql, (session['user_id'],))
        resultados = cursor.fetchall()

        for resultado in resultados:
            id_grupo = resultado[4]
            nombre_grupo = resultado[2]
            descripcion_grupo = resultado[3]
            integrantes = resultado[5]
            grupos[id_grupo] = {'nombre': nombre_grupo, 'descripcion': descripcion_grupo, 'integrantes': integrantes}

        cursor.close()

        print(grupos)

        return render_template('grups.html', data=data, grupos=grupos)
    except Exception as ex:
        print(ex)

@app.route('/eliminarUsuarioDelGrupo', methods=['POST'])
@login_required
def eliminar_usuario_del_grupo():
    try:
        usuario_id = request.form['usuarioId']
        grupo_id = request.form['grupoId']

        cursor = mysql.connection.cursor()
        sql = "DELETE FROM membresgrup WHERE idUsuari = %s AND idGrup = %s;"
        cursor.execute(sql, (usuario_id, grupo_id))
        mysql.connection.commit()

        return redirect(url_for('mostrar_grups'))
    except Exception as ex:
        print(ex)
        return 'Error al eliminar usuario del grupo', 500

@app.route('/eliminarGrupo/<int:grupo_id>', methods=['POST'])
@login_required
def eliminar_grupo(grupo_id):
    try:
        cursor = mysql.connection.cursor()
        sql_delete_membres = "DELETE FROM membresgrup WHERE idGrup = %s;"
        cursor.execute(sql_delete_membres, (grupo_id,))
        
        sql_delete_grupo = "DELETE FROM grup WHERE idGrup = %s;"
        cursor.execute(sql_delete_grupo, (grupo_id,))
        
        mysql.connection.commit()

        return redirect(url_for('mostrar_grups'))
    except Exception as ex:
        print(ex)
        return 'Error al eliminar el grupo', 500

@app.route('/crearGrupo', methods=['POST'])
@login_required
def crear_grupo():
    try:
        nombre_grupo = request.form['nombreGrupo']
        descripcion_grupo = request.form['descripcionGrupo']
        usuario_id = session['user_id']
        fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO grup (nomGrup, descripcioGrup, dataCreacioGrup) VALUES (%s, %s, %s);"
        cursor.execute(sql, (nombre_grupo, descripcion_grupo, fecha_creacion))
        mysql.connection.commit()

        nuevo_grupo_id = cursor.lastrowid

        sql_insert_miembro = "INSERT INTO membresgrup (idUsuari, idGrup) VALUES (%s, %s);"
        cursor.execute(sql_insert_miembro, (usuario_id, nuevo_grupo_id))
        mysql.connection.commit()

        return redirect(url_for('mostrar_grups'))
    except Exception as ex:
        print(ex)
        return 'Error al crear el grupo', 500


@app.route('/editarGrupo', methods=['POST'])
@login_required
def editar_grupo():
    try:
        print('hola')
        grupo_id = request.form['grupoIdEditar']
        nombre_grupo = request.form['nombreGrupoEditar']
        descripcion_grupo = request.form['descripcionGrupoEditar']

        print('si')

        cursor = mysql.connection.cursor()

        sql = "UPDATE grup SET nomGrup = %s, descripcioGrup = %s WHERE idGrup = %s"
        cursor.execute(sql, (nombre_grupo, descripcion_grupo, grupo_id))
        mysql.connection.commit()

        return redirect(url_for('mostrar_grups'))
    except Exception as ex:
        print(ex)
        print ('no')
        return ex, 500

@app.route('/agregarMiembros', methods=['POST'])
@login_required
def agregar_miembros():
    try:
        print('prova')
        email_miembro = request.form['emailMiembro']
        grupo_id = request.form['grupoId']
        print(grupo_id)

        cursor = mysql.connection.cursor()
        sql = "SELECT idUsuari FROM usuari WHERE emailUsuari = %s;"
        cursor.execute(sql, (email_miembro,))
        usuario = cursor.fetchone()

        if usuario:
            usuario_id = usuario[0]
            sql_check_membership = "SELECT * FROM membresgrup WHERE idUsuari = %s AND idGrup    = %s;"
            cursor.execute(sql_check_membership, (usuario_id, grupo_id))
            existing_membership = cursor.fetchone()
            print("Valor de usuario_id:", usuario_id)
            print("Valor de grupo_id:", grupo_id)

            if not existing_membership:
                sql_insert_membership = "INSERT INTO membresgrup (idGrup, idUsuari) VALUES (%s, %s);"
                cursor.execute(sql_insert_membership, (grupo_id, usuario_id))
                mysql.connection.commit()

                return redirect(url_for('mostrar_grups'))
            else:
                return "El usuario ya es miembro de este grupo."
        else:
            return "El correo electrónico proporcionado no está asociado a ningún usuario existente."
    except Exception as ex:
        print(ex)
        return 'Error al agregar miembro al grupo: {}'.format(ex), 500


@app.route('/perfil/<int:usuario_id>')
@login_required
def mostrar_perfil(usuario_id):
    try:
        cursor = mysql.connection.cursor()

        sql = "SELECT nomUsuari, cognomUsuari FROM usuari WHERE idUsuari = %s;"
        cursor.execute(sql, (usuario_id,))
        usuario = cursor.fetchone()

        if usuario:
            return render_template('perfil.html', usuario=usuario)
        else:
            return "Usuario no encontrado"
    except Exception as ex:
        return "Error: " + str(ex)


@app.route('/projectes')
@login_required
def mostrar_projectes():
    try:
        data = session.get('data', {})
        proyectos = {}

        conexion = mysql.connection
        cursor = conexion.cursor()

        sql_grupos_usuario = "SELECT idGrup, nomGrup FROM grup WHERE idGrup IN (SELECT idGrup FROM membresgrup WHERE idUsuari = %s)"
        cursor.execute(sql_grupos_usuario, (session['user_id'],))
        grupos_usuario = cursor.fetchall()

        sql_proyectos = """
            SELECT DISTINCT
                projecte.idProjecte, 
                projecte.nomProjecte, 
                projecte.descripcioProjecte, 
                tasca.idTasca, 
                tasca.titolTasca, 
                tasca.estatTasca
            FROM 
                projecte 
            JOIN 
                grupsprojecte ON projecte.idProjecte = grupsprojecte.idProjecte 
            JOIN 
                grup ON grupsprojecte.idGrup = grup.idGrup 
            JOIN 
                membresgrup ON grup.idGrup = membresgrup.idGrup 
            LEFT JOIN 
                tasca ON tasca.idProjecte = projecte.idProjecte AND membresgrup.idUsuari = %s
            WHERE 
                membresgrup.idUsuari = %s
        """
        cursor.execute(sql_proyectos, (session['user_id'], session['user_id']))
        resultados = cursor.fetchall()

        for resultado in resultados:
            id_proyecto = resultado[0]
            nombre_proyecto = resultado[1]
            descripcion_proyecto = resultado[2]
            id_tarea = resultado[3]
            nombre_tarea = resultado[4]
            estat_tasca = resultado[5]

            if id_proyecto not in proyectos:
                proyectos[id_proyecto] = {
                    'nombreP': nombre_proyecto,
                    'descripcionP': descripcion_proyecto,
                    'tareas': []
                }

            if id_tarea is not None:
                    proyectos[id_proyecto]['tareas'].append((id_tarea, nombre_tarea, estat_tasca))

        cursor.close()

        print(proyectos)
        print("Grupos del usuario:", grupos_usuario)

        return render_template('projectes.html', data=data, proyectos=proyectos, grupos_usuario=grupos_usuario)
    except Exception as ex:
        print(ex)
        return "Algo salió mal"


@app.route('/actualizar_tarea', methods=['POST'])
def actualizar_tarea():
    try:
        if request.method == 'POST':
            data = request.json
            tarea_id = data.get('tarea_id')
            estado_checkbox = data.get('estado_checkbox')
            print('tascaid', tarea_id)

            cursor = mysql.connection.cursor()
            sql_actualizar_tarea = "UPDATE tasca SET estatTasca = %s WHERE idTasca = %s"
            cursor.execute(sql_actualizar_tarea, (estado_checkbox, tarea_id))

            mysql.connection.commit()
            cursor.close()

            # Devolver una respuesta JSON indicando el éxito de la operación
            return jsonify({'success': True})
    except Exception as ex:
        print(ex)
        # Devolver una respuesta JSON indicando el error si algo salió mal
        return jsonify({'success': False, 'error': str(ex)})

@app.route('/calcularTareasP')
@login_required
def calcularTareasP():
    try:
        data = session.get('data', {})
        tareasPendientes = {}

        conexion = mysql.connection
        cursor = conexion.cursor()

        sql_grupos_usuario = """
            SELECT 
                projecte.idProjecte, 
                projecte.nomProjecte, 
                projecte.descripcioProjecte, 
                COUNT(DISTINCT tasca.idTasca) AS tareasCompletadas
            FROM 
                projecte 
            JOIN 
                grupsprojecte ON projecte.idProjecte = grupsprojecte.idProjecte 
            JOIN 
                grup ON grupsprojecte.idGrup = grup.idGrup 
            JOIN 
                membresgrup ON grup.idGrup = membresgrup.idGrup 
            LEFT JOIN 
                tasca ON tasca.idProjecte = projecte.idProjecte AND membresgrup.idUsuari = 3 AND tasca.estatTasca = 0
            WHERE 
                membresgrup.idUsuari = %s 
            GROUP BY 
                projecte.idProjecte, 
                projecte.nomProjecte, 
                projecte.descripcioProjecte;
        """
        cursor.execute(sql_grupos_usuario, (session['user_id'],))
        tareasPendientes = cursor.fetchone() 
        cursor.close()

        return render_template('mostrar_projectes.html', data=data, tareasPendientes=tareasPendientes) 
    except Exception as ex:
        print(ex)
        return "Algo salió mal"


@app.route('/eliminarProyecto/<int:proyecto_id>', methods=['POST'])
@login_required
def eliminar_proyecto(proyecto_id):
    try:
        cursor = mysql.connection.cursor()
        sql_delete_grups = "DELETE FROM grupsprojecte WHERE idProjecte = %s;"
        cursor.execute(sql_delete_grups, (proyecto_id,))
        
        sql_delete_proyecto = "DELETE FROM projecte WHERE idProjecte = %s;"
        cursor.execute(sql_delete_proyecto, (proyecto_id,))
        
        mysql.connection.commit()

        return redirect(url_for('mostrar_projectes'))
    except Exception as ex:
        print(ex)
        return 'Error al eliminar el proyecto', 500

@app.route('/crearProyecto', methods=['GET', 'POST'])
@login_required
def crear_proyecto():
    try:
        data = session.get('data', {})
        
        if request.method == 'POST':
            grupos_usuario = request.form.getlist('grupoUsuario[]')
            print('grupos', grupos_usuario)

            nombre_proyecto = request.form['nombreProyecto']
            descripcion_proyecto = request.form['descripcionProyecto']
            usuario_id = session['user_id']
            fecha_entrega_proyecto = request.form['fechaEntregaProyecto']
            fecha_creacion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cursor = mysql.connection.cursor()
            
            sql_insert_proyecto = "INSERT INTO projecte (nomProjecte, descripcioProjecte, dataCreacioProjecte, dataEntregaProjecte) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_insert_proyecto, (nombre_proyecto, descripcion_proyecto, fecha_creacion, fecha_entrega_proyecto))
            mysql.connection.commit()

            nuevo_proyecto_id = cursor.lastrowid

            for grupo_seleccionado in grupos_usuario:
                sql_insert_relacion = "INSERT INTO grupsprojecte (idProjecte, idGrup) VALUES (%s, %s)"
                cursor.execute(sql_insert_relacion, (nuevo_proyecto_id, grupo_seleccionado))
                mysql.connection.commit()

            cursor.close()
            print('grupos', grupos_usuario)

            return redirect(url_for('mostrar_projectes'))

        return render_template('crear_proyecto_modal.html', data=data)
    except Exception as ex:
        print(ex)
        return 'Error al crear el proyecto', 500


@app.route('/editarProyecto', methods=['POST'])
@login_required
def editar_proyecto():
    try:
        print('hola')
        proyecto_id = request.form['proyectoIdEditar']
        nombre_proyecto = request.form['nombreProyectoEditar']
        descripcion_proyecto = request.form['descripcionProyectoEditar']

        print('si')

        cursor = mysql.connection.cursor()

        sql = "UPDATE projecte SET nomProjecte = %s, descripcioProjecte = %s WHERE idProjecte = %s"
        cursor.execute(sql, (nombre_proyecto, descripcion_proyecto, proyecto_id))
        mysql.connection.commit()

        return redirect(url_for('mostrar_projectes'))
    except Exception as ex:
        print(ex)
        print ('no')
        return ex, 500


@app.route('/tasques')
@login_required
def mostrar_tasques():
    data = {}
    dataN = {}
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT idTasca, titolTasca, descripcioTasca, estatTasca, dataEntregaTasca, dataCreacioTasca FROM tasca WHERE idUsuari = %s ORDER BY dataEntregaTasca DESC"
        cursor.execute(sql, (session['user_id'],))

        notes = cursor.fetchall()
        # data['notes'] = notes
        # data['session'] = session.get('data')


        dataN = notes
        data = session.get('data')
       
        return render_template('tasques.html', data=data, dataN=dataN)
    except Exception as ex:
        print(ex)
        data['missatge'] = 'Error: ' + str(ex)
    return jsonify(data)

@app.route('/tasques/delete/<int:tasca_id>', methods=['POST'])
@login_required
def delete_tasca(tasca_id):
    data = {}
    try:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM tasca WHERE idTasca = %s AND idUsuari = %s"
        cursor.execute(sql, (tasca_id, session['user_id']))
        mysql.connection.commit()
        data['success'] = True
        return redirect(url_for('mostrar_tasques'))
    except Exception as ex:
        print(ex)
        data['success'] = False
        data['message'] = str(ex)
    return jsonify(data)

@app.route('/afegirTasca')
def new_tasca():
    print('no')
    data = session.get('data')
    tasca = obtener_proyectos_por_id()
    return render_template('afegirTasca.html', tasca=tasca, data=data)

@app.route('/add_tasca', methods=['POST'])
def agregar_tasca():
    if request.method == 'POST':
        titol = request.form['titol']
        contingut = request.form['contingut']
        proyecto_id = request.form['proyecto']

        try:
            cursor = mysql.connection.cursor()
            sql = "INSERT INTO tasca (titolTasca, descripcioTasca, idUsuari, idProjecte) VALUES (%s, %s, %s, %s)"

            cursor.execute(sql, (titol, contingut, session['user_id'], proyecto_id))
            mysql.connection.commit()
            data = session.get('data')
            print(data)
            return redirect(url_for('mostrar_tasques', data=data))
        except Exception as ex:
            print(ex)
            return "Error: " + str(ex)
    else:
        print('si')
        tasca = obtener_proyectos_por_id()
        data = session.get('data')
        return render_template('afegirTasca.html', tasca=tasca, data=data)


@app.route('/editarTasca/<int:tasca_id>', methods=['GET', 'POST'])
def editarTasca(tasca_id):
    data = {}
    if request.method == 'POST':
        # print(session['user_id'])
        titol = request.form['titol']
        contingut = request.form['contingut']
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE tasca SET titolTasca = %s, descripcioTasca = %s WHERE idTasca = %s AND idUsuari = %s"
            cursor.execute(sql, (titol, contingut, tasca_id, session['user_id']))
            mysql.connection.commit()
            data = session.get('data')
            # print(data)
            # print(session['user_id'])
            return redirect(url_for('mostrar_tasques', data=data))
        except Exception as ex:
            print(ex)
            return "Error: " + str(ex)
    else:
        tasca = obtener_tasca_por_id(tasca_id)
        data = session.get('data')
        return render_template('editarTasca.html', tasca=tasca, data=data)


def obtener_tasca_por_id(tasca_id):
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT idTasca, titolTasca, descripcioTasca, idUsuari FROM tasca WHERE idTasca = %s AND idUsuari = %s"
        cursor.execute(sql, (tasca_id, session['user_id']))
        nota = cursor.fetchone()
        #print(nota)
        #print(session['user_id'])
        return nota
    except Exception as ex:
        print(ex)
        return None

def obtener_proyectos_por_id():
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT projecte.idProjecte, projecte.nomProjecte FROM projecte JOIN grupsprojecte ON projecte.idProjecte = grupsprojecte.idProjecte JOIN grup ON grupsprojecte.idGrup = grup.idGrup JOIN membresgrup ON membresgrup.idGrup = grup.idGrup WHERE membresgrup.idUsuari = %s"
        cursor.execute(sql, (session['user_id'],))
        resultados = cursor.fetchall()
        
        tasca = {}
        for resultado in resultados:
            id_proyecto = resultado[0]
            nombre_proyecto = resultado[1]
            tasca[id_proyecto] = {'idP': id_proyecto, 'nombreP': nombre_proyecto}

        cursor.close()

        return tasca
    except Exception as ex:
        print(ex)
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute("SELECT idUsuari, usernameUsuari, contraUsuari, nomUsuari, cognomUsuari FROM usuari WHERE usernameUsuari = %s", (username,))
        user = cur.fetchone()

        if user and check_password_hash(user['contraUsuari'], password):
            session['user_id'] = user['idUsuari']
            session['username'] = username
            session['nombre'] = user['nomUsuari']
            session['apellido'] = user['cognomUsuari']
            return redirect(url_for('mostrar_notes'))
        
        error = 'Invalid username or password. Please try again.'
        return render_template('login.html', error=error)
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        fecha_nacimiento = request.form['fecha_nacimiento']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        premium = request.form['premium']

        if not all(request.form.get(field) for field in ['username', 'email', 'password', 'telefono', 'nombre', 'apellido', 'premium']):
            error = 'Por favor completa todos los campos obligatorios.'
            return render_template('register.html', error=error)
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error = 'Correo electronico incorrecto'
            return render_template('register.html', error=error)
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuari WHERE nomUsuari = %s", (username,))
        existing_username = cur.fetchone()
        if existing_username:
            error = 'Este nombre de usuario ya existe'
            return render_template('register.html', error=error)
        
        cur.execute("SELECT * FROM usuari WHERE emailUsuari = %s", (email,))
        existing_email = cur.fetchone()
        if existing_email:
            error = 'Correo electronico ya en uso'
            return render_template('register.html', error=error)
        
        if not re.match(r"^\d{9}$", telefono):
            error = 'El numero de telefono debe tener 9 digitos como minimo'
            return render_template('register.html', error=error)

        if not re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()-_=+\\|{}[\]:;\"'<>,.?/]).{8,}$", password):
            error = 'La contraseña debe tener al menos 8 caracteres y contener al menos una letra mayúscula, una letra minúscula, un número y un carácter especial.'
            return render_template('register.html', error=error)
        
        hashed_password = generate_password_hash(password)
        fecha_registro = datetime.now().strftime('%Y-%m-%d')
        
        sql = "INSERT INTO usuari (usernameUsuari, emailUsuari, contraUsuari, rolUsuari, telefonUsuari, direccioUsuari, dataRegistreUsuari, dataNaixementUsuari, nomUsuari, cognomUsuari, premiumUsuari) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (username, email, hashed_password, role, telefono, direccion, fecha_registro, fecha_nacimiento, nombre, apellido, premium)

        cur.execute(sql, val)
        mysql.connection.commit()
        
        session['username'] = username
        return redirect(url_for('profile'))
        error = 'Ha ocurrido un error en el formulario.'
    
    return render_template('register.html', error=error)


@app.route('/profile')
def profile():
    data = {}
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor()
        cur.execute("SELECT nomUsuari, emailUsuari, rolUsuari, dataRegistreUsuari, premiumUsuari, usernameUsuari, telefonUsuari, direccioUsuari, cognomUsuari FROM usuari WHERE usernameUsuari = %s", (username,))
        user_data = cur.fetchone()
        if user_data:
            username = user_data[5]
            email = user_data[1]
            role = user_data[2]
            dataR = user_data[3]
            premium = user_data[4]
            nombre = user_data[0]
            telefon = user_data[6]
            direccio = user_data[7]
            apellido = user_data[8]

            dataR_str = dataR.strftime('%Y-%m-%d')

            fecha_registro = datetime.strptime(dataR_str, '%Y-%m-%d')
            fecha_actual = datetime.now()
            experiencia = fecha_actual.year - fecha_registro.year

            # data = {'nombre': user_data[0], 'apellido': user_data[1]}
            # session['data'] = data
            data = session.get('data')

            return render_template('profile.html', username=username, email=email, role=role, dataR=dataR, premium=premium, experiencia=experiencia, nombre=nombre, telefon=telefon, direccio=direccio, apellido=apellido, data=data)
    return redirect(url_for('login'))

@app.route('/about')
def about():
    data = session.get('data')
    return render_template('about.html', data=data)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('data', None)
    return redirect(url_for('index'))

def pag_no_encontrada(error):
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.register_error_handler(404, pag_no_encontrada)
    app.run(debug=True, port=5000)