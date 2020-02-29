from backend.frase import frase
from random import randrange

def select(db, filters, order):
    query = "SELECT * FROM frases"

    if (filters != None):
        query += " WHERE "
        for i in range(0, len(filters)):
            if (i>0):
                query += "AND "
            parameter = filters[i]
            query += """{} = '{}' """.format(parameter[0], parameter[1])
    
    if (order != None):
        query += (" ORDER BY "+order)


    return db.select_frase(query)

def delete(db, id):
    return db.delete_frase(id)

def insert(db, content, type, genre, number, next):
    if (genre!='h' and genre!='m' and genre!='n'):
        return "[!] Genero "+" no valido. Pruebe con [h]ombre, [m]ujer o [n]eutro"
    
    if (number!='s' and number!='p' and number!='n'):
        return "[!] Numero "+number+" no valido. Pruebe con [s]ingular, [p]lural o [n]eutro"
        
    return db.insert_frase(frase(content, type, genre, number, next))

def get_random_frase(tipo, genre, number, db):
    #Obtenemos la accion solicitada
    accion = db.random_frase(tipo, genre, number)
    response = accion.content
    continuacion = accion.next

    #Comprobamos si tiene continuacion
    while (continuacion not in ('x')):
        accion = db.random_frase(continuacion, genre, number)
        response = response + accion.content
        continuacion = accion.next

    #Devolvemos la accion resultado
    return response

def get_tweet(db):
    try:
        decididor = (randrange(100)<60)
            
        sujeto = db.random_sujeto()
        main_action = get_random_frase('a', sujeto.genre, sujeto.number, db)

        if (decididor): 
            modifier = main_action
            while (modifier == main_action):
                modifier = get_random_frase('a',sujeto.genre, sujeto.number,db)
                
            modifier = "mientras que está " + modifier
        else:
            modifier = get_random_frase('m',sujeto.genre, sujeto.number,db)

        return sujeto.content + main_action + modifier


    except Exception as error:
        return "[!] Error: "+error.args[0]