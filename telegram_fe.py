from telegram.ext import Updater, CommandHandler, CallbackContext
from backend.frase import frase
from backend.db import database
from random import randrange
from generador import get_tweet, delete, select, insert


class TelegramFrontend:
    def __init__(self, db, tok):
        print("[*] Iniciando bot de Telegram con TOKEN = ",tok)# Authenticate to Twitter

        self.updater = Updater(token=tok, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.db = db

    #Auxiliares
    def check_args(self, expected, args, update, context):
        if (len(args)!=expected):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text = "[!] El numero de argumentos no es el esperado. Esperado: {}. Recibido: {}".format(expected,len(args))
            )
            return False
        
        return True
    def normalize(self, args, splitter, expected_first):        
        print(args)
        #Declaracion de las palabras de inicio y fin
        first_word = None
        last_word = None

        #Comprobamos que el primer caracter es valido
        if (args[expected_first][0]!=splitter):
            return("[!] Splitter inicial no valido. Intente poner "+splitter+" al principio de la frase")
            
        #Iniciamos la primera palabra y eliminamos el splitter
        first_index = expected_first
        first_word = args[first_index].replace(splitter, '')

        #Buscamos la ultima palabra y eliminamos el splitter
        for i in range(0, len(args)):
            if (args[i][-1]==splitter):
                last_index = i
                last_word = args[last_index].replace(splitter, '')

        #Comprobamos que el ultimo caracter es valido 
        if (last_word == None):
            return("[!] Splitter inicial no valido. Intente poner "+splitter+" al principio de la frase")
            
        #Reasignamos los args
        args[first_index] = first_word
        args[last_index] = last_word

        frase = ""

        for i in range(first_index, (last_index+1)):
            frase = frase + args[i]+" "

        #Devolvemos la frase y el largo de la frase
        return (frase, last_index-first_index+1)

    def insert(self, update, context):
        (content, length) = (self.normalize(context.args, "'", 0))
        args = context.args
        args = args[length : (len(args))]
        
        if (self.check_args((4), args, update, context)==False):
            return
        
        insert_type = args[0]
        insert_genre = args[1]
        insert_number = args[2]
        insert_next = args[3]
        
        response = insert(self.db, content, insert_type, insert_genre, insert_number, insert_next)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text = response
        )
    
    #Funciones auxiliares de insert
    def insert_sujeto(self, update, context):
        (content, length) = (self.normalize(context.args, "'", 0))
        args = context.args
        args = args[length : (len(args))]
        
        if (self.check_args((2), args, update, context)==False):
            return

        insert_type = 's'
        insert_next = 'x'
        insert_genre = args[0]
        insert_number = args[1]
        
        response = insert(self.db, content, insert_type, insert_genre, insert_number, insert_next)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text = response
        )
    
    def select(self, update, context):
        try:
            filter_parameter=None
            order_parameter=None

            for i in range(0, len(context.args)):
                if context.args[i] == '+order':
                    order_parameter = context.args[i+1]
                    i+=1
                if context.args[i] == '+filter':
                    if (filter_parameter == None):
                        filter_parameter = []
                    filter_condition = (context.args[i+1], context.args[i+2])
                    filter_parameter.insert(len(filter_parameter), 
                        filter_condition)
                    i+=2

            response = select(self.db, filter_parameter, order_parameter)
        
        except Exception as error:
            response = "[!] Error: "+error.args[0]
            print(response)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text = response
        )
    def delete(self,update, context):
        if (self.check_args(1, context.args, update, context)==False):
            return

        id = context.args[0]
        response = delete(self.db, id)
        
        context.bot.send_message(
            chat_id= update.effective_chat.id,
            text = response
        )

    def get_frase_bot(self, update, context):
        try:
            iterations = 1
            if (context.args!= []):
                iterations = int(context.args[0])   

            for i in range(0, iterations):
                response = get_tweet(self.db)

                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text = response
                )

        except Exception as error:
            response = "[!] Error: "+error.args[0]
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text = response
            )
            print(response)
    def get_help(self, update, context):
        mensaje = """
            Placeholder
        """

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text = mensaje
        )


    def dispatch_all(self):
        self.dispatcher.add_handler(CommandHandler('add', self.insert))
        self.dispatcher.add_handler(CommandHandler('add_sujeto', self.insert_sujeto))
        self.dispatcher.add_handler(CommandHandler('sel', self.select))
        self.dispatcher.add_handler(CommandHandler('rm', self.delete))

        self.dispatcher.add_handler(CommandHandler('random', self.get_frase_bot))
        self.dispatcher.add_handler(CommandHandler('help', self.get_help))
    def main_loop(self):
        print("[*] Main Telegram loop started")
        
        self.dispatch_all()
        self.updater.start_polling()
        self.updater.idle()