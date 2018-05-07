
# coding: utf-8

# In[ ]:

import requests
import time
import random
import draftScrappingv03
import extractTop_db
import check_nicks

class bot:
    url = "https://api.telegram.org/bot596033036:AAENZ-Z5qGbfsxF9cO9JWHvgcLnh5WlB_A8/"
url=bot.url

def get_all_updates(request):  #получаем все сообщения полученные ботом за последние сутки
    response = requests.get(request + 'getUpdates')
    #print(response.json())
    return response.json()
def get_last_message(all_updates): #get the last message
    try:
        a=len(all_updates['result'])-1
    except:
        print("need more messages")
    try:
        message_text=all_updates['result'][a]['message']["text"]
    except:
        message_text=None
    try:
        message_id=all_updates['result'][a]['message']["message_id"]
    except:
        message_id=None
    try:
        chat_id=all_updates['result'][a]['message']["from"]["id"]
    except:
        chat_id=None
        #print("id",message_id,"text",message_text)
    return message_id,message_text,chat_id
def send_mess(chat_id, text):  
    params = {'chat_id': chat_id, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)
    return response

###################################################
#we can add new commands there
def chooseAction(message,chat_id):
    if message == "start":
        refillDB(chat_id)
    elif message == "top":
        top(chat_id)
    elif message == "new":
        check_nicks.sendInstructions(chat_id,url)
    else:pass
###################################################




def refillDB(chat_id):
    send_mess(chat_id, text="Parce started, it takes few minutes")
    try:
        draftScrappingv03.uni_parce()
    except:
        send_mess(chat_id, text="Parce is done with ERROR")
    send_mess(chat_id, text="Parce is done successfully")
def top(chat_id):
    try:
        send_mess(chat_id, text="Insert minimum multiplier")
        flag = False
        while True:
            z, min_mul, x = get_last_message(get_all_updates(url))
            if min_mul.isdigit() == True:
                min_mul = float(min_mul)
                break
            else:
                time.sleep(2)
    except:pass
    ######################################################################
    try:
        a = extractTop_db.check_stats(min_mul)
    except:pass
    for item in a:
        message = "by " + "@" + item[0]+"\n\n"+item[4]
        send_mess(chat_id, text=message)
        time.sleep(1)
        send_mess(chat_id, text=item[3])
        time.sleep(3)
    send_mess(chat_id, text="Done.That was top posts")

def check_message():
    last_message, last_id = None, None
    while True:
        message_id,message_text,chat_id=get_last_message(get_all_updates(url))
        if message_text == None:
            time.sleep(5)
            continue
        elif last_id != message_id:
            print(message_text) #print last message
            last_message, last_id = message_text,message_id
            send_mess(chat_id, text="Obrabotka "+last_message)
            ########### перебор входящих сообщений ############
            chooseAction(message_text,chat_id)
        else:
            if last_id==message_id:
                time.sleep(5)
            else:
                last_id=message_id
                send_mess(chat_id, text="Please use text")
                time.sleep(5)

# In[ ]:

check_message()

