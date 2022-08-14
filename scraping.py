
#10.3.3 Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

#10.5.3 create function to initalize the browser, create a data dictionary, and end the WebDriver and return the scraped data
def scrape_all():
    # initiatie headless driver for deployment
    #10.3.3 set the executable path and the URL
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "las_modified": dt.datetime.now()
    }

    # stop webdriver and return data
    #10.3.5 end the scraping session by stopping webdriver and return data
    browser.quit()
    return data


#10.5.2 create the function to pull the news title, mars_news()
def mars_news(browser):   
    #10.3.3 visit the Mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # add optional delay of one minute for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #10.3.3 convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
   
    #10.5.2 add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        #10.3.3 scrape the webpage to return the HTML containing the content title and anything else nested inside of that <div /> tag
        #10.3.3 use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()

        #10.3.3 use the parent element to find the summary paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None
    
    #10.5.2 return the news title and summary
    return news_title, news_p

# ### JPL Space Images Featured Images
# create the function to pull the featured image
def featured_image(browser):
    #10.3.4 visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #10.3.4 find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #10.3.3 parse the resulting HTML with BeautifulSoup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #10.5.2 add try/except for error handling
    try:
        #10.3.3 find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
            return None

    #10.3.3 add the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


#10.5.2 create the function to pull the HTML table
def mars_facts():  
    #10.5.2 add try/except for error handling
    try:
        #10.3.5 use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None  
    
    #10.3.5 assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    #10.3.5 convert the table back to HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # if running as script, print scraped data
    print(scrape_all())