#!/usr/bin/python

import sys
import urllib2

def get():
    l0 = sorted([i.strip() for i in open(sys.argv[1])])
    l1 = []
    l1.append(l0[0])

    for i in l0:
        a = [j.split("=")[0] for j in urllib2.urlparse.urlparse(i).query.split("&")]
        b = [j.split("=")[0] for j in urllib2.urlparse.urlparse(l1[-1]).query.split("&")]

        if urllib2.urlparse.urlparse(i).netloc+urllib2.urlparse.urlparse(i).path != urllib2.urlparse.urlparse(l1[-1]).netloc+urllib2.urlparse.urlparse(l1[-1]).path:
            l1.append(i)
        else:
            for j in a:
                if j not in b:
                    l1.append(i)
                    break

    f = open("urls.txt", "w")
    for i in l1:
        f.write(i + "\n")
    f.close()

get()