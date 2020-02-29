import os
import psycopg2
from backend.frase import frase


class database: 
    def __init__(self, user, password, host, port, name):
        psql_url = "postgres://"+user+":"+password+"@"+host+":"+port+"/"+name
        print("[*] Iniciando base de datos con URL = ",psql_url)

        self.DATABASE_URL = psql_url
        self.create_tables()
    
    def create_tables(self):
        print("[*] Iniciando proceso de creación de tablas")
        command = ("""
            CREATE TABLE IF NOT EXISTS frases(
                id SERIAL PRIMARY KEY,
                content VARCHAR(255) NOT NULL,
                type CHAR NOT NULL,
                genre CHAR NOT NULL,
                number CHAR NOT NULL,
                next CHAR NOT NULL
            )""")
        conn = None
        try:
            conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute(command)
            cur.close()
            conn.commit()
            print("[*] Tablas creadas correctamente")
        except (Exception, psycopg2.DatabaseError) as error:
            print("[*] ERROR:"+error)
            conn.rollback()
        finally:
            if conn is not None:
                conn.close()
    def drop_tables(self):
        print('[*] Iniciando eliminación de tablas')
        command = 'DROP TABLE IF EXISTS frases'
        conn = None
        try:
            conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute(command)
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("[*] ERROR:"+error)
            conn.rollback()
        finally:
            print('[*] Tablas eliminadas correctamente')
            if conn is not None:
                conn.close()
              
    def insert_frase(self, f):
        try:
            conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            
            command = """
            INSERT INTO frases(content, type, genre, number, next)
            VALUES ('{}', '{}', '{}', '{}', '{}')
            """.format(f.content, f.type, f.genre, f.number, f.next)

            cur.execute(command)
            cur.close()
            conn.commit()
            return ("[*] Insert for {} completed".format(f.content))

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            conn.rollback()
            return ("[!] "+error)

        finally:
            if conn is not None:
                conn.close()
    def delete_frase(self, id):
        conn = None

        try:
            conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            SQL = "DELETE FROM frases WHERE id = '{}'".format(id)
            cur.execute(SQL)
            cur.close()
            conn.commit()
            return "[*] Delete for {} completed".format(id)
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            conn.rollback()
            return ("[!] "+error)
        finally:
            if conn is not None:
                conn.close()
    def select_frase(self, query):
        conn = None

        try:
            conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute(query)
            result = cur.fetchall() 
            data = " ID || TYPE || GENRE || NUMBER || NEXT || CONTENT\n"          
            for row in result:
                temp = "" 
                f = frase(row[1], row[2], row[3], row[4], row[5])
                temp = " {}  ||  {}  ||  {}  ||  {}  ||  {}  || {}".format(row[0],f.type,f.genre,f.number,f.next, f.content)
                data = data + temp + '\n'

            cur.close()

            return data
        
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error
        finally:
            if conn is not None:
                conn.close()


    def random_sujeto(self):
        command = ("""
            SELECT content, type, genre, number, next FROM frases 
            WHERE (type='s')
            ORDER BY random() LIMIT 1""")
        conn = None

        try:
            conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute(command)
            row = cur.fetchone() 
            
            f = frase(row[0], row[1], row[2], row[3], row[4])
            cur.close()

            return f
    
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error
        finally:
            if conn is not None:
                conn.close()
    def random_frase(self, tipo, genre, number):
        conn = None

        try:
            conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute("""
            SELECT content, type, genre, number, next FROM frases 
            WHERE (genre='{}' OR genre='n') AND (number='{}' OR number='n') AND (type='{}')
            ORDER BY random() LIMIT 1"""
            .format(genre, number, tipo))
            
            row = cur.fetchone() 
            
            f = frase(row[0], row[1], row[2], row[3], row[4])
            cur.close()

            return f
    
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error
        finally:
            if conn is not None:
                conn.close()
