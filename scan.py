#!/usr/bin/python

import bs4
from bs4 import BeautifulSoup as BS 
import json
import re
import requests
import sys
import threading
import urllib2

class Thread(threading.Thread):
    """ """
    def __init__(self, func, args):
        super(Thread, self).__init__()
        self.func = func
        self.args = args
 
    def run(self):
        self.func(*self.args)

class XssScan(object):
    """ """
    def __init__(self, url, cookies):
        self.url = url
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36"}
        self.cookies = cookies
        self.urls = []
        self.payloads = json.load(open("payloads.json"))
        self.testUrls = {"betweenCommonTag": [],
            "betweenTitle": [],
            "betweenTextarea": [],
            "betweenXmp": [],
            "betweenIframe": [],
            "betweenNoscript": [],
            "betweenNoframes": [],
            "betweenPlaintext": [],
            "betweenScript": [],
            "betweenStyle": [],
            "utf-7": [],
            "inSrcHrefAction": [],
            "inScript": [],
            "inStyle": [],
            "inCommonAttr": [],
            "inMetaRefresh": []
        }
        self.result = []
        self.go()

    def judegCharset(self):
        """ """
        try:
            r = requests.get(self.url, headers=self.headers, cookies=self.cookies, timeout=3)
            soup = BS(r.text)
            r.close() 
        except Exception, e:
            pass
        else:
            try:
                if ("gb" in r.headers["content-type"].lower() or 
                ("utf" not in r.headers["content-type"].lower() and
                    bool(soup.meta) and "gb" in soup.meta["content"].lower())
                ):
                    self.enc = "gbk"
                else:
                    self.enc = "utf-8"
            except Exception, e:
                self.enc = "utf-8"

    def judgeOut(self, url, keyword, list_):
        """ """
        try:
            r = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=3)
            html = r.text
            r.close()
        except Exception, e:
            html = ""
        if keyword in html:
                list_.append(url)

    def findParas(self):
        """ """
        query = urllib2.urlparse.urlparse(self.url).query
        paras = query.split("&")
        testParas = {}

        for i in paras:
            if i == paras[0]:
                if "=" not in i:
                    testParas["?"+i] = "?"+i+"=ADC22F"
                elif i.endswith("="):
                    testParas["?"+i] = "?"+i+"ADC22F"
                else:
                    testParas["?"+i] = "?"+i.replace(i[i.rindex("=")+1:], "ADC22F")
            else:
                if "=" not in i:
                    testParas["&"+i] = "&"+i+"=ADC22F"
                elif i.endswith("="):
                    testParas["&"+i] = "&"+i+"ADC22F"
                else:
                    testParas["&"+i] = "&"+i.replace(i[i.rindex("=")+1:], "ADC22F")

        threads = [Thread(self.judgeOut, (self.url.replace(i, testParas[i]), "ADC22F", self.urls)) for i in testParas]
        for i in threads: i.start()
        for i in threads: i.join()

    def getChildrenTags(self, Tag, tagList):
        for i in Tag.children:
            if type(i) == bs4.element.Tag:
                tagList.append(i)
                self.getChildrenTags(i, tagList)
    
    def judgeLocation(self, url):
        """"""
        try:
            r = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=3)
            html = r.text
            r.close()
        except Exception, e:
            html = ""
        soup = BS(html)
        tagList = []
        self.getChildrenTags(soup, tagList)

        re_key = re.compile("ADC22F")
        if soup.findAll(text=re_key):
            for i in soup.findAll(text=re_key):
                if i.findParent("title"):
                    self.testUrls["betweenTitle"].append(url)
                elif i.findParent("textarea"):
                    self.testUrls["betweenTextarea"].append(url)
                elif i.findParent("xmp"):
                    self.testUrls["betweenXmp"].append(url)
                elif i.findParent("iframe"):
                    self.testUrls["betweenIframe"].append(url)
                elif i.findParent("noscript"):
                    self.testUrls["betweenNoscript"].append(url)
                elif i.findParent("noframes"):
                    self.testUrls["betweenNoframes"].append(url)
                elif i.findParent("plaintext"):
                    self.testUrls["betweenPlaintext"].append(url)
                elif i.findParent("script"):
                    self.testUrls["betweenScript"].append(url)
                elif i.findParent("style"):
                    self.testUrls["betweenStyle"].append(url)
                else:
                    self.testUrls["betweenCommonTag"].append(url)
        
        if  soup.findAll(name="meta", attrs={"http-equiv": "Refresh", "content": re.compile("ADC22F")}):
            self.testUrls["inMetaRefresh"].append(url)
        
        if html.startswith("ADC22F"):
                self.testUrls["utf-7"].append(url)

        for i in tagList:
            for j in i.attrs:
                if "ADC22F" in i.attrs[j]:
                    self.testUrls["inCommonAttr"].append(url)

                    if j in ["src", "href", "action"] and i.attrs[j].startswith("ADC22F"):
                        self.testUrls["inSrcHrefAction"].append(url)
                    elif (j.startswith("on") or 
                        (j in ["src", "href", "action"] and i.attrs[j].startswith("javascript:"))
                    ):
                        self.testUrls["inScript"].append(url)
                    elif j == "style":
                        self.testUrls["inStyle"].append(url)

    def confirmParentTag(self,soup):
        for i in soup.findAll("x55test"):
            for j in i.parents:
                if j.name in ("title", "textarea", "xmp",
                    "iframe", "noscript", "noframes", "plaintext"):
                    return False
        return True

    def confirmInScript(self, soup, payload):
        tagList = []
        self.getChildrenTags(soup, tagList)
        for i in tagList:
            for j in i.attrs:
                if j.startswith("on") and payload in i.attrs[j]:
                    return True
        return False

    def testSinglePayload(self, url, location, payload):
        """ """
        url1 = url.replace("ADC22F", urllib2.quote(payload))
        try:
            r = requests.get(url1, headers=self.headers, cookies=self.cookies, timeout=3)
            html = r.text
            r.close()
        except Exception, e:
            html = ""
        soup = BS(html)
        if (location in ("betweenCommonTag", "betweenTitle", "betweenTextarea", 
            "betweenXmp", "betweenIframe", "betweenNoscript", "betweenNoframes", 
            "betweenPlaintext") 
        and soup.findAll("x55test") and self.confirmParentTag(soup)):
            self.result.append("[%s] [%s]: %s" % (location, payload, url1))

        if (location == "betweenScript" and (soup.findAll("x55test") 
            or soup.findAll(name="script", text=re.compile(r"[^\\]%s" % payload.replace("(", "\(").replace(")", "\)")))
            )
        ):
            self.result.append("[%s] [%s]: %s" % (location, payload, url1))

        if (location == "betweenScript" and self.enc == "gbk" and
            soup.findAll(name="script", text=re.compile(r"\\%s" % payload.replace("(", "\(").replace(")", "\)")))
        ):
            self.result.append("[GBK] [%s] [%s]: %s" % (location, payload, url1))

        if (location == "betweenStyle" and (soup.findAll("x55test") or 
            soup.findAll(name="style", text=re.compile("%s" % payload.replace(".", "\.").replace("(", "\(").replace(")", "\)")))
            )
        ):
            self.result.append("[%s] [%s]: %s" % (location, payload, url1))

        if (location == "inMetaRefresh" and soup.findAll(name="meta", attrs={"http-equiv": "Refresh", "content": re.compile(payload)})):
            self.result.append("[%s] [%s]: %s" % (location, payload, url1))

        if location == "utf-7" and html.startswith("+/v8 +ADw-x55test+AD4-"):
            self.result.append("[%s] [%s]: %s" % (location, payload, url1))

        if (location == "inCommonAttr" and (soup.findAll("x55test") or 
            soup.findAll(attrs={"x55test": re.compile("x55")}))
        ):
            self.result.append("[%s] [%s]: %s" % (location, payload, url1))

        if (location == "inSrcHrefAction" and (soup.findAll(attrs={"src": re.compile("^(%s)" % payload)})
            or soup.findAll(attrs={"href": re.compile("^(%s)" % payload)})
            or soup.findAll(attrs={"action": re.compile("^(%s)" % payload)}))
        ):
            self.result.append("[%s] [%s]: %s" % (location, payload, url1))

        if (location == "inScript" and self.confirmInScript(soup, payload)):
            self.result.append("[%s] [%s]: %s" % (location, payload, url1))

        if (location == "inStyle" and
            soup.findAll(attrs={"style": re.compile("%s" % payload.replace(".", "\.").replace("(", "\(").replace(")", "\)"))})
        ):
            self.result.append("[%s] [%s]: %s" % (location, payload, url1))

    def testXss(self, url, location):
        """ """
        threads = []
        for i in self.payloads[location]:
            threads.append(Thread(self.testSinglePayload, (url, location, i)))
        for i in threads:
            i.start()
        for i in threads:
            i.join()

    def go(self):
        """ """
        self.findParas()
        self.judegCharset()

        threads = [Thread(self.judgeLocation, (i,)) for i in self.urls]
        for i in threads: i.start()
        for i in threads: i.join()

        for i in self.testUrls:
            if self.testUrls[i]:
                self.testUrls[i] = list(set(self.testUrls[i]))

        threads = [Thread(self.testXss, (j, i)) for i in self.testUrls for j in self.testUrls[i]]
        for i in threads: i.start()
        for i in threads: i.join()

        for i in self.result:
            print i

def main():
    if len(sys.argv) == 3:
        url = sys.argv[1]
        cookies = {}
        cookies_text = open(sys.argv[2]).read().split("; ")
        for i in cookies_text:
            cookies[i.split("=")[0]] = i.split("=")[1] 

        xs = XssScan(url, cookies)

if __name__ == '__main__':
    main()