from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Date
# Create your views here.

def scrape(request):
    page = requests.get('https://www.tsa.gov/coronavirus/passenger-throughput')
    soup = BeautifulSoup(page.text, 'html.parser')

    rows =[]
    clear =[]
    z = 0
    trs = soup.find_all('tr')
    trs = trs[1:]

    for tr in trs: # for every table row
        rows.append([td.get_text(strip=True) for td in tr.find_all('td')]) # data row
    
    for row in rows:
        if row == []:
            rows.remove(row)      
        z=z+1
    
    for i in range(z):
        date_raw = rows[i][0].replace("/","")
        d="0"
        if len(date_raw)==7:
            d = d+date_raw
            y = d[4:]
            date_mod = y + "-" +d[:2] + "-" + d[2:4]
        elif len(date_raw)==6:
            dat = date_raw[0]+"0"+date_raw[2:] 
            d = d+dat
            date_mod = y + "-" +d[:2] + "-" + d[3:5]
        else:
            y = date_raw[3:]
            date_mod = y+"-"+date_raw[:1]+"-"+date_raw[2:3]
        date = date_mod
        today = int(rows[i][1].replace(",",""))
        year_ago = int(rows[i][2].replace(",",""))
        
        Date.objects.create(date=date,today=today,year_ago=year_ago)
        
    return render(request, 'scraper/result.html',{'rows':rows, 'clear':clear})