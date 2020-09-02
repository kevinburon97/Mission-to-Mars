from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd


def start_browser():
    executable_path = {"executable_path" : r"C:\Users\Kevin\Desktop\Bootcamp work\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

def scrape():
    #Start Browser
    browser = start_browser()
    #visit site
    url = "https://mars.nasa.gov/news"
    browser.visit(url)
    time.sleep(1)
    #Scrape title
    html = browser.html
    soup = bs(html, "html.parser")
    #Find newest head title
    head_title = soup.find_all("div", class_ ="content_title")[1].text
   

    #Click on article
    browser.click_link_by_text(str(head_title))
    time.sleep(1)
    #Create new soup instance for the article
    html = browser.html
    soup = bs(html, "html.parser")
    #find paragraph 
    body_text = soup.find("div", class_="wysiwyg_content").find_all('p')[1].text
    
    
    #visit featured image website
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    #click on full image
    browser.click_link_by_id("full_image")
    time.sleep(1)
    #Create new soup instance for the image site
    html = browser.html
    soup = bs(html, "html.parser")
    feat_image = soup.find("img", class_="fancybox-image")['src']
    
    #Find data about mars and export it to an html 
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)
    mars_table =table[0]
    mars_table.columns = ["fact","Measurement"]
    mars_table.set_index("fact")
    mars_table_html =mars_table.to_html("MarsTable.html")
    
    
    #Scrape Mars hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(1)
    #Clicki"ng on the hemishpere did not work, so i will visit each side individually
    html = browser.html
    soup = bs(html, "html.parser")
    #Find all links to each hemishpere website
    Cerberus = soup.find_all("a")[5]['href']
    Schia = soup.find_all("a")[6]['href']
    Syrtis = soup.find_all("a")[8]['href']
    Valles = soup.find_all("a")[10]['href']

    url2 = "https://astrogeology.usgs.gov/"
    
    #Cerberus
    browser.visit(f"{url2}{Cerberus}")
    #find image
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    x = soup.find_all("img")[5]['src']
    #Store picture on a variable
    Cerberus_pic= f"{url2}{x}"
    
    
    #Schiaparelli
    browser.visit(f"{url2}{Schia}")
    #find image
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    x = soup.find_all("img")[5]['src']
    #Store picture on a variable
    Schia_pic= f"{url2}{x}"
    
    
    #Syrtis
    browser.visit(f"{url2}{Syrtis}")
    #find image
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    x = soup.find_all("img")[5]['src']
    #Store picture on a variable
    Syrtis_pic= f"{url2}{x}"
    
    
    #Valles
    browser.visit(f"{url2}{Valles}")
    #find image
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    x = soup.find_all("img")[5]['src']
    #Store picture on a variable
    Valles_pic= f"{url2}{x}"
    
    #create dict w the data    
    nasa = {
        "Title": head_title,
        "Body": body_text,
        "Featured_Image" : f"https://www.jpl.nasa.gov/{feat_image}",
        "Hemispheres":[{"Title": "Cerberus Hemisphere", "url" :Cerberus_pic},
        {"Title": "Schiaparelli Hemisphere", "url" :Schia_pic},
        {"Title": "Syrtis Major Hemisphere", "url" :Syrtis_pic},
        {"Title": "Valles Marineris Hemisphere", "url" :Valles_pic}]
        }
        
     
    return nasa
