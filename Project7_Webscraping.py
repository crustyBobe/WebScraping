import bs4
import requests
import re
#URL should be https://en.wikipedia.org/wiki/List_of_highest-grossing_films
print("What url do you want to explore?") #Ask the user for the URL to use
url = input()
information = dict() #Dictionary to keep track of the year as keys and the money in the year as the value
res = requests.get(url) #Request the url with requests
res.raise_for_status() #Make sure the URL is valid and raise an exception if it isn't
page = bs4.BeautifulSoup(res.text, features="html.parser") #Parse the page with BeautifulSoup
moneySearch = re.compile(r'(?:\w+)?(\$[0-9,]+)') #Compile the regex search for the money
page = page.select('table[class="wikitable sortable plainrowheaders"] tbody td') #Get a list of the tds in tbodies on the top 50 table
#Set the values of the keys to 0. Otherwise it throws a key error when trying to add the data
for i in range(2, 250, 5): information[page[i+1].get_text()[:-1]] = 0
#Increment the value associated with the key to the regex match to find the money value. Remove the commas by replacing them with an empty string
for i in range(2, 250, 5):
    if(re.match(moneySearch, page[i].get_text()) != None): information[page[i+1].get_text()[:-1]] += int(re.match(moneySearch, page[i].get_text()).group(1)[1:-1].replace(',', ''))
#Print the year and total earnings by iterating through a the dictionary sorted by the values
for year, totalEarnings in sorted(information.items(), key=lambda item: item[1]): print('{:4}    ${:20,}'.format(year, totalEarnings))