## IMPORT LIBRARY

import requests
import urllib
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import facebook
import pandas as pd
import datetime

## FUNCTIONS

def get_user_access_token(email,password,client_id):
    '''
    Get user's access token
    '''

    # Initiate driver to log in to facebook
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(f"https://www.facebook.com/dialog/oauth?client_id={client_id}&redirect_uri=https://www.facebook.com/connect/login_success.html&response_type=token")
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[1]/input').send_keys(email)
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[2]/input").send_keys(password)
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/button").click()
    time.sleep(2)
    acc_tok = driver.current_url
    driver.close()    
    access_token = urllib.parse.urlparse(acc_tok).fragment[13:-55]
    
    return access_token

def get_page_access_token(user_acc_token,page_name):
    '''
    Get Page Access Token
    '''

    # Initiate Graph Api
    graph = facebook.GraphAPI(user_acc_token)
    
    # Get the list of available accounts
    listacc = graph.get_object('me/accounts')
    
    for i in listacc['data']:
#         print(i)
#         print(i['name']==page_name)
        if i['name']==page_name:
            page_access_token = i['access_token']
            page_id = i['id']
    return page_access_token,page_id
        
def date_to_timestamp(date_string):
    '''
    Convert date string to time stamp
    '''
    date = datetime.datetime.strptime(date_string, "%Y/%m/%d %H:%M:%S")
    timestamp = datetime.datetime.timestamp(date)
#     print(str(int(timestamp)))
    return str(int(timestamp))

def clean_message(msg):
    '''
    Receive message and convert hash sign into %23
    '''
    return msg.replace('#','%23')

def post_to_wall(page_id=None,message=None,page_access_token=None,
                 timestamp=None,link=None, VID_PATH=None, IMG_PATH=None, VID_TITLE=None):
    '''
    Function to post to wall
    '''
    print(link)
    publish=None
    
    if timestamp is not None:
        publish='false'
        timestamp = date_to_timestamp(timestamp)
    
    if VID_PATH is not None:
        print("Video Post")
        print("Dalam post-to_wall"+VID_TITLE)
        if link is None:
            link = ''
        
        data = {
        'title': VID_TITLE,
        'description': clean_message(message) + "\n\n" + link,
        'access_token': page_access_token,
        'published': publish,
        'scheduled_publish_time':timestamp,    
        }
        
        files = {
            'file': open(VID_PATH, 'rb')
        }
        
        x = requests.post(f'https://graph.facebook.com/{page_id}/videos',data=data, files=files)
        return x.text
    
    elif IMG_PATH is not None:
        print("Image Post")
        if link is None:
            link =''
        
        data = {
        'message': clean_message(message) + '\n' + link,
        'access_token': page_access_token,
        'published': publish,
        'scheduled_publish_time':timestamp,
        }
        
        files = {
            'file': open(IMG_PATH, 'rb')
        }
        
        x = requests.post(f'https://graph.facebook.com/{page_id}/photos', data=data, files=files)
        return x.text
    
    else:
        print("Normal Post")
        print(link)
        data={
        'message': clean_message(message),
        'access_token':page_access_token,
        'published': publish,
        'scheduled_publish_time':timestamp,
        'link':link
        }

        url=f"https://graph.facebook.com/{page_id}/feed"

        x = requests.post(url,data=data)
        return x.text

## MAIN PROGRAM

# Get the users details from csv file
details_df = pd.read_csv("login_details.csv")

email = details_df.loc[0][0]
password = details_df.loc[0][1]
client_id= details_df.loc[0][2]

# Get access token
access_token = get_user_access_token(email,password,client_id)

# Load post data
post_df= pd.read_csv("Post_templates.csv").fillna(value= '')

# Loop through the data and post it on FB
for index, row in post_df.iterrows():
    print()
    if row[2].strip() == '':
        print("masuk")
        link = None
    else:
        link = row[2]
    if row[3].strip() == '':
        IMG_PATH = None
    else:
        IMG_PATH = row[3]
    if row[4].strip() == '':
        VID_PATH = None
    else:
        VID_PATH = row[4]
    if row[5].strip() == '':
        VID_TITLE = None
    else:
        VID_TITLE = row[5]
    
    print(index,type(row[-1]))
    print(row[5])
    page_access_token,page_id = get_page_access_token(access_token,row[0])
    print(page_access_token,page_id)
    
#     timestamp = date_to_timestamp(row[-1])
#     print(timestamp)
    print(link)
    print(post_to_wall(page_id,row[1],page_access_token,row[-1],link,VID_PATH,IMG_PATH,VID_TITLE))

