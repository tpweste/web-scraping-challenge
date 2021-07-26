#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install splinter


# In[4]:


pip install webdriver_manager


# In[10]:


news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"

news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."


# In[11]:


from bs4 import BeautifulSoup as bs
import requests
from requests import get
import os
import pandas as pd
from splinter import Browser
import time
from webdriver_manager.chrome import ChromeDriverManager


# In[12]:


executable_path = {"executable_path": ChromeDriverManager().install()}
browser = Browser("chrome", **executable_path, headless=False)


# In[23]:


mars_data={}


# In[24]:


url = "https://redplanetscience.com/#"
browser.visit(url)

time.sleep(1)

html = browser.html
soup = bs(html, "html.parser")

title=soup.find_all("div", class_="content_title")


# In[25]:


title=title[0].text


# In[26]:


print(title)


# In[27]:


mars_data["title"]=title


# In[28]:


paragraph=soup.find('div', class_="article_teaser_body").get_text()


# In[29]:


print(paragraph)


# In[30]:


mars_data["paragraph"]=paragraph


# In[31]:


#getting images


# In[32]:


url = "https://spaceimages-mars.com/"
browser.visit(url)
full_image_button = browser.links.find_by_partial_text('FULL IMAGE')
full_image_button.click()
html = browser.html
soup = bs(html, "html.parser")
image=soup.find('img', class_='fancybox-image').get('src')
image_url=url + image
image_url


# In[33]:


mars_data["featured_image_url"]=image_url


# In[34]:


mars_earth_df = pd.read_html("https://galaxyfacts-mars.com/")[0]
mars_earth_df.reset_index(inplace=False)
mars_earth_df.columns=["Properties", "Mars", "Earth"]
mars_earth_df


# In[35]:


mars_earth_html = mars_earth_df.to_html(header=False, index=False)


# In[36]:


mars_data["facts"]=mars_earth_html


# In[38]:


url = "https://marshemispheres.com/"

response = requests.get(url)
soup_h = bs(response.text, 'html.parser')

results = soup_h.find_all("div",class_='item')

hemisphere_image_urls = []
for result in results:
    hemi_dict = {}
    titles = result.find('h3').text
    end_link = result.find("a")["href"]
    image_link = "https://marshemispheres.com/" + end_link
    response = requests.get(image_link)
    
    soup = bs(response.text, 'html.parser')
    downloads = soup.find("div", class_="downloads")
    image_url = "https://marshemispheres.com/" + downloads.find("a")["href"]
    hemi_dict['title']=titles
    hemi_dict['image_url']= image_url
    hemisphere_image_urls.append(hemi_dict)


# In[39]:


hemisphere_image_urls


# In[40]:


mars_data["hemisphere"] = hemisphere_image_urls


# In[ ]:




