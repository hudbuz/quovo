import sys
import time
from bs4 import BeautifulSoup as bs
import selenium
from selenium import webdriver
import urllib2
import subprocess


args = sys.argv



def get_cik():
    fund_id = ''
    for i in range(0,len(args)):
        if args[i] == '-cik' or args[i] == '-tik':
            ###works for both cik or ticker
            fund_id = args[i+1]
    return fund_id



class Holdings_Finder:

    def __init__(self,cik):
        self.cik = cik

    def get_13FHR(self):

        driver = webdriver.Chrome()
        driver.get("http://www.sec.gov/edgar/searchedgar/companysearch.html")
        ## use Webdriver to open SEC search portal and enter fund CIK
        cik_input = driver.find_element_by_id('cik').send_keys(self.cik)
        driver.find_element_by_id('cik_find').click()
        time.sleep(3) ### allows for page to load
        table = driver.find_element_by_class_name('tableFile2')
        rows = table.find_elements_by_xpath("//tr")
        doc_link = ''
        for i in rows:
            ###iterates through document table to find first instance of 13F-HR, which is also most recent since table organized chronologically
            if i.text[:6] == '13F-HR':
                doc_link = i.find_element_by_css_selector('a').get_attribute('href')
                break
        driver.get(doc_link)
        ### Finds 13-FHR link and clicks on it
        link_table = driver.find_element_by_class_name('tableFile')
        links = link_table.find_elements_by_xpath('//a')
        ## Finds all links within 13-FHR page and selects the full report with a .txt ending
        f_hr = ''
        for i in links:
            if i.text[-4:] == ('.txt'):
                f_hr = urllib2.urlopen(i.get_attribute('href'))
                driver.get(i.get_attribute('href'))

                break
        ## returns xml of full fund 13F-HR report
        return f_hr

    def read_13FRH(self,xml):
        data = xml.read()
        soup = bs(data, 'xml')
        ### Employs Beautiful Soup to parse through XML documentation
        holdings = soup.find_all('infoTable')
        filename = soup.find('formData').find('filingManager').find('name').text.replace(' ', '_')+'.txt'
        ### Looks through FormData table to find name of Fund
        file = open(filename, 'w')
        file.write('NAME OF ISSUER      TITLE OF CLASS      CUISP       VALUE       SSHPRNAMT       SSHPRNAMTTYPE       VOTINGSOLE      VOTINGSHARED \n')
        for i in holdings:
            ### Iterates though each funds holdings which has a tag of 'infoTable' within an 'informationTable' xml element
            file.write(i.nameOfIssuer.text + '        '+i.titleOfClass.text + '         '+i.cusip.text +'        '+i.value.text +'        '+i.shrsOrPrnAmt.sshPrnamt.text +'       '+ i.shrsOrPrnAmt.sshPrnamtType.text+'       '+ i.votingAuthority.Sole.text +'        ' +i.votingAuthority.Shared.text + '\n')
        file.close()
        subprocess.call(['open', '-a', 'TextEdit', filename])
        ### opens file in TextEdit so that it may be viewed by user
        webdriver.Chrome().close()

cik = get_cik()
docs = Holdings_Finder(cik)
text = docs.get_13FHR()
end_file = docs.read_13FRH(text)
