# -*- coding: utf-8 -*-
"""
@author: Arka Gupta
"""
import requests as r
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
 
company_dir={}
data_dict={}
Jav_str_end = ['06','07','08','09','10','11']
Jav_str1 = ['00','01','02','03','04','05','06','07','08','09','10']
Jav_str2 = ['02','03','04','05','06','07','08','09','10','11']


def Company_Scrape(data):
    Name = data.find_all("td",{"class":"contenth3"})
    print Name
    for fields in Name:
        Parse = BeautifulSoup(str(fields))
        for va in Parse.find_all('a', href=True):
            url2 = "http://www.timesbusinessdirectory.com/"+str(va['href'])
            url_data = r.get(url2)
            url_finder = BeautifulSoup(url_data.text)
            new_url = url_finder.find('a',attrs={'class': None},target="_blank")
            try:
                url_store = str(Parse.text).replace("\n","").lstrip()
            except:
                url_store = str(Parse.text).lstrip()
            print url_store
            try:
                url =new_url.text
            except:
                url=None
            company_dir[url_store]=str(url)
    print company_dir
    return company_dir
        
            
def main_scrap(company):
    for val in [company]:
        print "In "+str(val)
        driver = webdriver.Firefox()
        url = "http://www.timesbusinessdirectory.com/DirID-187-Name-Company+Listings-alpha-%s-CompanyListings_MG.aspx"%(val)
        data = r.get(url) #Render(url)
        bs121 = BeautifulSoup(data.text)
        a = bs121.find_all('td',id="listings_records")
        a2 = BeautifulSoup(str(a))
        dat = [int(s) for s in str(a2.text) if s.isdigit()]
        dat1=''
        for vl in dat:
            dat1 =dat1+str(vl)
        dat1 = int(dat1)
        if (dat1 % 10) == 0:
            new_total = int(dat1/10)
        else:
            new_total = int(dat1/10) + 1
        convert = str(new_total)
        new = int(convert[0]+'1')
        driver.get(url)
        def lop_str(Jav,count=1):
            flag=''
            if new_total <= 10:
                Jav = Jav[:new_total]
                for source in Jav:
                    flag ='Y'
                    java_ur="javascript:__doPostBack('dgrdCompany$ctl14$ctl%s','')"%(source)
                    print source
                    print java_ur
                    driver.execute_script(java_ur)
                    soup123 = BeautifulSoup(driver.page_source)
                    data_dict = Company_Scrape(soup123)
                    print "Inside"
                    abc =driver.get_cookies()
                driver.close()
                write2File(data_dict)
                return None
            for source in Jav:
                if count <= new:
                    flag ='Y'
                    java_ur="javascript:__doPostBack('dgrdCompany$ctl14$ctl%s','')"%(source)
                    print source
                    print java_ur
                    driver.execute_script(java_ur)
                    soup123 = BeautifulSoup(driver.page_source)
                    data_dict = Company_Scrape(soup123)
                    print "Inside"
                    count = count + 1 
                    print count
                else:
                    print "New Value : "+str(new)
                    Jav_str_end = Jav_str1[new-new_total:]
                    for source1 in Jav_str_end:
                        java_ur1="javascript:__doPostBack('dgrdCompany$ctl14$ctl%s','')"%(source1)
                        print source1
                        print java_ur1
                        driver.execute_script(java_ur1)
                        soup123 = BeautifulSoup(driver.page_source)
                        data_dict = Company_Scrape(soup123)
                        print data_dict
                        print "Inside"
                    flag ='N'
                    print "The END"
                    break
            if flag =='Y':
                return lop_str(Jav_str2,count)
            elif flag =='N':
                driver.close()
                write2File(data_dict)
            print flag
        lop_str(Jav_str1)
        return None
        
def write2File(dicto):
    writer = csv.writer(open('DirectoryListing_Times_W.csv', 'wb'))
    for key,value in dicto.items():
        writer.writerow([key, value])
