#Attention: this script won't be able to run one time because of the web server requests limit
#Change the range in the second loop to match the intended range
#The first code block needs to run just once, then you can remove it

import requests
from bs4 import BeautifulSoup

# This is for the first page, run it just once
file = open('Webjeux_games_names.txt','a')
r = requests.get("https://www.webjeux.com/jeux/tous-les-jeux/")
print("WebJeux status code : ",r.status_code)
soup = BeautifulSoup(r.text, "html.parser")
li = soup.find_all("li", class_="games")
for link in li:  
    a = link.find("a")
    name = a["href"]
    name = name[7:-5]
    name = name.replace('-'," ")
    file.write(name+'\n')
file.close()    

# This is for every other page, the range function in the loop can be changed
file = open('Webjeux_games_names.txt','a')
for i in range(2,842):
    r = requests.get("https://www.webjeux.com/jeux/tous-les-jeux/index"+str(i)+".html")
    print("WebJeux status code : ",r.status_code,' ',i)
    soup = BeautifulSoup(r.text, "html.parser")
    li = soup.find_all("li", class_="games")
    for link in li:  
        a = link.find("a")
        name = a["href"]
        name = name[7:-5]
        name = name.replace('-'," ")
        file.write(name+'\n')
file.close()    

