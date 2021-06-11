# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import requests
import pymongo
import pandas as pd


def scrape_info():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    ################################ NASA MARS NEWS #####################################################
    # URL of page to be scraped
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Retrieve page with the requests module
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    
    #results = soup.find_all('section', class_='image_and_description_container')

    results = soup.find_all('div', class_='list_text')    

    for result in results:
        news_title = result.find('div', class_='content_title').text
        news_p = result.find('div', class_='article_teaser_body').text
        
        print("--------------------")
        print(f'Title: {news_title}')
        print(f'News: {news_p}')    

    ############################### JPL Mars Space Images - Featured Image ################################    
    # URL of page to be scraped
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Retrieve page with the requests module
    html = browser.html
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = urljoin(url, results)

    ########################################## Mars Facts #################################################
    # URL of page to be scraped
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)

    df = tables[0]
    df.columns=['Mars-Earth Comparison', 'Mars', 'Earth']
    df.drop(0, inplace=True)
    html_content = df.to_html()

    ##################################### Mars Hemispheres ###################################################
    # URL of page to be scraped
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for item in items:
        element = {}
        link = item.find('a', class_='itemLink')['href']
        title = item.find('h3').text
        print('-------------------------')
        print(link)
        print(title)

        browser.visit(url+link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        downloads = soup.find('div', class_='downloads')
        img = downloads.find('img', class_='thumb')['src']
        print(img)

        element["title"] = title
        element["img_url"] = urljoin(url,img)
        
        hemisphere_image_urls.append(element)

    mars_data = {}
    mars_data['title'] = news_title
    mars_data['news']  = news_p
    mars_data['featured_image_url'] = featured_image_url
    mars_data["mars_facts"] = html_content
    mars_data["hemisphere_images_urls"] = hemisphere_image_urls

    # Quit the browser after scraping
    browser.quit()

    # Return results
    return mars_data
