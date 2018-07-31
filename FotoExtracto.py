from lxml import etree as ElementTree
import sys
import os
import urllib.parse
import shutil


def process_slideshow(filename):
    tree = ElementTree.parse(filename)
    plist = tree.getroot()
    process_plist(plist)


def process_plist(plist):
    for key in plist.find('dict').findall('key'):
        if key.text == 'slides':
            process_slides(key.getnext())


def process_slides(slides):
    for slide in slides.findall('dict'):
        process_slide(slide)


def process_slide(slide):
    for key in slide.findall('key'):
        if key.text == 'visualItems':
            process_visualitem(key.getnext())


def process_visualitem(visualitem):
    for visualitemdict in visualitem.findall('dict'):
        for key in visualitemdict.findall('key'):
            if key.text == 'fileRef':
                process_fileref(key.getnext())


def process_fileref(fileref):
    for key in fileref.findall('key'):
        if key.text == 'originalURL':
            process_originalurl(key.getnext())


def process_originalurl(originalurl):
    if originalurl.tag == 'string':
        unquotedurl = urllib.parse.unquote(originalurl.text)
        parsedurl = urllib.parse.urlparse(unquotedurl)
        path = os.path.abspath(os.path.join(parsedurl.netloc, parsedurl.path))
        if os.path.exists(path):
            # print(path, '=>', outputpath)
            shutil.copy2(path, outputpath)
        else:
            print('MISSING:', path)


if len(sys.argv) != 2:
    print('Usage: python', sys.argv[0], 'slideshow.fms')
    exit(1)

slideshowpath = os.path.abspath(sys.argv[1])
plistpath = os.path.join(slideshowpath, 'Slideshow.plist')

outputpath = os.path.splitext(slideshowpath)[0]

if not os.path.exists(outputpath):
    os.makedirs(outputpath)

process_slideshow(plistpath)
