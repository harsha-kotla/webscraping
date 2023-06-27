import csv 
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# import chromedriver_autoinstaller as chromedriver

# chromedriver.install()

options = Options()
options.add_experimental_option("detach", True)

start_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog"

browser = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)
browser.get(start_url)

time.sleep(2)

# browser.find_element("xpath", '//*[@id="gb"]/div/div[2]/a').click()

# browser.find_element("xpath", '//*[@id="identifierId"]').send_keys("harsha.kotla@gmail.com")

# time.sleep(2)

# browser.find_element("xpath", '//*[@id="identifierNext"]/div/button/span').click()

def scrape():
    headers = ["name", "light_years_from_earth", "planet_mass", "stellar_mag", "discovery_date"]
    planet_data = []
    for i in range(0, 214):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        exoplanets = soup.find_all("ul", attrs={"class", "exoplanet"})
        for exoplanet in exoplanets:
            chs = exoplanet.find_all("li")

            temp = []
            for li in range(len(chs)):
                if li == 0:
                    try:
# https://exoplanets.nasa.gov/exoplanet-catalog/2356/kepler-1486-b/
                        temp.append(chs[0].find_all("a")[0].contents[0])
                    except:
                        temp.append("")
                else:
                    try:
                        
                        temp.append(chs[li].contents[0])
                    except:
                        temp.append("")
            
            planet_data.append(temp)
        browser.find_element("xpath", '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    with open("data.csv", "w") as f:
        
        csv_writer = csv.writer(f)
        csv_writer.writerow(headers)
        csv_writer.writerows(planet_data)
        
        

scrape()
