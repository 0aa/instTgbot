
# coding: utf-8

# In[66]:

import sqlite3
import statistics
path_toDB="D:\\bot\\instaSQL.db"


# In[73]:


def check_stats(minimum):    
    conn = sqlite3.connect(path_toDB) #open DB
    c = conn.cursor() #create cursor
    c.execute('''SELECT DISTINCT nick FROM post_stats''')
    base=[]
    temp_base=[]
    for line in c.fetchall():
        nick=line[0]
        c.execute('''SELECT * FROM post_stats WHERE nick=(?)''',(line))
        for row in c.fetchall():
            base.append(row[5])
        cur_median=int(statistics.median(base)) #считаем медиану по нику 
        #print(nick, cur_median)
        c.execute('''SELECT * FROM post_stats WHERE nick=(?)''',(line))
        for row in c.fetchall():
            if row[5]/cur_median>minimum:
                a=row[5]/cur_median
                a=float('{:.2f}'.format(a))
                msg=nick,"x"+str(a),row[5],"https://www.instagram.com/p/"+row[1],row[16]
                temp_base.append(msg)
                #print(nick,"x"+str(a),row[5],"https://www.instagram.com/p/"+row[1])
            else:pass
            
        
        base=[]
    return temp_base
#m=7
#c=check_stats(m)
#for line in c:
#    print(line)

