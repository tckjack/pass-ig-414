#!/usr/bin/env python

import subprocess


def identify(filename):
    # print filename
    cmd = ["identify",filename]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    # return (out, err)
    if(len(err) == 0):
        return out
    else:
        return "Error"

def getinfo(filename):
    info = identify(filename)
    info = info.split(" ")
    size = info[2]
    size = size.split("x")
    return size

def discard(filename):
    cmd = "rm %s" %(filename)
    subprocess.call(cmd, shell=True)

def border(inpath , outpath):
    cmd = ["convert",inpath,"-bordercolor","black","-border","10",outpath]
    # cmd = ["convert",inpath,"-channel","R","-level","33%","-channel","G","-level","33%",outpath]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    # return (out, err)
    if(len(err) == 0):
        error = "Success"
        return error
    else:
        error = err
        return error

def lomo(inpath , outpath):
    cmd = ["convert",inpath,"-channel","R","-level","33%","-channel","G","-level","33%",outpath]
    # cmd = ["convert",inpath,"-bordercolor","black","-border","10",outpath]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    # return (out, err)
    if(len(err) == 0):
        error = "Success"
        return error
    else:
        error = err
        return error

def lensFlare(inpath , outpath):
    size = getinfo(inpath)
    width = size[0]
    cmd = ["convert", "/var/www/html/filter/lensflare.png", "-resize", str(width)+"x", "/var/www/html/tmp/tmp.png"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    # return (out, err)
    if(len(err) == 0):
        cmd2 = ["composite", "-compose", "screen", "-gravity", "northwest", "/var/www/html/tmp/tmp.png",inpath , outpath]
        q = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out2, err2) = q.communicate()
        if(len(err2) == 0):
            error = "Success"
            return error
        else:
            error = err2
            return error
    else:
        error = err
        return error

def blackWhite(inpath , outpath):
    size = getinfo(inpath)
    width = size[0]
    height = size[1]
    cmd = ["convert", inpath, "-type", "grayscale", "/var/www/html/tmp/itm"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    # return (out, err)
    if(len(err) == 0):
        resize = width + "x" + height
        # print resize
        cmd2 = ["convert", "/var/www/html/filter/bwgrad.png", "-resize" , resize, "/var/www/html/tmp/tmp.png"]
        q = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out2, err2) = q.communicate()
        if(len(err2) == 0):
            cmd3 = ["composite", "-compose", "softlight", "-gravity", "center", "/var/www/html/tmp/tmp.png","/var/www/html/tmp/itm" , outpath]
            r = subprocess.Popen(cmd3, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out3, err3) = r.communicate()
            if(len(err3) == 0):
                error = "Success"
                return error
            else:
                error = err3
                return error
        else:
            error = err2
            return error
    else:
        error = err
        return error

def blur(inpath , outpath):
    cmd = ["convert",inpath,"-blur","0.5x2",outpath]
    # cmd = ["convert",inpath,"-channel","R","-level","33%","-channel","G","-level","33%",outpath]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    # return (out, err)
    if(len(err) == 0):
        error = "Success"
        return error
    else:
        error = err
        return error

def top(inpath , outpath, fontsize ,font,text):
    cmd = ["convert",inpath, "-background", "red", "-pointsize", fontsize ,"-font" ,font, "label:"+text, "+swap", "-gravity" ,"center", "-append", outpath]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    # return (out, err)
    if(len(err) == 0):
        error = "Success"
        return error
    else:
        error = err
        return error

def bottom(inpath , outpath, fontsize ,font,text):
    cmd = ["convert",inpath, "-background", "red", "-pointsize", fontsize ,"-font" ,font, "label:"+text, "-gravity" ,"center", "-append", outpath]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    # return (out, err)
    if(len(err) == 0):
        error = "Success"
        return error
    else:
        error = err
        return error


