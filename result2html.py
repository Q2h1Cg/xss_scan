#!/usr/bin/python

import sys

html = open(sys.argv[1], "w")
result = [i.strip() for i in open("result.txt")]
div = "<div class='result'>%s</div><br>\n"
html.write("""<style>
.result {
border: 1px solid #ccc;
background: #ffff77;
padding: 10px;
}
</style>
""")
for i in result:
    html.write(div % i.replace(">", "&gt;").replace("<", "&lt;").replace(": ", "<br>", 1))
html.close()
