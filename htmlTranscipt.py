import requests 
from bs4 import BeautifulSoup 
from databaseconnection import localconnection
db = localconnection()

# Use this way is the site is whitelisted, which means that bots can crawl it
#my_url = 'https://www.mangareader.net/'

# Use this way if the site has security feature which blocks known spider/bot user agents 



def prof_pics(site, piclink_dict):
	req =  requests.get(site) 

	data = req.text

# Parses Html to make scrapping easier
	page_soup = BeautifulSoup(data, "html.parser")

# Tests

	name_containers = page_soup.findAll("span", {"class": "p-name"})

	img_containers = page_soup.findAll('img')
	del img_containers[len(img_containers)-1]

	src_containers = list()
	for container in img_containers:
		src_containers.append(container['src'])



	for i in range(0, len(src_containers)):
		try:
			#print("IM PUTTING IN :  " + name_containers[i].text.encode('utf-8') )
			piclink_dict[name_containers[i].text.encode('utf-8')] = str(src_containers[i])
		except UnicodeEncodeError:
			continue
#length of test is one more than name containers because it contains the ucsc logo at bottom of page to match everything up just 
#remove the last element from test

def art_pics(site, piclink_dict):
	req =  requests.get(site) 

	data = req.text

# Parses Html to make scrapping easier
	page_soup = BeautifulSoup(data, "html.parser")

# Tests

	name_containers = page_soup.findAll("span", {"class": "field-content"})

	img_containers = page_soup.findAll('img')

	src_containers = list()
	for container in img_containers:
		if 'sites/default/files/styles' in container['src']:
			src_containers.append(container['src'])

	# for entry in src_containers:
	# 	print(entry)



	name = []

	for i in range(0,len(name_containers)):
		name.append(name_containers[i].text.strip())  

	name = map(lambda s: s.strip(), name) 


	# for i in range(0, len(name)):
	# 	print(str(i) + " : " + name[i])


	# for entry in name:
	# 	print(entry)


	for i in range(0, len(src_containers)):
		try:
			#print(name[i] + " " + str(src_containers[i]))
			piclink_dict[name[i]] = str(src_containers[i])
		except UnicodeEncodeError:
			continue

def alt_art_pics(site, piclink_dict):
	req =  requests.get(site) 

	data = req.text

# Parses Html to make scrapping easier
	page_soup = BeautifulSoup(data, "html.parser")

# Tests

	name_containers = page_soup.findAll("span", {"class": "field-content"})

	img_containers = page_soup.findAll('img')

	src_containers = list()
	for container in img_containers:
		if 'sites/default/files/styles' in container['src']:
			src_containers.append(container['src'])

	# for entry in src_containers:
	# 	print(entry)



	name = []

	for i in range(0,len(name_containers)):
		if i%2 == 1:
			name.append(name_containers[i].text.encode('ascii','ignore'))  

	name = map(lambda s: s.strip(), name) 



	for i in range(0, len(src_containers)):
		try:
			#print(name[i] + " " + str(src_containers[i]))
			piclink_dict[name[i]] = str(src_containers[i])
		except UnicodeEncodeError:
			continue


def sociology(site, piclink_dict):
	req =  requests.get(site) 

	data = req.text

# Parses Html to make scrapping easier
	page_soup = BeautifulSoup(data, "html.parser")

# Tests

	name_containers = page_soup.findAll("span", {"class": "field-content"})

	img_containers = page_soup.findAll('img')

def manually_input_teachers(piclink_dict):
	piclink_dict['Edward Migliore']='https://mdtp.ucsd.edu/_images/workgroup-bio-photos/migliore-ed-photo'
	piclink_dict['Randa Roland']='https://www2.ucsc.edu/ali/Photos/Randa.png'
	piclink_dict['Bettina Aptheker']='http://50years.ucsc.edu/css/assets/images/original-thinkers/bettina-aptheker.jpg'
	piclink_dict['Richard Mitchell']='https://news.ucsc.edu/2013/04/images/richard-mitchell-250.jpg'
	piclink_dict['Frank Andrews'] = 'https://news.ucsc.edu/2013/11/images/andrews-frank.jpg'
	piclink_dict['K.C Fung']='https://wcms-prod-web-4.ucsc.edu/cache/directory/kcfung.jpg'
	piclink_dict['Baldo Marinovic']='https://i.ytimg.com/vi/w7xk5sVzfW8/maxresdefault.jpg'
	piclink_dict['Liza Monroy']='https://lareviewofbooks-org-cgwbfgl6lklqqj3f4t3.netdna-ssl.com/wp-content/uploads/2014/04/Monroy-Liza-photo-credit-andy-devlin3.jpg'
	piclink_dict['Patty Gallagher']='http://theater.ucsc.edu/sites/default/files/styles/standard_page_portrait__360_x_542/public/Patty_0200_web.jpg?itok=tlo4GhRg'
	piclink_dict['Audun Dahl']='https://cpb-us-e1.wpmucdn.com/sites.ucsc.edu/dist/7/135/files/2015/07/ad061318SMALL-1gru78y.jpg'
	piclink_dict['Robert Klevan']='https://www.york.org/uploaded/2014-15_News/rob-web.jpg'
	piclink_dict['Yoshihito Shibata']='https://www.amt-law.com/asset/professionals/profile/detail/YBS.jpg'




piclink_dict = {}
prof_pics('https://humanities.ucsc.edu/academics/faculty/index.php', piclink_dict)
prof_pics('https://www.math.ucsc.edu/faculty-research/regular.php', piclink_dict)
prof_pics('https://literature.ucsc.edu/faculty/index.php', piclink_dict)
prof_pics('https://psychology.ucsc.edu/faculty/lecturers.php', piclink_dict)
prof_pics('https://www.math.ucsc.edu/faculty-research/lecturers.php', piclink_dict)
prof_pics('https://sociology.ucsc.edu/about/directory-faculty.php', piclink_dict)
prof_pics('https://psychology.ucsc.edu/about/people/faculty.php',piclink_dict)
prof_pics('https://politics.ucsc.edu/faculty/index.php',piclink_dict)
art_pics('http://art.ucsc.edu/faculty', piclink_dict)
alt_art_pics('http://danm.ucsc.edu/faculty', piclink_dict) 

alt_art_pics('http://theater.ucsc.edu/faculty', piclink_dict)

manually_input_teachers(piclink_dict)

fname = []
lname = []
temp = []
links = []
for k,v in piclink_dict.items():
	#print(k)
	temp = k.split(" ")
	#print(temp[0])
	fname.append(temp[0])

	if len(temp[1]) == 1:
		#print(temp[2])
		lname.append(temp[2])
	else:
		lname.append(temp[1])
	links.append(v)

for i in range(0,len(fname)):
    print("HELLo")
    try:
		cursor = db.cursor()
		quer = "UPDATE Professors Set pic_link =" + '"' + str(links[i]) +'"' + " WHERE FirstName= " + '"' +str(fname[i]) +'"' + " AND LastName= " +'"' + str(lname[i]) + '"' + ";" 
		print(quer)
		cursor.execute(quer)
		db.commit()
    except Exception as e:
		print(e)
		print('Did not work: ')

'''
for i in range(0,len(fname)):
	print("IM MADE IT")
	try:
		cursor = db.cursor()
        print(lname[i])
        # quer = "UPDATE Professors Set pic_link " + str(links[i]) + " WHERE FirstName= " + str(fname[i]) + " AND LastName= " + str(lname[i]) 
		cursor.execute(quer)
		print(fname[i] + " " + lname[i] + " " + links[i]) 
	except Exception as e:
		print(e)
		print('Did not work: ')
db.commit()
'''

#FRANK BAUERLE HAS A NONSTANDARD SYMBOL OVER A so its not stored correctly in dictionary


#FRANK BAUERLE HAS A NONSTANDARD SYMBOL OVER A so its not stored correctly in dictionary
