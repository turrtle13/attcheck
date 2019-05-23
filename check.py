#!/usr/bin/env python3
from selenium.webdriver import Firefox
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

class attend():
    def __init__(self, sName=None, attnd=None, totalCon=None):
        self.sName=sName
        self.attnd=attnd
        self.totalCon=totalCon



userUSNId="16105079"
userPass="16105079"

opts = Options()
opts.headless=True
brow = Firefox(options=opts)

mainList=[]
brow.get('http://45.112.139.194:8088/WebForms/frmLogin.aspx')
a = brow.find_element_by_xpath("//input[@id ='ContentPlaceHolder1_Login1_UserName']")
a.send_keys(userUSNId)
b = brow.find_element_by_xpath("//input[@id ='ContentPlaceHolder1_Login1_Password']")
b.send_keys(userPass)
brow.find_element_by_xpath("//input[@id ='ContentPlaceHolder1_Login1_LoginButton']").click()

#if brow.find_element_by_id("ContentPlaceHolder1_WUCMessage_lblMessage").text
timeOut=10
wait = WebDriverWait(brow, timeOut)


invalid=wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_WUCMessage_lblMessage" )))
if invalid.text == "Invalid User Name Or Password":
    print(invalid.text)
    print("Enter Correctly!!!")    

brow.get('http://45.112.139.194:8088/WebForms/Admission/ViewStudentDetails.aspx')


studName=wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_lblStudentNameView')))
studId=wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_lblStudentCodeView')))
studUSN=wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_lblUSNView')))
studSem=wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_lblCurrentsemesterView')))


stuDetails="Name: "+studName.text+ " StudentId: "+ studId.text+ " USN: "+studUSN.text+ " Sem: "+ studSem.text
element = wait.until(EC.element_to_be_clickable((By.ID, 'radpnlAttendance')))
element.click()

addOne=0
if studSem.text=="4":
    addOne=2
subId1='ctl00_ContentPlaceHolder1_rpbTransactionDtls_i7_rgvAttendanceDetails_ctl00'
subId2='_lnkSubjectName'

k=0
subNameList=[]
resList=[]
resAttList=[]
for j in range(4,19+addOne,2):
    if j<9:
        subId=subId1+"_ctl"+"0"+str(j)+subId2
    else:
        subId=subId1+"_ctl"+str(j)+subId2
    #time.sleep(3)
    subName=subId1+"__"+str(k)
    

    k+=1
    nam=wait.until(EC.element_to_be_clickable((By.ID, subName))) ##to get the name of the subject
    #subNameList.append(nam.text.split("(")[0]) #added subname to list
    #print(nam.text.split("(")[0])
    subName=nam.text.split("(")[0]
    wait.until(EC.element_to_be_clickable((By.ID, subId))).click()
    res=0
    resAtt=0
    
    for i in range(4,15,2):
        totId1='ctl00_ContentPlaceHolder1_rpbTransactionDtls_i7_rgvSubjectAttendanceDetails_ctl00_ctl'
        totId2='_lblAttendancePercentage'
        if i<9:
            totId=totId1+"0"+str(i)+totId2
        else:
            totId=totId1+str(i)+totId2
        #time.sleep(2)
        tot=wait.until(EC.presence_of_element_located((By.ID, totId)))
        res=res+int(tot.text)
        if i<9:
            attId=totId1+"0"+str(i)+'_lblTotalAttendedClass'
        else:
            attId=totId1+str(i)+'_lblTotalAttendedClass'
        att=wait.until(EC.presence_of_element_located((By.ID, attId)))
        resAtt += int(att.text)
   #print("Total: ",res, " Attended: ", resAtt)
    #resList.append(res)
    #resAttList.append(resAtt)
    mainList.append(attend(subName, resAtt, res))
    backButton='ctl00_ContentPlaceHolder1_rpbTransactionDtls_i7_BtnBackTohomefromexam'
    brow.find_element_by_id(backButton).click()
brow.quit()
#print(subNameList)
#print(resList)
#print(resAttList)
print(stuDetails)
for k in mainList:
    print(k.sName, k.attnd, k.totalCon)


