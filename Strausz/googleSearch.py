import textrazor
import pyrebase
import requests

config = {
    "apiKey": "",
    "authDomain": "XXXXXXX",
    "databaseURL": "XXXXXXX",
    "storageBucket": "XXXXXXX"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyCNGghfsmXtrYn2VZrynpqHYPWwgCEtTtA&cx=004162974845821050489:wphk5ewujga&q='

keywords = []

def getKeywordsArray(url, min_relevance_score, min_topic_score):
    #textrazor.api_key = "1f0ebd1fc796a631ec72919329071930fede6007817a81744071c643"
    textrazor.api_key = "61c6b6644fcc630bd30a149e5d98eb762c57d10a0f390f519668ca88"
    client = textrazor.TextRazor(extractors=["entities", "topics"])
    response = client.analyze_url(url)

    for entity in response.entities():
        if entity.relevance_score > min_relevance_score and entity.id not in keywords:
            keywords.append(entity.id)

    for topic in response.topics():
        if topic.score > min_topic_score and topic.label not in keywords:
            keywords.append(topic.label)
    
    return keywords

def googleSearch():
    results = {}

    keywords = getKeywordsArray("https://www2.deloitte.com/mx/es.html", 0.4, 0.4)
    
    import textrazor
import pyrebase
import requests

config = {
    "apiKey": "",
    "authDomain": "XXXXXXX",
    "databaseURL": "XXXXXXX",
    "storageBucket": "XXXXXXX"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyCNGghfsmXtrYn2VZrynpqHYPWwgCEtTtA&cx=004162974845821050489:wphk5ewujga&q='

keywords = []

def getKeywordsArray(site_url, min_relevance_score, min_topic_score):
    textrazor.api_key = "1f0ebd1fc796a631ec72919329071930fede6007817a81744071c643"
    client = textrazor.TextRazor(extractors=["entities", "topics"])
    response = client.analyze_url(site_url)

    for entity in response.entities():
        if entity.relevance_score > min_relevance_score and entity.id not in keywords:
            keywords.append(entity.id)

    for topic in response.topics():
        if topic.score > min_topic_score and topic.label not in keywords:
            keywords.append(topic.label)
    
    return keywords

def googleSearch(keywords, company_name):
    results = {}

    #keywords = getKeywordsArray(site_url, 0.5, 0.5)

    for i in range(len(keywords)):
        word = keywords[i]
        #word = word.replace(" ", "%2520")
        googleUrl = url + word + company_name
        r = requests.get(googleUrl)
        results[word] = r.json()
    
    return results
    
    '''
    for word in keywords:
        word = word.replace(" ", "%2520")
        googleUrl = url + word + 'Deloitte'
        r = requests.get(googleUrl)
        results[word] = r.json()
    
    return results
    '''

#if __name__ == '__main__':
#    json = googleSearch("https://www2.deloitte.com/mx/es.html", "Deloitte")
#    print(json)
