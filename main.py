from neuralnet import train_model
from keywordSelector import textRazor
import subprocess
import numpy as np

'''
Registered sites
'''

# Train Tensorflow neural network (or load when previously trained)
#model = train_model.train_model('data/trainset.csv', hidden_units = 30, num_iterations = 1000, learning_rate = 0.03)


# Get websites selected by the user
registered_websites = []
registered_websites.append("https://www.paypal.com/mx")

# Loop for each registered website
for r_website in registered_websites:
    print("Registered Website: " , r_website)

    # Get webiste html tags from scrapper


    # Get keywords for each website (textRazor API)
    keywords = textRazor.getKeywordsArray(r_website, 0.5, 0.5)


    # Upload registered website info in database
    
    '''
    Phishing sites
    '''
    # Get array of possible phishing websites for this registered website (Google Search)
    phishing_websites = []
    #phishing_websites.append("https://www.wikipedia.org")
    phishing_websites.append("https://www.w3schools.com/html/html_iframe.asp")

    
    for p_website in phishing_websites:
        print("Phishing Website: ", p_website)

        # Run Scrapper for current phishing website
        p = subprocess.call(["scrapy", "crawl", "phishingSpider", "-a", "domain=" + p_website], cwd="PI")
        #p.wait()
        
        
        # Get feature vector (30 features) for current phishing website
        


        # Make prediction for phishing probability for current site


    # Upload Phishing website probabilities
