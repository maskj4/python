﻿
#-*-coding:utf-8-*-
'''
'''
import urllib.request,http.cookiejar,re
import json
class Login:
    def __init__(self, name, passwd):
        self.name = name
        self.passwd = passwd
    def login(self):
        cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')]
        resp=self.opener.open('https://www.baidu.com/')
        getapiUrl = "https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true"
        resp2=self.opener.open(getapiUrl)
        getapiRespHtml = resp2.read().decode("utf-8")
        foundTokenVal = re.search("bdPass\.api\.params\.login_token='(?P<tokenVal>\w+)';", getapiRespHtml)
        if foundTokenVal :
            tokenVal = foundTokenVal.group("tokenVal")
            print(tokenVal)

            staticpage = "http://tieba.baidu.com/tb/static-common/html/pass/v3Jump.html"
            baiduMainLoginUrl = "https://passport.baidu.com/v2/api/?login" 
            postDict = {
                        'charset':"utf-8",
                        'token':tokenVal,
                        'isPhone':"false",
                        'index':"0",
                        'staticpage': staticpage,
                        'loginType': "1",
                        'tpl': "mn",
##                        'callback': "parent.bd__pcbs__y1km65",
                        'username': self.name,   #鐢ㄦ埛鍚�
                        'password': self.passwd,   #瀵嗙爜
                        'mem_pass':"on",
                        "apiver":"v3",
                        "logintype":"basicLogin"
                        }
            postData = urllib.parse.urlencode(postDict);
            postData = postData.encode('utf-8')
            resp3=self.opener.open(baiduMainLoginUrl,data=postData)
##            for c in cj:
##                print(c.name,"="*6,c.value)
#             print(resp3.read().decode('utf-8'))
            res = self.opener.open('http://tieba.baidu.com/f/user/json_userinfo')
            ret = res.read().decode('gbk')
#             print(ret[0])
            if ret[0] != '{':
                print("login failed")
                return 
            val = ret[ret.index(':') + 1: ret.index(',')]
            if int(val) == 0:
                print("login success")
            else:
                print("login failed" )
                
    def getMember(self, tieba):
        url = 'http://tieba.baidu.com/bawu2/platform/listMemberInfo?word=' + urllib.parse.quote(tieba);
        resp = self.opener.open(url)
        print(resp.read().decode('gbk'));
    
if __name__=="__main__":
    print("="*10,"***")
    bd=Login('demo', '123456')
    bd.login()
    bd.getMember('中南大学')
 
