def start():
    print("import successful")

import yagmail
import time

def time_counter(user = '',  password='',to = [''],\
                 subject = 'No subject',content = None, attachment = None):
    '''
    user(str)
    password(str)
    to(str)(list(str))
    subject(str)
    content(str)
    attachment(str)(list(str))
    '''
    # edit decorator
    def decorator(func):
        def inner(*args, **kwargs):
            # time counter
            time_start=time.time()
            
            # run the main func.
            ret = func(*args, **kwargs)
            
            time_end=time.time()
            time_h = float(time_end-time_start)/3600.0
            
            # email sender
            content_time = 'Training result:\nTime cost: '+str(time_h)+' h\n'
            yag = yagmail.SMTP(user=user, password=password, host='smtp.163.com', encoding='GBK')
            yag.send(to, subject,content_time+str(content),attachment)

            
            yag.close()
            return ret
        return inner

    return decorator