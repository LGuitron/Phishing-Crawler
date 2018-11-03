from neuralnet import train_model
from Strausz import googleSearch
from keywordSelector import textRazor
from featureSelector import featureSelector
from featureSelector import featureDict
import subprocess
import numpy as np


#Possible negative features
# 14, 15
# Array of implemented features (numbers from 1 - 30 in order) 
implemented_features = [6,8,12,23]

'''
Registered sites
'''
# Train Tensorflow neural network (or load when previously trained)
model = train_model.train_model('data/trainset.csv', implemented_features , hidden_units = 30, num_iterations = 1000, learning_rate = 0.03)

# Get websites selected by the user
registered_websites = []
registered_websites.append("https://www.paypal.com/mx")

# Loop for each registered website
for r_website in registered_websites:
    print("\nLegitimate Website: " , r_website, "\n")
    
    keywords = googleSearch.getKeywordsArray(r_website, 0.5, 0.5)
    
    print("Keywords:")
    for i in range(2):
        print(keywords[i])
    
    print()
    
    json = googleSearch.googleSearch(keywords, "Paypal")
    # TODO get links only from google search

    
    '''
    Phishing sites
    '''
    # Get array of possible phishing websites for this registered website (Google Search)
    phishing_websites = []
    phishing_websites.append("https://www2.deloitte.com/mx/es.html")
    
    for p_website in phishing_websites:
        print("Phishing Website: ", p_website, "\n")

        # Run Scrapper for current phishing website
        p = subprocess.call(["scrapy", "crawl", "phishingSpider", "-a", "domain=" + p_website], cwd="PI")
        
        # Get feature vector (30 features) for current phishing website
        feature_vector = np.zeros((1, len(implemented_features)))
        for i in range(len(implemented_features)):
            feature_vector[0,i] = featureDict.dictionary[implemented_features[i]](p_website)

        
        print("Feature Vector: ")
        print(feature_vector)
        
        
        # Delete file obtained from scrapper
        #p = subprocess.call(["rm", "phish-site.html"], cwd="PI")

        # Make prediction for phishing probability for current site
        legit_probability = model.session.run(model.predict, feed_dict={model.X: feature_vector})
        print("Phishing probability: " , str.format('{0:.3f}', (1-legit_probability[0,0])*100), "%")
        
        
    # Upload Phishing website probabilities
