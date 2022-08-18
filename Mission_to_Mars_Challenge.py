#!/usr/bin/env python
# coding: utf-8

# In[1]:


#10.3.3 Import Splinter, BeautifulSoup, and Pandas
get_ipython().system('pip install selenium')
get_ipython().system('pip install webdriver_manager')

from splinter import Browser
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


#10.3.3 Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[3]:


#10.3.3 Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


#10.3.3 Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[5]:


#10.3.3  scrape the webpage to return the HTML containing the content title
slide_elem.find('div', class_='content_title')


# In[6]:


#10.3.3 Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


#10.3.3 Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[8]:


#10.3.4 Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


#10.3.4 Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


#10.3.3 Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[11]:


#10.3.3 find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


#10.3.3 Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[13]:


#10.3.5 Create a DataFrame from the HTML table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[14]:


#10.3.5 Add column names and set the index
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[15]:


#10.3.3 Convert the table back to HTML
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[16]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[18]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
images = browser.find_by_css('a.product-item img')

for image in range(len(images)):
    hemispheres = {}
    
    browser.find_by_css('a.product-item img')[image].click()
    
    # pulls full image link from page
    img_title_soup = soup(html, 'html.parser')
    img_elem = browser.links.find_by_text('Sample').first
    img_url = img_elem['href']
    hemispheres['img_url'] = img_url
    
    # pulls image title    
    html = browser.html
    title_soup = soup(html, 'html.parser')
    title = title_soup.find('h2', {'class':'title'}).get_text()
    hemispheres['title'] = title
    
    # add dictionary to list
    hemisphere_image_urls.append(hemispheres)
    
    # to back to home page
    browser.back()


# In[19]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[20]:


# 5. Quit the browser
browser.quit()


# In[ ]:




