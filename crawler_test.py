# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21:17:25 2019

@author: sskor

V2 : 26/09/2019
reality.cz/prodej/byty/Praha/ - flats in Prague
despite the fact that website looks like the button on bottom is to show 
25 more results, when reqested, only next page of another 25 results is loaded,
therefore button behaves like "next page" button

Output: 
    csv with colmns :   "Place" - place as described in header of offer
                        "Price" - as stated in header of offer
"""

###########################################################
### Imports
import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from bs4 import BeautifulSoup
import requests


###########################################################
### main
def main():
    start_time = time.time()
    
    url = "https://www.reality.cz/prodej/byty/Praha/"
    price = []
    place = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, features = "lxml") 
    
    for i in range(10):
        
        #elem_price = soup_next.findAll('p', attrs={'class':'vypiscena'})
        #for a in elem_price[len(price):] :
        for a in soup.findAll('p', attrs={'class':'vypiscena'}) :
            temp = a.strong
            if not temp :
                temp = a.find('span', attrs={'class':'neucena'})
        
            price.append(temp.text[0:(len(temp.text) - 3)])
        
        #elem_place = soup_next.findAll('p', attrs={'class':'vypisnaz'})
        #for a in elem_place[len(place):] :
        for a in soup.findAll('p', attrs={'class':'vypisnaz'}):
            temp = a.text
            if not temp :
                temp = "neuvedeno"
    
            temp = temp[(temp.find("\n")+1): temp.find("\n", temp.find("\n")+1)]
            place.append(temp) 
            
        # now get the new page    
        buttom_box = soup.find("div", {"class":"strankovani noprint"})
        button_item = buttom_box.find("a",{"class": "button wauto pl10 pr10 fss ui-corner-all"})
        button_href = button_item.get('href')
        print(button_href, button_item)
       
        req = requests.get(url + str(button_href))
        soup = BeautifulSoup(req.text, 'lxml')  
    
    print(price)
    print(place)
    df = pd.DataFrame({"place": place, "price" : price})
    df.to_csv('prices_reality_cz.csv', index=False, encoding='utf-8')
    
    print("Time to run: ", time.time() - start_time)
    
###########################################################
### start main
if __name__ == "__main__":
    main()