import sqlite3
import requests
import time

dataBasesql="instaSQL.db"

url=""

def getResponse():
    pass                    #return nicks
def writeUnique():
    pass                    #write unique nicks inti DB


def get_all_updates(request=url):  # получаем все сообщения полученные ботом за последние сутки
        response = requests.get(request + 'getUpdates')
        return response.json()

def get_last_message(all_updates):
    try:
        a = len(all_updates['result']) - 1
    except:
        print("need more messages")
    try:
        message_text = all_updates['result'][a]['message']["text"]
    except:
        message_text = None
    return message_id, message_text


def sendInstructions(chat_id,url):
    text="ome instructions" #istructions
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
def check_nicksDB():
    pass



