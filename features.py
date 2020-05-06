import os
import re
import random
import webbrowser as wb
import wikipedia as wk

from nltk.tokenize import word_tokenize as wtk
from nltk.tokenize import sent_tokenize as stk

youtube_url = 'https://www.youtube.com/results?search_query='
google_url = 'https://www.google.co.in/search?q='

#youtube search
def get_youtube_topic(query_name):
    for_check = False
    topic_search = ''
    query_name = query_name.lower()
    query_name = query_name.strip(' ')
    query_list = wtk(query_name)
    
    for i in range(0,len(query_list),1):
        if query_list[i] == 'for':
            for_check = True
            continue
        if for_check == True:
            topic_search = topic_search + query_list[i]+' '
    return topic_search

def open(query):
    topic_to_search = query #get_youtube_topic(query)
    final_url = youtube_url+topic_to_search
    wb.open(final_url)
    return


#google search
def browser_search(query):
    search_topic = ''
    for_check = False
    query = query.lower()
    query = query.strip(' ')
    query_list = wtk(query)
    if ('for' in query_list) or ('about' in query_list):
        for i in range(0,len(query_list),1):
            if (query_list[i] == 'for') or (query_list[i] == 'about'):
                for_check = True
                continue
            if for_check == True:
                search_topic = search_topic+query_list[i]+' '
    else:
        search_topic = query.replace('search','')
    search_topic = search_topic.strip(' ')
    search_topic.replace(' ','%20')
    final_url = google_url+search_topic
    wb.open(final_url)
    return

            
#wikipedia search            
def short(user_ask):
    #get data
    topic = ' '
    user_ask = user_ask.lower()
    user_list = wtk(user_ask)
    user_ask_len = len(user_list)
    i,j = 0,(user_ask_len-1)
    for k in range(0,user_ask_len,1):
        if user_list[k] == 'for':
            i = k+1
        if user_list[k] == 'on' or user_list[k] == 'in':
            j = k-1
    for t in range(i,j+1,1):
        topic = topic+user_list[t]+' '
    topic = topic.strip(' ')
    #send data
    summary = ''
    try:
        wiki_list = stk(wk.summary(topic))
        for i in range(0,5,1):
            summary = summary + wiki_list[i]    
    except wk.exceptions.DisambiguationError:
        summary = 'Sorry Can\'t retrieve data from internet.'
    return summary

#function to give complete wiki site
def long(wiki):
    out = wikipedia.page(wiki)
    return out.html

