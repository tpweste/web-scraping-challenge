from bs4 import BeautifulSoup as bs
import requests
from requests import get
import os
import pandas as pd
from splinter import Browser
import time
from webdriver_manager.chrome import ChromeDriverManager
import pymongo

mars_data = {}

def scrape():
    
        executable_path = {"executable_path": ChromeDriverManager().install()}
        browser = Browser("chrome", **executable_path, headless=False)
        
        url = "https://redplanetscience.com/#"
        browser.visit(url)

        time.sleep(1)

        html = browser.html
        soup = bs(html, "html.parser")

        title = soup.find_all("div", class_="content_title")
        title=title[0].text
        mars_data["title"]=title
        
        #Find Paragraphs
        paragraph=soup.find('div', class_="article_teaser_body").get_text()
        mars_data["paragraph"] = paragraph
        
        #Get Images
        
        url = "https://spaceimages-mars.com/"
        browser.visit(url)
        full_image_button = browser.links.find_by_partial_text('FULL IMAGE')
        full_image_button.click()
        html = browser.html
        soup = bs(html, "html.parser")
        image=soup.find('img', class_='fancybox-image').get('src')
        image_url=url + image
        image_url
        
        mars_data["featured_image_url"]=image_url
        
        #Scraping the facts
        
        mars_earth_df = pd.read_html("https://galaxyfacts-mars.com/")[0]
        mars_earth_df.reset_index(inplace=False)
        mars_earth_df.columns=["Properties", "Mars", "Earth"]
        mars_earth_df
        mars_earth_html = mars_earth_df.to_html(header=False, index=False)
        mars_data["facts"]=mars_earth_html
        
        
        #Get Hemisphere Image
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
        
        
    mars_data["hemisphere"] = hemisphere_image_urls
    
Browser.quit()
    
return mars_data