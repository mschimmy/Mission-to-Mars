
#10.3.3 Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#10.3.3 set the executable path and the URL
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#10.3.3 visit the Mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# add optional delay of one minute for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


#10.3.3 set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

#10.3.3 scrape the webpage to return the HTML containing the content title and anything else nested inside of that <div /> tag
slide_elem.find('div', class_='content_title')

#10.3.3 use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

#10.3.3 use the parent element to find the summary paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Images

#10.3.4 visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

#10.3.4 find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


#10.3.3 parse the resulting HTML with BeautifulSoup
html = browser.html
img_soup = soup(html, 'html.parser')


#10.3.3 find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

#10.3.3 add the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Data

#10.3.5 create a DataFrame from the HTML table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

#10.3.5 convert the table back to HTML
df.to_html()

#10.3.5 end the scraping session
browser.quit()



