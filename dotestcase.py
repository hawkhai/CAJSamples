#encoding=utf8
import re, os, sys
reldirx, _lidir = "", []
while not _lidir and len(reldirx) <= 100:
    reldirx += "../"
    checkfunc = lambda idir: os.path.exists(reldirx+idir+"/pythonx/funclib.py")
    _lidir = [reldirx+idir for idir in os.listdir(reldirx) if checkfunc(idir)]
    assert len(_lidir) in (0, 1), _lidir
    if _lidir: reldirx = os.path.abspath(_lidir[0])
if not reldirx in sys.path: sys.path.append(reldirx)
from pythonx.funclib import *
import codecs

count = 0
countx = {
    True: [],
    False: [],
}

minv = 100
maxv = 0

def mainfile(fpath, fname, ftype):
    if not ftype in ("caj",):
        return
    exefile = r"D:\worktemp\caj2pdfx_final\caj2pdf64.exe"
    
    tcmd = "\"{}\" \"{}\"".format(exefile, fpath)
    fpage = bytesToString(popenCmd(tcmd), "gbk")

    global count
    count += 1

    result = fpage.startswith("result = true")
    pdfpath = re.findall(r'destfile = "(.*?\.pdf)"', fpage)[0]
    
    xdata = readfile(pdfpath)
    ydata = readfile(pdfpath+".pdf")
    i = 0
    while xdata[i] == ydata[i]:
        i += 1
    ix = i / len(xdata)
    global minv
    global maxv
    if ix < minv: minv = ix
    if ix > maxv: maxv = ix
    print(ix, minv, maxv)
    
    copyfile(pdfpath, pdfpath+".pdf")
    print(count, fpath)
    print(result, pdfpath)
    countx[result].append(fpath)
    #print(countx)
    if not result:
        os.remove(fpath)

def printx(xlist):
    xlist.sort()
    print("***" * 30)
    print(len(xlist))
    for i in xlist:
        print(i)

def main():
    searchdir(r"D:\worktemp\CAJSamples", mainfile)
    printx(countx[True])
    printx(countx[False])
    clearemptydir(r"D:\worktemp\CAJSamples")

    print(minv, maxv)

if __name__ == "__main__":
    main()
