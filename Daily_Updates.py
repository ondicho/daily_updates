#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import numpy as np
import pandas as pd
from pretty_html_table import build_table


# In[2]:


from bs4 import BeautifulSoup


# In[3]:


from htmldate import find_date
from datetime import datetime, timedelta


# In[4]:


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


# In[5]:


import html
import base64


# In[6]:


#############   TABLE STYLES ####################################################################################
def make_clickable(val):
    return '<a target="_blank" href="{}">{}</a>'.format(val,val)
# define dataframe styles
th_props = [
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', '#6d6d6d'),
  ('background-color', '#f7f7f9'),
    ('font-family','Montserrat')
  ]

# Set CSS properties for td elements in dataframe
td_props = [
    ('font-family','Montserrat')
  ]

# Set table styles
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]   


# In[7]:


#################################### BUSINESS DAILY #############################################################


# In[8]:


base_url="https://www.businessdailyafrica.com"


# In[9]:


keywords = ["Capital Markets","Business"]


# In[10]:


daily_briefs=requests.get(base_url)


# In[11]:


soup=BeautifulSoup(daily_briefs.content,'html.parser')


# In[12]:


business_daily=soup.find(class_="article article-list-featured")


# In[13]:


headline=business_daily.find("header")
headline_title=headline.select('h2')[0].text
headline_oneLiner=headline.select('p')[0].text
headline_links=headline.select('a')
links=[]
bd_articles=[]


# In[14]:


for href in headline_links:
     links.append(base_url + (href['href']))


# In[15]:


business_daily_others=soup.find(class_="content-one-quarter small-list")
business_daily_other_articles=business_daily_others.find_all(class_="article article-list-small")


# In[16]:


# find span(categories) from page structure
for business_daily_other_article in business_daily_other_articles:
    spans=business_daily_other_article.find("span")
    for span in spans:
#         check if the categories match keywords array
        if span in keywords:
            #         find DOM parent of the matched spans/categories
            key_article=span.find_parent("article")
            key_article_link=key_article.select('a')
            #     pick publication link
            for href in key_article_link:
                key_article_url= (base_url + (href['href']))
#                  push article title and link to array to be printed later
                bd_articles.append([(key_article.select('h3')[0].text.strip().replace("\n","")),(key_article_url)]) 


# In[18]:


# convert bd_articles array to dataframe
business_daily=pd.DataFrame(bd_articles, columns=['title','link'])  
# apply styles
business_daily=business_daily.style.format({'link': make_clickable}).set_table_styles(styles,[{'selector': '.row_heading',
          'props': [('display', 'none')]},
         {'selector': '.blank.level0',
          'props': [('display', 'none')]}]).hide_index()


# In[19]:


############################ DAILY NATION BUSINESS ############################################################


# In[20]:


# scrape Daily Nation
nation_business_url="https://nation.africa"
nation_url="https://nation.africa/kenya/business/finance-and-markets"
nation_briefs=requests.get(nation_url)
soup=BeautifulSoup(nation_briefs.content,'html.parser')


# In[21]:


nation_business=soup.find(class_="teaser-image-large")


# In[22]:


nation_top=nation_business.select('h3')[0].text


# In[23]:


nation_top_links=nation_business.select('a')


# In[24]:


nation_top_summary=nation_business.select('p')[0].text


# In[25]:


nation_links=[]
nation_other_articles=[]


# In[26]:


# extract headline link form html
headline_link=soup.find(class_="col-1-1 large-col-1-3").select('a')


# In[27]:


for href in headline_link:
     nation_links.append(nation_business_url + (href['href']))


# In[28]:


# extract related publications
other_publications=soup.find(class_="article-collection")


# In[29]:


articles=other_publications.find_all('li')


# In[30]:


# find span(categories) from page structure
for article in articles:
    spans=article.find(class_='article-topic article-metadata_topic')
    for span in spans:
#         check if the categories match keywords array
        if span in keywords:
#         find DOM parent of the matched spans/categories
            nation_key_article=span.find_parent("li")
#     pick publication link
        nation_key_article_links=nation_key_article.select('a')
        for href in nation_key_article_links:
            article_url= (nation_business_url + (href['href']))
#             push article title and link to array to be printed later
            nation_other_articles.append([(nation_key_article.select('h3')[0].text.strip().replace("\n", "").replace("PRIME", "")),(article_url)])


# In[31]:


# style the dataframe make the links column clickable
nation = pd.DataFrame(nation_other_articles, columns=['title','link'])  
# apply styles to dataframe
nation=nation.style.format({'link': make_clickable}).set_table_styles(styles,[{'selector': '.row_heading',
          'props': [('display', 'none')]},
         {'selector': '.blank.level0',
          'props': [('display', 'none')]}]).hide_index()


# In[32]:


############################################THE STAR#############################################################
# scrap publications from the star
star_business_url="https://www.the-star.co.ke/business/"
star_briefs=requests.get(star_business_url)
soup=BeautifulSoup(star_briefs.content,'html.parser')
star_base_url="https://www.the-star.co.ke"
star_articles=[]
# headline
star_headline=soup.find(class_="featured-article")
headline_body=star_headline.find(class_="article-body")
star_top_story=headline_body.select('h3')[0].text.strip().replace("\n","")
headline_link=headline_body.findChildren("a", recursive=False)
for href in headline_link:
    star_headline_url= (star_base_url + (href['href']))
# featured stories
article_load=soup.find(class_='article-load')
article_section=article_load.find_all(class_='article-section')
for article_section in article_section:
    span=article_section.text.strip()
    if span in keywords:
        article_content=article_section.find_parent(class_="section-article section-article-has-comments")
        article_body=article_content.find(class_='article-body')
        article_link=article_body.findChildren("a", recursive=False)
        for href in article_link:
            star_key_article_url= (star_base_url + (href['href']))
            star_articles.append([(article_body.select('h3')[0].text.strip().replace("\n","")),(star_key_article_url)])
            


# In[33]:


star_top_story


# In[34]:


# convert featured story to dataframe 
star = pd.DataFrame(star_articles, columns=['title','link'])  
# apply styles to dataframe
star=star.style.format({'link': make_clickable}).set_table_styles(styles,[{'selector': '.row_heading',
          'props': [('display', 'none')]},
         {'selector': '.blank.level0',
          'props': [('display', 'none')]}]).hide_index()


# In[35]:


# import the necessary components first

port = 2525
smtp_server = "smtp.mailtrap.io"
login = "a19147812d7061"
# paste your login generated by Mailtrap
password = "4adf5d41f5d206" # paste your password generated by Mailtrap
sender_email = "mailtrap@example.com"
receiver_email = "new@example.com"
message = MIMEMultipart("alternative")
message["Subject"] = "Daily Updates"
message["From"] = sender_email
message["To"] = receiver_email


# write the HTML part
html = """<html>
  <head>
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
     <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400&display=swap" rel="stylesheet">
  </head>
  <body style="font-family: 'Montserrat', sans-serif;background-color:#F6F6F6;">
  <br>
    <img src="cid:logo">
    <h3 style="color: #006DB7;text-align: center;">Daily Updates</h3>
    <p>Good morning,<br>
       Here's a peak into the latest business news:
    </p>
    <h4 style="color:#F8A142;font-weight:bold;">Business Daily Top Story:</h4><p><a href={}>{}</a></p>
    <h4 style="color:#F8A142;font-weight:bold;">Business Daily Featured Publications:</h4>{}
    <h4 style="color:#F8A142;font-weight:bold;">The Star Business Top Story:</h4><a href={}>{}</a>
    <h4 style="color:#F8A142;font-weight:bold;">The Star Featured Publications:</h4><p>{}</p>
    <h4 style="color:#F8A142;font-weight:bold;">Nation Business Top Story:</h4><p><a href={}>{}</a></p><br>
    <h4 style="color:#F8A142;font-weight:bold;">Nation Featured Publications:</h4><p>{}</p><br>
    <p style="color:#F8A142;font-weight:bold;"> Do not reply to this email as it is auto-generated</p><br>
    <p style="color:#006DB7;;font-weight:bold;">Regards,<br>
     Strategy and Innovation Team</p>
  </body>
</html>
""".format(links[1],headline_title,business_daily.to_html(),headline_link,star_top_story,star.to_html(),nation_links[0],nation_top,nation.to_html())
# convert both parts to MIMEText objects and add them to the MIMEMultipart message
part1 = MIMEText(html, "html")
message.attach(part1)

# read image
fp=open('logo.png', 'rb')
image = MIMEImage(fp.read())
fp.close()

# Specify the  ID according to the img src in the HTML part
image.add_header('Content-ID', '<logo>')
message.attach(image)

# send your email
with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
    server.login(login, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
print('Sent') 


# In[36]:


###############deletes the arrays storing links so as to start afresh on a new iteration###############
# business daily
del bd_articles
del links
# nation
del nation_other_articles
del nation_links
del nation
#THE STAR
del star_articles


# In[ ]:




