import telegram_send
import requests
import json
import time
import telegram

token = "1652538492:AAFYyXkKBm-kDdVIPkSIgPFJdNwMaWE_Tvs"
bot = telegram.Bot(token)
scorelist = [0]*100
prevdata = ""

while True:

    count = 0
    response = requests.get('https://hs-consumer-api.espncricinfo.com/v1/pages/matches/live?')
    time.sleep(5)
    data = json.loads(response.text)

    if prevdata != data:
        prevdata = data
        for liveInning in data['content']['matches']:
            if liveInning['liveInning'] != None:
                msg = ""
                msg = msg + "### "+ liveInning['slug']  +" ###" + "\n"
                msg = msg + liveInning['state'] + "\n"
                msg = msg + liveInning['statusText'] + "\n"
                flag = False

                for isLive in liveInning['teams']:

                    if isLive['isLive'] == False:
                        if isLive['score'] == None:
                            msg = msg + "Bowling...🤾‍♂️" + "\n"
                        else:
                            msg = msg + isLive['team']['name']+" scored: "+isLive['score'] + "\n"
                    if isLive['isLive'] == True:
                        if scorelist[count] == 0:
                            scorelist.insert(count, isLive['score'])
                            flag = True
                        elif scorelist[count] != isLive['score']:
                            flag = True
                            scorelist[count] = isLive['score']
                        else:
                            flag = False

                        msg = msg + isLive['team']['name']+" current score: "+isLive['score'] + "\n"
                        msg = msg + "Score Info: "+isLive['scoreInfo'] + "\n"

                if flag == True:
                   output = bot.send_message(chat_id="-1001321042356", text=msg)

                count = count+1
