#import ping
import os
import re
import os.path
import getopt
import csv
import sys
import time
import string
import calendar
import requests, json
import socket
import shutil
import select
import pdb
import os, random, struct
import getpass
import traceback
import hashlib
from Crypto.Cipher import AES
import ConfigParser
from pyvirtualdisplay import Display
from inspect import currentframe
from decimal import Decimal
from datetime import datetime, timedelta
from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import smtplib
import imaplib
import getpass
import email
from cStringIO import StringIO
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import Charset
from email.generator import Generator
from inspect import currentframe
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
    
import gspread
from oauth2client.service_account import ServiceAccountCredentials    
    
start_time = datetime.now()    
       
NOPLACES = Decimal(10)
TWOPLACES = Decimal(10) ** -2

DO_ANDY_FD = 0

ANDYFD_URI = "http://www1.firstdirect.com/1/2/"
ANDYFD_ID = "ajb77777"
ANDYFD_PW = "Saints99"
ANDYFD_MEMINFO = "Pret A Manger"

VEND_USER_NAME = "mary@theconsortiumonline.co.uk"
VEND_PASSWORD  = "monkswood"
VEND_URI       = "https://theconsortium.vendhq.com/signin" 

SHOPURL        = "http://shop.theconsortiumonline.co.uk"

RB_EMAIL_USERNAME = 'rb210849@gmail.com'
RB_EMAIL_PASSWORD = 'monkswood9999'

CC_MARY = 0

# new stdout to write to stdout.txt
class new_stdout:
    nlo = True

    def write(self, x):
        fn = open("/home/pi/ron_python/stdout.txt", 'a')
        if x == '\n':
            fn.write(x)
            self.nlo = True
        elif self.nlo == True:
            fn.write('%s> %s' % (str(datetime.now()), x))
            self.nlo = False
        else:
            fn.write(x)
        fn.close();     

# new stdout to write to stdout.txt
class new_stderr:
    nle = True

    def write(self, x):
        fn = open("/home/pi/ron_python/stderr.txt", 'a')
        if x == '\n':
            fn.write(x)
            self.nle = True
        elif self.nle == True:
            fn.write('%s> %s' % (str(datetime.now()), x))
            self.nle = False
        else:
            fn.write(x)
        fn.close();     

#*****************
# Logging routines
#*****************
   
# log init   
def loginit ():
    
    ts = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    
    fn = open("/home/pi/ron_python/logfile.txt", 'w')
    fn.truncate();
    fn.write (ts + " : " + "Logging Started" + "\n")
    fn.close(); 
    
    fn = open("/home/pi/ron_python/stdout.txt", 'w')
    fn.truncate();
    fn.write (ts + " : " + "Stdout Logging Started" + "\n")
    fn.close(); 
    
    fn = open("/home/pi/ron_python/stderr.txt", 'w')
    fn.truncate();
    fn.write (ts + " : " + "Stderr Logging Started" + "\n")
    fn.close();  
    
# log a string to logfile.txt         
def logit (string):

    global prev_logit_string;
    global test_run
    global test_vend 
   
    ts = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    
    prev_logit_string = ts + " : " +  "(PID=" + str(os.getpid()) + ") " + str(string);
    
    if ((test_vend == 0) and (test_andy_fd == 0) and (test_andy_check == 0)and (test_run == 0)):  
        fn = open("/home/pi/ron_python/logfile.txt", 'a')
        fn.write (ts + " : " + "(PID=" + str(os.getpid()) + ") " + str(string) + "\n")
        fn.close(); 
    else:
        print (ts + " : " +  "(PID=" + str(os.getpid()) + ") " + str(string))

# returns the elapsed milliseconds since the start of the program
def millis():
   dt = datetime.now() - start_time
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return ms

#*******************************
# sleeps for a number of seconds
# using time.sleep 
def mysleep (sec):
#*******************************

    # using loop timer
    global k
    for i in range(sec):
        for j in range(1000*900):
            k = j + i    
    
    # using time.sleep
    #time.sleep(sec)
    return

#***********************************  
def daterange(start_date, end_date):
#***********************************  

    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)   
 
#****************************    
def mytrace(num):
#****************************

    fo = open("/home/pi/ron_python/mytrace.txt", "a") 
    fo.write(" " + str(num)) 
    fo.close

#**********************************
def save_screenshot (name):
#**********************************  
    global driver
    fn = "/home/pi/ron_python/" + name + ".png";
    logit (fn);
    try:
        os.remove(fn)
    except:
        pass
    driver.save_screenshot(fn)
    logit ("Saving screenshot " + fn);
    return

#**************************
def getxpath (name, xpath):
#**************************     
   
    logit ("looking for " + name);
    waittime = 1
    maxretries = 999
    count = 0;
    rc = 0;
    while True:
        element,rc = waitxpath (xpath, 1)
        if rc==0:
            if count==0:
                logit ("getxpath " + name + " succeeded on first attempt");
            else:
                logit ("getxpath " + name + " succeeded after " + str(count) + " retries");
            break 
        else:
            count = count + 1
            if count == maxretries:
                logit ('getxpath ERROR : ' + name  + " failed after " + str(count) + " retries");
                string.replace (name, " " , "_");
                save_screenshot (name);
                logit ("returning RC=-1")
                rc = -1
                break
    return element, rc       
   
#***************************
def doclick (name, element):
#***************************   
 
    waittime = 1
    maxretries = 30
    count = 0;
    rc = 0
    while True:
        try:
            element.click();
            if count == 0:
                logit ("doclick " + name + " succeeded on first attempt")
            else:
                logit ("doclick  " + name + " succeeded after " + str(count) + " retries");
            break
        except:
            count = count + 1
            if count == maxretries:
                logit ('ERROR : doclick ' + name  + " failed after " + str(count) + " retries");
                string.replace (name, " " , "_");
                save_screenshot (name);
                logit ("returning RC=-1")
                rc = -1;
                break
            else:
                time.sleep (1);  
    return rc      

#************************************
def dosendkeys (name, element, keys):
#***********************************   
 
    waittime = 1
    maxretries = 30
    count = 0;
    rc = 0
    while True:
        try:
            element.send_keys(keys);
            if count == 0:
                logit ("dosendkeys " + name + " succeeded on first attempt")
            else:
                logit ("dosendkeys  " + name + " succeeded after " + str(count) + " retries");
            break
        except:
            count = count + 1
            if count == maxretries:
                logit ('ERROR : dosendkeys ' + name  + " failed after " + str(count) + " retries");
                string.replace (name, " " , "_");
                save_screenshot (name);
                logit ("returning RC=-1")
                rc = -1;
            else:
                time.sleep (1);  
    return rc      

#***************************
def clear_flag (name):
#***************************  
    
    os.chdir ('/home/pi/ron_python')
    os.system ('rm name.flag')  
    return
    
#***************************
def set_flag (name):
#***************************  
    
    os.chdir ('/home/pi/ron_python')
    os.system ('touch name.flag')   
    return
    
#***************************
def test_flag (name):
#***************************  

    os.chdir ('/home/pi/ron_python')
    try:
        statinfo = os.stat('name.flag')
        return 1
    except:
        return 0
 
#****************************
def waitxpath (xpath, time):
#****************************

    global driver
    
    rc = 0
    element = 0
    try:
        element = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, xpath))) 
    except:
        rc = -1
    return element, rc
    
'''   
#****************************
def waitcsspath (csspath, time):
#****************************

    global driver
    rc = 0
    element = 0
    try:
        element = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.CSS_SELECTOR, csspath))) 
    except:
        rc = -1 
    return element, rc     
'''    

#****************************
def do_format (val):
#****************************  
     if val <   0:
        val = - val
        return ('-' + u"\xA3" + '{:,.2f}'.format(val))  
     else: 
        return (u"\xA3" + '{:,.2f}'.format(val))        

#**************************
def letter_to_index(letter):
#**************************

    _alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return next((i for i, _letter in enumerate(_alphabet) if _letter == letter), None)
    
#**************************
def index_to_letter(index):
#**************************

    _alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return _alphabet[index];    

#****************************
def do_vend ():
#****************************     
           
    global driver
    global testing
         
    # use todays date  
    dnow = datetime.now()  
  
    start_date = dnow
    end_date = start_date
    
    # use a specific date (normally comment out the next two lines)
    #start_date = datetime (2018, 6, 1, 0, 0);
    #end_date = datetime  (2018, 6, 30, 0, 0);
    
    sdate = start_date.strftime("%d/%m/%y")
    edate = sdate
    
    logit ("Today's date=" + str(sdate))
  
    '''
    # check vend is up
    logit ("checking Vend is up...")
    hostname = "www.vendhq.com" 
    response = os.system("ping -c 4 " + hostname + "2>/dev/null >/dev/null")

    #and then check the response...
    if response == 0:
        logit (hostname + ' is up!')
    else:
        logit (hostname + ' seems to be down!')
        return -1
    '''
    
    # get various times and dates 
    sdate = dnow.strftime("%d %b %Y").lstrip ('0')
    date = dnow.strftime("%d %B %Y")
    day = dnow.strftime("%a")
    longday = dnow.strftime("%A")
    d = dnow - timedelta(days=6)
    date_week_ago = d.strftime("%d %B %Y")
    date_jan1 = dnow.strftime("01 January %Y")
    date_mon1 = dnow.strftime("01 %B %Y")
    timenow = time.strftime("%H:%M")
    day_of_year = dnow.timetuple().tm_yday
    day_of_month = dnow.day 
   
    # open vend uri
    try:
        logit ("Opening " + VEND_URI)
        driver.get(VEND_URI )
    except: 
        logit ("vend driver.get failed")
        return -1
    
    # Resize the window to the screen width/height
    try:
        driver.set_window_size(2000, 1500)
    except:
        logit ("driver.set_window_size failed")
        return -1
        
    # Move the window to position x/y
    try:
        driver.set_window_position(0, 0)
    except:
        logit ("driver.set_window_position failed")
        return -1
    
    element, rc = getxpath ('Signin User Name', '//*[@id="signin_username"]')
    if rc == -1:
        return -1
    
    logit ("entering user name")
    
    rc = dosendkeys("entering user name", element, VEND_USER_NAME);
    if rc == -1:
        return -1
    
    element, rc = getxpath ('Signin Password', '//*[@id="signin_password"]')
    if rc == -1:
        return -1
    
    logit ("entering password")
    rc = dosendkeys("entering password", element, VEND_PASSWORD);
    if rc == -1:
        return -1
        
    element, rc = getxpath ('Signin Button', '//*[@id="main"]/section/div/div[1]/div[1]/form/div[5]/div/button')
    if rc == -1:
        logit ("return -1");
        return -1
    
    rc = doclick ("Signin Button", element);
    if rc == -1:
        return -1
    
    # wait for screen with main register
    element, rc = getxpath ('Main Register', '/html/body/div[1]/nv-sidenav/div/vd-sidebar-drawer/div[1]/nv-sidenav-drawer-before/register-info/div/vd-header')
    if rc == -1:
        return -1
        
     # wait for screen with sales ledger
    element, rc = getxpath ('Sales Ledger click', '/html/body/div[1]/nv-sidenav/div/vd-sidebar-tabs/vd-nav-item[3]/a/vd-icon')
    if rc == -1:
        return -1    
        
    rc = doclick ("Sales Register", element);
    if rc == -1:
        return -1

    # wait for screen with ledger
    element, rc = getxpath ('Sales Ledger wait', '//*[@id="main-body"]/div[1]/div[4]/div[1]/a')
    if rc == -1:
        return -1
    
    # Get sales history for entire year month by month, add to dictionary 
    adate = datetime.now()
    data = [] 
    
    #/* loop for all dates */
    for single_date in daterange(start_date, end_date+timedelta(1)):
    
        my_date = single_date.strftime("%d %B %Y")
        this_day = single_date.strftime("%Y-%m-%d")
        
        logit (  "processing date " + my_date)
    
        # Remove all CSV files from downloads 
        os.chdir ('/home/pi/Downloads')
        filelist = [ f for f in os.listdir(".") if f.endswith(".csv") ]
        for f in filelist:
            os.remove(f) 
        
        # Remove all CSVX files from downloads (renamed versions of downloaded csv files)   
        os.chdir ('/home/pi/Downloads')
        filelist = [ f for f in os.listdir(".") if f.endswith(".csvx") ]
        for f in filelist:
            os.remove(f) 
    
        # look for start date
        element, rc = getxpath ('Start Date', '//*[@id="date_from"]')
        if rc == -1:
            return -1
    
        logit ("entering start date " + my_date) 
        element.send_keys (my_date)
        element.submit();
    
        # look for end date
        element, rc = getxpath ('End Date', '//*[@id="date_to"]')   
        if rc == -1:
            return -1
    
        logit ("entering end date " + my_date)
        element.send_keys (my_date)   
        element.submit();

        element, rc = getxpath ('Update button', '//*[@id="main-body"]/div[1]/div[4]/form/div/button') 
        if rc == -1:
            return -1
            
        rc = doclick ("Update", element);
        if rc == -1:
            return -1

        element, rc = getxpath ('Export Button', '//*[@id="main-body"]/div[1]/div[4]/div[1]/a') 
        if rc == -1:
            return -1
        
        rc = doclick ("Export", element);
        if rc == -1:
            return -1

        # wait for csv file to arrive
        logit (  "looking for CSV file")
        for cnt in xrange(1, 30):
            filelist = [ f for f in os.listdir(".") if f.endswith(".csv") and not f.startswith("vend-sales-by-day")]
            if len(filelist) != 0:
                break  
            mysleep(1)
        
        try:
            fn = filelist[0]   
        except:
            logit ("file not found .. retrying")
            
            # wait for csv file to arrive
            logit (  "looking for CSV file")
            for cnt in xrange(1, 30):
                filelist = [ f for f in os.listdir(".") if f.endswith(".csv") and not f.startswith("vend-sales-by-day")]
                if len(filelist) != 0:
                    break  
                mysleep(1)
        
            try:
                fn = filelist[0]   
            except:
                logit ("file not found after retry ... exit")
                return -1
             
        logit ("CSV File = " + str(filelist[0])) 
        
        #Wait 30 seconds to make sure that the file is all present and correct
        logit ("30 sec wait for file to arrive")
        mysleep(30);
    
        # Add sales files to dictionary so that we have entire calendar year sales info
        logit ('processing data')
        os.chdir ('/home/pi/Downloads')
        adate = datetime.now()
        data = []    
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q']     
        with open(fn) as csvfile: 
            rownum = 0
            for row in csv.DictReader(csvfile, fieldnames=columns, delimiter=','): 
                if rownum != 0:
                    data.append(row) 
                rownum += 1     
        csvfile.close()
        
        # Convert dictionary into sales array
        data.reverse()
        sales = []
        sales_list = []
        payment_list = []
        sales_pending = 0
        prev_receipt = 0
        pending_receipt = '-'
        for row in data:
            if row['c'] == 'Payment':
                payment_total =  Decimal(row['l'].replace(',',''))
                payment_type = row['m']
                payment_list.append([payment_total, payment_type])
            elif row['c'] == 'Sale Line':
                sale_item_qty = int(Decimal(row['g'].replace(',','').replace('-','')).quantize(NOPLACES))
                sale_item_subttl = Decimal(row['h'].replace(',','')) 
                sale_item_tax = Decimal(row['i'].replace(',','')) 
                sale_item_total = Decimal(row['k'].replace(',',''))  
                sale_item_detail = row['m']
                sales_list.append([sale_item_qty, sale_item_subttl, sale_item_tax, sale_item_total, sale_item_detail])
            elif row['c'] == 'Sale':   
                receipt = row['b'] 
                sale_status = row['p']
                index = row['a'].find(' ')
                sale_date = row['a'][0:index+1]
                sale_time = row['a'][index+1:len(row['a'])]
                sale_time = sale_time[:-3]
                sale_datetime = row['a']
                sale_subttl = Decimal(row['h'].replace(',','')) 
                sale_tax = Decimal(row['i'].replace(',','')) 
                sale_total = Decimal(row['k'].replace(',','')) 
                sale_qty =  int(Decimal(row['g'].replace(',','')).quantize(NOPLACES))
                sales.append([sale_date.rstrip(), sale_time, receipt, payment_list, sale_status, sale_qty, sale_subttl, sale_tax, sale_total, sales_list])
                payment_list = []
                sales_list = []
            else:
                logit (  "Bad Line Type .." + row['c'] + ' at line ' + str(get_linenumber()))
                return (1)   

        # look for sales in each day
        hw_count = 0
        hw_total = Decimal(0)
        furn_count = 0
        furn_total = Decimal(0)
        paint_count = 0
        paint_total = Decimal(0)
        disc_count = 0
        disc_total = Decimal(0)
        romsey_count = 0
        romsey_total = Decimal(0)
        books_count = 0
        books_total = Decimal(0)  

        cash = Decimal(0) 
        card = Decimal(0) 
        cheque = Decimal(0) 
        bacs = Decimal(0) 
        internet = Decimal(0)
    
        for sale in sales:
            if sale[0] == this_day:
                if sale[4] == "CLOSED": 
                    for sale_line in sale[9]:
                        if sale_line[4] == "Homewares":
                            hw_count += sale_line[0]
                            hw_total += sale_line[3]
                            sales_update_col = 'C'
                        elif sale_line[4] == "Annie Sloan Chalk Paint":
                            paint_count += sale_line[0]
                            paint_total += sale_line[3]
                            sales_update_col = 'D'
                        elif sale_line[4] == "Furniture":
                            furn_count += sale_line[0]
                            furn_total += sale_line[3]
                            sales_update_col = 'E'
                        elif sale_line[4] == "Discount":
                            disc_count += sale_line[0]
                            disc_total += sale_line[3]
                            sales_update_col = 'F'    
                        elif sale_line[4] == "Romsey":
                            romsey_count += sale_line[0]
                            romsey_total += sale_line[3]
                            sales_update_col = 'G'   
                        elif sale_line[4] == "Books":
                            books_count += sale_line[0]
                            books_total += sale_line[3]
                            sales_update_col = 'H'                  
                        else:
                            s =  "Vend Bad sale line detail " + sale_line[4] + ' at line ' + str(get_linenumber())
                            logit (s)
                            send_warning_email (s)   
                    
                    for payment in sale[3]:
                        if payment[1] == "Cash":
                            cash += payment[0]
                        elif payment[1] == "Debit Card":
                            card += payment[0] 
                        elif payment[1] == "Cheque":
                            cheque += payment[0]  
                        elif payment[1] == "BACS payment":
                            bacs += payment[0]   
                        elif payment[1] == "Internet Purchase":
                           internet += payment[0]     
                        else:
                            s = "Vend Bad payment type " + payment[1] + ' at line ' + str(get_linenumber()) 
                            logit (s)
                            send_warning_email (s)     
                    
                elif sale[4] == "VOIDED":
                    logit (  "Payment status = " + sale[4])
                elif sale[4] == "SAVED":
                    logit (  "Payment status = " + sale[4])
                else:
                    s = "Vend Bad payment status " + sale[4] + ' at line ' + str(get_linenumber()) 
                    logit (s)
                    send_warning_email (s); 

        hw_total = Decimal(hw_total).quantize(TWOPLACES)
        paint_total = Decimal(paint_total).quantize(TWOPLACES)
        furn_total = Decimal(furn_total).quantize(TWOPLACES)
        disc_total = Decimal(disc_total).quantize(TWOPLACES)
        romsey_total = Decimal(romsey_total).quantize(TWOPLACES) 
        hw_count = Decimal(hw_count).quantize(NOPLACES)
        paint_count = Decimal(paint_count).quantize(NOPLACES)
        furn_count = Decimal(furn_count).quantize(NOPLACES)
        disc_count = Decimal(disc_count).quantize(NOPLACES)
        romsey_count = Decimal(romsey_count).quantize(NOPLACES)
        books_count = Decimal(books_count).quantize(NOPLACES)

        sales_total = hw_total + paint_total + furn_total + disc_total + romsey_total + books_total;      
      
        cash = cash.quantize(TWOPLACES)
        card = card.quantize(TWOPLACES) 
        cheque = cheque.quantize(TWOPLACES)
        bacs = bacs.quantize(TWOPLACES) 
        internet = internet.quantize(TWOPLACES)  

        payment_total = cash+card+cheque+bacs+internet;

        correction = 0
        if (payment_total != sales_total):
            correction = payment_total-sales_total 
        correction = Decimal(correction).quantize(TWOPLACES)  
        h = hashlib.md5()
        
        h.update (str(sales_total))
        h.update (str(payment_total))
        h.update (str(this_day))
        newhash = h.hexdigest()

        #/* get current saved sum */
        f = open("/home/pi/ron_python/vendpi.hash", 'r')
        currhash = f.readline()
        f.close()  
    
        #/* check if hashcodes are the same */
        logit ("check hash")
        if (currhash == newhash):
            logit ("hash codes match .. no database update")
            send_update = 0 
        else:
            logit ("hash code mismatch .. updating database")
            send_update = 1
            
        # for now always send update    
        logit ("Always sending update")
        send_update = 1 
        
        if (send_update == 1):
        
            # write new hash to file
            f = open("/home/pi/ron_python/vendpi.hash", 'w')
            f.truncate()
            f.write(newhash)
            f.close()  
    
            adate = single_date.strftime("%Y-%m-%d")
            atime = single_date.strftime("%H:%M:%S")
            aday = single_date.strftime("%A")

            #update google sheet (Winchester Sales)
            adate = single_date.strftime("%d/%m/%Y")
            creation_date = datetime.now().strftime("%d/%m/%Y")
            creation_time = datetime.now().strftime("%H:%M:%S")
        
            mystr = SHOPURL + "/wp-json/doUpdateSheet"
            mystr = mystr + "?db_date="          + str(adate);
            mystr = mystr + "&db_day="           + str(aday);
            mystr = mystr + "&db_furn_total="    + str(furn_total);
            mystr = mystr + "&db_hw_total="      + str(hw_total);
            mystr = mystr + "&db_paint_total="   + str(paint_total);
            mystr = mystr + "&db_disc_total="    + str(disc_total);
            mystr = mystr + "&db_romsey_total="  + str(romsey_total);
            mystr = mystr + "&db_books_total="   + str(books_total);
            mystr = mystr + "&db_sales_total="   + str(sales_total);  
            mystr = mystr + "&db_cash="          + str(cash);
            mystr = mystr + "&db_card="          + str(card);
            mystr = mystr + "&db_cheque="        + str(cheque);
            mystr = mystr + "&db_bacs="          + str(bacs); 
            mystr = mystr + "&db_internet="      + str(internet); 
            mystr = mystr + "&db_payment_total=" + str(payment_total); 
            mystr = mystr + "&db_correction="    + str(correction); 
            mystr = mystr + "&db_adate="         + str(creation_date);
            mystr = mystr + "&db_atime="         + str(creation_time);
            mystr = mystr + "&db_key=020380" 

            logit ("sending update sheet request to server")

            r = requests.get(mystr)  
            if (r.status_code != 200):
                logit ( "ERROR : Bad status updating sheet, code " + str(r.status_code))
                return (1)
        
            result = r.json();    
            if (result['success'] == False):
                logit ("ERROR : " + result['msg'])
            else:
                logit ("Google sheet updated")
        
            # write to shop database
            adate = single_date.strftime("%Y-%m-%d")
            
            mysql = SHOPURL + "/wp-json/doSQL?db_sql="
            mysql = mysql + "DELETE FROM shop_vend WHERE date = '" + adate + "'";
            mysql = mysql + "&db_key=020380" 
        
            logit (  "sending SQL Delete request to server")

            r = requests.get(mysql)  
            if (r.status_code != 200):
                logit (  "ERROR on SQL DELETE vend data to DB code " + str(r.status_code))
            else:
                mysql = SHOPURL + "/wp-json/doSQL?db_sql="
                mysql = mysql + "INSERT INTO shop_vend (date, day, furn_sales, hw_sales, paint_sales, discount_sales, romsey_sales, books_sales, total_sales, " 
                mysql = mysql + "cash_payments, card_payments, cheque_payments, bacs_payments, internet_payments, total_payments, correction, creation_date, creation_time)" 
            
                # send insert request to server
                mysql = mysql + " VALUE(";          
                mysql = mysql + "'" + str(adate)              + "', "
                mysql = mysql + "'" + str(aday)               + "', "
                mysql = mysql + "'" + str(furn_total)         + "', "
                mysql = mysql + "'" + str(hw_total)           + "', "
                mysql = mysql + "'" + str(paint_total)        + "', "
                mysql = mysql + "'" + str(disc_total)         + "', "
                mysql = mysql + "'" + str(romsey_total)       + "', "
                mysql = mysql + "'" + str(books_total)        + "', "
                mysql = mysql + "'" + str(sales_total)        + "', "
                mysql = mysql + "'" + str(cash)               + "', "
                mysql = mysql + "'" + str(card)               + "', "
                mysql = mysql + "'" + str(cheque)             + "', "
                mysql = mysql + "'" + str(bacs)               + "', "
                mysql = mysql + "'" + str(internet)           + "', "
                mysql = mysql + "'" + str(payment_total)      + "', "
                mysql = mysql + "'" + str(correction)         + "', ";
                mysql = mysql + "'" + str(adate)              + "', ";
                mysql = mysql + "'" + str(atime)              + "')";
                mysql = mysql + "&db_key=020380" 
        
                logit (  "sending SQL Insert request to server")
        
                headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
                }        
        
                r = requests.get(mysql)  
                if (r.status_code != 200):
                    logit (  "ERROR on SQL INSERT vend data to DB code " + str(r.status_code))
                logit (r)    
            pass
            
            # write new hash to file 
            f = open("/home/pi/ron_python/vendpi.hash", 'w')
            f.truncate()
            f.write(newhash)
            f.close()  
        pass
        
     	# open up a link to the google spreadsheet
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/ron_python/Shop wvend-5c522b3b4a70.json', scope)
        gc = gspread.authorize(credentials)
        sh = gc.open("Shop wvend") 
        wsh = sh.worksheet("shop_vend")
    
        # get the index (currently written line)
        ix = wsh.cell(1,1).value
     
     	# get the current date from the index line
        curdate = wsh.cell(ix,1).value
    
        # if different, then step the line 
    	if curdate != adate:
    		ix = ix + 1
    		wsh.update_cell(1,1, ix)
    
        # Select a range
        cell_list = wsh.range('A' + ix + ':R' + ix)
     
        cell_list[0].value = str(adate)               
        cell_list[1].value = str(aday)               
        cell_list[2].value = str(furn_total)         
        cell_list[3].value = str(hw_total)            
        cell_list[4].value = str(paint_total)       
        cell_list[5].value = str(disc_total)          
        cell_list[6].value = str(romsey_total)       
        cell_list[7].value = str(books_total)         
        cell_list[8].value = str(sales_total)       
        cell_list[9].value = str(cash)               
        cell_list[10].value = str(card)                
        cell_list[11].value = str(cheque)             
        cell_list[12].value = str(bacs)               
        cell_list[13].value = str(internet)           
        cell_list[14].value = str(payment_total)      
        cell_list[15].value = str(correction)         
        cell_list[16].value = str(adate)              
        cell_list[17].value = str(atime)                 

        # Update in batch
        wsh.update_cells(cell_list);
    
        
    return 0

#****************************
def do_andy_fd ():
#****************************     
           
    global driver
     
    # first send database update to indicate that update has started
    
    #update google sheet 
    update_cells = ""
    update_values = ""
    
    the_date = datetime.now().strftime("%d/%m/%Y")
    the_time = datetime.now().strftime("%H:%M:%S")
    the_day  = datetime.now().strftime("%A")
    
    s = "Updating Andy FD at " + the_time + " on " + the_day + " " + the_date
    
    update_cells = update_cells + "A1" 
    update_values = update_values + s

    s = "Balance = ????" 
    
    update_cells = update_cells + "!"
    update_values = update_values + "!" 
    update_cells = update_cells + "A2" 
    update_values = update_values + s
    
     
    s = "Available = ????" 
    
    update_cells = update_cells + "!"
    update_values = update_values + "!" 
    update_cells = update_cells + "A3" 
    update_values = update_values + s
    
    s = "Pending = ????" 
    
    update_cells = update_cells + "!"
    update_values = update_values + "!" 
    update_cells = update_cells + "A4" 
    update_values = update_values + s
    
    s = "Calc Balance = ????" 
    
    update_cells = update_cells + "!"
    update_values = update_values + "!" 
    update_cells = update_cells + "A5" 
    update_values = update_values + s
    
    s = "Calc Balance O/D = ????" 
    
    update_cells = update_cells + "!"
    update_values = update_values + "!" 
    update_cells = update_cells + "A6" 
    update_values = update_values + s
      
    mystr = SHOPURL + "/wp-json/UpdateGoogleSheet"
    mystr = mystr + "?db_appname="   + str("Update Summary Sheet");
    mystr = mystr + "&db_ssname="    + str("Andy Accounts");
    mystr = mystr + "&db_sheetname=" + str("First Direct");
    mystr = mystr + "&db_cred="      + str("rons-credentials.json");
    mystr = mystr + "&db_cell="      + update_cells;
    mystr = mystr + "&db_value="     + update_values;
    mystr = mystr + "&db_key=020380";

    logit ("sending update Andy sheet request to server")

    r = requests.get(mystr)  
    if (r.status_code != 200):
        logit ( "ERROR : Bad status updating sheet, code " + str(r.status_code))
    else:
        result = r.json();    
        if (result['success'] == False):
            logit ("ERROR : " + result['msg'])
        else:
            logit ("Google sheet updated")
    
    try:
        logit ('opening ' + ANDYFD_URI)
        driver.get(ANDYFD_URI) 
    except: 
        logit ('andy_fd driver.get failed')
        return -1
    
    # Enter userid
    element,rc = getxpath ('Internet Banking', '//*[@id="fd_head_pib"]')
    if rc == -1:
        return -1
        
    logit ('Click Internet banking') 
    rc = doclick ('Click Internet banking', element)   
    if rc == -1:
        return -1
    
     # Wait for new window to become available
    logit ("waiting for new window")
    count = 0
    while True:
        logit ("try for new window")
        try:            
            for handle in driver.window_handles:
                driver.switch_to_window(handle)
            logit ("got new window")
            break;
        except:
            logit ("exception")
            count = count + 1
            mysleep(1)
            
        if count >= 50:
            logit ("ERROR: New window not found")
            driver.quit()
            return (-1)    
    pass    
     
    logit ("Waiting for Internet banking or Maintenance screen")
    count = 0
    while True:
        # look for main internet banking screen
        try:
            logit ("test for main internet")
            element, rc = waitxpath ('//*[@id="csMain"]/div[3]/div[2]/div/div/h1', 1)
             
            # enter userid found .. proceed
            if rc != -1:
                logit ("Main Internet screen found - click and break")
                rc = doclick("Main Screen Click", element);
                if rc == -1:
                    return -1
                break
        except:
            pass    
            
        # look for maintenance screen
        try:
            logit ("test for maintenance");
            element, rc = waitxpath ('//*[@id="grid"]/div/div/p[5]/strong/a/span/span/span', 1)
            
            # maintenance screen found .. click
            if rc != -1:
                logit ("Maintenance screen found")
                rc = doclick("Maintenance Screen Click", element);
                if rc == -1:
                    return -1
                count = 0;
        except:
            pass
            
        # look for marketing screen
        try:
            logit ("test for marketing screen")
            element, rc = waitxpath ('//*[@id="grid"]/div/div/a/img', 1)
            
            # maintenance screen found .. click
            if rc != -1:
                logit ("Marketing screen found - click and break")
                rc = doclick("Marketing Screen Click", element);
                if rc == -1:
                    return -1
                break;
        except:
            pass    
    
        count = count + 1
        mysleep(1)  
        
        if count >= 50:
            logit ("ERROR: Internet banking, Marketing or Maintenance screen not found")
            driver.quit()
            return (-1)
      
    # Resize the window to the screen width/height
    driver.set_window_size(1000, 1500)

    # Move the window to position x/y
    driver.set_window_position(0, 0)

    # wait for userid screen 
    logit ("Find & Enter Userid")    
    element, rc = waitxpath ('//*[@id="userid1"]', 30)
    if rc == -1:
        return -1
    element.send_keys(ANDYFD_ID)
       
    # find and click proceed  
    element,rc = getxpath ('Proceed', '//*[@id="viewns_7_I0881101HGU0D0IN12V4RN0047_:_idJsp9ns_7_I0881101HGU0D0IN12V4RN0047_:proceed-nav"]' )
    if rc == -1:
        return -1
        
    rc = doclick("Proceed", element);
    if rc == -1:
        return -1
     
    # wait for 'no digital secure key' and click
    element,rc = getxpath ('No Secure Key', '//*[@id="viewns_7_I0881101HG6V70A0BP2DAA10G2_:inputForm"]/div[1]/div[2]/div/p/a');
    if rc == -1:
        return -1
        
    rc = doclick(" No Secure Key", element);
    if rc == -1:
        return -1
     
    # wait for memorable info screen 
    logit ("Find & Get memorable info sentence")
    element,rc = getxpath ('Mem Info', '//*[@id="viewns_7_I0881101HGU0D0IN12V4RN00K6_:_idJsp19ns_7_I0881101HGU0D0IN12V4RN00K6_"]/p[2]')
    if rc == -1:
        return -1

    # get text saying which characters are needed
    s = element.text
    
    n1 = s.find (" 1st,")
    if n1 != -1:
        n1 = 1
    else:
        n1 = s.find (" 2nd,")
        if n1 != -1:
            n1 = 2
        else:    
            n1 = s.find (" 3rd,") 
            if n1 != -1:
                n1 = 3
            else:   
                n1 = s.find (" 4th,") 
                if n1 != -1:
                    n1 = 4
                else:
                    n1 = s.find (" 5th,") 
                    if n1 != -1:
                        n1 = 5
                    else:
                        n1 = s.find (" 6th,") 
                        if n1 != -1:
                            n1 = 6  
                
    n2 = s.find (", 2nd ")
    if n2 != -1:
        n2 = 2
    else:   
        n2 = s.find (", 3rd ")
        if n2 != -1:
            n2 = 3
        else:   
            n2 = s.find (", 4th ") 
            if n2 != -1:
                n2 = 4
            else:   
                n2 = s.find (", 5th ") 
                if n2 != -1:
                    n2 = 5
                else:   
                    n2 = s.find (", 6th ") 
                    if n2 != -1:
                        n2 = 6
                    else:    
                        n2 = s.find (", penultimate ") 
                        if n2 != -1:
                            n2 = 7    
                
    n3 = s.find ("and 3rd")
    if n3 != -1:
        n3 = 3
    else:   
        n3 = s.find ("and 4th")
        if n3 != -1:
            n3 = 4
        else:   
            n3 = s.find ("and 5th") 
            if n3 != -1:
                n3 = 5
            else:   
                n3 = s.find ("and 6th")             
                if n3 != -1:
                    n3 = 6
                else:    
                    n3 = s.find ("and penultimate ") 
                    if n3 != -1:
                        n3 = 7  
                    else:    
                        n3 = s.find ("and Last ") 
                        if n3 != -1:
                            n3 = 8        
    
    if n1 == -1 or n2 == -1 or n3 == -1:
        logit ("Could not parse first direct string")
        logit (s)         
        logit (n1)
        logit (n2)
        logit (n3)
        sys.exit()
    
    memdata =  (ANDYFD_PW)
    
    # memorable data character 1
    element,rc = getxpath ('Meminfo Char 1', '//*[@id="keyrcc_password_first"]')
    if rc == -1:
        return -1
    element.send_keys(memdata[n1-1])
    
    # memorable data character 2
    element,rc = getxpath ('Meminfo Char 2','//*[@id="keyrcc_password_second"]')
    if rc == -1:
        return -1
    element.send_keys(memdata[n2-1])
    
    # memorable data character 2
    element,rc = getxpath ('Meminfo Char 3','//*[@id="keyrcc_password_third"]')
    if rc == -1:
        return -1
    element.send_keys(memdata[n3-1])
    
    # memorable data
    element,rc = getxpath ('Memorable Word', '//*[@id="memorableAnswer"]')
    if rc == -1:
        return -1
    element.send_keys(ANDYFD_MEMINFO)
    
    # find and click proceed
    element,rc = getxpath ('Proceed', '//*[@id="viewns_7_I0881101HGU0D0IN12V4RN00K6_:_idJsp19ns_7_I0881101HGU0D0IN12V4RN00K6_:proceed-nav"]')
    if rc == -1:
        return -1
        
    rc = doclick("Proceed", element);
    if rc == -1:
        return -1
    
    # find and click account name  
    element,rc = getxpath ('Account Name', '//*[@id="vcpost10"]/a')
    if rc == -1:
        return -1
        
    rc = doclick("Account Name", element);
    if rc == -1:
        return -1
    
    # wait for statement
    element,rc = getxpath ('Statement', '//*[@id="ulv1"]/table[1]/tbody/tr[1]/td/h1')
    if rc == -1:
        return -1
    
    # save screenshot
    logit ("Saving statement screenshot") 
    save_screenshot("statement")
    
    # find and click payments
    element,rc = getxpath ('Payments', '//*[@id="link2"]')
    if rc == -1:
        return -1
        
    rc = doclick("Payments", element);
    if rc == -1:
        return -1

    # find and click pay a bill
    element,rc = getxpath ('Pay a Bill', '//*[@id="link2,0"]')
    if rc == -1:
        return -1
        
    rc = doclick("Pay a bill", element);
    if rc == -1:
        return -1
 
    # find and click account
    element,rc = getxpath ('Account 7', '//*[@id="viewns_7_H2A01KS0HGJO00INBL992B1041_:accountSelectionForm:selectaccountdropdown-option"]')
    if rc == -1:
        return -1
    element.send_keys("7")

    # find and click proceed
    logit ("Find & Click proceed")
    element,rc = getxpath ('Proceed2', '//*[@id="viewns_7_H2A01KS0HGJO00INBL992B1041_:accountSelectionForm:go-nav"]')
    if rc == -1:
        return -1
        
    rc = doclick("Proceed2", element);
    if rc == -1:
        return -1

    # find balance
    logit ("Find & Get balance") 
    element,rc = getxpath ('Balance', '//*[@id="viewns_7_H2A01KS0HGJO00INBL992B10O0_:destinationListPage:_idJsp12ns_7_H2A01KS0HGJO00INBL992B10O0_:tbody_element"]/tr[2]/td[2]')
    if rc == -1:
        return -1
    curr_bal = element.text
    
    # correctly format available
    curr_bal = curr_bal.replace(u"\xA3",'')
    curr_bal = curr_bal.replace(',','')
    
    curr_bal_last2 = curr_bal[-2:]
    curr_bal = curr_bal[:-2]
    curr_bal = Decimal(curr_bal).quantize(TWOPLACES)
    if curr_bal_last2 == " D":
        curr_bal = -curr_bal
    else:
        logit ("Unexpected curr_bal_last2 : " + str(curr_bal_last2)) 
    logit ("Andy FD Balance: " + str(curr_bal))
    
    # find available
    element,rc = getxpath ('Available', '//*[@id="viewns_7_H2A01KS0HGJO00INBL992B10O0_:destinationListPage:_idJsp12ns_7_H2A01KS0HGJO00INBL992B10O0_:tbody_element"]/tr[3]/td[2]')
    if rc == -1:
        return -1
    curr_avail =  element.text
    
    # correctly format available
    curr_avail = curr_avail.replace(u"\xA3",'')
    curr_avail = curr_avail.replace(',','')
    curr_avail = Decimal(curr_avail).quantize(TWOPLACES)
    logit ("Andy FD Available: " + str(curr_avail))

    # Wit/click logout
    element,rc = getxpath ('Logout', '//*[@id="fdMastheadDiv"]/div[2]/div/div/a')
    if rc == -1:
        return -1
        
    rc = doclick("Pay a bill", element);
    if rc == -1:
        return -1

    # get last saved balances 
    f = open("/home/pi/ron_python/balances.dat", 'r')
    prev_bal = f.readline()
    prev_bal = prev_bal[:-1]
    prev_avail = f.readline()
    prev_avail = prev_avail[:-1]
    f.close()  
    
    try:
        prev_bal = Decimal(prev_bal).quantize(TWOPLACES)
        prev_avail = Decimal(prev_avail).quantize(TWOPLACES)
    except:
        prev_bal = 0
        prev_avail = 0
    
    prev_pending = prev_bal + 500 - prev_avail
    curr_pending = curr_bal + 500 - curr_avail
    
    #update google sheet 
    update_cells = ""
    update_values = ""
    
    the_date = datetime.now().strftime("%d/%m/%Y")
    the_time = datetime.now().strftime("%H:%M:%S")
    the_day  = datetime.now().strftime("%A")
    
    s = "Updated at " + the_time + " on " + the_day + " " + the_date
    
    update_cells = update_cells + "A1" 
    update_values = update_values + s

    s = "Balance = " + do_format(curr_bal) 
    
    update_cells = update_cells + "!"
    update_values = update_values + "!" 
    update_cells = update_cells + "A2" 
    update_values = update_values + s
    
     
    s = "Available = " + do_format(curr_avail) 
    
    update_cells = update_cells + "!"
    update_values = update_values + "!" 
    update_cells = update_cells + "A3" 
    update_values = update_values + s
    
    s = "Pending = " + do_format(curr_pending) 
    
    update_cells = update_cells + "!"
    update_values = update_values + "!" 
    update_cells = update_cells + "A4" 
    update_values = update_values + s
    
    s = "Calc Balance = " + do_format(curr_bal-curr_pending) 
    
    update_cells = update_cells + "!"
    update_values = update_values + "!" 
    update_cells = update_cells + "A5" 
    update_values = update_values + s
    
    s = "Calc Balance O/D = " + do_format(500 + curr_bal - curr_pending) 
    
    update_cells = update_cells + "!"
    update_values = update_values + "!" 
    update_cells = update_cells + "A6" 
    update_values = update_values + s
    
    mystr = SHOPURL + "/wp-json/UpdateGoogleSheet"
    mystr = mystr + "?db_appname="   + str("Update Summary Sheet");
    mystr = mystr + "&db_ssname="    + str("Andy Accounts");
    mystr = mystr + "&db_sheetname=" + str("First Direct");
    mystr = mystr + "&db_cred="      + str("rons-credentials.json");
    mystr = mystr + "&db_cell="      + update_cells;
    mystr = mystr + "&db_value="     + update_values;
    mystr = mystr + "&db_key=020380";

    logit ("sending update sheet request to server")

    r = requests.get(mystr)  
    if (r.status_code != 200):
        logit ( "ERROR : Bad status updating sheet, code " + str(r.status_code))
    else:
        result = r.json();    
        if (result['success'] == False):
            logit ("ERROR : " + result['msg'])
        else:
            logit ("Google sheet updated")
     
    # check for change
    if ((prev_bal!=curr_bal) or (prev_avail!=curr_avail)):
        logit ("Balances mismatch")
        logit (">>" + str(prev_bal) + "<< >>" + str(curr_bal) + "<<")
        logit (">>" + str(prev_avail) + "<< >>" + str(curr_avail) + "<<")
    else:
        logit ("Balances are equal")
        logit (">>" + str(prev_bal) + "<< >>" + str(curr_bal) + "<<")
        logit (">>" + str(prev_avail) + "<< >>" + str(curr_avail) + "<<")
        return 0
    
    # mismatch write new balances to file 
    f = open("/home/pi/ron_python/balances.dat", 'w')
    f.write(str(curr_bal))
    f.write("\n")
    f.write(str(curr_avail))
    f.write("\n")
    f.close()  
    
    # get time and date
    sdate = datetime.now().strftime("%d %b %Y").lstrip ('0')
    date = datetime.now().strftime("%d %B %Y")
    day = datetime.now().strftime("%a")
    longday = datetime.now().strftime("%A")
    d = datetime.now() - timedelta(days=6)
    date_week_ago = d.strftime("%d %B %Y")
    date_jan1 = datetime.now().strftime("01 January %Y")
    date_mon1 = datetime.now().strftime("01 %B %Y")
    timenow = time.strftime("%H:%M")
    day_of_year = datetime.now().timetuple().tm_yday
    day_of_month = datetime.today().day
    
    # send email
    subject = 'Andy FD Change ' + timenow + ' on ' + longday + ' ' + sdate
    sender = RB_EMAIL_USERNAME
    
    # Send to me
    recipient = 'ron.bowater@gmail.com'
    logit ("Sending email to " + recipient)  
    
    # Credentials 
    username = RB_EMAIL_USERNAME
    password = RB_EMAIL_PASSWORD

    Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')
    
    multipart = MIMEMultipart()
    multipart['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
    multipart['To'] = Header(recipient.encode('utf-8'), 'UTF-8').encode()
    
    if CC_MARY == 1:
        cc_recipient = 'maryrobinson1@gmail.com'
        multipart['Cc'] = Header(cc_recipient.encode('utf-8'), 'UTF-8').encode()
    
    multipart['From'] = Header(sender.encode('utf-8'), 'UTF-8').encode()
    
    htmltext = '<html><head></head><body><pre style="font: monospace">' 
    if (prev_bal!=curr_bal):
        if (prev_bal > curr_bal):
            htmltext = htmltext + "Balance decreased from " + do_format(prev_bal) + " to " + do_format(curr_bal) + " by " + do_format(curr_bal-prev_bal) + "<br>"
        else:
            htmltext = htmltext + "Balance increased from " + do_format(prev_bal) + " to " + do_format(curr_bal) + " by " + do_format(prev_bal-curr_bal) + "<br>"
    else:
        htmltext = htmltext + "Balance is unchanged at " + do_format(curr_bal) + "<br>"
        
    if (prev_avail!= curr_avail):
        if (prev_avail > curr_avail):
            htmltext = htmltext + "Available decreased from " + do_format(prev_avail) + " to " + do_format(curr_avail)  + " by " + do_format(prev_avail-curr_avail) + "<br>" 
        else:
            htmltext = htmltext + "Available increased from " + do_format(prev_avail) + " to " + do_format(curr_avail)  + " by " + do_format(curr_avail-prev_avail) + "<br>"
    else:
        htmltext = htmltext + "Available is unchanged at " + do_format(curr_avail)  +"<br>"
        
    if (prev_pending!= curr_pending):
        if (prev_pending > curr_pending):
            htmltext = htmltext + "Pending decreased from " + do_format(prev_pending) + " to " + do_format(curr_pending)  + " by " + do_format(prev_pending-curr_pending) + "<br>" 
        else:
            htmltext = htmltext + "Pending increased from " + do_format(prev_pending) + " to " + do_format(curr_pending)  + " by " + do_format(curr_pending-prev_pending) + "<br>"
    else:
        htmltext = htmltext + "Pending is unchanged at " + do_format(curr_pending) + "<br>"
    
    calc_balance = curr_bal-curr_pending
    htmltext = htmltext + "Calculated balance = " + do_format(calc_balance) + "<br>"
    
    calc_balance_od = 500 + calc_balance;

    htmltext = htmltext + "Calculated balance O/D = " + do_format(calc_balance_od) + "<br>"
    
    htmltext = htmltext + "</pre></body></html>"
    
    htmlpart = MIMEText(htmltext.encode('utf-8'), 'html', 'UTF-8')
    multipart.attach(htmlpart)
     
    ImgFileName = '/home/pi/ron_python/statement.png'
    fp = open(ImgFileName, 'rb');
    imagepart = MIMEImage(fp.read())
    fp.close();
    imagepart.add_header('Content-Disposition', 'attachment; filename=screenie.png')
    multipart.attach(imagepart)
    
    io = StringIO()
    g = Generator(io, False)  
    g.flatten(multipart)
  
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.ehlo
    server.login(username,password)
    server.sendmail(sender, recipient, io.getvalue())
    server.quit()
  
    '''  
    # Send to Andy
    recipient = 'andy.bowater@gmail.com'
    logit ("Sending email to " + recipient)  
       
    # Credentials 
    username = RB_EMAIL_USERNAME
    password = RB_EMAIL_PASSWORD

    Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')
    multipart = MIMEMultipart('alternative')
    multipart['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
    multipart['To'] = Header(recipient.encode('utf-8'), 'UTF-8').encode()
    multipart['From'] = Header(sender.encode('utf-8'), 'UTF-8').encode()
    
    text = 'Statement changed .. balance = ' + do_format(bal)
    
    textpart = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
    multipart.attach(textpart)
     
    ImgFileName = '/home/pi/ron_python/screenie.png'
    fp = open(ImgFileName, 'rb');
    imagepart = MIMEImage(fp.read())
    fp.close();
    imagepart.add_header('Content-Disposition', 'attachment; filename=screenie.png')
    multipart.attach(imagepart)
    
    io = StringIO()
    g = Generator(io, False)  
    g.flatten(multipart)
  
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.ehlo
    server.login(username,password)
    server.sendmail(sender, recipient, io.getvalue())
    server.quit()
    '''
  
    #/* and return */
    return 0       


#************************    
def send_restart_email():
#************************   
         
    global prev_logit_string  
         
    # send email
    timenow = time.strftime("%H:%M")
    dnow = datetime.now()  
    longday = dnow.strftime("%A")
    sdate = datetime.now().strftime("%d %b %Y").lstrip ('0')
    
    subject = 'Rpi restarted ' + timenow + ' on ' + longday + ' ' + sdate
    sender = RB_EMAIL_USERNAME
       
    # Send to me
    recipient = 'ron.bowater@gmail.com'
    logit ("Sending email to " + recipient)  
    
    # Credentials 
    username = RB_EMAIL_USERNAME
    password = RB_EMAIL_PASSWORD

    Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')
    multipart = MIMEMultipart('alternative')
    multipart['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
    multipart['To'] = Header(recipient.encode('utf-8'), 'UTF-8').encode()
    multipart['From'] = Header(sender.encode('utf-8'), 'UTF-8').encode()
    
    text = 'last logit string = ' + prev_logit_string
    
    textpart = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
    multipart.attach(textpart)
     
    filename = '/home/pi/ron_python/logfile.txt'
    f = file(filename)
    attachment = MIMEText(  f.read())
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)           
    multipart.attach(attachment) 
    
    io = StringIO()  
    g = Generator(io, False)  
    g.flatten(multipart)
  
    # The actual mail send
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.ehlo
        server.login(username,password)
        server.sendmail(sender, recipient, io.getvalue())
        server.quit()
    except:
        pass
  
    #/* and return */
    return 0                 
  

#************************************************************    
def send_warning_email(s):
#************************************************************   
    
    # send email
    timenow = time.strftime("%H:%M")
    dnow = datetime.now()  
    longday = dnow.strftime("%A")
    sdate = datetime.now().strftime("%d %b %Y").lstrip ('0')
    
    subject = 'Vend problem'
    sender = RB_EMAIL_USERNAME
       
    # Send to me
    recipient = 'ron.bowater@gmail.com'
    logit ("Sending email to " + recipient)  
    
    # Credentials 
    username = RB_EMAIL_USERNAME
    password = RB_EMAIL_PASSWORD

    Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')
    multipart = MIMEMultipart('alternative')
    multipart['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
    multipart['To'] = Header(recipient.encode('utf-8'), 'UTF-8').encode()
    multipart['From'] = Header(sender.encode('utf-8'), 'UTF-8').encode()
     
    textpart = MIMEText(s.encode('utf-8'), 'plain', 'UTF-8')
    multipart.attach(textpart)
    
    io = StringIO()
    g = Generator(io, False)  
    g.flatten(multipart)
  
    # The actual mail send
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.ehlo
        server.login(username,password)
        server.sendmail(sender, recipient, io.getvalue())
        server.quit()
    except:
        logit ("email send failed")
        pass
  
    logit ("email sent")
  
    #/* and return */
    return 0                   
  
#************************************************************    
def send_cannot_access_fd_email (line1, line2, line3, line4):
#************************************************************   
         
    global prev_logit_string  
         
    # send email
    timenow = time.strftime("%H:%M")
    dnow = datetime.now()  
    longday = dnow.strftime("%A")
    sdate = datetime.now().strftime("%d %b %Y").lstrip ('0')
    
    subject = 'Cannot Access Andy FD ' + timenow + ' on ' + longday + ' ' + sdate
    sender = RB_EMAIL_USERNAME
       
    # Send to me
    recipient = 'ron.bowater@gmail.com'
    logit ("Sending email to " + recipient)  
    
    # Credentials 
    username = RB_EMAIL_USERNAME
    password = RB_EMAIL_PASSWORD

    Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')
    multipart = MIMEMultipart('alternative')
    multipart['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
    multipart['To'] = Header(recipient.encode('utf-8'), 'UTF-8').encode()
    
    if CC_MARY == 1:
        cc_recipient = 'maryrobinson1@gmail.com'
        multipart['Cc'] = Header(cc_recipient.encode('utf-8'), 'UTF-8').encode()
    
    multipart['From'] = Header(sender.encode('utf-8'), 'UTF-8').encode()
    
    text = str(line1) + '\n' + str(line2) + '\n' + str(line3) + '\n' + str(line4)
     
    textpart = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
    multipart.attach(textpart)
    
    io = StringIO()
    g = Generator(io, False)  
    g.flatten(multipart)
  
    # The actual mail send
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.ehlo
        server.login(username,password)
        server.sendmail(sender, recipient, io.getvalue())
        server.quit()
    except:
        logit ("email send failed")
        pass
  
    logit ("email sent")
  
    #/* and return */
    return 0                   
  
#****************************
def do_andy_check ():
#****************************     
       
    mystr = SHOPURL + "/wp-json/ReadGoogleSheet"
    mystr = mystr + "?db_appname="   + str("Read Andy Accounts Sheet");
    mystr = mystr + "&db_ssname="    + str("Andy Accounts");
    mystr = mystr + "&db_sheetname=" + str("First Direct");
    mystr = mystr + "&db_cred="      + str("rons-credentials.json");
    mystr = mystr + "&db_key=020380";

    logit ("sending get Andy sheet request to server")
    
    r = requests.get(mystr)  
    if (r.status_code != 200):
        logit ( "ERROR : Bad status getting sheet, code " + str(r.status_code))
    else:
        result = r.json();    
        if (result['success'] == False):
            logit ("ERROR : " + result['msg'])
        else:
            logit ("Andy account sheet fetched")
            
    data = result['data']
    for line in data:
        if line[0] == 'A1':
            line1 = line[1]
        elif line[0] == 'A2':
            line2 = line[1]
        elif line[0] == 'A3':
            line3 = line[1]
        elif line[0] == 'A4':
            line4 = line[1]
     
    line2 = line2.replace(u"\xA3",'')
    line3 = line3.replace(u"\xA3",'')  
    line4 = line4.replace(u"\xA3",'')       

    print line1
    print line2
    print line3
    print line4

    # send email if not updated
    if (line1 == "Balance = ????"):
        logit ("Cannot access FD account ... sending email")
        send_cannot_access_fd_email(line1, line2, line3, line4)
    else:
        logit ("Able to access FD account ... email not sent")
    
    return  
 
#****************************
def do_vend_signout ():
#****************************      
 
    # sign out 
    logit ( "looking for signoff .. sleeping 30 secs")
    
    mysleep (30)
    
    mytrace(11)
    element, rc = waitxpath ('//*[@id="home"]/vv-navigation/div/nav[1]/ul/ng-transclude/li[6]/a/span', 30)
    mytrace(22)
    if rc == -1:
        mytrace(33)
        logit ("***** Signoff (home) not found")
        element, rc = waitxpath ('//*[@id="register"]/vv-navigation/div/nav[1]/ul/ng-transclude/li[6]/a/span', 30)
        if rc == -1:
            logit ("***** Signoff (register or home) not found")
            save_screenshot("vend_signoff_not_found")
            return -1
        else:
            logit ("***** Signoff (register) found")    
    else:
        mytrace(44)
        logit ("***** Signoff (home) found")    

    mytrace(55)
    mysleep(10)
    mytrace(66)
    logit (  "clicking signout")
    element.click()   
    mysleep (10)
    
    # return
    return 0       

#**************************    
def notify_new_error(name):
#**************************   
 
    # get times
    timenow = time.strftime("%H:%M")
    dnow = datetime.now()  
    longday = dnow.strftime("%A")
    sdate = datetime.now().strftime("%d %b %Y").lstrip ('0')
    
    subject = name + 'Access error ' + timenow + ' on ' + longday + ' ' + sdate
    sender = RB_EMAIL_USERNAME
       
    # Send to me
    recipient = 'ron.bowater@gmail.com'
    logit ("Sending email to " + recipient)  
    
    # Credentials 
    username = RB_EMAIL_USERNAME
    password = RB_EMAIL_PASSWORD

    Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')
    multipart = MIMEMultipart('alternative')
    multipart['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
    multipart['To'] = Header(recipient.encode('utf-8'), 'UTF-8').encode()
    
    if CC_MARY == 1:
        cc_recipient = 'maryrobinson1@gmail.com'
        multipart['Cc'] = Header(cc_recipient.encode('utf-8'), 'UTF-8').encode()
    
    multipart['From'] = Header(sender.encode('utf-8'), 'UTF-8').encode()
    
    log_filename = '/home/pi/ron_python/logfile.txt'
    fp = open(log_filename, 'r');
    text = fp.read()
    fp.close();
     
    textpart = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
    multipart.attach(textpart)
    
    io = StringIO()
    g = Generator(io, False)  
    g.flatten(multipart)
  
    # The actual mail send
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.ehlo
        server.login(username,password)
        server.sendmail(sender, recipient, io.getvalue())
        server.quit()
    except:
        logit ("email send failed")
        pass
  
    logit ("email sent")
  
    return;    
    
#********************************    
def notify_recovered_error(name):
#********************************    

    # get times
    timenow = time.strftime("%H:%M")
    dnow = datetime.now()  
    longday = dnow.strftime("%A")
    sdate = datetime.now().strftime("%d %b %Y").lstrip ('0')
    
    subject = name + 'Access recovered ' + timenow + ' on ' + longday + ' ' + sdate
    sender = RB_EMAIL_USERNAME
       
    # Send to me
    recipient = 'ron.bowater@gmail.com'
    logit ("Sending email to " + recipient)  
    
    # Credentials 
    username = RB_EMAIL_USERNAME
    password = RB_EMAIL_PASSWORD

    Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')
    multipart = MIMEMultipart('alternative')
    multipart['Subject'] = Header(subject.encode('utf-8'), 'UTF-8').encode()
    multipart['To'] = Header(recipient.encode('utf-8'), 'UTF-8').encode()
    
    if CC_MARY == 1:
        cc_recipient = 'maryrobinson1@gmail.com'
        multipart['Cc'] = Header(cc_recipient.encode('utf-8'), 'UTF-8').encode()
    
    multipart['From'] = Header(sender.encode('utf-8'), 'UTF-8').encode()
    
    text = "No text"
     
    textpart = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
    multipart.attach(textpart)
    
    io = StringIO()
    g = Generator(io, False)  
    g.flatten(multipart)
  
    # The actual mail send
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.ehlo
        server.login(username,password)
        server.sendmail(sender, recipient, io.getvalue())
        server.quit()
    except:
        logit ("email send failed")
        pass
  
    logit ("email sent")
  
    return;    
    
#************
def run_loop():  
#************
      
    global testing
   
    logit ("Waiting for time triggers to send email..")
    
    timeflag = 0
    rebootflag = 0
    old_min = 999;
    while True:
        
        this_hour = int(time.strftime("%H"))
        this_min = int(time.strftime("%M"))
        this_time = time.strftime("%H:%M:%S")
        this_date = datetime.now().strftime("%d %B %Y")
        this_day = datetime.now().strftime("%A")
        
        if old_min != this_min:
            old_min=this_min; 
            logit ("min = " + str(this_min))
            pass

        # reboot on the hour
        if ((this_min == 58) and (rebootflag == 0)):
            logit ('Arming reboot trigger')
            rebootflag = 1
            pass
            
        if ((this_min == 59) and (rebootflag == 1)):
            logit ('Reboot Triggered')
            os.system ("sudo reboot"); 
            pass   

        # do vend on quarter past and to the hour
        if (((this_min == 14) and (timeflag == 0)) or ((this_min == 44) and (timeflag == 0))):
            logit ('Arming Vend trigger')
            timeflag = 1
            pass
           
        if (((this_min == 15) and (timeflag == 1)) or ((this_min == 45) and (timeflag == 1))):
            logit ('Vend triggered')
            timeflag = 0
            count = 0;
            while count<10:
             logit ("Starting do_vend count" + str(count))
             start_webdriver();
             rc = do_vend();
             stop_webdriver();
             logit ("do_vend return rc=" + str(rc))
             if rc==0:
              break;
             count = count + 1
            if ((rc==-1) and (test_flag("venderr")==0)):
                set_flag ("venderr");
                notify_new_error("Vend")
            if ((rc==0) and (test_flag("venderr")==1)):
                clear_flag ("venderr")
                notify_recovered_error("Vend")
            pass
            
        # do andy fd at half past the hour    
        if ((this_min == 29) and (timeflag == 0)):
            if (do_andy_fd == 1):
                logit ('Arming Andy trigger')
                timeflag = 1
            pass
            
        if ((this_min == 30)and (timeflag == 1)):
            logit ('Andy triggered')
            timeflag = 0
            logit ("Starting do_andy_fd")
            start_webdriver()
            rc = do_andy_fd()
            stop_webdriver()
            logit ("do_andy_fd return rc=" + str(rc))
            if ((rc==-1) and (test_flag("andyerr")==0)):
                notify_new_error("Andy FD")
            if ((rc==0) and (test_flag("andyderr")==1)):
                clear_flag ("andyerr")
                notify_recovered_error("Andy FD")
            pass    
            
        if ((this_min == 39) and (timeflag == 0)):
            if (do_andy_fd == 1):
                logit ('Arming Andy check trigger')
                timeflag = 1
            pass
            
        if ((this_min == 40) and (timeflag == 1)):
            logit ('Andy check triggered')
            timeflag = 0
            do_andy_check()   
            pass
                
        time.sleep(10)
    #end while
#end def run_loop         
  
#********************
def stop_webdriver():  
#********************  
       
    global driver
    
    logit ("stop_webdriver entry")
    
    # kill chromedriver 
    os.system("ps -ef | grep chromedriver | grep -v grep | awk '{print $2}' >chromedriver.pid")
    statinfo = os.stat('chromedriver.pid')
    if (statinfo.st_size !=0):
        logit ("killing chromedriver process(es)")
        os.system("ps -ef | grep chromedriver | grep -v grep | awk '{print $2}' | xargs sudo kill -9 2>/dev/null >/dev/null")
        
    # kill chrome browser
    os.system("ps -ef | grep chromium | grep -v grep | awk '{print $2}' >chromium.pid")
    statinfo = os.stat('chromium.pid')
    if (statinfo.st_size !=0):
        logit ("killing chromium process(es)")
        os.system("ps -ef | grep chromium | grep -v grep | awk '{print $2}' | xargs sudo kill -9 2>/dev/null >/dev/null")
  
    # kill Xvfb 
    os.system("ps -ef | grep Xvfb | grep -v grep | awk '{print $2}' >xvfb.pid")
    statinfo = os.stat('xvfb.pid')
    if (statinfo.st_size !=0):
        logit ("killing xvfb process(es)")
        os.system("ps -ef | grep Xvfb | grep -v grep | awk '{print $2}' | xargs sudo kill -9 2>/dev/null >/dev/null")
  
    #cleanup /tmp
    os.system ("sudo rm -rf /tmp/tmp*");
    
    logit ("stop_webdriver exit")

  
#*********************
def start_webdriver():
#*********************

    global driver
    
    logit ("start_webdriver entry")

    # kill webdriver if it exists
    logit ("Stopping webdriver and xvfb")
    stop_webdriver()
  
    logit ("Starting xvfb display") 
    display = Display(visible=0, size=(1024,800))
    display.start()
    
    logit ("Starting chrome webdriver")
    try:
        driver = webdriver.Chrome()
    except Exception as e:
        s = str(e)
        logit ("Exception : " + s )
        sys.exit()

    logit ("Webdriver is up and running")
    logit ("start_webdriver exit")

    return
          
#*****************
def do_main(argv):
#*****************
   
    global driver
    global test_vend
    global test_andy_fd  
    global test_andy_check 
    global test_run
      
    test_vend = 0
    test_andy_fd = 0
    test_andy_check = 0
    test_run = 0
    real_run = 0
 
    # process args    
    try:
        opts, args = getopt.getopt(argv,"vactrh")
    except getopt.GetoptError:
        print ("**** Error ****")
        print ("Use -h option for help") 
        sys.exit(2)
  
    for o, a in opts:
        print (o)
        if o == "-v":
            test_vend = 1
        elif o == "-a":
            test_andy_fd = 1; 
        elif o == "-c":
            test_andy_check = 1; 
        elif o == "-t":
            test_run = 1; 
        elif o == "-r":
            real_run = 1
        elif o == "-h":
            print ("bad option..." + o)
            print ("-v to test vend once")
            print ("-a to test andy_fd once")
            print ("-c to test andy_check once")
            print ("-t to test run")
            print ("-r for real run")
            print ("-h for this help")
            sys.exit()
        else:
            print ("bad option..." + o)
            print ("-v to test vend once")
            print ("-a to test andy_fd once")
            print ("-c to test andy_check once")
            print ("-t to test run")
            print ("-r for real run")
            print ("-h for this help")
            sys.exit()
           
    # switch stdout and stderr recording if any test mode       
    if ((test_vend == 0) and (test_andy_fd == 0) and (test_andy_check == 0) and (test_run==0)):       
        sys.stdout = new_stdout()
        sys.stderr = new_stderr()     
      
    # init the log file         
    loginit()
    logit ("hello from " + __file__)            
           
    # make sure that webdriver etc are stopped    
    stop_webdriver()    
    
    # check for test vend
    if (test_vend == 1):
        logit ("Running test_vend..")
        start_webdriver()
        rc = do_vend()
        stop_webdriver()
        logit ("do_vend returned rc=" + str(rc))
        
    # check for test andy    
    elif (test_andy_fd == 1):
        logit ("Running test_andy..")
        start_webdriver()
        rc = do_andy_fd()
        stop_webdriver()
        logit ("do_vend returned rc=" + str(rc))

        
    # andy check
    elif (test_andy_check == 1):
        logit ("Running test_andy check..")
        do_andy_check()
     
    # else run mode (real or test)  
    else:
        if (test_run == 1):
            logit ("Running runloop in debug mode..") 
        else:     
            logit ("Running runloop..") 
        
        # main loop
        while (1):
            logit ("forking process..")
            pid = os.fork()
            logit ("forked this pid = " + str(os.getpid()) + " child_pid = " + str(pid))
        
            #  pid = 0 for child process - run the main loop
            if pid == 0:
                logit ("Child process this pid = " + str(os.getpid()) + " entering run loop..")
                run_loop() 
                logit ("child exiting")
                sys.exit()  
            
            # pid = child pid for parent process - check for child dying      
            else: 
                child_pid = pid
                logit ("Parent process this pid = " + str(os.getpid()))
                logit ("waiting for child pid  = " + str(child_pid) + " to die")
                dead_pid, status = os.waitpid(child_pid, 0)
                logit ("wait returned, dead pid = " + str(dead_pid) + " status = " + str(status))
                logit ("child died .. restarting")
                dnow = datetime.now()
                os.rename ('/home/pi/ron_python/stderr.txt', '/home/pi/ron_python/stderr.txt' + '.' + str(dnow))
                send_restart_email();
                time.sleep(10);
                os.system ("sudo reboot");
    return

#****************************
# __main__
#****************************         
if __name__ == '__main__':
    
    do_main(sys.argv[1:])