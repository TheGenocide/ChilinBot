#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
#core bot v.2.7 dev by aof 2018/02/15
#This is bot chilindo create By Using Webdriver PhantomJS v2.1

import time, os, runpy, sys, winsound, pickle, pdb
import configparser, pymysql.cursors, tkinter
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait

#=================================== Set Var =========================================
#[Common]
url = '' #link web page
urlLogin = '' #link login page
path_driver = '' 
path_script = '' #path of script
email = '' #email or user for login
password = '' #password for login
flgBid = '' #1 = enable, 0 = disenable bid function 
flgDB = '' #1 = enable, 0 = disenable save result of bid to database 
elmExceptRe = 0 #Count of NoSuchElementException for Restart
elmExceptSt = 0 #Count of NoSuchElementException for Stop
#[DBinfo]
DBhost = '' # database host
DBuser = '' #username database
DBpass = '' #password database
DBname = '' #database name
#[Product]
productID = '' #Product ID
size = '' #Option of product
targetBidMin = 0
targetBidMax = 0
timeBid = 0
viewStyle = 0 #1 = new style , 0 = old style defalut = 0
#Other Var
version = '2.7' #version of bot
i = 0 #round for bid
aid = '' #auction id
aid_old = '' #old aid
getItem = 0
browser = '' #var webdriver
except_r = 0 #var for count elmExcept restart
except_s = 0 #var for count elmExcept stop

#=================================== Config =========================================
def getConfig():
    global url, urlLogin, path_driver, path_script, email, password, flgBid, flgDB, elmExceptRe, elmExceptSt  #[Common]
    global productID, size, targetBidMin, targetBidMax, timeBid, viewStyle #[Product]
    global DBhost, DBuser, DBpass, DBname #[DBinfo]
    
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini', encoding='utf-8')
    config.sections()
    url = config['Common']['url']
    urlLogin = config['Common']['urlLogin']
    path_driver = os.path.dirname(os.path.abspath(__file__)) + config['Common']['path_driver']
    path_script = config['Common']['path_script']
    email = config['Common']['email']
    password = config['Common']['password']
    flgBid = config['Common']['flgBid']
    flgDB = config['Common']['flgDB']
    elmExceptRe = int(config['Common']['elmExceptRe'])
    elmExceptSt = int(config['Common']['elmExceptSt'])
    DBhost = config['DBinfo']['DBhost']
    DBuser = config['DBinfo']['DBuser']
    DBpass = config['DBinfo']['DBpass']
    DBname = config['DBinfo']['DBname']
    productID = config['Product']['productID']
    size = config['Product']['size']
    targetBidMin = int(config['Product']['targetBidMin'])
    targetBidMax = int(config['Product']['targetBidMax'])
    timeBid = int(config['Product']['timeBid'])
    viewStyle = int(config['Product']['viewStyle'])
 
#=================================== Main GUI =========================================
def setTop():
    top = tkinter.Tk()
    top.mainloop()

#=================================== Database Connect =========================================
def setConn():
    global DBhost
    global DBpass
    global DBuser
    global DBname
    try:
        cn = pymysql.connect(host=DBhost,user=DBuser,password=DBpass,db=DBname,charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    except:
        print("\033[1;31;40mCan't Connect Database!!")
        cn.close()
    finally:
        return cn;

#=================================== Database Disconnect =========================================
def setDisConn(cn):
    cn.close()
    
#=================================== Insert Data =========================================
def setInsert(cn,sqlcmd):
    try:
        with cn.cursor() as cursor:
            cursor.execute(str(sqlcmd)) #query sql
            no = cursor.lastrowid
        cn.commit()
        cursor.close()
    except:
        print("\033[1;31;40mCan't Query SQL Command!!")
        cn.rollback()
    finally:
        return no;
        
#=================================== Pause =========================================
def setPause():
    global browser
    browser.save_screenshot('debug/debug.jpg')
    getBeep()
    print(input("\033[1;31;40m     Press the <ENTER> key to continue..."))
    sys.exit()
    browser.quit()
    
#=================================== Print out screen fix position =========================================
def setPrint(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (int(x), int(y), str(text)))
     sys.stdout.flush()

#=================================== Clear Screen =========================================
def setClear():
    if sys.platform == "linux":
        os.system('clear')
    elif sys.platform == "win32":
        os.system('cls')
    else:
        return False;
    return True;
 
#=================================== Restart Script =========================================
def setRestart(e):
    global path_script,browser
    setClear()
    if e != "":
        print("\033[1;31;40mError!! is " + str(e))
    print("\033[1;31;40mWait for refresh")
    browser.quit()
    runpy.run_path(path_script)
    time.sleep(2)
    sys.exit()
    
#=================================== Restart Script =========================================
def setWebDriver():
    global browser,path_driver
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["pantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0")
    #pdb.set_trace()
    browser = webdriver.PhantomJS(path_driver,desired_capabilities=dcap)
    browser.implicitly_wait(10) # try to wait for load page (seconds)
    browser.set_window_position(0, 0)
    browser.set_window_size(1024, 768)
        
#=================================== Connect web ,check status and get login infomation =========================================   
def setStart(url):
    global browser
    browser.get(str(url))
    assert('Chilindo' in browser.title)
    print("Connect " + str(url) + " OK")
 
#=================================== Popup Country =========================================  
def setCountry(id):
    global browser
    #pdb.set_trace()
    try:
        browser.find_element_by_id(id)
        browser.implicitly_wait(6)
        return True;
    except NoSuchElementException:
        return False;
 
#=================================== Setup Login =========================================  
def setLogin(email,password):
    global browser
    is_element_present = setCountry("pnlCountryPopup")
    print("Get Country Popup")
    if is_element_present:
        browser.execute_script("btnSubmitSelectCountry()") #click button select country
        browser.implicitly_wait(6)
        print("Submit Country Popup")
        setLogin(email,password)
    else:
        if email != "":
            browser.find_element_by_link_text("เข้าสู่ระบบ").click()
            browser.implicitly_wait(2)
            browser.find_element_by_link_text("หรือคลิกที่นี่เพื่อเข้าสู่ระบบแบบธรรมดา").click()
            browser.implicitly_wait(2)
            browser.find_element_by_id("Signin1_txtEmail").send_keys(email)
            browser.find_element_by_id("Signin1_txtPassword").send_keys(password)
            browser.find_element_by_id("Signin1_btnSignIn").click()
            browser.implicitly_wait(6)
            pickle.dump( browser.get_cookies() , open("debug/cookies.pkl","wb"))
            print("Dump Cookie")
                
            print("Login OK")
            result = True
            browser.implicitly_wait(6)
        else:
            print("\033[1;31;40m Null email!!")
            result = False
            setPause()
        return result;      
    
#=================================== Redirect to bid page ========================================= 
def setRedirectPage(url,path,product,txt = ''):
    global browser
    if url == "":
        print("\033[1;31;40m Null url!!")
        setPause()
    else:
        global browser
        if product != "":
            browser.get(url + path + str(product).strip())
        else:
            browser.get(url + path)
            
        print("\033[1;31;40m Redirect! ( " + txt + " )")
        #time.sleep(5)
        browser.implicitly_wait(6)
        
#=================================== Send Bid =========================================     
def setSubmit():
    global browser
    browser.execute_script("__doPostBack('ctl00$ContentPlaceHolder1$btnBid','')") #Send Bid
        
#=================================== Print Out Result =========================================     
def setResult(txt = ''): #opt 1 = new style , 0 = old style defalut = 0
    global version,viewStyle,targetBidMin,targetBidMax
    global timeBid,getItem
    userID = getUserInfo()
    CountDown = ''
    if getItem > 0:
        CountDown = 'THE END'
    else:
        CountDown = getCountDown()
        
    line = "\033[1;32;40m**************************************************"
    
    if viewStyle == 1:
        setPrint(0,0,line)
        setPrint(0,1,"     Chilindo Bot Auto Bid V " + version + " Dev by Aof")
        setPrint(0,2,line)
        setprint(0.3,"Status: " + txt)
        setPrint(0,4,"Product Info: " + getProductInfo())
        setPrint(0,5,"USER ID: " + userID)
        setPrint(0,6,"Count Down: " + CountDown)
        setPrint(0,7,"Round Bid: " + str(i))
        setPrint(0,8,"Min Price: " + str(targetBidMin) + " Baht")
        setPrint(0,9,"Max Price: " + str(targetBidMax) + " Baht")
        setPrint(0,10,"Time Start: <= " + str(timeBid) + " Sec")
        setPrint(0,11,"Last Price: " + getLastBid() + " Baht")
        setPrint(0,12,"Next Price: " + getNextBid() + " Baht")
        setPrint(0,13,"Current Winner: " + getLastWin())
        setPrint(0,14,"Get Item: " + str(getItem) + " EA")
        setPrint(0,15,line)
        setPrint(0,16,"<< PRESS CTRL + C TO EXIT >>")
        setPrint(0,17,line)
        setPrint(0,18," ")
    else:
        setClear()
        print(line)
        print("\033[1;31;40m     Chilindo Bot Auto Bid V " + version + " Dev by Aof")
        print(line)
        print("\033[1;37;40m Status: \033[2;34;47m " + txt + " ")
        print("\033[1;37;40m Product Info: \033[1;33;40m" + getProductInfo())
        print("\033[1;37;40m USER ID: \033[1;33;40m" + userID)
        print("\033[1;37;40m Count Down: \033[1;36;40m" + CountDown)
        print("\033[1;37;40m Round Bid: \033[1;33;40m" + str(i))
        print("\033[1;37;40m Min Price: \033[1;33;40m" + str(targetBidMin) + "\033[1;37;40m Baht")
        print("\033[1;37;40m Max Price: \033[1;33;40m" + str(targetBidMax) + "\033[1;37;40m Baht")
        print("\033[1;37;40m Time Start: \033[1;33;40m<= " + str(timeBid) + "\033[1;37;40m Sec")
        print("\033[1;37;40m Last Price: \033[1;31;40m" + getLastBid() + "\033[1;37;40m Baht")
        print("\033[1;37;40m Next Price: \033[1;32;40m" + getNextBid() + "\033[1;37;40m Baht")
        print("\033[1;37;40m Current Winner: \033[1;35;40m" + getLastWin())
        print("\033[1;37;40m Get Item: \033[1;36;40m" + str(getItem) + "\033[1;37;40m EA")
        print(line)
        print("\033[1;32;40m     << PRESS \033[1;31;40mCTRL + C \033[1;32;40mTO EXIT >>")
        print(line)
        print(" ")

#=================================== INPUT =========================================        
def setInput():
    setPrint(0,14,input("\033[1;31;40m     INPUT NEW Price? "))

#=================================== Beep =========================================     
def getBeep():
    if sys.platform == "linux":
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 1000, 500))
        time.sleep(0.5)
    elif sys.platform == "win32":
        winsound.Beep(1000,500)
        time.sleep(1)
    else:
        return False;
    return True;
    
#=================================== Beep =========================================          
def getUserInfo():
    global browser
    userTmp1 = browser.find_element_by_id('show_user_profile')
    browser.implicitly_wait(6)
    userTmp2 = userTmp1.text.strip()
    userTmp3 = userTmp2.split(" ")
    return userTmp3[1];  
        
#=================================== Beep =========================================      
def getSession():
    global browser
    getSession = browser.get_cookie('ASP.NET_SessionId'); #session
    browser.implicitly_wait(6)
    return str(getSession['value']);
        
#=================================== Last Winner =========================================  
def getLastWin():
    global browser
    element = browser.find_element_by_class_name('current_winner') #current winner info
    browser.implicitly_wait(6)
    
    return element.text.strip();
    
#=================================== Count Down =========================================   
def getCountDown():
    global browser,productID
    element = browser.find_element_by_id('spanCountDown')
    browser.implicitly_wait(3)
    if element.text.strip() == "":
        time.sleep(5)
        setRedirectPage(url,'/th/product/',str(productID),'Count Down is null')
    else:
        return element.text.strip(); # Find count down

#=================================== Bid Text Box =========================================   
def getBidBox():
    global browser
    element = browser.find_element_by_id('ContentPlaceHolder1_txtBidNew')
    return element;  # bid box

#=================================== Option =========================================  
def getOption(opt = 0):  #opt : 0 = intext,1 = value,2 = index defalut = 0
    global browser,size
    if size != "":
        if int(opt) == 0:
            Selectsize = browser.find_element_by_xpath("//select[@id='ContentPlaceHolder1_ddlRelatedItems']/*[contains(text(),'%s')]" % (size)) #select size by visible text
        elif int(opt) == 2:
            Selectsize = browser.find_element_by_id("ContentPlaceHolder1_ddlRelatedItems") #select size by index
            Selectsize.click()
            j = 1
            for j in range(1,3):
                Selectsize.send_keys(Keys.ARROW_UP)
                
            j=1
            for j in range(1,int(size)):
                Selectsize.send_keys(Keys.ARROW_DOWN)
            Selectsize.click()
        else:
            Selectsize = browser.find_element_by_xpath("//select[@id='ContentPlaceHolder1_ddlRelatedItems']/*[contains(value,'%s')]" % (size)) #select size by value
        browser.implicitly_wait(6)
        return Selectsize;
    else:
        print("Null size option!!")
        setPause()
    
#=================================== Last Bid =========================================  
def getLastBid():
    global browser
    rawElm = browser.find_element_by_xpath("//p[contains(@class, 'info_data') and contains(@class, 'current_bid')]")
    browser.implicitly_wait(6)
    rawBid = rawElm.text.strip()
    Bid = rawBid.split(" ")
    return Bid[0];

#=================================== Next Bid =========================================  
def getNextBid():
    global browser
    element = browser.find_element_by_id('ContentPlaceHolder1_txtBid')
    browser.implicitly_wait(6)
    return element.get_attribute('value').strip();  # bid box
    
#=================================== End Bid Round =========================================      
def getEndBid():
    global browser
    #element = browser.find_element_by_xpath("//p[contains(@class, 'info_data') and contains(@class, 'timeout') and contains(@class, 'last_minute')]")
    element = browser.find_element_by_id('spanEndAuction')
    browser.implicitly_wait(6)
    return element.text.strip();  # bid box
    
#=================================== Bid Success =========================================      
def getBidSucess():
    global browser
    element = browser.find_element_by_id('ContentPlaceHolder1_pBiddingInfo')
    browser.implicitly_wait(6)
    return element.element.value_of_css_property('display');  # success box

#=================================== Bid Price =========================================    
def getBidPrice():
    global targetBidMin,targetBidMin
    NextBid = getNextBid()
    LastBid = getLastBid()
    price = 0
    
    if int(targetBidMin) > int(targetBidMax):
        print("Error targetBidMin More than targetBidMin! Please check price.")
        time.sleep(2)
        price = -1
    elif int(LastBid) < int(targetBidMin):
        price = targetBidMin
    elif int(LastBid) >= int(targetBidMax):
        price = targetBidMax
    elif int(LastBid) >= int(targetBidMin) and int(LastBid) < int(targetBidMax) and getLastWin() != getUserInfo():
        price = NextBid
    else:
        price = -1
    return int(price);
 
#=================================== Auction Id =========================================   
def getAuctionId():
    global browser
    parentElement = browser.find_element_by_id("view_details")
    elementList = parentElement.find_elements_by_tag_name("td")
    browser.implicitly_wait(6)
    i = 1
    for aid_txt in elementList:
        if i == 2:
            aid = aid_txt.text.strip()
        i = i + 1
    return aid;

#=================================== Sec =========================================  
def getSec(time_str):
    try:
        time_str = str(time_str)
        if ":" in time_str:
            h, m, s = time_str.split(':')
        else:
            h = 0
            m = 0
            s = time_str
    except:
        return 0;
    finally:
        return int(h) * 3600 + int(m) * 60 + int(s);
    
#=================================== Product info =========================================       
def getProductInfo():
    global browser
    productTmp1 = browser.find_element_by_id('ContentPlaceHolder1_lbTitle')
    browser.implicitly_wait(6)
    return productTmp1.text.strip(); 
        
#=================================== Main =========================================
if __name__ == '__main__':
    getConfig()
    setWebDriver()
    #pdb.set_trace()
    setStart(urlLogin)
    setLogin(email,password)
    setRedirectPage(url,'/th/product/',productID,'First open')
    userID = getUserInfo()
    setClear()
    winner = ''
    winner_old = ''
    price = 0
    price_old = 1
    aid = ''
    aid_old = ''
    if flgDB == "1":
        cn = setConn()
    while True:
        try:
            #check current page
            if productID in browser.current_url == False:
                setRedirectPage('/th/product/',productID,'check current page')
            #get element info
            count = getCountDown()
            elem_bid = getBidBox()
            if len(size) == 1:
                elem_size = getOption(2)
            else:
                elem_size = getOption(0)
            bidPrice = getBidPrice()
            endBid = getEndBid()
            aid = getAuctionId() #get bid id
            price = int(getLastBid())
            winner = getLastWin()
            txt = ''
            sqlcmd = ''  
            #start bid
            if "END" in endBid.upper() or "สิ้นสุดแล้ว" in endBid: #End Bid
                i = 0 #reset work round
                if (getLastWin() == userID and getLastWin() != '') or getBidSucess() != "none":
                    getItem = getItem + 1
                    
                #End Bid
                if getItem > 0:
                    txt = 'Mission Complete!!'
                    setResult(txt) #print result  
                    setPause()
                    break
                else:
                    time.sleep(randint(5,10))
                    setRedirectPage('/th/product/',productID,'End Bid else')
                    txt = 'End round! You\'r not winner'
                    setResult(txt) #print result   
            elif "wait" in endBid:
                txt = 'Please wait!!'
                setResult(txt) #print result   
                #setInput()
                #time.sleep(randint(1,2))
            elif getLastWin() == userID: #Winner bid current
                txt = 'You Winner Now!!'
                setResult(txt) #print result   
                #setInput()
                #time.sleep(randint(1,3))
            elif int(getLastBid()) >= int(targetBidMax): #Over target price
                txt = 'Over target price!!'
                setResult(txt) #print result   
                #setInput()
                #time.sleep(randint(5,10))
            else: #Bid
                if flgBid == '1': #enable Bid function
                    if int(getSec(timeBid)) >= int(getSec(getCountDown())) and \
                    int(getSec(getCountDown())) > 0 and \
                    int(getSec(getCountDown())) != None: #check time to bid
                        i += 1
                        if int(bidPrice) > 0: 
                            elem_size.click()
                            time.sleep(1)
                            elem_bid.clear();
                            elem_bid.send_keys(bidPrice)
                            setSubmit() #Send Bid
                            txt = 'Bid Success!!'
                        else:
                            txt = 'None Price Bid!!'
                        setResult(txt) #print result   
                        #setInput()
                    else:
                        txt = 'Wait Time to Bid!!'
                        setResult(txt) #print result   
                else:
                    txt = 'Monitor Mode!!'
                    setResult(txt) #print result   
                    
            if flgDB == "1": #insert bid history
                if (price == 0 or price < price_old) and aid_old != aid:
                    if aid_old != "":
                        txt = 'Insert Data Complete!!'
                        sqlcmd = "INSERT " + DBname + ".trkprice SET aid='" + aid_old + "',product_id='" + productID + "', product_name='" +  \
                        getProductInfo() + "',opt_txt='" + size + "',winner='" + winner_old + "',price='" + str(price_old) + "' ;"
                        setInsert(cn,sqlcmd)
                    aid_old = aid
                price_old = price
                winner_old = winner 
                
            except_r = 0
            time.sleep(0.5)
            #pdb.set_trace()
        except KeyboardInterrupt:
            if flgDB == "1":
                setDisConn(cn)
            setPause()
        except ValueError:
            time.sleep(2)
            continue
        except NoSuchElementException: #element not found
            if except_s > int(elmExceptSt):
                print("\033[1;31;40mStop Error NoSuchElementException!")
                setDisConn(cn)
                setPause()
            elif except_r > int(elmExceptRe):
                print("\033[1;31;40mRestart Error NoSuchElementException!")
                except_s += 1
                time.sleep(1)
                setRedirectPage('/th/product/',productID,'Restart Fail Page')
            else:
                print("\033[1;31;40mError NoSuchElementException!")
                except_r += 1
                time.sleep(3)
                continue
            #setRestart()
        except Exception as e: # catch *all* exceptions
            #print(e)
            time.sleep(3)
            if aid == "":
                setRedirectPage(url,'/th/product/',str(productID),'Except:normal')
            else:
                time.sleep(5)
                setRedirectPage(url,'/th/product/' + str(productID) + '?aucid=' + str(aid),'Except:aid=' + str(aid))
            continue
            #setRestart(e)
        else:
            continue