from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

#Opening a .csv file in which the output will be stored
filename = "products.csv"
file = open(filename, 'w')

#Aetting up headers or column names
column_names = "Name, Description, Cost, Image Urls\n"
file.write(column_names)

#Sending a get request to the url to fetch the page source and parsing it using BS4
url = "https://www.houseofindya.com/zyra/necklace-sets/cat"
client_request = urlopen(url)
source = client_request.read()
client_request.close()
parsed_source = soup(source, 'html.parser')

#Getting all the urls for necklace sets embedded in the list items
elements = parsed_source.find('ul', {"id": "JsonProductList"})
necklace_urls = []
elements_li = elements.findAll('li')
for element in elements_li:
	necklace_urls.append(element['data-url'])

#Sending request all the urls in necklace_urls and fetching their source code
for url in necklace_urls:
	necklase_url = url
	necklase_client = urlopen(necklase_url)
	necklase_source = necklase_client.read()
	necklase_client.close()
	parsed_necklase_source = soup(necklase_source, 'html.parser')

	#Getting all the image urls for a particular necklace set
	image_container = parsed_necklase_source.find('div', {"class": "prodLeft"})
	images = image_container.findAll('img')
	image_urls = ""
	for image in images:
		image_urls += image['data-original'] + ';'

	information_container = parsed_necklase_source.find('div', {'class': 'prodRight'})

	name = information_container.find('h1').text

	cost = information_container.find('h4').findAll('span')[1].text.strip()

	description = information_container.find('div', {'id': 'tab-1'}).find('p').text.strip()

	#Replacing all the ',' in the description with ';' 
	description = description.replace(',', ';')

	#Creating a row out of the fetched data 
	row = name + ',' + description + ',' + cost + ',' + image_urls + '\n'

	#Writing the row to the file
	file.write(row)