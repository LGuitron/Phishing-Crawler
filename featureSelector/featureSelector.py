import urllib.request

def iframeTag(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()
    
    #print(mystr)
    if "iframe" in mystr:
        return -1           # Phishing
    return 1                # Legitimate
    
    
    
print(iframeTag('https://www.w3schools.com/tags/tag_iframe.asp'))
print(iframeTag('https://www.wikipedia.org/'))
