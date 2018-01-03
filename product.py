#coding=utf-8
import time
from scripts import common
from scripts import login
from scripts import common
import traceback
from selenium.webdriver.support.expected_conditions import element_located_selection_state_to_be as elsstb

def add(driver,licenseID,productName,showName,keyType,productInfo,testCaseName):
    try:
        common.seleteSubject(driver,'产品管理')
        driver.find_element_by_id("newProject-btn").click()
        common.writeLog('新建产品')
        time.sleep(1)
        driver.find_element_by_id("addLicenseID").clear()
        driver.find_element_by_id("addLicenseID").send_keys(licenseID)
        driver.find_element_by_id("addProductName").clear()
        driver.find_element_by_id("addProductName").send_keys(productName)
        driver.find_element_by_id("newProDisplayName").clear()
        driver.find_element_by_id("newProDisplayName").send_keys(showName)
        driver.find_element_by_id("newProDescription").clear()
        driver.find_element_by_id("newProDescription").send_keys(productInfo)
        if keyType =='云锁':
            list = driver.find_elements_by_tag_name("label")
            for li in list:
                # common.writeLog(li.text)
                #temp = li.find_element_by_tag_name("span")
                if li.text == u"云锁":
                    li.click()
                    break
            
        if keyType =='软锁':
            list = driver.find_elements_by_tag_name("label")
            for li in list:
                #temp = li.find_element_by_tag_name("span")
                if li.text == u"软锁":
                    li.click()
                    break
        
        if keyType =='云锁软锁':
            
            list = driver.find_elements_by_tag_name("label")
            for li in list:
                #temp = li.find_element_by_tag_name("span")
                if li.text == u"软锁" or li.text == u"云锁":
                    
                    li.click()        
                
        driver.find_element_by_id("newProduct").click()
        time.sleep(2)
        dialog = driver.find_element_by_id("newProject")
        # test = dialog.get_attribute('style')
        # common.writeLog(test)

        if dialog.get_attribute('style') == 'display: none;':
            common.writeLog('完成新建产品')
            return True
        else:            
            common.writeLog('新建产品失败')
            #截图
            common.getScreenshot(driver,testCaseName)
            return False
    except:
        common.getScreenshot(driver,testCaseName)
        msg = traceback.format_exc()
        common.writeLog(msg)
        return False
     

def delProduct(driver,licenseID,testCaseName):
    table = driver.find_element_by_id('productTable')
    rows =  table.find_elements_by_tag_name('tr')
    flag = 0
    for row in rows:
        colums = row.find_elements_by_tag_name('td')
        for colum in colums:
            try:
                if colum.get_attribute('aria-describedby') == 'productTable_licenseId':

                    if colum.text == licenseID :
                        flag = 1
                        break
            except:
                pass

        if flag == 1:
            break

    if not flag == 1:
        common.getScreenshot(driver,testCaseName)
        common.writeLog('没有找到目标')
        return False
    else:
        try:
            time.sleep(1)
            # row.find_element_by_xpath("//td[@aria-describedby='productTable_myac']/span[2]").click()
            row.find_element_by_css_selector("span[title='删除']").click()

            time.sleep(10)
            driver.find_element_by_id('sense-modal').find_element_by_class_name('btnOk').click()
            # driver.find_element_by_xpath("(//button[@class='btn btn-info btnOk'])").click()

            time.sleep(10)
            return True
        except:
            common.getScreenshot(driver,testCaseName)
            msg = traceback.format_exc()
            common.writeLog(msg)
            common.writeLog('找到目标,无法删除')
            return False

        

    
    
##############################################################  
def finddialog(driver,name,select):
    print('删除产品窗口')
    dialog = driver.find_element_by_id('sense-modal')
    print(dialog.get_attribute('class'))
    button = dialog.find_element_by_xpath(".//button[@class='fa fa-trash']")    
    print(button.text)
    for d in dialog:
        print(d)
        title = d.find_elements_by_tag_name('h4')
        print(title.text)
        if title.text== name:
            print('删除产品窗口1')
            button = dialog.find_elements_by_class_name('btn btn-info btnOk')
            if button.text == select:
                print('删除产品窗口2')
                button.click()
    
    
def findAddDialog(driver):
    time.sleep(30)
    try:
        dialog = driver.find_element_by_id('newProject')
    except:
        return False
    
    if dialog.get_attribute('style')=='display: block;':
        return True
    else:
        return False
    
def errorinfo(driver,info):
    try:
        element = driver.find_element_by_id("layui-layer11")
        try:
            temp = element.find_element_by_tag_name('div')
            print(temp.text)
            return 0
        except:
            return 1
    except:
        return 2
    
    
def search(driver,productName):
    common.seleteSubject(driver,'产品管理')
    try:
        driver.find_element_by_id("produce_searchValue").clear()
        driver.find_element_by_id("produce_searchValue").send_keys(productName)
        driver.find_element_by_css_selector("span.pro-ser").click()
    except:
        print('error')
    
def findTableResult(driver,productId,productName):   
    
    table = driver.find_element_by_id("productTable")
    rows =  table.find_elements_by_tag_name('tr')
    for i in range(0,len(rows)):
        colum = rows[i].find_elements_by_tag_name('td')
        
        for j in range(0,len(colum)):
            try:
                if colum[j].get_attribute('aria-describedby') == 'productTable_licenseId':
                    if colum[j].text == productId:
                        return True
            except:
                pass   
    
    return False

def delAllProduct(driver):    
    common.writeLog('删除全部产品')
    common.seleteSubject(driver,'产品管理')
    time.sleep(15)
    try:
        while True:
            table = driver.find_element_by_id('productTable')
            rows =  table.find_elements_by_tag_name('tr')
            if len(rows)==1:
                break                
            for row in rows:
                delButton = row.find_element_by_xpath("//td[@aria-describedby='productTable_myac']/span[2]")
                if delButton.get_attribute('title') == '删除':
                        delButton.click()
                        time.sleep(1)
                        driver.find_element_by_xpath("(//button[@class='btn btn-info btnOk'])").click()     
                        time.sleep(1)
                        break
    except:
        msg = traceback.format_exc()
        common.writeLog(msg)
        common.writeLog('没有找到删除按钮')            

    common.writeLog('删除完成')

def editProduct(driver,licenseID,productName,showName,keyType,productInfo,testCaseName):
    table = driver.find_element_by_id('productTable')
    rows = table.find_elements_by_tag_name('tr')
    flag=0
    for row in rows:
        colums = row.find_elements_by_tag_name('td')
        for colum in colums:
            try:
                if colum.get_attribute('aria-describedby') == 'productTable_licenseId':

                    if colum.text == licenseID :
                        flag = 1
                        break
            except:
                pass

        if flag ==1:
            break
    if not flag ==1:
        common.getScreenshot(driver,testCaseName)
        common.writeLog('没有找到目标')
        return False
    else:
        try:
            # row.find_element_by_xpath("//td[@aria-describedby='productTable_myac']/span[1]").click() #点击编辑按钮 这有问题 总是编辑第一个
            row.find_element_by_css_selector("span[title='修改']").click()
            time.sleep(5)
            driver.find_element_by_id('updateProductName').clear()
            driver.find_element_by_id('updateProductName').send_keys(productName)
            driver.find_element_by_id('updateProDisplayName').clear()
            driver.find_element_by_id('updateProDisplayName').send_keys(showName)
            driver.find_element_by_id('updateProDescription').clear()
            driver.find_element_by_id('updateProDescription').send_keys(productInfo)
            list = driver.find_elements_by_tag_name("label")
            if keyType =='云锁':
                common.writeLog('传入参数只有云锁')
                list = driver.find_elements_by_tag_name("label")

                for li in list:
                    # temp = li.find_element_by_tag_name("span")
                    if li.text == u"云锁":
                        # print(driver.find_element_by_id('on_per').is_selected())
                        if not driver.find_element_by_id('on_per').is_selected():
                        # e1 = driver.find_element_by_id('on_per')
                        # if elsstb(e1,True):
                            li.click()
                    if li.text == u"软锁":
                        if  driver.find_element_by_id('off_per').is_selected():
                        # e2 = driver.find_element_by_id('off_per')
                        # if elsstb(e2,True):
                            li.click()


            if keyType == '软锁':
                common.writeLog('传入参数只有软锁')
                list = driver.find_elements_by_tag_name("label")
                for li in list:
                    if li.text == u"软锁":
                        if not driver.find_element_by_id('off_per').is_selected():
                            li.click()
                    if li.text == u"云锁":
                        if  driver.find_element_by_id('on_per').is_selected():
                            li.click()


            if keyType == '云锁软锁':
                common.writeLog('传入参数软锁云锁')
                list = driver.find_elements_by_tag_name("label")
                for li in list:
                    # temp = li.find_element_by_tag_name("span")
                    if li.text == u"软锁":
                        if not driver.find_element_by_id('off_per').is_selected():
                            li.click()

                    if li.text == u"云锁":
                        if not driver.find_element_by_id('on_per').is_selected():
                            li.click()



            driver.find_element_by_id("updateProductBtn").click()
            time.sleep(5)
            dialog = driver.find_element_by_id("updateProject")
            # test = dialog.get_attribute('style')
            # common.writeLog(test)

            if dialog.get_attribute('style') == 'display: none;':
                common.writeLog('修改卡片页关闭')
                return True
            else:
                common.writeLog('修改产品失败')
                # 截图
                common.getScreenshot(driver, testCaseName)
                return False
        except:
            common.getScreenshot(driver, testCaseName)
            msg = traceback.format_exc()
            common.writeLog(msg)
            return False



def compareProduct(driver, productId, productName):
    table = driver.find_element_by_id("productTable")
    rows = table.find_elements_by_tag_name('tr')
    flag = 0
    for i in range(0, len(rows)):
        colum = rows[i].find_elements_by_tag_name('td')

        for j in range(0, len(colum)):
            try:
                if colum[j].get_attribute('aria-describedby') == 'productTable_licenseId':
                    if colum[j].text == productId:
                        flag = flag+1
                if colum[j].get_attribute('aria-describedby') == 'productTable_productName':
                    if colum[j].text ==productName:
                        flag = flag+1
            except:
                pass
    if flag == 2:
        common.writeLog('修改产品成功')
        return  True
    else:
        return False










    
    
    
    
    
