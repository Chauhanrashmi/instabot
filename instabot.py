import requests                                                                             #import request library to accessed API through HTTP verbs
import urllib                                                                               #urllib helps us in fetching data across the web.
from textblob import TextBlob                                                               #for sentimental analysis we use textblob library
from textblob.sentiments import NaiveBayesAnalyzer

APP_ACCESS_TOKEN='5698775381.716a5b5.70b4ba745f0943689bcf14a0d1702434'                      #saving of App Access Token in global variables

BASE_URL = 'https://api.instagram.com/v1/'                                                  #saving of Base_URL in global variables



#Function declaration to get your own info starts
def own_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()                                             #JSON response is similar to a dictionary . hence we can read data from it in a similar way that we used for the dictionary.

    if user_info['meta']['code'] == 200:
    # To check if the user that we have searched for exists or not, we check the status code of response and fetch the user ID if response received is 200.
        if len(user_info['data']):                                                            # to get the username, number of follower, posts and people we follow from
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'
#Function declaration to get your own info ends


#Function declaration to get the ID of a user by username & returns users id in return starts
def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:                                                           #check for status code of the request
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()
#Function declaration to get the ID of a user by username ends


#Function declaration to get the info of a user by username starts
def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:                                                          #check for status code of the request
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'
#Function declaration to get the info of a user by username ends



#Function declaration to get your recent post starts and returns the image
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:                                                           #check for status code of the request
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)                                              #retreive the url of the image
            print 'Your image has been downloaded!'                                                #returns the image that we have recently posted on Instagram.
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'
#Function declaration to get your recent post ends


#Function declaration to get the recent post of a user by username and returns the id of the most recent image starts
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:                                                            #check for status code of the request
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']                #retreive the url of the image
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'
# Function declaration to get the recent post of a user by username ends



#function declaration to get a list of people who likes the recent post
def get_like_list(insta_username):
    media_id=get_post_id(insta_username)                                                        #use of function get_post_id to get madia_id
    request_url=(BASE_URL+"media/%s/likes?access_token=%s")%((media_id,APP_ACCESS_TOKEN))
    print"get request url:%s"%(request_url)
    get_list=requests.get(request_url).json()
    if get_list['meta']['code'] == 200:                                                          #check for status code of the request
        if (get_list['data']):
            for i in range(0,len(get_list['data'])):
               print "liked by %s"%(get_list['data'][i]['username'])
               print " Wow (^_^) ! username who liked post are fetched successfully."             #printing of message on getting all user that liked
        else:
            print "No like Yet"
    else:
        print" error!status code other then 200 received"


#Function declaration to get the ID of the recent post of a user by username starts
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)                                                     #get request
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:                                                            #check for status code of the request
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()
#Function declaration to get the ID of the recent post of a user by username ends


#Function declaration to like the recent post of a user starts
def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)                                                 #POST request which takes the request url and the data as input.

    post_a_like = requests.post(request_url, payload).json()                                      #data being send with the post request is called payload

    if post_a_like['meta']['code'] == 200:                                                        #check for status code of the request
        print 'Wow (^_^) Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'
# Function declaration to like the recent post of a user ends


#Function declaration to get the list of comments on a post .it accepts the user's username starts
def get_comment_list(insta_username):
    media_id=get_post_id(insta_username)                                                          #use of function get_post_id to get madia_id
    request_url=(BASE_URL+"media/%s/comments?access_token=%s")%(media_id,APP_ACCESS_TOKEN)
    print 'get request url:%s'%(request_url)
    get_list=requests.get(request_url).json()
    if get_list['meta']['code'] == 200:                                                           #check for status code of the request
        if (get_list['data']):
            for i in range(0,len(get_list['data'])):
                print "comment is %s" % (get_list['data'][i]['text'])
                print " Wow (^_^) !post comments are fetched successfully."                        #printing of message on getting all comments
        else:
            print "No comment Yet"
    else:
        print" error!status code other then 200 received"
# Function declaration to get the list of comments on a post it accepts the user's username ends



#Function declaration to make a comment on the recent post of the user starts
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)                                                          #to get id of a post
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:                                                         #check for status code of the request
        print "Wow (^_^) Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"
# Function declaration to make a comment on the recent post of the user ends


#function declaration to delete negative comments from a given user's post. It should accept the users' username as the input parameters starts.
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:                                                        #check for status code of the request
        if len(comment_info['data']):
                                                                                                   # code to delete a comment
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']

                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())                       #analyse the intent using the TextBlob library and look for comments with negative intent.
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                    media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)

                    delete_info = requests.delete(delete_url).json()                            #make a delete call to delete the comment with negative intent

                    if delete_info['meta']['code'] == 200:                                      #check for status code of the request
                        print 'Wow (^_^) Comment successfully deleted!\n'                       #printing of meaningfull msg on the successfull deletion of negative comment
                    else:
                        print 'Unable to delete comment!'                                       #error in deleting comment
                else:
                    print 'Positive comment : %s\n' % (comment_text)                            #printing of meaningfull msg or  positive comment
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'
# function declaration to delete negative comments from a given user's post. It should accept the users' username as the input parameters ends.



# function declaration to get the recent media liked  by the user starts
def recent_media_liked():
    request_url = (BASE_URL + "users/self/media/liked?access_token=%s") % (APP_ACCESS_TOKEN)
    print"get request url:%s" % (request_url)
    media_liked = requests.get(request_url).json()
    if media_liked['meta']['code'] == 200:                                                         #check for status code of the request
        if len(media_liked['data']):
            image_name = media_liked['data'][0]['id'] + '.jpeg'
            image_url = media_liked['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)                                              #image url is retrieved
            print 'Your image has been downloaded!'
            return media_liked['data'][0]['id']
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"
    return None
# function declaration to get the recent media liked  by the user ends


#function declaration to iterate through the negative comments on a post which gets users post starts.
def iterate_through_negative_comments(media_id):
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                #analyse the intent using the TextBlob library and look for comments with negative intent.
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment is : %s' % (comment_text)
# function declaration to iterate through the negative comments on a post which gets users post ends.


# function declaration to find minimum number of likes on a post starts
def min_likes_on_post(insta_username):
    user_id=get_user_id(insta_username)
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:                                                             # check for status code of the request
        if len(user_media['data']):
            like=[]
            i=0
            while(i<len(user_media['data'])):
                likes_on_post=user_media['data'][i]['likes']['count']
                like.append(likes_on_post)
                i=i+1
            min_like=min(like)
            j=0
            while(j<len(like)):
               if(like[j]==min_like):
                    image_name = user_media['data'][j]['id'] + '.jpeg'
                    image_url = user_media['data'][j]['images']['standard_resolution']['url']
                    urllib.urlretrieve(image_url, image_name)                                               # image url is retrieved
                    print image_url
                    print 'Your image has been downloaded! By clicking above link you can view you the image with minimum number of likes'
               j=j+1
        else:
            print 'This account has zero post'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

# function declaration to find minimum number of likes on a post ends

#def start_bot() function starts
def start_bot():
    while True:
        print '\n'
        print 'Hey! Welcome to instaBot! (^_^)\n Using this bot you can get the information of users, liking their posts, deleting and making comments and much more \n'
        print '(*_*) What you want to do \n'
        request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
        user_info = requests.get(request_url).json()
        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                # The bot should ask the username for whom you want to perform any of the action.
                print "%s Are you want to perform action for yourself or another user?\n" % (user_info['data']['username'])
                print"Please enter your choice from the options below:"
                print"a.For yourself"
                print"b.For another user \n"
                choose = raw_input("choose from a or b:\n")
                if (choose == 'a'):
                    insta_username=user_info['data']['username']
                    print "Menu to choose which task is to be performed:\n"
                    print "1.Get your own details"
                    print "2.Get your own recent post"
                    print "3.To get the recent media liked by the user(astha_rc_)."
                    print "6.Get a list of people who have liked the recent post of a user"
                    print "7.Like the recent post of a user"
                    print "8.Get a list of comments on the recent post of a user"
                    print "9.Make a comment on the recent post of a user"
                    print "10.Delete negative comments from the recent post of a user"
                    print "11.To iterate through the negative comments on a post"
                    print "12.Post having minimum number of likes"
                    print "13.exit\n"
                elif (choose == 'b'):
                    print "Choose for which user task to be performed:\n"
                    print("My sandbox users are:")
                    print("itzz_mehakk")
                    print("ruchikagarg764""\n")
                    insta_username = raw_input("Enter the username of the user:")                  # The bot should ask the user of what they want to do for the username already provided.
                    print "Menu to choose which task is to be performed:\n"
                    print "3.To get the recent media liked by the user."
                    print "4.Get details of a user by username"
                    print "5.Get the recent post of a user by username"
                    print "6.Get a list of people who have liked the recent post of a user"
                    print "7.Like the recent post of a user"
                    print "8.Get a list of comments on the recent post of a user"
                    print "9.Make a comment on the recent post of a user"
                    print "10.Delete negative comments from the recent post of a user"
                    print "11.To iterate through the negative comments on a post"
                    print "12.Post having minimum number of likes"
                    print "13.Exit"
                else:
                    print("Oops! You entered a wrong choice")
                    exit()


        choice=raw_input("Enter you choice: ")
        if choice=="1":
            own_info()
        elif choice=="2":
            get_own_post()
        elif choice=="3":
            recent_media_liked()
        elif choice== "4":
            get_user_info(insta_username)
        elif choice== "5":
            get_user_post(insta_username)
        elif choice=="6":
            get_like_list(insta_username)
        elif choice=="7":
            like_a_post(insta_username)
        elif choice=="8":
            get_comment_list(insta_username)
        elif choice=="9":
            post_a_comment(insta_username)
        elif choice == "10":
            delete_negative_comment(insta_username)
        elif choice == "11":
            media_id = get_post_id(insta_username)
            iterate_through_negative_comments(media_id)
        elif choice == "12":
            min_likes_on_post(insta_username)
        elif choice=="13":
            exit()
        else:
            print "wrong choice"
#def start_bot() function ends


start_bot()    #start_bot() function called