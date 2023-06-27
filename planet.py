import csv 
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
# import chromedriver_autoinstaller as chromedriver

# chromedriver.install()

options = Options()
# options.add_experimental_option("detach", True)

start_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog"

browser = webdriver.Chrome("/usr/local/bin/chromedriver", chrome_options=options)
browser.get(start_url)

time.sleep(2)

# browser.find_element("xpath", '//*[@id="gb"]/div/div[2]/a').click()

# browser.find_element("xpath", '//*[@id="identifierId"]').send_keys("harsha.kotla@gmail.com")

# time.sleep(2)

# browser.find_element("xpath", '//*[@id="identifierNext"]/div/button/span').click()

planet_data = []


def scrape():
    headers = ["name", "light_years_from_earth", "planet_mass", "stellar_mag", "discovery_date", "planet_type", "discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]
    
    for i in range(0, 1):
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
            # print("https://exoplanets.nasa.gov"+chs[0].find_all("a", href=True)[0]["href"])
            fs = scrape_more("https://exoplanets.nasa.gov"+chs[0].find_all("a", href=True)[0]["href"])
            for r in fs:
                r = r.replace("\n", "")
                temp.append(r)
            temp2 = []
            for j in temp:
                if j not in temp2:
                    temp2.append(j)
            planet_data.append(temp2)
        print(str(i) + " pages done")

        browser.find_element("xpath", '//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

    with open("data.csv", "w") as f:
        
        csv_writer = csv.writer(f)
        csv_writer.writerow(headers)
        csv_writer.writerows(planet_data)
def scrape_more(link):  
    try:
        html = requests.get(link)
        soup = BeautifulSoup(html.content, "html.parser")
        rows = soup.find_all("tr", attrs={"class", "fact_row"})
        facts = []
        for row in rows:
            cells = row.find_all("td")
            for cell in cells:
                try:
                    d = cell.find_all("div", attrs={"class", "value"})[0].contents[0]
                    facts.append(d)
                except:
                    facts.append("no data")
        return facts

    except:
        time.sleep(1)
        scrape_more(link)
        

scrape()
# print(scrape_more("https://exoplanets.nasa.gov/exoplanet-catalog/6988/11-comae-berenices-b/"))