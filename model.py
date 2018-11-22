from neuralnet import train_model
from Strausz import googleSearch
from featureSelector import featureSelector
from featureSelector import featureDict
import subprocess
import numpy as np
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import pyrebase

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/": {"origins": "*"}})
app.config['CORS_HEADERS'] = '*'

config = {
    "apiKey": "AIzaSyAVXnv4lUTrQc7mBJai4eFTxGLYoDZzVUw",
    "authDomain": "deloitte-scrapper.firebaseapp.com",
    "databaseURL": "https://deloitte-scrapper.firebaseio.com",
    "storageBucket": "deloitte-scrapper.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

trusted_domains = []
suspicious_domains = []
suspicious_probabilities = []
phishing_domains = []
phishing_probabilities = []

def run(company_name, domain_2_check, implemented_features, trust_threshold, suspicious_threshold):



    # Array of implemented features (numbers from 1 - 30 in order) 
    #implemented_features = [2,6,8,12,23,24]

    # Train Tensorflow neural network (or load when previously trained)
    model = train_model.train_model('data/trainset.csv', implemented_features , hidden_units = 30, num_iterations = 1000, learning_rate = 0.03)

    # Get websites selected by the user
    registered_websites = []
    registered_websites.append(domain_2_check)

    # Get list of trusted domains to avoid checking them with the tensorflow model
    # trust_threshold = 0.01                                                # Trust websites if phishing probability is below this value

    domains_fb = db.child(company_name).child("trusted").get()
    domains_fb = domains_fb.val()
    
    # Add trusted domains if entry is already specified in DB
    if domains_fb != None:
        for key, value in domains_fb.items():
            trusted_domains.append(key.replace("_", "."))   # Trust websites if phishing probability is below this value

    # Loop for each registered website
    for r_website in registered_websites:
        print("\nLegitimate Website: ", r_website, "\n")

        keywords = googleSearch.getKeywordsArray(r_website, 0.5, 0.5)
        json = googleSearch.googleSearch(keywords, company_name)

        for entry in json:
            if(json[entry]['searchInformation']['totalResults'] != '0'):
                print("------------------------")
                print("Keyword: ", entry)
                print("------------------------")
                for item in json[entry]['items']:

                    p_website = item['link']
                    
                    # Check if this link is in the set of trusted domains
                    p_domain = p_website.split("//")[-1].split("/")[0]
                    if p_domain not in trusted_domains:

                        print("Phishing Website: ", p_website, "\n")

                        # Run Scrapper for current phishing website
                        p = subprocess.call(["scrapy", "crawl", "phishingSpider", "-a", "domain=" + p_website], cwd="PI")

                        # Get feature vector (30 features) for current phishing website
                        feature_vector = np.zeros((1, len(implemented_features)))
                        for i in range(len(implemented_features)):
                            feature_vector[0,i] = featureDict.dictionary[implemented_features[i]](p_website)

                        print("Feature Vector: ")
                        print(feature_vector)

                        # Make prediction for phishing probability for current site
                        legit_probability = model.session.run(model.predict, feed_dict={model.X: feature_vector})
                        print("Phishing probability: ", str.format('{0:.3f}', (1 - legit_probability[0, 0]) * 100), "%", "\n")

                        # Add domain to trusted domains if probability is below threshold
                        if (1 - legit_probability[0, 0] < trust_threshold):
                            trusted_domains.append(p_domain)
                        elif (1 - legit_probability[0, 0] < suspicious_threshold):
                            suspicious_domains.append(p_domain)
                            suspicious_probabilities.append(1 - legit_probability[0, 0])
                        else:
                            phishing_domains.append(p_domain)
                            phishing_probabilities.append(1 - legit_probability[0, 0])

    # Write list of trusted_domains in file at end of execution
    for item in trusted_domains:
        item = item.replace(".", "_")
        db.child(company_name).child("trusted").update({item: 0})

    for i in range(len(suspicious_domains)):
        item = suspicious_domains[i]
        prob = suspicious_probabilities[i]
        item = item.replace(".", "_")
        db.child(company_name).child("suspicious").update({item: prob})

    #for item in suspicious_domains:
    for i in range(len(phishing_domains)):
        item = phishing_domains[i]
        prob = phishing_probabilities[i]
        item = item.replace(".", "_")
        db.child(company_name).child("suspicious").update({item: prob})


# Helper function to get phishing probability of a given website
def getPhishingProbability(test_domains, implemented_features):
    
    model = train_model.train_model('data/trainset.csv', implemented_features , hidden_units = 30, num_iterations = 1000, learning_rate = 0.03)

    for p_website in test_domains:
        # Check if this link is in the set of trusted domains
        p_domain = p_website.split("//")[-1].split("/")[0]
        print("Phishing Website: ", p_website, "\n")

        # Run Scrapper for current phishing website
        p = subprocess.call(["scrapy", "crawl", "phishingSpider", "-a", "domain=" + p_website], cwd="PI")

        # Get feature vector (30 features) for current phishing website
        feature_vector = np.zeros((1, len(implemented_features)))
        for i in range(len(implemented_features)):
            feature_vector[0,i] = featureDict.dictionary[implemented_features[i]](p_website)

        print("Feature Vector: ")
        print(feature_vector)

        # Make prediction for phishing probability for current site
        legit_probability = model.session.run(model.predict, feed_dict={model.X: feature_vector})
        print("Phishing probability: ", str.format('{0:.3f}', (1 - legit_probability[0, 0]) * 100), "%", "\n")

# Possible negative features
# 14, 15
implemented_features = [2,6,8,12,23,24]
trust_threshold    = 0.01
suspicious_threshold = 0.30

# Get probability of a particular phishing website
'''
test_domains = ["http://aquarelas94.com/css/application/renewal/identity/try/upgrade/security/contents/index.php",
                "https://twitter.com/onedrive",
                "https://click.mail.onedrive.com/?qs=a39b03b50dc27ef245997bf2d6e37e2e4090b22aa32fe216a1217f7b36d2aab0eba1374eb62bc068b277b99fa462189788801b9d1bf8c1a0d8e31fd616643119",
                "http://ogofarm.com/CF",
                "http://stcroixlofts.com/inc/manager/config/auth/log/3ca9cf355a2b9e09f921b4634a78d907ZTk0ODhmYzU1YWY2ZTk4NTkzMjhhOWEzN2QzZjZlYmQ=/resolution/websc_login/",
                "http://marcoferno.com/po/order/order/biggyoff/",
                "http://pakital.com/bbbb/suntrustrequestuseridpassword.html",
                "http://pakital.com/bbbb/suntrust.html",
                "http://stcroixlofts.com/inc/manager/config/auth/log/66e74b07f09d780b0e0f87365716582cMzc3YjUyMTA2ZjE2ZDA4ZDk0MTgyNzZiOWJlZjZiY2E=/resolution/websc_login/",
                "http://bbfurnitureconcepts.com/sennottinsurance/fonts/",
                "http://jjohnson10.com/pdf/adobeCom/inc/",
                "http://stcroixlofts.com/inc/manager/config/auth/log/e5548beb55def8126c8980670deb857aZWYzYjI3MDA5NzFmZDVmNjNiYWEzZjdlMWVkNTNhODc=/resolution/websc_login/",
                "https://payqal-check-com.umbler.net/log/5f98ad632f858cb66bbf285691b789f1YjdjODRkM2E5ZWUwOGYyMDEyODI1YWI2NTFjNGY5NjU=/myaccount/websc_login/?country.x=US&locale.x=en_US",
                "http://www.kadirdekorasyon.com/wp-content/plugins/vwcleanerplugin/drama/",
                "https://dispute-webbsid71.redirectme.net/?k4mpl3ngzob"]
'''
#getPhishingProbability(test_domains, implemented_features)


# Look for phishing website based on company name an domain
run("Amazon", "https://www.amazon.com/", implemented_features, trust_threshold, suspicious_threshold)
run("Paypal", "https://www.paypal.com/mx/home", implemented_features, trust_threshold, suspicious_threshold)
run("Facebook", "https://www.facebook.com/", implemented_features, trust_threshold, suspicious_threshold)
run("Deloitte", "https://www2.deloitte.com/mx/es.html", implemented_features, trust_threshold, suspicious_threshold)
run("Microsoft", "https://onedrive.live.com/about/es-mx/", implemented_features, trust_threshold, suspicious_threshold)
