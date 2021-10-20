import discum
from celery import shared_task
from .models import UserAuthentication, User
import billiard
import random
import time

global Nor_Timer_Back, Send_Message_Front

def Send_Message(Message, tokan, ch_id, usera, bnumb, user):

    if usera is not None and bnumb is not None:
        sec = random.choice([3, 4, 5, 6])
        time.sleep(sec)
        discum.Client(token=tokan, user_agent=usera, build_num=bnumb).sendMessage(ch_id, Message)
        print("Top")
    else:
        bot = discum.Client(token=tokan)
        bnumb = bot.getBuildNumber()
        usera = bot._Client__user_agent
        user_obj = User.objects.get(username=user)
        print("Bottom")
        bot.sendMessage(ch_id, Message)

        userobj = UserAuthentication.objects.update_or_create(
            U_User = user_obj,
            defaults={
                "U_Agen": usera,
                "B_Numb": bnumb,
            }
        )

def Nor_Timer(item, Messages):

    Messages.remove(item)

    for i in range(item[1]+1):
        time.sleep(1)
        if i == item[1]:
            Messages.append(item)

def CommandSelection(Messages, user):

    while True:

        try:

            tokan = getattr(UserAuthentication.objects.first(), 'D_Auth')
            ch_id = str(getattr(UserAuthentication.objects.first(), 'D_ChID'))
            usera = getattr(UserAuthentication.objects.first(), 'U_Agen')
            bnumb = getattr(UserAuthentication.objects.first(), 'B_Numb')

            item = random.choice(Messages)


            if item[0] in ['pls se', 'pls bet', '!flip heads', '!flip tails', '!slots']:

                item_1 = random.randrange(500, 3000)

                Nor_Timer_Back = billiard.Process(target=Nor_Timer, args=(item, Messages))
                Send_Message_Front = billiard.Process(target=Send_Message, args =(f'{item[0]} {str(item_1)}', tokan, ch_id, usera, bnumb, user))

                Nor_Timer_Back.daemon = True
                Send_Message_Front.daemon = True

                Nor_Timer_Back.start()
                Send_Message_Front.start()

                Send_Message_Front.join()

            else:

                Nor_Timer_Back = billiard.Process(target=Nor_Timer, args=(item, Messages))
                Send_Message_Front = billiard.Process(target=Send_Message, args =(item[0], tokan, ch_id, usera, bnumb, user),)

                Nor_Timer_Back.daemon = True
                Send_Message_Front.daemon = True

                Nor_Timer_Back.start()
                Send_Message_Front.start()

                Send_Message_Front.join()


        except IndexError:

            time.sleep(10)
            CommandSelection(Messages)

@shared_task(bind=True)
def bbot(self, bot, user):

    if bot == 'Dank_Memer':
        Messages = [['pls fish', 40], ['pls hunt', 40], ['pls dig', 40],
                      ['pls se', 10], ['pls beg', 40], ['pls dep all', 300],
                      ['pls bal', 120], ['pls level', 3600], ['pls bet', 8],
                      ]
    else:
        Messages = [['!tips', 300], ['!clean', 7200], ['!work', 600], ['!flip heads', 60], ['!flip tails', 60], ['!scratch', 30], ['!slots', 60], ['!roll', 60]]

    main = billiard.Process(target=CommandSelection, args = (Messages, user))

    main.start()

    time.sleep(60)

    main.terminate()

    return "Done"