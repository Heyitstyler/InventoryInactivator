import os
import sys
import csv
import numpy
import pandas as pd
import selenium
import time
import glob
import openpyxl
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def dlSummary(barSelect):
    global sum_e
    found_Sum = "False"
    try:
        sum_e = "Failed"
        os.chdir(repDL)
        keyword = 'Summary'
        options = Options()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", repDL)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        # options.add_argument("--headless")


        summary_driver = webdriver.Firefox(options=options)
        sumWait = WebDriverWait(summary_driver, 90)

        summary_driver.get("https://www.barkeepapp.com/BarkeepOnline/inventories.php")

        login_Loaded = sumWait.until(EC.presence_of_element_located((By.NAME, 'session_username')))
        username_field = summary_driver.find_element(By.NAME, 'session_username')
        username_field.send_keys(barSelect)
        password_field = summary_driver.find_element(By.NAME, 'session_password')
        password_field.send_keys(passwd)
        login_button = summary_driver.find_element(By.NAME, 'login')
        login_button.click()

        inventories_Loaded = sumWait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[4]/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/a[1]')))
        full_summary = summary_driver.find_element(By.XPATH, '/html/body/div/div[4]/div/div[3]/div[2]/table/tbody/tr[1]/td[1]/a[1]')
        full_summary.click()

        full_Loaded = sumWait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dropdownMenu1"]')))
        dropdown_summary = summary_driver.find_element(By.XPATH, '//*[@id="dropdownMenu1"]')
        dropdown_summary.click()

        full_Loaded = sumWait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div[2]/ul/li[1]/a')))
        download_summary = summary_driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[2]/ul/li[1]/a')
        download_summary.click()

        while found_Sum == "False":
        # List all files in the specified directory
            files = os.listdir(repDL)

        # Check if any file contains the keyword
            for file in files:
                if file.startswith(keyword) and not file.endswith(".part"):
                    print(f"Found file: {file}")
                    sum_e = (f"{proper} Summary report")
                    time.sleep(1)
                    summary_driver.close()
                    time.sleep(0.5)
                    summary_driver.quit()
                    os.chdir(root)
                    found_Sum = "True"
                    return
        
        
    except:
        sum_e = ("Error Collecting Summary Report")
        summary_driver.close()
        time.sleep(1)
        summary_driver.quit()
        os.chdir(root)
        log = open("dllog.txt", "a")
        L = [f"Failed Summary Report\n"]
        log.writelines(L)
        log.close()
        return


def xl_to_csv():
    global itemsCsv
    barSum = glob.glob(os.path.join(repDL, "Summary_Report*.xlsx"))[0]

    os.chdir(repDL)

    print(barSum)

    df = pd.read_excel(barSum)

    Item_Names = df.iloc[:, 0]

    ConvertCsv = Item_Names.to_csv('Item_List.csv', index=False)

    itemsCsv = glob.glob('Item_List.csv')


def compare_to_csv():
        os.chdir(repDL)
        csv_Data = pd.read_csv('Item_List.csv')
        ItemsList = csv_Data.iloc[:, 0].to_list()
        options = Options()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", repDL)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        # options.add_argument("--headless")


        Items_driver = webdriver.Firefox(options=options)
        ItemsWait = WebDriverWait(Items_driver, 90)

        Items_driver.get("https://www.barkeepapp.com/BarkeepOnline/items.php")

        login_Loaded = ItemsWait.until(EC.presence_of_element_located((By.NAME, 'session_username')))
        username_field = Items_driver.find_element(By.NAME, 'session_username')
        username_field.send_keys(barSelect)
        password_field = Items_driver.find_element(By.NAME, 'session_password')
        password_field.send_keys(passwd)
        login_button = Items_driver.find_element(By.NAME, 'login')
        login_button.click()

        Items_Loaded = ItemsWait.until(EC.presence_of_element_located((By.CLASS_NAME, 'even')))
        firstItem = Items_driver.find_element(By.XPATH, "/html/body/div/div[4]/div/div[2]/div[2]/table/tbody/tr[1]/td[1]/a[1]/img")
        firstItem.click()

        while True:
            try:
                pageLoad = ItemsWait.until(EC.presence_of_element_located((By.ID, "barcodes")))
                waitForName = ItemsWait.until(EC.presence_of_element_located((By.ID, 'itemName')))
                inactivate = Items_driver.find_element(By.CSS_SELECTOR, '#itemInactive')
                nameBox = Items_driver.find_element(By.ID, "itemName")
                itemName = nameBox.get_attribute('value')
                if itemName in ItemsList:
                    print (f"Match Found - {itemName}")
                    try:
                        Items_driver.find_element(By.XPATH, "//span[@class='ui-icon ui-icon-arrowthickstop-1-e grayIcon']")
                        print ("Item List Complete")
                        Items_driver.execute_script(saveExit)
                        time.sleep(1)
                        Items_driver.quit()
                        break
                    except:
                        pass
                    Items_driver.execute_script(nextjs)
                    time.sleep(.5)
                    continue
                else:
                    print (f"No Match Found - {itemName}")
                    if itemName == "":
                        nameBox.send_keys("0Unnamed")
                    inactivate = Items_driver.find_element(By.CSS_SELECTOR, '#itemInactive')
                    inactivate.click()
                    time.sleep(.75)
                    changePrice = Items_driver.find_element(By.ID, 'itemPrice')
                    curPrice = changePrice.get_attribute('value')
                    priceInt = str(curPrice + '0')
                    print (curPrice)
                    changePrice.clear()
                    changePrice.send_keys(priceInt)
                    try:
                        Items_driver.find_element(By.XPATH, "//span[@class='ui-icon ui-icon-arrowthickstop-1-e grayIcon']")
                        print ("Item List Complete")
                        Items_driver.execute_script(saveExit)
                        time.sleep(1)
                        Items_driver.quit()
                        break
                    except:
                        pass
                    Items_driver.execute_script(nextjs)
                    time.sleep(.5)
                    continue
            except Exception as e:
                print (e)
                break

def Reset():
    filelist = [ f for f in os.listdir(repDL)]
    for f in filelist:
        os.remove(os.path.join(repDL, f))



root = os.getcwd()
repDL = os.path.join(root, "reportdownloads")
barDB = os.path.join(root, "barDB")

bars = pd.read_csv(os.path.join(barDB, "bardb.csv"))

while True:
    barSelect = input("What bar are we working with: ")

    userRow = bars[bars["user"] == barSelect]

    if userRow.empty:
        print("Username not found. Please try again.")
        continue
    else:
        break

passwd = userRow["pass"].iloc[0]
proper = userRow["proper"].iloc[0]
street = userRow["street"].iloc[0]
city = userRow["city"].iloc[0]
inv = userRow["invoicename"].iloc[0]
price = userRow["price"].iloc[0]


nextjs = 'nextItem()'
savejs = 'saveChanges()'
saveExit = 'saveAndExit()'

dlSummary(barSelect)
xl_to_csv()
compare_to_csv()
Reset()

