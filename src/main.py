import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup
import smtplib, ssl


def main(config_params):
    email_sent = False
    paramaters = parse_json(config_params)

    while(True):
        stock_status = get_content(paramaters["url"])
        
        if stock_status:
            print("Item in stock!")
            command = 'curl ' + paramaters["push_link"] + ' -d "Item is now in stock!"'
            os.system(command)
            if not email_sent:
                send_email(paramaters)
                email_sent = True

        else:
            print("Item not in stock!")
                
        time.sleep(2)

def get_content(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    #Following line of code is specific to Decathlons website stock system
    in_stock = soup.find_all("label", {"class": "color-green"})
    if len(in_stock) > 0:
        stock_status = True
    else:
        stock_status = False
    return stock_status



def send_email(config_params):
    
    gmail_user = config_params["sender_email"]
    gmail_password = config_params["sender_password"]

    sent_from = gmail_user
    to = config_params["receiver_emails"]
    subject = config_params["email_contents"][0]["subject"]
    body = config_params["email_contents"][0]["body"] + "{}".format(config_params["url"])

    email_text = """
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Something went wrong...')

def parse_json(json_path):
    with open(json_path) as json_file:
        json_contents = json.load(json_file)
    return json_contents


    

if __name__ == "__main__":
    print("Searching for Kayak")
   
    '''
    1. Settings file path below may need to be edited depending on how script is executed
    2. Placeholder settings file provided. Needs to be configured to user requirements

    '''
    settings_file = r"KayakSailor\data\settings.json" 
    main(settings_file)




    
    
        
        

