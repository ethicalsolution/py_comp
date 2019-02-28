# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cx_Oracle
import os
import MySQLdb

from urllib.request import urlopen
from bs4 import BeautifulSoup

con = MySQLdb.connect('144.76.137.232', user='clearsightext', password='Qsy3n98?',db='clearsight_development')
cur = con.cursor()
path = '/home/ubuntu/html'  # This is your folder name which stores all your html
# be careful that you might need to put a full path such as C:\Users\Niche\Desktop\htmlfolder
for filename in os.listdir(path):  # Read files from your path
    # Here we are trying to find the full pathname
    # Getting the full path of a particular html file
    fullpath = os.path.join(path, filename)
    # If we have html tag, then read it
    if fullpath.endswith('.html'):
        #continue
        print(fullpath)
        # Then we will run beautifulsoup to extract the contents
        soup = BeautifulSoup(open(fullpath), "html.parser")
        title = soup.title
        #print(title)
        text = soup.get_text()
        url=fullpath 
        cur.execute("delete from PY_PRE_INSERT where url=%s", [url])
        cur.execute("delete from PY_MAIN where url=%s", [url])
        nonfraction = soup.find_all({"ix:nonnumeric", "ix:nonfraction"})
        x = 0
        i = 0
        to_pos = 0
        row = []
        for row in nonfraction:
            # print(row)
            i = i+1
            if str(row).find("StatementThatCompanyEntitledToExemptionFromAuditUnderSection477CompaniesAct2006RelatingToSmallCompanies") > 0:
                to_pos = str(row).find("StatementThatCompanyEntitledToExemptionFromAuditUnderSection477CompaniesAct2006RelatingToSmallCompanies")
                x = i
            if str(row).find("CompanyEntitledToExemptionUnderSection480CompaniesAct2006RelatingToDormantCompanies") > 0 and to_pos== 0:
                to_pos = str(row).find("CompanyEntitledToExemptionUnderSection480CompaniesAct2006RelatingToDormantCompanies")
                x = i

        i = 0
        row = []
        for row in nonfraction:
            i = i+1
            if str(row).find(":FixedAssets") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'FixedAssets',i])
            if str(row).find(":CurrentAssets") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'CurrentAssets',i])
            if str(row).find(":PropertyPlantEquipment") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'PropertyPlantEquipment',i])
            if str(row).find(":Debtors") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'Debtors',i])
            if str(row).find(":CashBankOnHand") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'CashBankOnHand',i])
            if str(row).find(":CashBankInHand") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'CashBankInHand',i])
            if str(row).find(":CalledUpShareCapital") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'CalledUpShareCapital',i])
            if str(row).find(":NetAssetsLiabilitiesIncludingPensionAssetLiability") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'NetAssetsLiabilitiesIncludingPensionAssetLiability',i])
            if str(row).find(":Creditors") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'Creditors',i])
            if str(row).find(":NetCurrentAssetsLiabilities") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'NetCurrentAssetsLiabilities',i])
            if str(row).find(":TotalAssetsLessCurrentLiabilities") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'TotalAssetsLessCurrentLiabilities',i])
            if str(row).find(":Equity") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'Equity',i])
            if str(row).find(":EntityCurrentLegalOrRegisteredName") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'CompanyName',i])
            if str(row).find(":UKCompaniesHouseRegisteredNumber") > 0 and i < x:
                cur.execute("insert into PY_PRE_INSERT(url,NON_FRACTION,TYPE,RN) values (%s,%s,%s,%s)", [url, str(row),'RegisteredNumber',i])
        cur.callproc('SP_COMPANY_VALUE', [url])
        con.commit()