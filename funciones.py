from flask import render_template, request, redirect, session, url_for
import psycopg
from psycopg import sql

def login_func():
    error = None
    if request.method == 'POST':
        session['user'] = request.form['username']
        session['password'] = request.form['password']
        session['host'] = request.form.get('host', 'localhost')
        session['dbname'] = request.form.get('dbname', 'postgres')

        try:
            conn = psycopg.connect(
                dbname=session['dbname'],
                user=session['user'],
                password=session['password'],
                host=session['host']
            )
            conn.close()
            return redirect(url_for('tables'))
        except Exception as e:
            error = str(e)

    return render_template('login.html', error=error)

def tables_func():
    try:
        conn = psycopg.connect(
            dbname=session['dbname'],
            user=session['user'],
            password=session['password'],
            host=session['host']
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public';
        """)
        tables = [row[0] for row in cur.fetchall()]
        conn.close()
        return render_template('tables.html', tables=tables)
    except Exception as e:
        return f"Ha ocurrido un error recuperando las tablas de la base de datos."

def table_data_func(name):
    try:
        with psycopg.connect(
            dbname=session['dbname'],
            user=session['user'],
            password=session['password'],
            host=session['host']) as conn:
            
            with conn.cursor() as cur_check:
                cur_check.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
                allowed_tables = {row[0] for row in cur_check.fetchall()}
            
            if name not in allowed_tables:
                return f"Tabla no permitida por el usuario actual."
            
            with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(name))
                cur.execute(query)
                rows = cur.fetchall()
                headers = [desc.name for desc in cur.description]
        
        return render_template('records.html', table=name, rows=rows, headers=headers)
    
    except Exception as e:
        return f"Error al acceder a la tabla seleccionada."

