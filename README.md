XSS Scan  
Author: Chu  
Mail: chuhades#gmail.com

扫描xss 的python 脚本，时间紧，webkit 还没有整合进去，模块已经写完了，有需要的自己修改一下（感谢Monster 提供webkit 模块）。

目录结构：
```
chu@system:~/Dropbox/tools/xssscan$ tree
.
├── geturls.py              ----url 去重
├── loadurls.py             ----加载url
├── payloads.json           ----payloads
├── README.md               ----readme
├── result2html.py          ----结构转成html格式，便于检查
├── scan.py                 ----核心脚本
├── scan.py.urllib2         ----换用urllib2 模块，无cookies
└── webkit.py               ----webkit 模块
```

说明：

- scan.py.urllib2 是以前的版本，没有cookies 机制，采用urllib2 模块，scan.py 对其升级为requests 模块，并添加cookies。之所以保留scan.py.urllib2 是因为一些不需要cookies 的单个url 用它扫描方便些，批量扫描的话，还是建议使用scan.py。  
- pyayloads中，BetweenScript 和 InScript 中的```x55test```误报较高，如不需要可自行去掉。（建议保留，这两个payload 有时会带来惊喜～）

用法:
 
对于单个url：
```
chu@system:~/Dropbox/tools/xssscan$ ./scan.py.urllib2 "http://192.168.1.7/xss.php?x"
[inCommonAttr]: http://192.168.1.7/xss.php?x=%22%20x55test%3Dx55
[betweenCommonTag]: http://192.168.1.7/xss.php?x=%3Cx55test%3E
[utf-7]: http://192.168.1.7/xss.php?x=%2B/v8%20%2BADw-x55test%2BAD4-
[betweenCommonTag]: http://192.168.1.7/xss.php?x=--%3E%3Cx55test%3E
[inCommonAttr]: http://192.168.1.7/xss.php?x=%22%3E%3Cx55test%3E
[inCommonAttr]: http://192.168.1.7/xss.php?x=%27%3E%3Cx55test%3E
[inCommonAttr]: http://192.168.1.7/xss.php?x=%3E%3Cx55test%3E
[betweenScript]: http://192.168.1.7/xss.php?x=x55test%281%29

或者：
chu@system:~/Dropbox/tools/xssscan$ ./scan.py "http://192.168.1.7/xss.php?x" cookies.txt
[utf-7] [+/v8 +ADw-x55test+AD4-]: http://192.168.1.7/xss.php?x=%2B/v8%20%2BADw-x55test%2BAD4-
[betweenCommonTag] [--><x55test>]: http://192.168.1.7/xss.php?x=--%3E%3Cx55test%3E
[betweenCommonTag] [<x55test>]: http://192.168.1.7/xss.php?x=%3Cx55test%3E
[inCommonAttr] [" x55test=x55]: http://192.168.1.7/xss.php?x=%22%20x55test%3Dx55
[betweenScript] [x55test(1)]: http://192.168.1.7/xss.php?x=x55test%281%29
[inCommonAttr] ["><x55test>]: http://192.168.1.7/xss.php?x=%22%3E%3Cx55test%3E
[inCommonAttr] ['><x55test>]: http://192.168.1.7/xss.php?x=%27%3E%3Cx55test%3E
[inCommonAttr] [><x55test>]: http://192.168.1.7/xss.php?x=%3E%3Cx55test%3E

其中 cookies.txt 为你访问目标站点时的cookies。
```
批量urls：
如果你抓取了一定数量的url，可以通过loadurls.py 进行批量测试：
```
chu@system:~/Dropbox/tools/xssscan$ ./loadurls.py urls.txt cookies.txt 
[inCommonAttr] [" x55test=x55]: http://192.168.1.7/xss.php?x=%22%20x55test%3Dx55
[betweenCommonTag] [<x55test>]: http://192.168.1.7/xss.php?x=%3Cx55test%3E
[betweenCommonTag] [--><x55test>]: http://192.168.1.7/xss.php?x=--%3E%3Cx55test%3E
[utf-7] [+/v8 +ADw-x55test+AD4-]: http://192.168.1.7/xss.php?x=%2B/v8%20%2BADw-x55test%2BAD4-
[inCommonAttr] ["><x55test>]: http://192.168.1.7/xss.php?x=%22%3E%3Cx55test%3E
[inCommonAttr] [><x55test>]: http://192.168.1.7/xss.php?x=%3E%3Cx55test%3E
[inCommonAttr] ['><x55test>]: http://192.168.1.7/xss.php?x=%27%3E%3Cx55test%3E
[betweenScript] [x55test(1)]: http://192.168.1.7/xss.php?x=x55test%281%29
[http://192.168.1.7/xss.php?x] Finished 50.00% ...
[betweenScript] [x55test(1)]: http://www.baidu.com/s?wd=x55test%281%29&rsv_spt=1&issp=1&rsv_bp=0&ie=utf-8&tn=baiduhome_pg&rsv_sug3=3&inputT=765
[http://www.baidu.com/s?wd=xxxx&rsv_spt=1&issp=1&rsv_bp=0&ie=utf-8&tn=baiduhome_pg&rsv_sug3=3&inputT=765] Finished 100.00% ...

其中：urls.txt 为你抓到的urls， cookies.txt 为访问目标站点时的cookies。（注：脚本没有自动去除空行，所以结尾的换行符要手动去掉，你也可以自己修改loadurls.py 判断以下是否为空。）

扫描完毕后，会在目录下生成result.txt，即为结果。
```