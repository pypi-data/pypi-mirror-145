# esender
## Introduction
This package is developed based on yagmail and is used to send e-mail in python. It can only work with 163 e-mail now. Personaly, I use it to send deep learning progress to my mailbox. (Significantly reduced my anxiety)  
## Installation
```
pip install esender

# With Tsinghua open source mirror
pip install esender -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```
## Notes for @163.com 
Usually, you need to turn on the IMAP/SMTP service of your account manually. That is free. It will generate an authorization password which is exactly the input password in the example below. Note that you don't need the password of your account to send the e-mail.

## Usage

### Scenario 1
Send a email directly with function 'Esender'

Example:
```
from esender import Esender

Esender(user = 'your163account@163.com',  password='****',to = ['yourtargetemail@qq.com'],\
    subject = 'Subject',content = 'your content', attachment = './hello.txt')
```
### Scenario 2
Monitor the time consuming of a your task and send emails when the it ends.  

Example:
```
from esender import time_counter
@time_counter(user = 'your163account@163.com',  password='***',to = ['yourtargetemail@qq.com'],\
    subject = 'Subject',content = 'Your content', attachment = None)
def main():
    return ...

main()
```

# To do
- [ ] Add help()  
- [ ] Work with more e-mail