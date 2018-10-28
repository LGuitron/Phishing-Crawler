# Function that returns 0 (for not implemented functions)
def zeroFeature(url):
    return 0


# Feature # 23 (1.3.5)
def iframeTag(url):
    
    html_file = "PI/phish-site.html"
    
    
    if "<iframe" in open(html_file).read():
        return -1           # Phishing
    return 1                # Legitimate
