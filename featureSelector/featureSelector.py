import OpenSSL
import ssl, socket
import subprocess
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta


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
    #return https_token(url)
    protocol = url.split("//")[0]
    if "https" not in protocol:
        return -1            # Phishing
    
    domain = url.split("//")[-1].split("/")[0]
    try:
        cert=ssl.get_server_certificate((domain, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        if(x509.has_expired()):
            return -1            # Phishing
        return 1                 # Legitimate
    
    except:
        return 0

# Feature #12 (1.1.12)
def https_token(url):
    domain = url.split("//")[-1].split("/")[0]
    
    if "https" in domain:
        return -1           # Phishing
    return 1                # Legitimate

# Feature #14 (1.2.2)
def url_of_anchor(url):
    
    # Return 1 when pdf file
    split_url = url.split(".")
    
    if split_url[len(split_url)-1] == "pdf":
        return 1

    html_file = "PI/phish-site.html"
    
    try:
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
    except:
        return 0

# Feature #15 (1.2.3)
def tag_links(url):
    
    # Return 1 when pdf file
    split_url = url.split(".")
    
    if split_url[len(split_url)-1] == "pdf":
        return 1
    
    html_file = "PI/phish-site.html"
    
    try:
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
    except:
        return 0


# Feature #23 (1.3.5)
def iframe(url):

    # Return 1 when pdf file
    split_url = url.split(".")
    
    if split_url[len(split_url)-1] == "pdf":
        return 1
    
    try:
        html_file = "PI/phish-site.html"
        if "<iframe" in open(html_file).read():
            return -1           # Phishing
        return 1                # Legitimate
    except:
        return 0


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

    if(len(links)==0):
        return 1
    return owned/len(links)

# Feature # 24 (1.4.1)
def domain_age(domain):
	apiKey = 'at_ihb1nWWpJYvoL2l985uMwz6WpeIJa'
	url_whois = 'https://www.whoisxmlapi.com/whoisserver/WhoisService?'\
    + 'domainName=' + domain + '&apiKey=' + apiKey + "&outputFormat=JSON"
	r = requests.get(url_whois)
	results = r.json()

	if("WhoisRecord" in results and "createdDate" in results['WhoisRecord']):
		createdDate = results['WhoisRecord']['createdDate']
		createdDate = createdDate.split('T')[0]
		createdDate = datetime.strptime(createdDate, '%Y-%m-%d')
		six_months = datetime.now() - timedelta(days=185)
		if createdDate < six_months:
			return 1
		else:
			return -1
	return 0


# Feature #2 (1.1.2)
def long_url(url):
	if len(url) > 50:
		return -1
	else:
		return 1
    
