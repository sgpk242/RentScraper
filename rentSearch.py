import requests, os, subprocess
from bs4 import BeautifulSoup
from datetime import datetime

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://exmaple.com"}
date_format = "%A, %d %B %Y"
candidates = []
old_list = []
errors = []
pageNum = 1

while True:
	url = "https://www.rent.ie/rooms-to-rent/dublin/ballsbridge,booterstown,cabinteely,carrickmines,churchtown,dalkey,donnybrook,dublin-2,dun-laoghaire,dundrum,foxrock,goatstown,leopardstown,loughlinstown,milltown,monkstown,rathfarnham,rathgar,rathmines,sandymount,windy-arbour,dublin-6,dublin-6w,dublin-12,dublin-14,dublin-18/room-type_either/rent_0-800/page_"+str(pageNum)
	page = requests.get(url, headers=headers, timeout=10)
	soup = BeautifulSoup(page.content, 'html.parser')

	# check that we're not on invalid page
	check = soup.find(id='searchresults_summaryline').find('div').get_text().split()[3]
	if check == "There":
		break

	print("Page {}".format(pageNum))
	page_results = soup.find_all('div', class_='search_result')

	for result in page_results:
		url = result.find('a')['href']
		page = requests.get(url, headers=headers, timeout=10)
		soup = BeautifulSoup(page.content, 'html.parser')
		try:
			box = list(soup.find_all(class_='smi_details_box'))[2]
		except IndexError:
			print(url)
		try:
			try:
				date = str(list(box.find('div').find('p'))[2].strip())
				date_obj = datetime.strptime(date, date_format)
				if date_obj > datetime(2018, 9, 27):
					candidates.append([date, url])
			except (ValueError, TypeError):
				errors.append(url)
		except IndexError:
			pass
	pageNum += 1

# check for repeats
os.chdir('C:\\Users\\PC\Desktop\\')
with open("rent_results.txt", "r") as file:
	for line in file:
		line = line.rstrip().split()
		for item in line:
			if item[0:4] == "http":
				old_list.append(item)
file.close()
candidates = [item for item in candidates if item[1] not in old_list]
errors = [item for item in errors if item not in old_list]

# save to file
file = open("rent_results.txt", "a")
file.write("Ran at {}\n".format(datetime.now().strftime("%H:%M on %A, %d %b")))
file.write("Candidates:\n")
file.write("\n")
for item in candidates:
	file.write("{}: {}\n".format(item[0], item[1]))
file.write("\n")
file.write("Errors:\n")
for item in errors:
	file.write("{}\n".format(item))
file.write("\n")
file.close()
print("success")

os.startfile('C:\\Users\\PC\\Desktop\\rent_results.txt')
