rom databaseconnection import localconnection
db = localconnection()
import re
from bs4 import BeautifulSoup


filename = "transcript.html"
file = open(filename, "r")


#gets all the text
page_soup = BeautifulSoup(file, "html.parser")

units_containers = page_soup.find_all("span",{"class":"c11"})
course_containers = page_soup.find_all("td",{"class":"c60"})
student_id_container = page_soup.find_all("p",{"class":"c19"})
student_id =student_id_container[1].text
stud_id = student_id.split()[2]	

course_list = []
for container in course_containers:
	course_list.append(container.text)


# I GOT THIS CODE FROM https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def gradeToFloat(num):
	if 'A'  in num :
		if num == 'A+':
			return 4.00
		elif num == 'A-':
			return 3.67
		else:
			return 4.00
	if 'B' in num:
		if num == 'B+':
			return 3.33
		elif num == 'B-':
			return 2.67
		else:
			return 3.00
	if 'C' in num  :
		if num == 'C+':
			return 2.33
		elif num == 'C-' :
			return 1.67 
		else:
			return 2.00
	if  'D' in num :
		if num == 'D+':
			return 1.33
		elif num == 'D-':
			return 0.67
		else:
			return 1.00
	if 'F' in num :
		return 0.00
	if num == 'P':
		return (None)
	if num == "0.000":
		return None



# Gets course without duplicates and course number

fin = []
for entry in course_list:
	if entry not in fin and not(is_number(entry[0])):
		fin.append(str(entry))

fin = map(lambda s: s.strip(), fin)
fin = map(lambda s: s.rstrip(), fin) 

print(fin) 
lines = []

lin = ''

quarter = ["Fall", "Winter", "Spring", "Summer"]




str_units = []
for entry in units_containers:
	try:
		str_units.append(str(entry.text))
	except UnicodeEncodeError:
		print("Could not decode string")

str_units = map(lambda s: s.strip(), str_units)
str_units = map(lambda s: s.rstrip(), str_units) 



transcript = []

curr_quarter = ""
for i in range(0, len(str_units)):
	if any(x in str_units[i] for x in quarter):
		curr_quarter = str_units[i]
	#print(str_units[i])
	if str_units[i] in fin:
		curr_quarter_parts = curr_quarter.split(" ")
		lin = curr_quarter_parts[0] + "  " + curr_quarter_parts[1]  +  " " + str_units[i] + " " + str_units[i+1] + " " + str_units[i+2] + " " + str_units[i+3] + " " + str_units[i+4] + " " + str(gradeToFloat(str_units[i+5]))
		transcript.append(stud_id)
		transcript.append(curr_quarter_parts[0])
		transcript.append(curr_quarter_parts[1])
		transcript.append(str_units[i] + " " + str_units[i+1] )
		transcript.append(str_units[i+2])
		transcript.append(str_units[i+3])
		transcript.append(str_units[i+4])
		transcript.append(str(gradeToFloat(str_units[i+5])))
		lines.append(lin) 


for i in range(0,len(transcript), 8):
	try:
		cursor = db.cursor()
		query = "INSERT INTO GRADES(student_id, attempted, earned, year, quarter, course_string, grade_float) VALUES(%i, %f, %f, %i, %s, %s, %f);"
		args = (transcript[i] , transcript[i+1] ,transcript[i+2] , transcript[i +3] , transcript[i+4] , transcript[i+5] , transcript[i+6] , float(transcript[7]))
		cursor.execute(query, args)
		db.commit()
	except Exception as e:
		print(e)
		print('Did not work: ')
