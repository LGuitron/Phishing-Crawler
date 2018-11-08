from neuralnet import train_model
from Strausz import googleSearch
from keywordSelector import textRazor
from featureSelector import featureSelector
from featureSelector import featureDict
import subprocess
import numpy as np


def run(company_name, domain_2_check):

    #Possible negative features
    # 14, 15
    # Array of implemented features (numbers from 1 - 30 in order) 
    implemented_features = [2,6,8,12,23,24]

    # Train Tensorflow neural network (or load when previously trained)
    model = train_model.train_model('data/trainset.csv', implemented_features , hidden_units = 30, num_iterations = 1000, learning_rate = 0.03)

    # Get websites selected by the user
    registered_websites = []
    registered_websites.append(domain_2_check)

    # Get list of trusted domains to avoid checking them with the tensorflow model
    with open('trusted_domains.txt') as f:
        trusted_domains = f.readlines()
        trusted_domains = [x.strip() for x in trusted_domains] 
    trust_threshold = 0.01                                                # Trust websites if phishing probability is below this value


    # Loop for each registered website
    for r_website in registered_websites:
        print("\nLegitimate Website: " , r_website, "\n")
        
        keywords = googleSearch.getKeywordsArray(r_website, 0.5, 0.5)
        json = googleSearch.googleSearch(keywords, company_name)

        for entry in json:
            if(json[entry]['searchInformation']['totalResults'] != '0'):
                print("------------------------")
                print("Keyword: " , entry)
                print("------------------------")
                for item in json[entry]['items']:

                    p_website = item['link']

                    # Check if this link is in the set of trusted domains
                    p_domain = p_website.split("//")[-1].split("/")[0]
                    if p_domain not in trusted_domains:

                        print("Phishing Website: " , p_website, "\n")

                        # Run Scrapper for current phishing website
                        p = subprocess.call(["scrapy", "crawl", "phishingSpider", "-a", "domain=" + p_website], cwd="PI")
                        p = subprocess.call(["scrapy", "crawl", "spider", "-a", "domain=" + p_website], cwd="PI")

                        # Get feature vector (30 features) for current phishing website
                        feature_vector = np.zeros((1, len(implemented_features)))
                        for i in range(len(implemented_features)):
                            feature_vector[0,i] = featureDict.dictionary[implemented_features[i]](p_website)

                        
                        print("Feature Vector: ")
                        print(feature_vector)

                        # Make prediction for phishing probability for current site
                        legit_probability = model.session.run(model.predict, feed_dict={model.X: feature_vector})
                        print("Phishing probability: " , str.format('{0:.3f}', (1-legit_probability[0,0])*100), "%", "\n")

                        # Add domain to trusted domains if probability is below threshold
                        if (1-legit_probability[0,0] < trust_threshold):
                            trusted_domains.append(p_domain)

    # Write list of trusted_domains in file at end of execution
    with open('trusted_domains.txt', 'w') as f:
        for item in trusted_domains:
            f.write("%s\n" % item)

company_name   = "Paypal"
domain_2_check = "https://www.paypal.com"
run(company_name, domain_2_check)