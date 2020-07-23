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
    d=input("do you want to todays quiz only? Yes or no ")
    if d.lower()=='y' or d.lower()=='yes':
        todayquiz=True
    else:
        todayquiz=False
        
    
    searchlist=['UPscquiz','SSCquiz','NEETquiz','HSCquiz','ias','upsc','ssc','neet','https://t.me/BotQuizGroup','https://t.me/PollQuizeBreaker','@banking_quizs',  
                'GATE','GRE','IAS','IPS','XAT','NABARD','CSE','IBPS','NDA','CDS','CAT','CTET','SSCCPO','SSCJE','SSCJHT','SSCMTS','RRBALP','RRBJE','RRBSSE','RRBNTPC',
                'DRDO','ISRO','ESIC','FCI','LICAAO','IITJAM','JEEMAIN','JEEADVANCED','AIIMS','JIPMER','BITSAT','UGCNET','CSIRNET','VITEEE','ITSAT',
                'NATA','LPUNEST','AMIE','ENAT','ECETFDH','PGCET','KEAM','BCECE','OrissaJEE','WBJEE','TripuraJEE','SRMJEEE','MAHCET','IPUCET','IMUCET',
                'VMUEEE','VSAT','AUEET','KIITEE','BVPCET','AEEE','KEE','BSAUEEE','SAAT','CUSATCAT','Sliet','VEE','BEEE','AMUEEE','AUEET',
                'FITJEE','Quest','vidyamandir','unacademy','Aakash','allencareer','IMS','Career','Brilliant','Bansal','elite','Naik','NarayanaGroup',
                'sahilstudy','Meditech','Insight','Advent','Agrawal','Resonance','Vidyasagar','Pie Education','KRISHNA COACHING','Mathiit Learning','Rao IIT',
                'Pathfinder','Raus IAS Study Circle','Chanakya IAS Academy','Sathya IAS Academy','Brain Tree India','Astitva I.C.S.','ALS IAS Academy',
                'Vajiram and Ravis IAS Academy','Khan Study Circle','Advance Education Center','Marigold Classes','Butchi Reddy Institute','Professional Rating',
                'Emphatic Result Academy','Symcom','Jayant Pai','ifocus training services','Phoenix Anglo Academy','TIME (Triumphant Institute of Management Education)',
                'Bulls Eye','BYJUs CAT Classes','TCYonline','Alchemist','Mindworkzz','MBAcrystalball','TIME','Competitive Careers','Excel Management Foundation',
                'Matrix Academy','Real Business Education','CET Tutorials','Magnus Institute','Defence Academy Coimbatore','mathematics','physics','chemistry',
                'biology','geography','civics','Indian Architecture incl. Art & Craft & Paintings','Physical Geography',' Geophysical phenomena','Indian Soils',
                'Finance','English','hindi','marathi','gujrati','tamil','SAARC','BRICS','IBSA','BIMSTEC','SCO','QUAD','NAFTA','GCC','Medical','Engineering','OSEE',
                'NATO','ASEM','UNASUR','NSG','ADB','Marketing','agricultural produce','Agricultural Finance & Insurance','Technology','Economics',
                'RailwayExam','IT','Electronics','Programming','languages','Nanotechnology','machine learning','data science','python','java','ruby',
                'Robotics','Electricity','magnetism','Bio-Chemistry','Atomic Chemistry','Degradation','Accountancy','General Awareness','Quantitative Aptitude',
                ' Reasoning Ability','https://t.me/ibpsclerkexam','https://t.me/RbiGradeBadda','https://t.me/ibpspoexam','https://t.me/sbipoexam',
                'https://t.me/sbiclerk','https://t.me/licaao','https://t.me/psujobs','https://t.me/defencejobsindia','https://t.me/studymaterialoureducation',
                'https://t.me/upsciascivil','https://t.me/gateexamonly','https://t.me/ssc4u','https://t.me/bankdotoureducationdotin','https://t.me/engineeringaspirant',
                'https://t.me/ouredu','	https://t.me/joinchat/ID-W5ULCnSiQRlf2xGY26w','	https://t.me/railwayrecruitmentboard','https://t.me/gsnotes',
                'https://t.me/VerbalReasoning','https://t.me/IESExamPreparation','https://t.me/studygroupour','https://t.me/railwayrecruitmentboard',
                'https://t.me/Quantitativea','https://t.me/boardexam'
                ]
    user_input_channel=[]
    for search in searchlist:
        try:
            #print("started",search)
            channels= await client(functions.contacts.SearchRequest(
        q=search,
        limit=100
        ))
            ch=channels.results
            for c in range (0,len(ch)):
                l=str(ch[c].channel_id)
                if l not in user_input_channel:
                    user_input_channel.append(l)
                    #print(search,l)
            #print("ended: ",search) 
                
        except:
            continue
            #print("northinh found in: ",search)        
    print(len(user_input_channel))
    #print(user_input_channel)    
    for i in user_input_channel:
        print(i)
        if i.isdigit():
            entity = PeerChannel(int(i))
        else:
            entity = i    
        my_channel = await client.get_entity(entity)
        if todayquiz==True:
            jsonname=str(my_channel.id)+"-"+str(date.today())+".json"
        else:    
            jsonname=str(my_channel.id)+".json"
        offset_id = 0
        all_messages = []
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
            max_id=0,
            min_id=0,
            hash=0,
            ))
            if not history.messages:
                break
            messages = history.messages
            for m in messages:
                all_messages.append(m.to_dict())
                d={}
                ans=[]
                try:    
                    r=m.media.results.results
                    anwer=m.media.poll.answers
                    now=str(m.date)
                    now1=now.split()
                    if now1[0]==str(date.today()) and todayquiz==True:
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
                    elif todayquiz==False:
                        k=1
                        print('hekko')
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
                except:
                    continue
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                if quiz:
                    with open(jsonname, 'w') as outfile:
                        json.dump(quiz, outfile)
                break
with client:
    client.loop.run_until_complete(main(phone))