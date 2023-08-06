from bs4 import BeautifulSoup
import requests
import re
# SudoSaeed
def search_film(url):
    s = f"https://www.uptvs.com/?s={url}"
    r = requests.get( s ,timeout=10 )
    msoup = BeautifulSoup(r.text ,"html.parser")
    for i in msoup.find_all("article" ,attrs={"class":"post-layout bg-white rounded mb-20 shadow p-20"}):
        titles = i.text.split()
        links=i.a['href']
        jsons_info = {s:{
                "info":titles,
                "link":links
        }}
        print(jsons_info)


