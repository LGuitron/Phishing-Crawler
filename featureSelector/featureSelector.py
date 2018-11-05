import OpenSSL
import ssl, socket
import subprocess
from bs4 import BeautifulSoup


# Function that returns 0 (for not implemented functions)
def zeroFeature(url):
    return 0

# Feature #6 (1.1.6)
def pref_suf(url):
    domain = url.split("//")[-1].split("/")[0]
    
    if "-" in domain:
        return -1           # Phishing
    return 1                # Legitimate
    
# Feature #8 (1.1.8)
def ssl_state(url):
    
    # TODO do this wih openSSL library
    return https_token(url)
    '''
    protocol = url.split("//")[0]
    if "https" not in protocol:
        return -1            # Phishing
    
    domain = url.split("//")[-1].split("/")[0]
    cert=ssl.get_server_certificate((domain, 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    if(x509.has_expired()):
        return -1            # Phishing
    
    return 1                 # Legitimate
    '''

# Feature #12 (1.1.12)
def https_token(url):
    domain = url.split("//")[-1].split("/")[0]
    
    if "https" in domain:
        return -1           # Phishing
    return 1                # Legitimate

# Feature #14 (1.2.2)
def url_of_anchor(url):
    html_file = "PI/phish-site.html"
    
    with open(html_file) as myfile:
        html = myfile.read().replace('\n', '')
    
    soup = BeautifulSoup(html, "html.parser")
    
    links = []
    for tag in soup.find_all("a"):
        link = str(tag).split("href=\"")[-1].split("\"")[0]
        links.append(link)
    
    link_own = link_ownership(url,links)
    if link_own > 0.69:
        return 1            # Legitimate
    elif link_own > 0.33:
        return 0            # Suspicious
    else:
        return -1           # Phishing

# Feature #15 (1.2.3)
def tag_links(url):
    html_file = "PI/phish-site.html"
    
    with open(html_file) as myfile:
        html = myfile.read().replace('\n', '')
    
    soup = BeautifulSoup(html, "html.parser")
    
    links = []
    for tag in soup.find_all(["meta","script","link"]):
        link = str(tag).split("href=\"")[-1].split("\"")[0]
        links.append(link)
    
    link_own = link_ownership(url,links)
    if link_own > 0.69:
        return 1            # Legitimate
    elif link_own > 0.33:
        return 0            # Suspicious
    else:
        return -1           # Phishing


# Feature #23 (1.3.5)
def iframe(url):
    html_file = "PI/phish-site.html"
    if "<iframe" in open(html_file).read():
        return -1           # Phishing
    return 1                # Legitimate


# Feature #29 (1.4.6)
def links_to_page(url):
    p = subprocess.call(["lynx", "-dump", url, ">", "lynx.txt"])
    return 0

# Helper function to determine ownership percentage of a list of links
def link_ownership(url, links):
    owned = 0
    for link in links:
        if len(link) > 0:
            if link[0]=="/":
                owned += 1
                continue
            
            url_domain  = url.split("//")[-1].split("/")[0]
            link_domain = url.split("//")[-1].split("/")[0]
            if(url_domain==link_domain):
                owned += 1

    return owned/len(links)
    
