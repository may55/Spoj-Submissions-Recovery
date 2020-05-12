from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import os
import getpass
import shutil

class Questions:
    def __init__ (self):
        self.name=''
        self.link=''
        
    
def compressFile(output_filename, dir_name):
    shutil.make_archive(output_filename, 'zip', dir_name)




driver = None
            
user_name = input('Put Username here:')
print("Don't worry you'll not be able to see password.")
password=getpass.getpass("Enter Your Password Here: ")


driver = webdriver.Chrome('./Files/chromedriver')
url = 'http://www.spoj.com/login/' 
driver.get(url)
time.sleep(1)


u_name = user_name
pass_word = password

##putting user name in the field
username = driver.find_element_by_xpath('//*[@id="inputUsername"]')
username.send_keys(u_name)


#putting password in the field
passw = driver.find_element_by_xpath('//*[@id="inputPassword"]')
passw.send_keys(pass_word)


#clicking on the button
butt = driver.find_element_by_xpath('//*[@id="content"]/div/div/form/div[4]/button')
butt.click()
time.sleep(1) 


## Going to the profile page of user
url2 = 'http://www.spoj.com/myaccount/'
driver.get(url2)
soup = bs(driver.page_source, 'lxml')
table = soup.find('table' , class_ = 'table table-condensed')


que = []# list of names of all Questions objects
que_list = table.find_all('tr') # found every question row tag under 'tr'

for row in que_list:
    td = row.find_all('td') #td got each question
    for i in td:
        if i.text:
            q = Questions() #object made for question name and its submission link
            a= i.find('a')
            href = 'http://www.spoj.com'+a['href']
            q.link = href
            q.name = i.text.strip()
            que.append(q)
            print(i.text)
            

xyz = 'Extracted by Spoj Code Extractor(' + u_name+')'

if not os.path.exists(xyz):
        os.makedirs(xyz) # folder is made under project folder

count =0
Total_no_que = len(que)
for q1 in que:
    name = q1.name
    link = q1.link
    count+=1
    
    driver.get(link)#driver got link
    soup2 = bs(driver.page_source, 'lxml') # page source got parsed
    td = soup2.find('td' , class_= 'statusres text-center')
    a = td.find('a')
    href = 'http://www.spoj.com'+a['href']
    
    print('Going for '+name+ ' and ' +str(Total_no_que-count) + ' remaining ' + 'Progress : '+str((count*100)//Total_no_que)+'%')
    
    
    driver.get(href) # driver got solution link
    soup3 = bs(driver.page_source, 'lxml')
    div = soup3.find('textarea') #got solution
    
    f = open(xyz+'/'+name , 'wb')#File is open with name in folder made    
    f.write(div.text.encode())#code is written in file
    f.close()
driver.quit()  # finally driver closed.
compressFile('Spoj_Extractor', xyz) #zipping folder

