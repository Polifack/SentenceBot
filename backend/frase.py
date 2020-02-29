class frase:
    def __init__(self, content, tipo, genre, number, next_element):
        #El genero del sujeto del bot. Debe ser masculino o femenino o neutro.
        if (genre!='h' and genre!='m' and genre!='n'):
            raise Exception("Genero no valido")
    
        #La cardinalidad del sujeto del bot. Debe ser singular o plural o neutro.
        if (number!='s' and number!='p' and number!='n'):
            raise Exception("Numero no valido")
        

        self.content = content
        self.type = tipo
        self.genre = genre
        self.number = number
        self.next = next_element