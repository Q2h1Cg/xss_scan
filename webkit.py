#! /usr/bin/env python
#! encode=utf-8

import sys
import signal
import urllib
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import QNetworkCookieJar, QNetworkCookie
from PyQt4.QtWebKit import QWebPage

_cookieJar = QNetworkCookieJar()
_cookie = 'a=m;\nb=1;\nc=test'

def userAgent(url):
	return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36"

def alert(frame, message):
	print message
	pass

def consoleMessage(s1, i, s2):
	pass

class MyWebPage(QWebPage):
	def __init__(self, url, app):
		global _cookieJar, cookie
		self._url = url
		self._app = app
		QWebPage.__init__(self)
		self.networkAccessManager().setCookieJar(_cookieJar)
		_cookieJar.setCookiesFromUrl(QNetworkCookie.parseCookies(_cookie), QUrl(url))
		self.bind()
	
	def bind(self):
		self.userAgentForUrl = userAgent
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		self.connect(self, SIGNAL("loadFinished(bool)"), self._finished_loading)
		self.javaScriptAlert = alert
		self.javaScriptPrompt = alert
		self.javaScriptConfirm = alert
		self.javaScriptConsoleMessage = consoleMessage
		self.mainFrame().load(QUrl(self._url))

	def _finished_loading(self, result):
		html = self.mainFrame().toHtml().toUtf8()
		print html
		self._app.quit()
	

def getUrl():
	if len(sys.argv) == 2:
		return urllib.unquote(sys.argv[1])
	return ""

def main():
	app = QApplication([])
	url = getUrl()
	if len(url) != 0:
		page = MyWebPage(url, app)
		sys.exit(app.exec_())

if __name__ == "__main__":
	main()
