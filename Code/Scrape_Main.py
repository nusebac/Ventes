# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 14:37:52 2015

@author: HP
"""

import Times_Scrape_Co


Company_Lists = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','Others']

for Company_List in Company_Lists:
    print "---------------------Scraping :%s------------------------"%(Company_List)
    Times_Scrape_Co.main_scrap(Company_List)
