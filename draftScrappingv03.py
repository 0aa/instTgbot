
# coding: utf-8

# In[17]:


from bs4 import BeautifulSoup 
import requests
import time
import random
import sqlite3

css_selector="div._6d3hm a" #задаем div.класс для поиска в css на странице инстаграма
linksBasePath="D:\\bot\\geeks.txt" #документ со ссылками на нужные аккаунты 
resultsBasePath="D:\\bot\\results.txt" # документ для вывода  информации
uaList="D:\\bot\\User-agents.txt" #список юзер-агентов
dataBasesql="D:\\bot\\instaSQL.db"


# In[18]:


def txt_to_list():
    temp_clearLinks=[]
    with open(linksBasePath,'r') as f:
        for line in f:
            clear=line.split()
            for a in clear:
                if a not in temp_clearLinks: 
                    temp_clearLinks.append(a)
    return temp_clearLinks
#clearLinks=txt_to_list()
#print(clearLinks)



# In[19]:


def parce(link,user_ag):  #принимаем ссылку на аккаунт и юзер-агеннт
    while True:    
        try:
            html = requests.get(link,
                                data=None, 
                                headers={'User-Agent':user_ag}) #переходим на один пост по ссылке link (одной из 12)
            break
        except:
            print('W8 60 sec')
            print("ZZzzzz...")
            time.sleep(60)
            
    soup = BeautifulSoup(html.text, 'lxml')
    soup=soup.text
    return soup #возвращаем html страницы
#inst_html=parce()
#print(inst_html)


# In[20]:


def db_set(): #создание таблицы и колонок
    conn=sqlite3.connect(dataBasesql)
    cur=conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS post_stats
                (nick TEXT,
                 post TEXT,
                 time_ofposting INT,
                 type_ofpost TEXT,
                 time_ofIter1 INT,
                 likes1 INT,
                 video_views1 INT,
                 comments1 INT,
                 time_ofIter2 INT,
                 likes2 INT,
                 video_views2 INT,
                 comments2 INT,
                 time_ofIter3 INT,
                 likes3 INT,
                 video_views3 INT,
                 comments3 INT,
                 hashtags TXT)''' )
    conn.commit()
    cur.close()
#db_set()
 


# In[21]:


def age_ofpost(timePost): #check the age of post
    if timePost is not None:
        if (time.time()-int(timePost))>604800:
            return False
        else:
            return True
    else:
        return False

def db_write1(nick,post,timePost,contentType,time_of_iter,like,comment,video_view_count,hashtag): #write 1st iteration
    conn=sqlite3.connect(dataBasesql)
    cur=conn.cursor()
    cur.execute('''INSERT INTO post_stats (nick, post, time_ofposting, type_ofpost, time_ofIter1, likes1, video_views1, comments1, hashtags)
              VALUES (?,?,?,?,?,?,?,?,?)''',(nick,post,timePost,contentType,time_of_iter,like,video_view_count,comment,hashtag))
    conn.commit()
    cur.close()
    
def db_write2(time_of_iter,like,video_view_count,comment,post): #wtite 2nd iteration 
    conn=sqlite3.connect(dataBasesql)
    cur=conn.cursor()
    cur.execute('''UPDATE post_stats SET time_ofIter2=(?), likes2=(?), video_views2=(?), comments2=(?) 
                WHERE post=(?)''',(time_of_iter,like,video_view_count,comment,post))
    conn.commit()
    cur.close()

def db_write3(time_of_iter,like,video_view_count,comment,post):#write 3rd iteration
    conn=sqlite3.connect(dataBasesql)
    cur=conn.cursor()
    cur.execute('''UPDATE post_stats SET time_ofIter3=(?), likes3=(?), video_views3=(?), comments3=(?) 
                    WHERE post=(?)''',(time_of_iter,like,video_view_count,comment,post))
    conn.commit()
    cur.close()
    
def db_check(post): #checking of availability of post in the DB
    conn=sqlite3.connect(dataBasesql)
    cur=conn.cursor()
    cur.execute('''SELECT DISTINCT * FROM post_stats WHERE post=(?)''',(post,))
    a=cur.fetchone()
    if a is None:
        return "iter1"
        #print("a is None") #if post not in base write full line
    elif post in a: 
        #print(a)           #check a[12] for avaliabl of Iter 3 
        if a[8]==None:
            return "iter2"
            #db_write2(post)
        else:
            if a[12]==None:
                return "iter3"
                #db_write3(post)
            else:pass #что делать если все три этерации пройдены 
    else:
        pass


"""
ПЕРЕДЕЛАТЬ, сейчас временно всё в 1 столбик (как будто в первую итерацию)
"""
#uniting check func
def check_func(nick,post,timePost,contentType,time_of_iter,like,comment,video_view_count,hashtag): #выбираем какую итерацию выполнить
    check=db_check(post)
    if check == "iter1":
        db_write1(nick,post,timePost,contentType,time_of_iter,like,comment,video_view_count,hashtag)
    elif check == "iter2":
        db_write1(time_of_iter,like,video_view_count,comment,post)
    elif check == "iter3":
        db_write1(time_of_iter,like,video_view_count,comment,post)
    else:pass


# In[22]:


def find_data(input_html): #вытаскиваем днный из html страницы
    a=input_html.split('edge_media_to_caption') #находим первый пост
    nick=a[0].split('"username":"')[1].split('","')[0]
    localBase={}
    for counter in range(1,13):
        try:
            shortcode=a[counter].split('"shortcode":"')[1].split('"')[0]
            post=shortcode
        except:
            post= None
            pass
        try:
            comment=a[counter].split('"edge_media_to_comment":{"count":')[1].split('}')[0]  
        except:
            comment= None
            pass
        try:
            like=a[counter].split('"edge_media_preview_like":{"count":')[1].split('}')[0]
        except:
            like= None
            pass
        try:
            is_video=a[counter].split('"is_video":')[1].split('}')[0]
        except:
            like= None
            pass
        try:
            timePost=a[counter].split('"taken_at_timestamp":')[1].split(',')[0]
        except:
            timePost= None
            pass
        try:
            textPost=a[counter].split('{"text":')[1].split('}}]},"shortcode"')[0]
            #textPost = textPost.compile('[^a-zA-Z ]')
            textPost=textPost.split()
            hashtag=""
            for item in textPost: #находим все хештеги на английском
                if "#" in item:
                    try:
                        item=item.split('\\')[0]
                    except:pass
                    try:
                        item=item.split('"')[0]
                    except:pass
                    hashtag=hashtag+item
        
        except:
            hashtag= None
            pass
        #print(hashtag)
        try:
            if is_video=="false":
                contentType="photo"
            else:
                contentType="video"
        except:
            contentType = None
        try: #count of video views
            if contentType == "video":
                video_view_count = a[counter].split('"video_view_count":')[1].split('}}')[0]
            else:
                video_view_count = None
        except:
            video_view_count = None
        ################################запаковываем в бд
        time_of_iter=time.time()
        check=db_check(post)
        ########## определим возраст поста
        if age_ofpost(timePost) is True:
            check_func(nick,post,timePost,contentType,time_of_iter,like,comment,video_view_count,hashtag)
        else:
            if post is not None:pass
                #print("Post",post,"is too old")
            elif post is None:pass
                #print("Post is not available")
            else:
                pass
        ##########


# In[23]:


def random_UA():     #выбираем рандомный юзер-агент из файла uaList // генерация юзер-агента
    lines = open(uaList).read().splitlines()
    myline =random.choice(lines)
    myline="'"+myline+"'" #добавляем кавычки
    return myline
    


# In[24]:


def uni_parce(): #вызывам парсинг и упаковку данных в строку
    clearLinks=txt_to_list()
    db_set()
    locbase={}
    while True:
        for item in clearLinks: # берем ссылки на акки из базы
            print(item)
            try:
                time.sleep(7)########################################SLEEP################################
                user_agent=random_UA()
                instas_html=parce(item,user_agent)
                if "Page Not Found" in instas_html:
                    print(item,"Page Not Found")
                elif '"is_private":true' in instas_html:
                    print(item,"This Account is Private")
                elif "Sorry, this page isn't available." in instas_html:
                    print(item,"Sorry, this page isn't available.")
                elif "Please wait a few minutes before you try again" in instas_html:
                    print("Please wait a few minutes before you try again")
                else:
                    locbase=find_data(instas_html)
            except IndexError:
                print("Oooops... IndexError")
        break
#uni_parce()
#print(5*"#","DONE",5*"#")
    

