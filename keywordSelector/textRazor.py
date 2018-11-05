import textrazor

def getKeywordsArray(url, min_relevance_score, min_topic_score):

    # Array of keywords to return for google search
    keywords = []
    
    textrazor.api_key = "1f0ebd1fc796a631ec72919329071930fede6007817a81744071c643"
    client = textrazor.TextRazor(extractors=["entities", "topics"])
    response = client.analyze_url(url)

    for entity in response.entities():
        if entity.relevance_score > min_relevance_score and entity.id not in keywords:
            keywords.append(entity.id)

    for topic in response.topics():
        if topic.score > min_topic_score and topic.label not in keywords:
            keywords.append(topic.label)
    
    return keywords
    
#keywords = getKeywordsArray("https://www2.deloitte.com/mx/es.html", 0.5, 0.5)
#for word in keywords:
#    print(word)
