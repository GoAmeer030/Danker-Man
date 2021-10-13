from celery import shared_task
from .models import UserAuthentication
import billiard as mp
import requests
import random
import time

def Danker_Man(Token, Channel_Id, Message):
    payload = {
        'content': Message
    }

    header = {
        'authorization': Token
    }

    url_typing = 'https://discord.com/api/v9/channels/{}/typing'.format(Channel_Id)

    url_message = 'https://discord.com/api/v9/channels/{}/messages'.format(Channel_Id)

    r1 = requests.post(url_typing, headers=header)

    sec = random.choice([3, 4, 5, 6])
    time.sleep(sec)

    r2 = requests.post(url_message, data=payload, headers=header)

def Nor_Timer(item, Messages):

    Messages.remove(item)

    for i in range(item[1]+1):
        time.sleep(1)
        if i == item[1]:
            Messages.append(item)

def CommandSelection(Token, Channel_Id, Messages):

    while True:

        try:

            item = random.choice(Messages)


            if item[0] in ['pls se', 'pls bet', '!flip heads', '!flip tails', '!slots']:

                item_1 = random.randrange(500, 3000)

                Nor_Timer_Back = mp.Process(target=Nor_Timer, args=(item, Messages))
                Danker_Man_Front = mp.Process(target=Danker_Man, args =(Token, Channel_Id, ('{0} {1}'.format(item[0],str(item_1)))))

                Nor_Timer_Back.start()
                Danker_Man_Front.start()

                Danker_Man_Front.join()

            else:

                Nor_Timer_Back = mp.Process(target=Nor_Timer, args=(item, Messages))
                Danker_Man_Front = mp.Process(target=Danker_Man, args =(Token, Channel_Id, item[0]))

                Nor_Timer_Back.start()
                Danker_Man_Front.start()

                Danker_Man_Front.join()


        except IndexError:

            time.sleep(10)
            CommandSelection(Token, Channel_Id, Messages)

@shared_task(bind=True)
def dank_memer(self):

    field_name = 'D_Auth'
    obj = UserAuthentication.objects.first()
    Token = getattr(obj, field_name)

    field_name = 'D_ChID'
    obj = UserAuthentication.objects.first()
    Ch_ID = getattr(obj, field_name)

    Messages = [['pls fish', 40], ['pls hunt', 40], ['pls dig', 40],
                ['pls se', 10], ['pls beg', 40], ['pls dep all', 300],
                ['pls bal', 120], ['pls level', 3600], ['pls bet', 8],
                ]

    y = mp.Process(target=CommandSelection, args = (Token, Ch_ID, Messages))

    y.start()

    time.sleep(60)

    y.terminate()

    return "Done"

@shared_task(bind=True)
def taco(self):

    field_name = 'D_Auth'
    obj = UserAuthentication.objects.first()
    Token = getattr(obj, field_name)

    field_name = 'D_ChID'
    obj = UserAuthentication.objects.first()
    Ch_ID = getattr(obj, field_name)

    Messages = [['!tips', 300], ['!clean', 7200], ['!work', 600], ['flip heads', 60], ['flip tails', 60], ['!scratch', 30], ['!slots', 60], ['!roll', 60]]

    y = mp.Process(target=CommandSelection, args = (Token, Ch_ID, Messages))

    y.start()

    time.sleep(60)

    y.terminate()

    return "Done"