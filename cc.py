from appium import webdriver 
des = {} 
des['platformName'] = 'Android' 
des['platformVersion'] = '10'
des['deviceName'] = 'MI_8'
des['app'] = "C:\\Users\\hanlizhi\Desktop\\app-gemini-debug_243.apk"
webdriver.Remote('http://localhost:4723/wd/hub', des)

#35987d7f