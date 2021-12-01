from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def enterData(field,data):
    try:
        driver.find_element_by_xpath(field).send_keys(data)
        pass
    except Exception:
        time.sleep(1)
        enterData(field,data)

def clickButton(xpath):
    try:
        driver.find_element_by_xpath(xpath).click()
        pass
    except Exception:
        time.sleep(1)
        clickButton(xpath)

def login():
    email='//*[@id="userEmail"]'
    password = '//*[@id="userPassword"]'
    loginButton = '//button[text()="LOGIN"]'
    enterData(email, "mohanadarafework@gmail.com")
    enterData(password, "MohanadKhadijaMK")

def fillForm(subjectId):
    subId='//*[@name="subjectId"]'
    series='//*[@name="seriesDesc"]'
    enterData(subId, str(subjectId))
    enterData(series, "MPRAGE")
    clickButton('//*[@id="searchQuery"]')
    time.sleep(3)
    clickButton('//input[@name="imageId"][1]')
    clickButton('//*[@id="addCollectId"]')
    clickButton('//*[@id="candidateNames"]')
    clickButton('//option[text()="research"]')
    clickButton('//*[@id="regroupDialogTitle"]')
    clickButton('//*[@id="regroupDialogTitle"]')
    time.sleep(2)
    clickButton('//button[text()="OK"]')
    time.sleep(2)
    clickButton('//a[@href="#tab1"]')


driver = webdriver.Chrome("./chromedriver")
driver.get('https://ida.loni.usc.edu/login.jsp?project=PPMI')
login()
time.sleep(10)
NC_ID = [3114,3157,3165,3172,3300,3316,3369,3390,3563,3570,3750,3765,3769,3804,3807,3812,3817,3853,4010,4067,3106,3115,3160,3169,3188,3301,3320,3370,3551,3565,3571,3756,3767,3779,3805,3809,3813,3850,3855,4018,4085,3112,3151,3161,3171,3191,3310,3368,3389,3554,3569,3572,3759,3768,3803,3806,3811,3816,3852,4004,4032,4139]
PD_ID = [3589,3757,3770,3781,3808,3823,3829,3838,4012,4026,4035,4081,3113,3124,3130,3166,3176,3190,3314,3328,3371,3377,3387,3559,3584,3591,3758,3771,3787,3814,3824,3830,3863,4013,4027,4037,4082]
for subID in PD_ID:
    fillForm(subID)