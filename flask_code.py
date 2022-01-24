

import flask
import get_user_data_for_flask
import time

# global username
NAME = None

app = flask.Flask(__name__)
@app.route('/')
# to open the login page
def login():
    return flask.render_template('login.html')

# set into the global NAME the username taked fromthe form
def getName():
    global NAME
    if NAME == None:
        NAME = flask.request.form['username']
        return NAME
    else:
        return NAME

# get the user profile data using username and reurn (name, img, username)    
def getProfileData():

    name = getName()
    
    if(get_user_data_for_flask.validUser(name)):
        profile_name, profile_img, sc_name = get_user_data_for_flask.get_profile_name_and_img(name)
        
        
        return name, profile_name, profile_img, sc_name
    else:
        print('error')

# get the user timeline
def getTimelineData():
    name = getName()
    if(get_user_data_for_flask.validUser(name)):
        data = get_user_data_for_flask.get_tweets_timeline(name)
        return data
    else:
        print('error')
  
# this function will call after loggined to get home page and the user timeline
@app.route('/', methods=['POST'])
def getHome():
    name, profile_name, profile_img, sc_name = getProfileData()
    data = getTimelineData()
    return flask.render_template('home.html', prof_name = profile_name, prof_img = profile_img,prof_screen_name = sc_name, data = data)
    
    get_updated_tweets(name, profile_name, profile_img, sc_name)

#global mode to turn off the updated for the user home page
MODE = True

# every 15 minutes it make update for the user home page
def get_updated_tweets(name, profile_name, profile_img, sc_name):
    global MODE
    while(MODE):
        time.sleep(300)
        data = get_user_data_for_flask.get_tweets_timeline(name)
        return flask.render_template('home.html', prof_name = profile_name, prof_img = profile_img, prof_screen_name = sc_name, data = data)
       

# to log out
@app.route('/redirected_form')  
def redirected_form():
    global MODE
    MODE = False
    return flask.render_template('login.html')

# when press ترفيه button it get the funny tweets back to the funny page
@app.route('/funny_page')
def funny_page():

    data = getTimelineData()
    get_user_data_for_flask.get_pred_tweets(data)
    f_data = get_user_data_for_flask.get_funny_tweets()
    return flask.render_template('funny.html', data = f_data)

# when press اجتماعيه button it get the others tweets back to the others page
@app.route('/others_page')
def others_page():
    data = getTimelineData()
    get_user_data_for_flask.get_pred_tweets(data)
    others = get_user_data_for_flask.get_others_tweets()
    return flask.render_template('others.html', data = others)

# when press سياسه button it get the politices tweets back to the politices page
@app.route('/politics_page')
def politics_page():
    data = getTimelineData()
    get_user_data_for_flask.get_pred_tweets(data)
    politics = get_user_data_for_flask.get_politics_tweets()
    return flask.render_template('politics.html', data = politics)

# when press اقتصاد button it get the finance tweets back to the finance page
@app.route('/finance_page')
def finance_page():
    data = getTimelineData()
    get_user_data_for_flask.get_pred_tweets(data)
    finance = get_user_data_for_flask.get_finance_tweets()
    return flask.render_template('finance.html', data = finance)

# when press صحه button it get the medical tweets back to the medical page

@app.route('/medical_page')
def medical_page():
    data = getTimelineData()
    get_user_data_for_flask.get_pred_tweets(data)
    medical = get_user_data_for_flask.get_medical_tweets()
    return flask.render_template('medical.html', data = medical)

# when press تكنولوجيا button it get the tech tweets back to the tech page
@app.route('/tech_page')
def tech_page():
    data = getTimelineData()
    get_user_data_for_flask.get_pred_tweets(data)
    tech = get_user_data_for_flask.get_tech_tweets()
    return flask.render_template('tech.html', data = tech)

# when press دين button it get the religion tweets back to the religion page
@app.route('/religion_page')
def religion_page():
    data = getTimelineData()
    get_user_data_for_flask.get_pred_tweets(data)
    religion = get_user_data_for_flask.get_religion_tweets()
    return flask.render_template('religion.html', data = religion)

# when press رياضه button it get the sports tweets back to the sports page
@app.route('/sports_page')
def sports_page():
    data = getTimelineData()
    get_user_data_for_flask.get_pred_tweets(data)
    sports = get_user_data_for_flask.get_sports_tweets()
    return flask.render_template('sports.html', data = sports)

# to run flask app
if __name__ == '__main__':
    
    app.debug = True
    app.run()
    

