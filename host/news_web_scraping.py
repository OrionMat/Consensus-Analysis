# NEWS WEB SCRAPING
import sys
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re 
import data_saving as save_to_CSV





#query = "Can Trump declare a national emergency to build a wall?"
# Shares in Boeing fell by 12.9% on Monday in the wake of the crash
# Can Trump declare a national emergency to build a wall?
# New Zealand mosque shootings





#%% New York Times: 

# gets NYT links from google with article dates
def google_NYT_links(query):
    NYT_query = "new york times + " + query
    article_links = search(NYT_query, tld="com", num=15, stop=10, pause=2)    # gets 15 top links from google
    url_list = []
    date_list = []
    for link in article_links:
        if re.search(r"www.nytimes.com/\d{4}/\d{2}/\d{2}", link) != None:
            date = re.search(r"\d{4}/\d{2}/\d{2}", link)
            url_list = url_list + [link]
            date_list = date_list + [date.group()]
    return url_list, date_list

# gets a list of NYT articles and their corresponing headlines from a list of links
def NYT_links_scrape(link_list):
    title_list = []
    article_list = []
    for link in link_list:
        title, article = NYT_article_scrape(link)
        if title and article:
            title_list = title_list + [title]
            article_list = article_list + [article]
    return title_list, article_list

# scrapes a NYT article and its headline
def NYT_article_scrape(url):
    try:
        # gets a webpage
        response = requests.get(url)
    except:
        print("no response from webpage. Error: ", sys.exc_info()[0])
        raise
    soup = BeautifulSoup(response.text, 'html.parser')
    # get article title
    title = soup.find('h1')
    if title == None:
        print("NYT article title not found")
        return "", ""
    headline = title.get_text() 
    # get all paragraphs in the article body
    articlebody = soup.find(attrs={"name": "articleBody"})
    if articlebody == None: # catches videos
        return "",""
    all_paragraphs = articlebody.find_all('p')
    # get the text of all paragraphs and flatten them into an article
    article = ''
    for paragraph in all_paragraphs:
        text = paragraph.get_text()
        article = article + text
    return headline, article

# scrapes all article links on a NYT page
def NYT_link_scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    article_links = soup.find_all('article') 
    hyp_link_list = []
    for link in article_links:
        url = link.find('a')
        hyperlink = url.get('href')
        hyp_link_list = hyp_link_list + [hyperlink]
    return hyp_link_list

# gets a list of NYT articles and their corresponing headlines from a page url
def NYT_page_scrape(url):
    hyp_link_list = NYT_link_scrape(url)
    title_list = []
    article_list = []
    for hyp_link in hyp_link_list:
        url = 'https://www.nytimes.com'+ hyp_link
        title, article = NYT_article_scrape(url)
        if title and article:
            title_list = title_list + [title]
            article_list = article_list + [article]
    return title_list, article_list

#%% BBC:

# gets BBC links from google
def google_BBC_links(query):
    BBC_query = "BBC news + " + query
    article_links = search(BBC_query, tld="co.uk", num=15, stop=10, pause=2)    # gets 15 top links from google
    url_list = []
    for link in article_links:
        if re.search(r"www.bbc.co.uk/news/[^ av]", link) != None:
            url_list = url_list + [link]
    return url_list

# gets a list of BBC articles and their corresponing headlines and dates from a list of links
def BBC_links_scrape(link_list):
    title_list = []
    article_list = []
    date_list = []
    for link in link_list:
        title, article, date = BBC_article_scrape(link)
        if title and article and date:
            title_list = title_list + [title]
            article_list = article_list + [article]
            date_list = date_list + [date]
    return title_list, article_list, date_list

# scrapes a BBC article, its headline and its date
def BBC_article_scrape(url):
    # get webpage
    try:
        response = requests.get(url)
    except:
        print("no response from webpage. Error: ", sys.exc_info()[0])
        raise
    soup = BeautifulSoup(response.text, 'html.parser')
    # get article title
    title = soup.find('h1')
    if title == None:
        print("BBC article title not found")
        return "", "", ""
    headline = title.get_text() 
    # get all paragraphs in the article body
    articlebody = soup.find(attrs={"property": "articleBody"})
    if articlebody == None: # catches videos
        return "","", ""
    all_paragraphs = articlebody.find_all('p')
    # get the text of all paragraphs and flatten them into an article
    article = ''
    for paragraph in all_paragraphs:
        text = paragraph.get_text()
        article = article + text
    # get article date
    date_section = soup.find(attrs={"class": "mini-info-list__item"})
    date_location = date_section.find('div')
    date = date_location.get_text()
    return headline, article, date

#%% AP

# gets AP links from google
def google_AP_links(query):
    AP_query = "AP news + " + query
    article_links = search(AP_query, tld="co.uk", num=15, stop=10, pause=2)    # gets 15 top links from google
    url_list = []
    for link in article_links:
        if (re.search(r"www.apnews.com", link) != None) and  (re.search(r"gallery", link) == None) :
            url_list = url_list + [link]
    return url_list

# gets a list of AP articles and their corresponing headlines and dates from a list of links
def AP_links_scrape(link_list):
    title_list = []
    article_list = []
    date_list = []
    for link in link_list:
        title, article, date = AP_article_scrape(link)
        if title and article and date:
            title_list = title_list + [title]
            article_list = article_list + [article]
            date_list = date_list + [date]
    return title_list, article_list, date_list

# scrapes a AP article, its headline and its date
def AP_article_scrape(url):
    # get webpage
    try:
        response = requests.get(url)
    except:
        print("no response from webpage. Error: ", sys.exc_info()[0])
        raise
    soup = BeautifulSoup(response.text, 'html.parser')
    # get article title
    title = soup.find('h1')
    if title == None:
        print("AP article title not found")
        return "", "", ""
    headline = title.get_text() 
    # get all paragraphs in the article body
    articlebody = soup.find(attrs={"data-key": "article"})
    if articlebody == None: # catches videos
        return "","", ""
    all_paragraphs = articlebody.find_all('p')
    # get the text of all paragraphs and flatten them into an article
    article = ''
    for paragraph in all_paragraphs:
        text = paragraph.get_text()
        article = article + text
    # get article date
    date_location = soup.find(attrs={"data-key": "timestamp"})
    date = date_location.get_text()
    return headline, article, date

#%% reuters

# gets reuters links from google
def google_reuters_links(query):
    reuters_query = "reuters + " + query
    article_links = search(reuters_query, tld="com", num=15, stop=10, pause=2)    # gets 15 top links from google
    url_list = []
    for link in article_links:
        if (re.search(r"reuters.com/article", link) != None):
            url_list = url_list + [link]
    return url_list

# gets a list of reuters articles and their corresponing headlines and dates from a list of links
def reuters_links_scrape(link_list):
    title_list = []
    article_list = []
    date_list = []
    for link in link_list:
        title, article, date = reuters_article_scrape(link)
        if title and article and date:
            title_list = title_list + [title]
            article_list = article_list + [article]
            date_list = date_list + [date]
    return title_list, article_list, date_list

# scrapes a reuters article, its headline and its date
def reuters_article_scrape(url):
    # get webpage
    try:
        response = requests.get(url)
    except:
        print("no response from webpage. Error: ", sys.exc_info()[0])
        raise
    soup = BeautifulSoup(response.text, 'html.parser')
    # get article title
    title = soup.find('h1')
    if title == None:
        print("reuters article title not found")
        return "", "", ""
    headline = title.get_text() 
    # get all paragraphs in the article body
    articlebody = soup.find(attrs={"class": "StandardArticleBody_body"}) 
    if articlebody == None: # catches videos
        return "","", ""
    all_paragraphs = articlebody.find_all('p')
    # get the text of all paragraphs and flatten them into an article
    article = ''
    for paragraph in all_paragraphs:
        text = paragraph.get_text()
        article = article + text
    # get article date
    date_location = soup.find(attrs={"class": "ArticleHeader_date"})
    date = date_location.get_text()
    return headline, article, date