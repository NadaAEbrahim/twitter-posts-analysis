

import pandas as pd
import tweepy

consumer_key = 'zhuAFoU2EgONsSBPktifQs8SV'
consumer_secret = '7WeZc98tNWhGM3tzcuo0RcDL7F02dVUm4tox05LhjbSlmY3AO7'
access_token_key = '1199033096554852352-bnR7ejM8Ve4v1tgKQRNOBLNxUDPlx9'
access_token_secret = 'dWZmqwXnxygFC4PNfb6YMcquZZ1cGXkkb6G8EjDsG4nZ8'

# make an auth to twitter to get the user data
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

#connect with twitter api
api = tweepy.API(auth)

# takes the username from formand check for if it exists, return all timeline if this user exists
def getUser(name):
    
    user = api.get_user(name)
    return user


def validUser(name):
    valid = getUser(name)
    if (valid) == None:     
        return False
    else:
        return True
      
# takes the username and get back his name and his profile img
def get_profile_name_and_img(name):
    user = getUser(name)
    profile_name = user.name
    img = user.profile_image_url
    screen_name = user.screen_name
    return profile_name, img, screen_name

# take the username and get his friends pages(that's he follow it) and get back 5 tweets from every page
# the data returned containes the page name, screen name(username), tweets, created time, favorite counts(likes), retweet counts 
def get_tweets_timeline(name):
    data = []
    user = getUser(name)
    friend = user.friends()
    for page in friend:
        frinds_tweets_dict = {}
        tweets = []
        f_retweet_count = []
        f_favorite_count = []
        f_created_at = []
        u = page.screen_name
        user = getUser(u)
        user_name = user.screen_name
        f_name = user.name
        f_img_url = user.profile_image_url
        stats = user.timeline()
        if len(stats) < 5:
            for t in stats:
                tweets.append(t.text)
                f_retweet_count.append(t.retweet_count)
                f_favorite_count.append(t.favorite_count)
                f_created_at.append(t.created_at)
        else:
            for t in user.timeline(count = 5):
                tweets.append(t.text)
                f_retweet_count.append(t.retweet_count)
                f_favorite_count.append(t.favorite_count)
                f_created_at.append(t.created_at)
        frinds_tweets_dict.update(name=f_name, screen_name='@'+user_name, img_url=f_img_url, tweets=tweets, retweet_counts=f_retweet_count, fav_count=f_favorite_count, created_time=f_created_at) 
        data.append(frinds_tweets_dict)
    
    data.sort(key = lambda x:x['created_time'], reverse = True)
    return data

# take the data and return it as a Dataframe used for dividing tweets to each category
def get_df_data(data):
    names = []
    sc_names = []
    imgs = []
    tweets = []
    retweet_c = []
    fav_c = []
    created_time = []
    dataset = pd.DataFrame(data, columns=['name', 'screen_name', 'img_url', 'tweets', 'retweet_counts', 'fav_count', 'created_time'])
    for i in range(len(dataset['tweets'])):
        for j in range(len(dataset['tweets'][i])):
            names.append(dataset['name'][i])
            sc_names.append(dataset['screen_name'][i])
            imgs.append(dataset['img_url'][i])
            tweets.append(dataset['tweets'][i][j])
            retweet_c.append(dataset['retweet_counts'][i][j])
            fav_c.append(dataset['fav_count'][i][j])
            created_time.append(dataset['created_time'][i][j])
            
            
    df_data = pd.DataFrame(columns=['name', 'screen_name', 'img_url', 'tweets', 'retweet_counts', 'fav_count', 'created_time'])
    df_data['name'] = names
    df_data['screen_name'] = sc_names
    df_data['img_url'] = imgs
    df_data['tweets'] = tweets
    df_data['retweet_counts'] = retweet_c
    df_data['fav_count'] = fav_c
    df_data['created_time'] = created_time
    
    return df_data

# importing test model to predict the classes and get it back
    
import test_model
df = pd.DataFrame()
funny_tweets, others_tweets, politics_tweets, finance_tweets, medical_tweets, tech_tweets, religion_tweets, sports_tweets = [], [], [], [], [], [], [], []

# takes the predicted classes and check for each class and assign to it the indes of its tweets
def get_pred_tweets(data):
    pred_labels = test_model.get_data_index(data)

    global df
    df = get_df_data(data)

    global funny_tweets 
    funny_tweets = pred_labels[0]['ترفيه']
    global others_tweets 
    others_tweets = pred_labels[1]['اجتماعيه']
    global politics_tweets 
    politics_tweets = pred_labels[2]['سياسه']
    global finance_tweets 
    finance_tweets = pred_labels[3]['اقتصاد']
    global medical_tweets 
    medical_tweets = pred_labels[4]['صحه']
    global tech_tweets 
    tech_tweets = pred_labels[5]['تكنولوجيا']
    global religion_tweets 
    religion_tweets = pred_labels[6]['دين']
    global sports_tweets 
    sports_tweets = pred_labels[7]['رياضه']
    return pred_labels
    
# get the funny tweets by the indexs of it
def get_funny_tweets():
    
    f_data = []

    global funny_tweets
    
    global df
    df_data = df
    for i in range(len(funny_tweets)):
        
        if i in funny_tweets:
            f_dict = {}
            f_dict.update(name=df_data['name'][i], screen_name=df_data['screen_name'][i], img_url=df_data['img_url'][i], tweets=df_data['tweets'][i], retweet_counts=df_data['retweet_counts'][i], fav_count=df_data['fav_count'][i], created_time=df_data['created_time'][i])
            
            f_data.append(f_dict)
        
    return f_data

# get the others(اجتماعيه) tweets by the indexs of it
def get_others_tweets():
    global others_tweets
    
    
    o_data = []
      
    global df
    df_data = df
    
    for i in range(len(others_tweets)):
        
        if i in others_tweets:
            o_dict = {}
            o_dict.update(name=df_data['name'][i], screen_name=df_data['screen_name'][i], img_url=df_data['img_url'][i], tweets=df_data['tweets'][i], retweet_counts=df_data['retweet_counts'][i], fav_count=df_data['fav_count'][i], created_time=df_data['created_time'][i])
            
            o_data.append(o_dict)
        
    return o_data

# get the politics(سياسه) tweets by the indexs of it
def get_politics_tweets():
    global politics_tweets
    p_data = []
    

    global df
    df_data = df
    
    for i in range(len(politics_tweets)):
        
        if i in politics_tweets:
            p_dict = {}
            p_dict.update(name=df_data['name'][i], screen_name=df_data['screen_name'][i], img_url=df_data['img_url'][i], tweets=df_data['tweets'][i], retweet_counts=df_data['retweet_counts'][i], fav_count=df_data['fav_count'][i], created_time=df_data['created_time'][i])
            
            p_data.append(p_dict)
        
    return p_data

# get the finance(اقتصاد) tweets by the indexs of it
def get_finance_tweets():
    global finance_tweets
    e_data = []
       
    global df
    df_data = df
    
    for i in range(len(finance_tweets)):
        
        if i in finance_tweets:
            e_dict = {}
            e_dict.update(name=df_data['name'][i], screen_name=df_data['screen_name'][i], img_url=df_data['img_url'][i], tweets=df_data['tweets'][i], retweet_counts=df_data['retweet_counts'][i], fav_count=df_data['fav_count'][i], created_time=df_data['created_time'][i])
            
            e_data.append(e_dict)
        
    return e_data

# get the medical(صحه) tweets by the indexs of it
def get_medical_tweets():
    global medical_tweets
    m_data = []
    
    global df
    df_data = df
    
    for i in range(len(medical_tweets)):
        
        if i in medical_tweets:
            m_dict = {}
            m_dict.update(name=df_data['name'][i], screen_name=df_data['screen_name'][i], img_url=df_data['img_url'][i], tweets=df_data['tweets'][i], retweet_counts=df_data['retweet_counts'][i], fav_count=df_data['fav_count'][i], created_time=df_data['created_time'][i])
            
            m_data.append(m_dict)
        
    return m_data

# get the tech(تكنولوجيا) tweets by the indexs of it
def get_tech_tweets():
    global tech_tweets
    t_data = []
    
    global df
    df_data = df
    
    for i in range(len(tech_tweets)):
        
        if i in tech_tweets:
            t_dict = {}
            t_dict.update(name=df_data['name'][i], screen_name=df_data['screen_name'][i], img_url=df_data['img_url'][i], tweets=df_data['tweets'][i], retweet_counts=df_data['retweet_counts'][i], fav_count=df_data['fav_count'][i], created_time=df_data['created_time'][i])
            
            t_data.append(t_dict)
        
    return t_data

# get the religion(دين) tweets by the indexs of it
def get_religion_tweets():
    global religion_tweets
    r_data = []
        
    global df
    df_data = df
    
    for i in range(len(religion_tweets)):
        
        if i in religion_tweets:
            r_dict = {}
            r_dict.update(name=df_data['name'][i], screen_name=df_data['screen_name'][i], img_url=df_data['img_url'][i], tweets=df_data['tweets'][i], retweet_counts=df_data['retweet_counts'][i], fav_count=df_data['fav_count'][i], created_time=df_data['created_time'][i])
            
            r_data.append(r_dict)
        
    return r_data

# get the sport(رياضه) tweets by the indexs of it
def get_sports_tweets():
    global sports_tweets
    s_data = []
    
    
    global df
    df_data = df
    
    for i in range(len(sports_tweets)):
        
        if i in sports_tweets:
            s_dict = {}
            s_dict.update(name=df_data['name'][i], screen_name=df_data['screen_name'][i], img_url=df_data['img_url'][i], tweets=df_data['tweets'][i], retweet_counts=df_data['retweet_counts'][i], fav_count=df_data['fav_count'][i], created_time=df_data['created_time'][i])
            
            s_data.append(s_dict)
        
    return s_data



