# grabs the html content
from urllib.request import urlopen as uReq
import xml.etree.ElementTree as ET
import bs4
from bs4 import BeautifulSoup as soup


# parse the html text

filename = "data.csv"

f = open(filename, "w")

headers = "Title,Description,Location,Date Posted,Name,Number,Email,URL,Domain\n"


tree = ET.parse('FILE NAME WITH THE LINKS.xml')
root = tree.getroot()

f.write(headers)

for url in root.iter('url'):
    my_url=url.text
    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    title = page_soup.find("h1", {"class": "tr-h1 ct-sans-serif tr-solo_record"})
    description = page_soup.find("div", {"class": "ct-body3 tr-indent2"})
    location= page_soup.find("div", {"id": "COLLAPSE-Locations"})
    texts=page_soup.find("div", {"class": "tr-status tr-recruiting-colors"})
    if texts is not None:
        texts=' '.join(texts.text.split())
    else:
        texts=page_soup.find("div", {"class": "tr-status tr-not-recruiting-colors"})
        texts=' '.join(texts.text.split())
        texts=texts.replace(",", "|")

    date= texts.rpartition('First')[2].rpartition('Last')[0]

    phone=page_soup.find("td", {"headers": "contactPhone"})
    if phone is not None:
        phone=phone.text
    else:
        phone="not available"

    email=page_soup.find("td", {"headers": "contactEmail"})
    if email is not None:
        email=email.text
        domain="@"+email.rpartition('@')[2]
    else:
        email="not available"

    name=page_soup.find("td", {"headers": "contactName"})
    if name is not None:
        name=name.text.replace(",", "|")
    else:
        name="not available"

    f.write(title.text.replace(",", "|")+ ","+ description.text.replace(",", "|").replace("\n", " ")+","+ location.text.replace(",", "|").replace("\n", " ").rpartition('information')[2]+","+date.replace(",", "|")+","+name+","+phone+","+email+ ","+my_url+","+domain+ "\n")

f.close()
