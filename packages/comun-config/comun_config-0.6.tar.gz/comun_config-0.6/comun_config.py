import psycopg
from psycopg.rows import namedtuple_row, dict_row


def get_config_params(connection_string, id_project):

    conn = psycopg.connect(connection_string, row_factory=namedtuple_row)

    cursor = conn.cursor()
    cursor.execute('SELECT key, value FROM params WHERE project_id=%s OR project_id=0', [id_project])
    rows = cursor.fetchall()
    conn.close()

    db_config = {}
    for row in rows:
        db_config[row[0]] = row[1]

    return db_config


def get_deploy_params(connection_string, id_project):

    conn = psycopg.connect(connection_string, row_factory=dict_row)

    cursor = conn.cursor()
    cursor.execute('''select project_path, a.server,deploy_user from projects a 
                    inner join servers b on a.server=b.host
                   WHERE project_id=%s''', [id_project])
    row = cursor.fetchone()
    conn.close()

    return row
