'''
Created on Feb 10, 2019

@author: justo
'''
import imaplib, email, Proxy, json, re, smtplib
from random import randint
from time import sleep
from time import time
debug = False
proxies = Proxy.GetProxies(10)

def getNewEmails():
    connection = imaplib.IMAP4_SSL('imap.gmail.com')
    connection.login('REDACTED', 'REDACTED')
    connection.select('inbox')
    typ, data = connection.search(None, '(UNSEEN SUBJECT "survey")')
    emails = []
    for num in data[0].split():
        typ, data = connection.fetch(num, '(RFC822)')
        emailobj = email.message_from_bytes(data[0][1])
        emails.append(emailobj)
    connection.close()
    connection.logout()
    return emails

def sendEmail(recipient,message):
    connection = smtplib.SMTP_SSL("smtp.gmail.com")
    connection.login('REDACTED', 'REDACTED')
    connection.sendmail('SurveyBot',recipient,message)
    connection.close()
    print('Email sent')
    
def Next(chrome):
    sleep(1)
    chrome.find_element_by_id('NextButton').click()
    sleep(1)
    
def CheckProxy(chrome):
    start = time()
    chrome.get('REDACTED')
    if chrome.find_elements_by_id('main-frame-error') or time()-start >= 10:
        print("Invalid Proxy")
        return False
    else:
        return True
        
def takeSurvey(code):
    global debug,proxies
    ccs = ['//*[@id="FNSR00704"]/span/span','//*[@id="FNSR00637"]/span/span']
    bk = ['//*[@id="FNSR00701"]/span/span','//*[@id="FNSR00031"]/span/span']
    paths = [ccs,bk]
    fries = bool(randint(0,1))
    loading = True
    trys = 25
    while loading:
        options = Proxy.webdriver.ChromeOptions()
        if not debug: options.add_argument('--window-position=-500,0'); options.add_argument('--window-size=500,500')
        if len(proxies) == 0: print('getting new proxies'); proxies = Proxy.GetProxies(10)
        chrome = Proxy.StartChromeProxy(proxies.pop(0),options)
        if trys > 0:
            try:
                loading = not CheckProxy(chrome)
                if loading: chrome.quit()
            except Exception as error:
                chrome.quit()
                return False, str(error)
        else:
            chrome.quit()
            return False, 'ProxyError: Could not connect to a valid proxy'
        trys -= 1
    try:
        sleep(2)
        chrome.find_element_by_id('Initial_StoreID').send_keys('REDACTED')
        Next(chrome)
        trys = 10
        while not chrome.find_elements_by_id('CN1'):
            sleep(1)
            trys -= 1
            if trys == 0: return False, 'PageLoadError: Could not the page'
        chrome.find_element_by_id('CN1').send_keys(code[:3])
        sleep(.5)
        chrome.find_element_by_id('CN2').send_keys(code[3:6])
        sleep(.5)
        chrome.find_element_by_id('CN3').send_keys(code[6:9])
        sleep(.5)
        chrome.find_element_by_id('CN4').send_keys(code[9:12])
        sleep(.5)
        chrome.find_element_by_id('CN5').send_keys(code[12:15])
        sleep(.5)
        chrome.find_element_by_id('CN6').send_keys(code[15:18])
        sleep(.5)
        chrome.find_element_by_id('CN7').send_keys(code[18:])
        Next(chrome)
        if chrome.find_elements_by_class_name('Error'):
            chrome.quit()
            raise ValueError(f'InvalidCodeError: {code} is an invalid/expired Survey Code')
        chrome.find_element_by_xpath('//*[@id="FNSR04000"]/td[2]/span').click() #Highly satisfied
        Next(chrome)
        chrome.find_element_by_xpath('//*[@id="FNSR01000"]/div[2]/div/div[1]/span/span').click() #Drive-Thru
        Next(chrome)
        chrome.find_element_by_xpath('//*[@class="Opt4 rbloption"]/span/span').click() #Speaker
        Next(chrome)
        chrome.find_element_by_xpath('//*[@id="FNSR10000"]/td[2]/span').click() #speed
        sleep(.5)
        chrome.find_element_by_xpath('//*[@id="FNSR00108"]/td[2]/span').click() #friendliness
        sleep(.5)
        chrome.find_element_by_xpath('//*[@id="FNSR15000"]/td[2]/span').click() #temperature
        sleep(.5)
        chrome.find_element_by_xpath('//*[@id="FNSR00622"]/td[2]/span').click() #cleanliness
        sleep(.5)
        chrome.find_element_by_xpath('//*[@id="FNSR00002"]/td[2]/span').click() #quality
        sleep(.5)
        chrome.find_element_by_xpath('//*[@id="FNSR00251"]/td[2]/span').click() #accuracy
        Next(chrome)
        chrome.find_element_by_xpath('//*[@id="FNSR29000"]/td[2]/span').click() #return
        Next(chrome)
        chrome.find_element_by_xpath('//*[@id="FNSR00623"]/div[2]/div/div[1]/span/span').click() #on screen
        sleep(.5)
        chrome.find_element_by_xpath('//*[@id="FNSR00604"]/div[2]/div/div[1]/span/span').click() #got at window
        Next(chrome)
        chrome.find_element_by_xpath('//*[@id="FNSR33000"]/td[3]/span').click() #problem
        Next(chrome)
        if fries: chrome.find_element_by_xpath('//*[@id="FNSR00702"]/span/span').click(); print('French Fries!'); sleep(.5)
        path = randint(0,1)
        print('Bacon King!' if path else 'Crispy Chicken Sandwich!')
        path = paths[path]
        chrome.find_element_by_xpath(path[0]).click() #food type
        Next(chrome)
        chrome.find_element_by_xpath(path[1]).click() #sandwich
        Next(chrome)
        if fries: chrome.find_element_by_xpath('//*[@id="FNSR00064"]/span/span').click(); Next(chrome)
        chrome.find_element_by_xpath('//*[@id="FNSR44000"]/td[2]/span').click() #satisfaction
        Next(chrome)
        chrome.find_element_by_xpath('//*[@id="FNSR50000"]/td[2]/span').click() #packaged
        sleep(.5)
        chrome.find_element_by_xpath('//*[@id="FNSR00392"]/td[2]/span').click() #appearance
        sleep(.5)
        chrome.find_element_by_xpath('//*[@id="FNSR54000"]/td[2]/span').click() #value
        sleep(.5)
        chrome.find_element_by_xpath('//*[@id="FNSR46000"]/td[2]/span').click() #size
        Next(chrome)
        chrome.find_element_by_xpath('//*[@id="FNSR52000"]/td[2]/span').click() #taste
        sleep(.5)
        chrome.find_element_by_xpath('//*[@id="FNSR53000"]/td[2]/span').click() #temperature
        sleep(.5)
        chrome.find_element_by_xpath('//*[@id="FNSR00391"]/td[2]/span').click() #quality
        Next(chrome)
        chrome.find_element_by_xpath('//*[@id="FNSR55000"]/td[2]/span').click() #re-purchase
        Next(chrome)
        Next(chrome)
        chrome.find_element_by_xpath('//*[@id="FNSR02000"]/div[2]/div/div[1]/span/span').click() #just myself
        sleep(.5)
        chrome.find_element_by_xpath('//*[@id="FNSR00595"]/div[2]/div/div[1]/span/span').click() #learn
        Next(chrome)
        chrome.find_element_by_xpath('//*[@id="FNSR00638"]/td[3]/span').click() #recognize
        Next(chrome)
        chrome.quit()
        return True, None
    except Exception as error:
        input('Can you see what went wrong?')
        chrome.quit()
        return False, str(error)
while True:
    emails = getNewEmails()
    print('Found',len(emails),'new emails')
    for mail in emails:
        successes = 0
        errors = []
        reply = False
        for part in mail.walk():
            if 'plain' in part.get_content_type():
                text = part.get_payload()
                if text.lower() == 'stop':
                    print('stop')
                    reply = True
                    userfile = open('users.dat','r')
                    users = json.load(userfile)
                    userfile.close()
                    user = re.search('<.*>', mail['From']).group(0).replace('<','').replace('>','')
                    users[user] = 0
                    userfile = open('users.dat','w')
                    json.dump(users, userfile)
                    userfile.close()
                elif text.lower() == 'errors':
                    print('errors')
                    reply = True
                    userfile = open('users.dat','r')
                    users = json.load(userfile)
                    userfile.close()
                    user = re.search('<.*>', mail['From']).group(0).replace('<','').replace('>','')
                    users[user] = 1
                    userfile = open('users.dat','w')
                    json.dump(users, userfile)
                    userfile.close()
                else:
                    text = ''.join(text.split())
                    codes = text.split(',')
                    print('codes =',codes)
                    for code in codes:
                        if code.isdigit():
                            if len(code) == 20:
                                if len(proxies) == 0: proxies = Proxy.GetProxies(len(codes))
                                success, error = takeSurvey(code)
                                if success:
                                    successes += 1
                                else:
                                    errors.append(error)
                            else:
                                errors.append(f"InvalidCodeError: Survey Codes must be 20 digits long and {code} is {len(code)} digits long")
                        else:
                            errors.append(f"InvalidCodeError: Survey Codes can only contain digits and {code} contains non-digit characters")
        if not reply:
            userfile = open('users.dat','r')
            users = json.load(userfile)
            userfile.close()
            feedback = 2
            user = re.search('<.*>', mail['From']).group(0).replace('<','').replace('>','')
            if user in users:
                feedback = users[user]
            else:
                users[user] = feedback
                userfile = open('users.dat','w')
                users = json.dump(users, userfile)
                userfile.close()
            if feedback == 2:
                message = f'Submited {successes} survey(s) with {len(errors)} errors\n'
                for error in errors:
                    message += error+'\n'
                message += 'Reply ERRORS to only receive feedback on errors or STOP to not receive any feedback.'
                sendEmail(user, message)
            elif feedback == 1 and len(errors) > 0:
                message = f'Ran into {len(errors)} errors while submitting survey(s)\n'
                for error in errors:
                    message += error+'\n'
                message += 'Reply ERRORS to only receive feedback on errors or STOP to not receive any feedback.'
                sendEmail(user, message)
            if len(errors) > 0:
                message = f'Ran into {len(errors)} errors while submitting survey(s) on behalf of {mail["From"]}\n'
                for error in errors:
                    message += error+'\n'
                sendEmail('justoboy13@gmail.com', message)
    sleep(60*30)
