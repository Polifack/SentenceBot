from telegram_fe import TelegramFrontend
from backend.db import database
from twitter_fe import TwitterFrontend
import threading
import json


def get_config_vars():
    print("[*] Leyendo de config.json las variables de configuracion")
    with open('config_local.json') as json_data_file:
        data = json.load(json_data_file)
    return (data['postgresql'], data['telegram'], data['twitter'], int(data['tweet_seconds']))

def main():
    (psql, telegram, twitter, tweet_time) = get_config_vars()

    db = database(psql['user'],psql['password'],psql['host'],psql['port'],psql['name'])
    tg = TelegramFrontend(db, telegram["token"]) 
    tw = TwitterFrontend(db, twitter['consumer_key'],twitter['consumer_secret'],
        twitter['access_token'],twitter['access_token_secret'])
    
    #Lanzamos en un thread aparte el bot de twitter
    threading.Thread(target = tw.tweet_bot, args=([tweet_time])).start()    
    #Lanzamos en el main thread el telegram loop
    tg.main_loop()


if __name__ == '__main__':
    main()