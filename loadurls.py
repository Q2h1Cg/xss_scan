#!/usr/bin/python

import sys
from scan import XssScan

def scan():
    urls = [i.strip() for i in open(sys.argv[1])]
    cookies = {}
    cookies_text = open(sys.argv[2]).read().split("; ")
    for i in cookies_text:
        cookies[i.split("=")[0]] = i.split("=")[1] 
    n = 0
    for i in urls:
        xs = XssScan(i, cookies)
        f = open("result.txt", "a")
        for j in xs.result:
            f.write(j + "\n")
        f.close()

        n += 1
        print "[%s] Finished %.2f%% ..." % (i, ((100.0*n)/len(urls)))

scan()