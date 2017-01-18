import sys
import os
import requests
import pdb
import time
from bs4 import BeautifulSoup as bs
import selenium
from selenium import webdriver
import urllib2

args = sys.argv

cik = ''

for i in range(0,len(args)):
    if args[i] == '-cik':
        cik = args[i+1]



driver = webdriver.Chrome()
driver.get("http://www.sec.gov/edgar/searchedgar/companysearch.html")


cik_input = driver.find_element_by_id('cik').send_keys(cik)
driver.find_element_by_id('cik_find').click()
time.sleep(3)
table = driver.find_element_by_class_name('tableFile2')
rows = table.find_elements_by_xpath("//tr")
doc_link = ''
for i in rows:
    if i.text[:6] == '13F-HR':

        doc_link = i.find_element_by_css_selector('a').get_attribute('href')
        break
driver.get(doc_link)

link_table = driver.find_element_by_class_name('tableFile')
links = link_table.find_elements_by_xpath('//a')

f_hr = ''
for i in links:

    if i.text[-4:] == ('.txt'):
        f_hr = urllib2.urlopen(i.get_attribute('href'))
        driver.get(i.get_attribute('href'))

        break


data = f_hr.read()
soup = bs(data, 'xml')
holdings = soup.find_all('infoTable')
filename = soup.find('formData').find('filingManager').find('name').text.replace(' ', '_')+'.txt'
file = open(filename, 'w')
file.write('NAME OF ISSUER      TITLE OF CLASS      CUISP       VALUE       SSHPRNAMT       SSHPRNAMTTYPE       VOTINGSOLE      VOTINGSHARED \n')
for i in holdings:
    file.write(i.nameOfIssuer.text + '        '+i.titleOfClass.text + '         '+i.cusip.text +'        '+i.value.text +'        '+i.shrsOrPrnAmt.sshPrnamt.text +'       '+ i.shrsOrPrnAmt.sshPrnamtType.text+'       '+ i.votingAuthority.Sole.text +'        ' +i.votingAuthority.Shared.text + '\n')


file.close()

driver.close()
