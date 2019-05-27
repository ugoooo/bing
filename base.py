# -*- encoding: utf-8 -*-
import random, math, urllib2, urllib, time, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from setting import ENV_TYPE, MOBILE_ENV, PC_ENV
os.chdir(os.path.realpath(''))
CWDPATH = os.getcwd()
BROWSEPATH = os.path.join(CWDPATH,'chrome')

import my_logging
log = my_logging.get_logger(__name__, os.path.join(CWDPATH, "task.log"))

class baseBing():
    def __init__(self):
        self.chrome = None

    def openChrome(self):
        pathSys = os.environ["PATH"]
        if pathSys.find(BROWSEPATH) == -1 :
            os.environ["PATH"]= BROWSEPATH + ";" + pathSys
        chromeOptions = Options()
        userDataPath = os.path.join(BROWSEPATH, "userData")
        chromeOptions.add_argument('--ignore-certificate-errors')
        chromeOptions.add_argument('--ignore-ssl-errors')
        chromeOptions.add_argument('--allow-running-insecure-content')
        chromeOptions.add_argument('--disable-web-security')
        chromeOptions.add_argument('--disable-desktop-notifications')
        chromeOptions.add_argument('disable-infobars')
        chromeOptions.add_argument(r'--user-data-dir=%s' % userDataPath)
        chromeOptions.add_argument(r'--disk-cache-size=524288000')
        chromeOptions.add_argument(r'--media-cache-size=314572800')
        chromeOptions.add_argument('log-level=3')

        if ENV_TYPE == 'pc':
            width = PC_ENV.get('width')
            height = PC_ENV.get('height')
            chromeOptions.add_argument(r"--user-agent="+PC_ENV.get('ua'))
        else:
            width = MOBILE_ENV.get('width')
            height = MOBILE_ENV.get('height')
            mobile_emulation = {"deviceMetrics": { "width": width, "height": height, "pixelRatio": 3.0 },"userAgent": MOBILE_ENV.get('ua') }
            chromeOptions.add_experimental_option("mobileEmulation", mobile_emulation)
        chromeOptions.add_argument('--window-size=%d,%d' % (width+16, height+89))
        self.size = [width, height]
        print self.size
        chrome = webdriver.Chrome(executable_path=os.path.join(BROWSEPATH,'chromedriver.exe'),chrome_options=chromeOptions)
        chrome.set_window_size(width+16, height+89)
        self.chrome = chrome
        return chrome

    def screenshot(self, msg='', rate=30):
        """
        拷屏
        :param msg: 自定义输出信息
        :param rate: 截图比例,30表示截图概率为30%
        :return: None
        """
        try:
            jscode = "(()=>{let div = document.documentElement.appendChild(document.createElement('div'));div.style.cssText = 'z-index:88888;border-radius:10px;font-size:16px;top:0;left:0;position:absolute;background:rgba(255,255,255,.9);padding:5px;color:#000';div.innerHTML='%s';setTimeout(()=>div.parentNode.removeChild(div),4000)})();" % msg
            self.runJs(jscode)
        except Exception:
            pass
        self.wait(2)
        if self.rnd(100) <= rate:
            if not os.path.isdir(r"C:\set\screen_capture"):
                os.makedirs(r"C:\set\screen_capture")
            self.chrome.get_screenshot_as_file(r"C:\set\screen_capture\chrome-%d.png" % int(time.time()))

    def randomClick(self):
        """
        Random Click
        :return: None
        """
        size = self.size
        scrWidth = int(size[0])
        scrHeight = int(size[1])
        r = 1 if self.rnd(2) else -1
        x = math.floor(scrWidth/2 + self.rnd2(scrWidth/2-1) * r)
        r = 1 if self.rnd(2) else -1
        y = math.floor(scrHeight/2 + self.rnd2(scrHeight/2-1) * r)
        obj = self.chrome.execute_script('try{cobj = document.elementFromPoint(arguments[0],arguments[1]);cobj.setAttribute("target","_top")}catch(e){};return cobj;', x, y)
        osize = obj.size
        width = osize['width']
        height = osize['height']
        r2 = 1 if self.rnd(2) else -1
        x2 = math.floor(width/2 + self.rnd2(width/2-1) * r2)
        r2 = 1 if self.rnd(2) else -1
        y2 = math.floor(height/2 + self.rnd2(height/2-1) * r2)
        action = ActionChains(self.chrome)
        action.move_to_element_with_offset(obj,int(x2),int(y2)).click().perform()

    def rndScrollClick(self,cssSelector = None):
        """
        随机滚屏点坐标
        :param cssSelector: CSS 选择器，当前页面匹配到元素并且成功执行随机点
        :return: None
        """
        log.info(u'Random Click!')
        isPc = False
        if ENV_TYPE == 'pc':
            isPc = True
        self.pageDown(self.rnd(1,4)) if isPc else self.touchUp(self.rnd(1,4))
        pageHeight = self.runJs('return document.body.scrollHeight')
        scrollHeight = self.rnd2(pageHeight)
        self.scrollTo(0, scrollHeight)
        targets = True if cssSelector is None else self.find(cssSelector)
        self.randomClick()

    # 点击元素
    def clickDom(self, obj):
        size = obj.size
        width = size['width']
        height = size['height']
        oneFiveWidth = math.floor(width/5)
        twoFiveWidth = math.floor(2*width/5)
        oneTwoHeight = math.floor(height/2)
        r = self.rnd(100)
        if r<90 :
            r2 = 1 if self.rnd(2) else -1
            x = math.floor(width/2 + self.rnd2(width/2-1) * r2)
            r2 = 1 if self.rnd(2) else -1
            y = math.floor(height/2 + self.rnd2(height/2-1) * r2)
        else :
            r2 = 1 if self.rnd(2) else -1
            x = twoFiveWidth + math.floor(oneFiveWidth/2 + self.rnd2(oneFiveWidth/2-1) * r2)
            r5 = 1 if self.rnd(5) else -1
            y = oneTwoHeight + math.floor(oneTwoHeight/2 + self.rnd2(oneTwoHeight/2-1) * r5)
        try:
            self.chrome.execute_script('target_obj = arguments[0];target_obj.scrollIntoViewIfNeeded(true);',obj)
        except:
            log.info('clickDom runjs err')
        self.wait(1,2)
        log.info(u'Click %s position:%d,%d' % (obj.tag_name,x,y))
        action = ActionChains(self.chrome)
        action.move_to_element_with_offset(obj,x,y).click().perform()



    def getProxyIp(self):
        pass

    def setProxyIp(self):
        pass

    def domShot(self, cssSelector):
        """
        dom元素截图
        :param cssSelector: 要截图的dom选择器
        :return:
        """
        from PIL import Image
        damaDir = os.path.join(CWDPATH,r'vercode')
        if not os.path.isdir(damaDir):
            os.makedirs(damaDir)
        fileName =  "%s-%s.png" % (time.strftime("%y%m%d%H%M%S", time.localtime()),str(random.randint(1000,9999)))
        damaPath = os.path.join(damaDir,fileName)
        target = self.find(cssSelector)[0]
        size = self.runJs('damaObj = arguments[0];damaObj.scrollIntoViewIfNeeded(true);return damaObj.getBoundingClientRect();',target)
        self.wait(2,3)
        self.chrome.get_screenshot_as_file(damaPath)
        left = int(size['left'])
        top = int(size['top'])
        right = int(size['right'])
        bottom = int(size['bottom'])
        im = Image.open(damaPath)
        im = im.crop((left, top, right, bottom))
        im.save(damaPath)
        return damaPath

    def scrollBy(self, x = 0, y = 100):
        """
        从当前位置，滚动指定距离
        :param x: 页面纵向距离
        :param y: 页面横向距离
        :return:
        """
        self.runJs('window.scrollBy(%d,%d)' % (x,y))

    def scrollTo(self, x = 0, y = 500):
        """
        滚动至离页面顶部的指定位置
        :param x: 页面纵向距离
        :param y: 页面横向距离
        :return:
        """
        self.runJs('window.scrollTo(%d,%d)' % (x,y))


    def mouseWheel(self, direct = 'down', winx=None, winy=None):
        """
        模拟滚轮
        :param direct:滚动方向默认向下
        :param winx:鼠标相对浏览器x轴位置,默认值浏览器中间
        :param winy:鼠标相对浏览器y轴位置,默认值浏览器中间
        :return:None
        """
        import win32con,win32gui,win32api
        try:
            hd_notepad = win32gui.FindWindow("Chrome_WidgetWin_1", r"%s - Google Chrome" % self.chrome.title)
            win32gui.SetForegroundWindow(hd_notepad)
            size = self.chrome.get_window_size()
            pos = self.chrome.get_window_position()
            delta = -120
            if winx and type(winx) == int:
                mouseX = pos['x'] + winx
            else:
                mouseX = pos['x']+size['width']/2
            if winy and type(winy) == int:
                mouseY = pos['y'] + winy
            else:
                mouseY = pos['y']+size['height']/2
            win32api.SetCursorPos((mouseX, mouseY))
            if direct != 'down':
                delta = 120
            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, delta, 0)
        except Exception as e:
            print str(e)

    def pageDown(self,n=0):
        """
        模拟按键盘PAGE_DOWN
        :param n: 按键次数
        :return:
        """
        while n >= 0:
            self.find('body')[0].send_keys(Keys.PAGE_DOWN)
            self.wait(0,1)
            n -= 1

    def pageUp(self,n=0):
        """
        模拟按键盘PAGE_UP
        :param n: 按键次数
        :return:
        """
        while n >= 0:
            self.find('body')[0].send_keys(Keys.PAGE_UP)
            self.wait(0,1)
            n -= 1

    def pcDrag(self, fr, argu2, argu3=None):
        """
        拖拽
        :param fr: 要拖动的元素
        :param argu2: 拖放的指定元素 或 要放置的坐标x轴,argu2为数字时,拖拽到指定坐标,否则拖动到指定元素
        :param argu3: 坐标y轴，拖动到指定坐标有效
        :return:
        """
        action = ActionChains(self.chrome)
        if isinstance(argu2, int):
            action.drag_and_drop_by_offset(fr, argu2, argu3).perform()
        else:
            action.drag_and_drop(fr, argu2).perform()

    def mouseover(self, elem):
        """
        模拟hover效果
        :param elem: 目标元素
        :return:
        """
        action = ActionChains(self.chrome)
        action.move_to_element(elem).perform()
        self.wait(2,3)



    def rnd(self, begin=0, end=0):
        """
        取随机数
        :param begin:
        :param end:
        :return:
        """
        if begin and not end:
            return random.randint(0,begin-1)
        else:
            return random.randint(begin,end-1)


    def rnd2(self, length):
        a = math.floor(random.random() * length)
        b = math.floor(random.random() * length)
        if a > b:
            return int(b)
        else:
            return int(a)

    def wait(self, min=0, max=0):
        """
        任务等待，
        如只传一个参数，则等待指定秒数
        如传递二个参数，则取min->max的随机值
        :param min: 最小等待时间
        :param max: 最大等待时间
        :return:
        """
        if min !=0 and max==0:
            time.sleep(min)
        else:
            time.sleep(random.randint(min, max))

    def find(self, selector):
        """
        根据css selector查找元素
        :param selector: css选择器
        :return: List
        """
        return self.chrome.find_elements_by_css_selector(selector)

    def findById(self, id):
        """
        根据id选中单个元素
        :param id: css id
        :return:
        """
        cssId = id.replace('#','')
        return self.chrome.find_element_by_id(id)

    def runJs(self, jscode, *arg):
        """
        植入js代码
        :param jscode: js代码
        :param arg: 参数
        :return:
        """
        if arg:
            return self.chrome.execute_script(jscode, *arg)
        else:
            return self.chrome.execute_script(jscode)

    def stop(self):
        try:
            self.chrome.execute_script('window.stop();')
        except Exception:
            log.error('window_stop err')

    def waitDomReady(self, css, t=40):
        """
        等待页面某个元素加载完成
        :param css: 目前元素选择器
        :param t: 最长等待时间
        :return:
        """
        try:
            def isfind(chrome):
                boolVar = chrome.find_elements_by_css_selector(css)
                if boolVar : return boolVar
            return WebDriverWait(self.chrome, t, 2).until(isfind)
        except Exception as e:
            log.error('element load timeout: %s ' % e.__str__())
            return None

    def readUrl(self, url, data='', referrer='', userAgent='', method = 'GET'):
        """
        触发请求
        :param url: 请求url
        :param data: post请求参数
        :param referrer: 请求来源
        :param userAgent: 请求ua
        :param method: 请求方法，默认为get
        :return:
        """
        try:
            if method == 'GET' :
                request = urllib2.Request(url)
            else:
                encodeData = urllib.urlencode(data)
                request = urllib2.Request(url = url, data=encodeData)
            if referrer != '':
                request.add_header('Referer', referrer)
            if userAgent != '':
                request.add_header('User-Agent', userAgent)
            response = urllib2.urlopen(request,timeout=30)
            content = response.read()
            response.close()
            return content
        except Exception as e:
            log.warning(u'readUrl error:' + str(e))
            return ''

    def getPageUrl(self):
        """
        返回当前页面的url
        :return:
        """
        return self.chrome.current_url

    def changeHandle(self):
        """
        关闭chrome旧标签
        :return:
        """
        winBeforeHandle = self.chrome.current_window_handle
        winHandles = self.chrome.window_handles
        if len(winHandles) == 1 : return True
        for handle in winHandles:
            if winBeforeHandle != handle:
                self.chrome.close()
                self.chrome.switch_to.window(handle)
                winBeforeHandle = handle
                break

class Bing(baseBing):
    def __init__(self):
        baseBing.__init__(self)

    def mscroll(self, direct='up', x=0, y=0):
        """
        移动端滚动
        :param direct:
        :param x:
        :param y:
        :return:
        """
        width = int(self.size[0])
        height = int(self.size[1])
        oneTwoH = math.floor(height/2)
        oneTwoW = math.floor(width/2)
        oneThreeH = math.floor(oneTwoH/3)
        oneThreeW = math.floor(oneTwoW/3)
        r1 = 1
        if direct != 'up' : r1 = -1
        if x==0:
            x = oneTwoW + math.floor(self.rnd(1,int(oneThreeW)) * r1)
        if y==0:
            y = height * r1 + math.floor(self.rnd(1,int(oneThreeH)) * r1)
        action = TouchActions(self.chrome)
        action.scroll(x,y).perform()

    def touchUp(self,n=0):
        while n >= 0:
            self.mscroll('up')
            n -= 1

    def touchDown(self,n=0):
        while n >= 0:
            self.mscroll('down')
            n -= 1

    def flick(self,obj=None):
        """
        划屏
        :param obj: 目标元素
        :return:
        """
        action = TouchActions(self.chrome)
        if obj != None:
            size = obj.size
            width = size['width']
            height = size['height']
            oneThreeH = math.floor(height/3)
            oneThreeW = math.floor(width/3)
            action.flick_element(obj,oneThreeW,oneThreeH*-1,600).perform()
        else:
            action.flick(1,500).perform()

    def tap(self, element):
        """
        移动端点击方法
        :param element: 目标元素
        :return:
        """
        action = TouchActions(self.chrome)
        action.tap(element).perform()
