#!/usr/bin/env python
# coding: utf-8

# Import dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import pandas as pd
import time

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {} 

    
    # NASA Mars News

    '''Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    Assign the text to variables that you can reference later.'''

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at \
        +desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    # Retrieve page & parse with BeautifulSoup
    
    try:
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Give the page time to load, otherwise it will throw an error
        time.sleep(1)
        mars_data['news_title'] = soup.find_all('div', class_='content_title')[1].text
        mars_data['news_para'] = soup.find_all('div', class_='article_teaser_body')[0].text
    except:
        mars_data['news_title'] = "No news found"
        mars_data['news_para'] = "Hopefully, no news is good news!"

    # ## JPL Mars Space Images - Featured Image
    
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and 
    # assign the url string to a variable called featured_image_url.
    
    try:
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        s = soup.find('article', class_='carousel_item')['style']
        url = s.split("'")[1]
        mars_data['featured_image_url'] = 'https://www.jpl.nasa.gov' + url
    except:
        pass
    
    
    # ## Mars Weather (Twitter)

    '''
    Visit the Mars Weather twitter account and scrape the latest Mars weather tweet from the page. 
    Save the tweet text for the weather report as a variable called mars_weather.
    '''

    url = 'https://twitter.com/marswxreport?lang=en'

    try:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        mars_weather = soup.find_all('p', class_='tweet-text')[0].text
        mars_weather = mars_weather.split('pic.twitter.com')
        mars_data['mars_weather'] = mars_weather[0]
    except:
        mars_data['mars_weather'] = f"Weather data not found. Try visiting {url} for more information."
    
    
    # ## Mars Facts

    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet 
    
    try:
        r = requests.get("https://space-facts.com/mars/")
        soup = BeautifulSoup(r.content,'lxml')
        table = soup.find('table', id='tablepress-p-mars-no-2')
        df = pd.read_html(str(table))
        df = df[0]

        df.columns = ['description', 'value']
        df.set_index(keys=['description'], inplace=True)

        # Use Pandas to convert the data to a HTML table string.
        html = df.to_html()
        mars_data['html_table'] = html.replace('\n', '')
    except:
        pass
    
    # ## Mars Hemispheres

    try:
        r = requests.get("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
        soup = BeautifulSoup(r.content,'lxml')

        links = soup.find_all('a', class_='itemLink')

        hemisphere_image_urls = []

        for link in links:
            hemisphere = {}
            r = requests.get("https://astrogeology.usgs.gov/" + link['href'])
            soup = BeautifulSoup(r.content,'lxml')
            l = soup.find('li')
            link = l.contents[0]
            img_url = link['href']
            title = soup.title.text
            title = title.split("|")[0]
            hemisphere["title"] = title
            hemisphere["img_url"] = img_url
            hemisphere_image_urls.append(hemisphere)
            time.sleep(1)

        mars_data['hemisphere_urls'] = hemisphere_image_urls
    except:
        pass

    return mars_data           
