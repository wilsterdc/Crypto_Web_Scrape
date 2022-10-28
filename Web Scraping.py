"""
Created on Thu Oct  6 08:51:15 2022

@author: Wilster_DC
"""

from bs4 import BeautifulSoup as Soup
import requests
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import pandas as pd


name_list = []
price_list = []
ch24h_list = []
vol_list = []

def main():
    win = tk.Tk()
    win.geometry("650x450-0+0")
    win.title("Crypto Web Scraper")
    win.resizable(0, 0)
    
################################################################################################################## 
    
    f1 = Frame(win, width = 650, height = 450, bg = "#1B2631")
    f1.place(x = 0, y = 0) 
    
    f2 = Frame(win, width = 629, height = 78, bg = "#34495E")
    f2.place(x = 10, y = 10)
 
##################################################################################################################
    
    title = Label(win, text = "Top 10 Crypto from coinmarketcap.com", width = 89,
                  height = 2, background = "#34495E", fg = "white")
    title.place(x = 10, y = 10)

##################################################################################################################
    
    coinlistbox = Listbox( win, width = 40, height = 10, bg = "#34495E", fg = '#ffffff', justify = LEFT, selectmode = EXTENDED)
    coinlistbox.place(x = 11, y = 115)
    
    pricelistbox = Listbox(win, width = 20, height = 10, bg = "#34495E", fg = '#ffffff', justify = LEFT, selectmode = EXTENDED)
    pricelistbox.place (x = 265, y = 115)
    
    changelistbox = Listbox(win, width = 7, height = 10, bg = "#34495E", fg = '#ffffff', justify = CENTER, selectmode = EXTENDED)
    changelistbox.place (x = 400, y = 115)
    
    volumelistbox = Listbox(win, width = 30, height = 10, bg = "#34495E", fg = '#ffffff', justify = LEFT, selectmode = EXTENDED)
    volumelistbox.place (x = 455, y = 115)
    

##################################################################################################################
    
    search = Label(win, text = "YYYY-MM-DD", width = 10,
                  height = 2, background = "#34495E", fg = "white")
    search.place(x = 105, y = 44)
    
    cname = Label(win, text = "Name", width = 34, height = 1, bg = "#1B2631", fg = "white")
    cname.place(x = 11, y = 90)
    
    pname = Label(win, text = "Price", width = 17, height = 1, bg = "#1B2631", fg = "white")
    pname.place(x = 265, y = 90)
    
    chname = Label(win, text = "% 24h", width = 5, height = 1, bg = "#1B2631", fg = "white")
    chname.place(x = 399, y = 90)
    
    vname = Label(win, text = "24h Volume", width = 25, height = 1, bg = "#1B2631", fg = "white")
    vname.place(x = 455, y = 90)
    
##################################################################################################################

    se = Entry(win, width = 30, bg = "white", justify = LEFT, text = "Search", font = "Calibre")
    se.place(x = 185, y = 50)
    
    def search_scrape():
        concat = se.get()
        concat = concat.replace("-", "")
        link = f"https://coinmarketcap.com/historical/{concat}"
        access = requests.get(link)
        soup = Soup(access.text, "html.parser")
        tr = soup.find_all("tr", {"class": "cmc-table-row"})
        return tr

    def web_scrape():
        if (se.get()):
            tr = search_scrape()
        else:
        
            link = "https://coinmarketcap.com/historical/"
            access = requests.get(link)
            soup = Soup(access.text, "html.parser")
            
            tr = soup.find_all("tr", {"class" : "cmc-table-row"})
        
        counter = 0
        
        for row in tr:
            if counter == 10:
                break
            counter += 1
            
            column_name = row.find("td", {"class" : "cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name"})
            coin_name = column_name.find("a", {"class" : "cmc-table__column-name--name cmc-link"}).text.strip()
            coin_price = row.find("td", {"class" : "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price"}).text.strip()
            coin_change = row.find("td", class_ = "cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-24-h").text.strip()
            coin_vol24h = row.find("td", {"cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__volume-24-h"}).text.strip()
            
            name_list.append(coin_name)
            price_list.append(coin_price)
            ch24h_list.append(coin_change)
            vol_list.append(coin_vol24h)
            
            
        for i in range(10):
            if (len(name_list) > 0):
                coinlistbox.insert(END, name_list[i])
                pricelistbox.insert(END, price_list[i])
                changelistbox.insert(END, ch24h_list[i])
                volumelistbox.insert(END, vol_list[i])
                        
            
            # coinlistbox.insert(END, coin_name)
            # pricelistbox.insert(END, coin_price)
            # changelistbox.insert(END, coin_change)
            # volumelistbox.insert(END, coin_vol24h)
            
            
    web_scrape()
    
    def save_csv():
        df = pd.DataFrame()
        
        df["Name"] = name_list
        df["Price"] = price_list
        df["% 24h"] = ch24h_list
        df["volume"] = vol_list
        
        df.to_csv(f"Data {se.get()}.csv", index = False)
    
    save_csv()
    
##################################################################################################################
    
    buttsearch = tk.Button(win, text="Search", command = web_scrape)
    buttsearch.place(x = 462, y = 49)
    
    buttsave = tk.Button(win, text = "Save", command = save_csv, height = 2, width = 10, activebackground = "LightBlue1" , background = 'sky blue')
    buttsave.place(x = 450, y = 330)
    # messagebox.showinfo("File saved. \n press ok to proceed")
    
##################################################################################################################   
    
    win.mainloop()

main()

#git