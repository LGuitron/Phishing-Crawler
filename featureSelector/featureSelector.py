#import urllib.request


# Feature 1.3.5
'''
def iframeTag(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()
    
    #print(mystr)
    if "iframe" in mystr:
        return -1           # Phishing
    return 1                # Legitimate
    
'''

'''
def iframeTag(url):
    
    if "<iframe" in open('../PI/phish_site.html').read():
        return -1           # Phishing
    return 1                # Legitimate
    
print(iframeTag("https://www.w3schools.com/html/html_iframe.asp"))
'''
#print(iframeTag('https://www.wikipedia.org/'))
