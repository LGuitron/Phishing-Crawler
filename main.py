from neuralnet import train_model
from keywordSelector import textRazor

'''
Registered sites
'''

# Train Tensorflow neural network (or load when previously trained)
model = train_model.train_model('data/trainset.csv', hidden_units = 30, num_iterations = 1000, learning_rate = 0.03)


# Get registered websites from database
registered_websites = []
registered_websites.append("https://www2.deloitte.com/mx/es.html")

# Loop for each registered website
for r_website in registered_websites:
    print("Registered Website: " , r_website)

    # Get webiste html tags from scrapper


    # Get keywords for each website (textRazor API)
    keywords = textRazor.getKeywordsArray(r_website, 0.5, 0.5)

    '''
    Phishing sites
    '''
    # Get array of possible phishing websites for this registered website


    # Get feature vector (30 features) for each possible phishing website




    # Get phishing probabilities for possible phishing sites


    # Upload info to database
