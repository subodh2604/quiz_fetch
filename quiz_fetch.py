import configparser
import json
import asyncio
from datetime import date, datetime
from datetime import date
from telethon.sync import TelegramClient, events
from telethon.tl import functions
from telethon.tl.functions.messages import SearchRequest
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.types import InputPeerUser, InputMessagesFilterEmpty
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)
today = date.today()
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)
config = configparser.ConfigParser()
config.read("config-sample.ini")
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

#  client created and connect....
client = TelegramClient(username, api_id, api_hash)
#filter=InputMessagesFilterMedia()
async def main(phone):
    await client.start()
    print("Client Created")
    
    d=input("do you want to todays quiz only? ")
    if d=='y':
        todayquiz='y'
    else:
        todayquiz=None
        
    search="UPscquiz"
    channels= await client(functions.contacts.SearchRequest(
        q=search,
        limit=100
    ))
    ch=channels.results
    user_input_channel=[]
    for c in range (0,len(ch)):
        l=str(ch[c].channel_id)
        user_input_channel.append(l)
    all_messages = []
    for i in user_input_channel:
        #print(i)
        if i.isdigit():
            entity = PeerChannel(int(i))
        else:
            entity = i    
        my_channel = await client.get_entity(entity)
        jsonname=str(my_channel.id)+".json"
        offset_id = 0
        total_messages = 0
        total_count_limit = 100
        quiz=[]
        limit = 100
        while True:
            history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            #offset_date=datenow,
            #min_date=datenow,  # Minimum date
            #max_date=datenow,  # Maximum date
            max_id=0,
            min_id=0,
            hash=0,
            ))
            if not history.messages:
                break
            messages = history.messages
            for m in messages:
                #all_messages.append(m.to_dict())
                try:
                    d={}
                    ans=[]
                    r=m.media.results.results
                    anwer=m.media.poll.answers
                    now=str(m.date)
                    now1=now.split()
                    #print(now1[0])
                    #print()
                    #print(date.today())
                    if now1[0]==str(date.today()) and todayquiz=='y':
                        #print(now1[0])
                        #print()
                        #print(date.today())
                        #print(m.date)
                        k=1
                        d['Date']=str(m.date)
                        d["question"]=m.media.poll.question

                        for j in anwer:        
                            m="option%s"%(k)
                            d[m]=j.text
                            ans.append(j.text)
                            k=k+1
                        try:
                            for t in r:
                                corr=t.correct
                                if corr is True:
                                    op=t.option.decode("utf-8")
                                    inte=int(op)
                                    d['Answer']=ans[inte]
                        
                        except:
                            d['Answer']="No answer given"  
                        s=d.copy()    
                        quiz.append(s)
                    else:
                        d={}
                        ans=[]
                        r=m.media.results.results
                        anwer=m.media.poll.answers
                        #print("all_msg")
                        #print(all_messages)
                        k=1
                        d['Date']=str(m.date)
                        d["question"]=m.media.poll.question

                        for j in anwer:        
                            m="option%s"%(k)
                            d[m]=j.text
                            ans.append(j.text)
                            k=k+1
                        try:
                            for t in r:
                                corr=t.correct
                                if corr is True:
                                    op=t.option.decode("utf-8")
                                    inte=int(op)
                                    d['Answer']=ans[inte]
                                    s=d.copy()
                                    all_messages.append(s)
                        
                        except:
                            d['Answer']="No answer given"  
                        s=d.copy()    
                        all_messages.append(s)

                except:
                    continue
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
        with open(jsonname, 'w') as outfile:
                    json.dump(quiz, outfile)
        
    with open("all_messagesquiz.json", 'w') as outfile:
        json.dump(all_messages, outfile)
with client:
    client.loop.run_until_complete(main(phone))