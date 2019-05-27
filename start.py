# -*- encoding: utf-8 -*-
from base import Bing
me = Bing()


if __name__=='__main__':
    chrome = me.openChrome()

    ### 需打开的测试页面 ###
    chrome.get('https://www.baidu.com/')

    def taskFn():
        me.findById('kw').send_keys(u'百度')
        me.wait(2,4)
    taskFn()
