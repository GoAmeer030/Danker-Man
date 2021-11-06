from celery import shared_task
from django.contrib import messages
from django.http import HttpRequest
from .models import UserAuthentication, User
from .helpers import key_mail
import discum
import billiard
import random
import time
import rsa

global Nor_Timer_Back, Send_Message_Front

def Send_Message(Message, tokan, ch_id, usera, bnumb, user):

    if usera is not None and bnumb is not None:

        sec = random.choice([3, 4, 5, 6])
        time.sleep(sec)
        discum.Client(token=tokan, user_agent=usera, build_num=bnumb).sendMessage(ch_id, Message)
            
    else:

        user_obj = User.objects.get(username=user)

        bot = discum.Client(token=tokan)
            
        bnumb = bot.getBuildNumber()
        usera = bot._Client__user_agent
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

def CommandSelection(Messages, user, pri_key):

    while True:

        try:

            user_obj = User.objects.get(username=user)

            e_tokn = getattr(UserAuthentication.objects.first(), 'D_Auth')
            e_email = getattr(UserAuthentication.objects.first(), 'E_Mail')
            e_passw = getattr(UserAuthentication.objects.first(), 'P_Word')

            print(e_tokn, e_email, e_passw)

            if e_tokn != '' and e_tokn is not None:
                n, e, d, p, q = pri_key.split(',')
                p_key = rsa.PrivateKey(int(n), int(e), int(d), int(p), int(q))
                token = rsa.decrypt(e_tokn, p_key).decode()

                email = ''
                passw = ''

            elif e_email != '' and e_email is not None:
                n, e, d, p, q = pri_key.split(',')
                p_key = rsa.PrivateKey(int(n), int(e), int(d), int(p), int(q))
                email = rsa.decrypt(e_email, p_key).decode()
                passw = rsa.decrypt(e_passw, p_key).decode()

                bot = discum.Client(email=email, password=passw)
                token = bot._Client__user_token

                pub_key, pri_key = rsa.newkeys(1024)
                e_auth = rsa.encrypt(token.encode(), pub_key)

                userobj = UserAuthentication.objects.update_or_create(
                    U_User = user_obj,
                    defaults={
                        "D_Auth": e_auth,
                    }
                )

                key_mail(pri_key, user_obj.email)
                messages.success(HttpRequest, 'New key has send to your mail, start the bot again with the new key')

                raise ValueError('Start Again')

            ch_id = str(getattr(UserAuthentication.objects.first(), 'D_ChID'))
            usera = getattr(UserAuthentication.objects.first(), 'U_Agen')
            bnumb = getattr(UserAuthentication.objects.first(), 'B_Numb')


            item = random.choice(Messages)


            if item[0] in ['pls se', 'pls bet', '!flip heads', '!flip tails', '!slots', 'bg']:

                item_1 = random.randrange(500, 3000)

                Nor_Timer_Back = billiard.Process(target=Nor_Timer, args=(item, Messages))
                Send_Message_Front = billiard.Process(target=Send_Message, args =(f'{item[0]} {str(item_1)}', token, ch_id, usera, bnumb, user))

                Nor_Timer_Back.daemon = True
                Send_Message_Front.daemon = True

                Nor_Timer_Back.start()
                Send_Message_Front.start()

                Send_Message_Front.join()

            else:

                Nor_Timer_Back = billiard.Process(target=Nor_Timer, args=(item, Messages))
                Send_Message_Front = billiard.Process(target=Send_Message, args =(item[0], token, ch_id, usera, bnumb, user))

                Nor_Timer_Back.daemon = True
                Send_Message_Front.daemon = True

                Nor_Timer_Back.start()
                Send_Message_Front.start()

                Send_Message_Front.join()


        except IndexError:

            time.sleep(10)
            CommandSelection(Messages)

@shared_task(bind=True)
def bbot(self, bot, user, pri_key):

    if bot == 'Dank_Memer':
        Messages = [['pls fish', 40], ['pls hunt', 40], ['pls dig', 40],
                      ['pls se', 10], ['pls beg', 40], ['pls dep all', 300],
                      ['pls bal', 120], ['pls level', 3600], ['pls bet', 8],
                      ]

    elif bot == 'Taco':
        Messages = [['!tips', 300], ['!clean', 7200], ['!work', 600], 
                      ['!flip heads', 60], ['!flip tails', 60], ['!scratch', 30], 
                      ['!slots', 60], ['!roll', 60]]

    elif bot == 'VirFish':
        Messages = [['%f', 1], ['%s all', 3600]]

    else:
        Messages = [['bb', 600], ['bw', 30], ['be', 5], 
                      ['bi', 1200], ['bdep all', 6000], ['brankup', 12000], 
                      ['bsa force', 12000], ['bh', 5], ['bg', 360]]

    main = billiard.Process(target=CommandSelection, args = (Messages, user, pri_key))

    main.start()

    time.sleep(60)

    main.terminate()

    return "Done"
