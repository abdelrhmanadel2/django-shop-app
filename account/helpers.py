import random

from django.core.cache import cache

def send_otp_to_email(email,user_obj):
    if cache.get(email):
        return False
    else:
        try:
            otp_to_sent=random.randint(1000,9999)
            cache.set(email,otp_to_sent,timeout=25)
            print(otp_to_sent)
            user_obj.otp=otp_to_sent
            user_obj.save()
            return True,

        except Exception as e:
            print(e)
