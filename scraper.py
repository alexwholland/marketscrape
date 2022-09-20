# Web Scraping
import requests
from bs4 import BeautifulSoup

# Sentiment Analysis
import nltk
#nltk.download()
import nltk.corpus
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

# Pattern Matching
import re

def sentiment_analysis(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
   
    if sentiment["compound"] >= 0.05:
        return("🙂 with {:.2f}% confidence".format(sentiment["pos"] * 100))
    elif sentiment["compound"] <= -0.05:
        return("🙁 with {:.2f}% confidence".format(sentiment["neg"] * 100))
    else:
        return("😐 with {:.2f}% confidence".format(sentiment["neu"] * 100))

def html_debug(soup):
    f = open("index.html", "w")
    f.write(soup.prettify())
    f.close()

def clean_text(text):
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|http\S+')
    tokenized = tokenizer.tokenize(text)
    tokenized = [word.lower() for word in tokenized]

    stop_words = stopwords.words('english')
    filtered = [word for word in tokenized if word not in stop_words and word.isalpha()]

    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word) for word in filtered]
    
    return " ".join(lemmatized)

def get_title(soup):
    title = soup.find("meta", {"name": "DC.title"})
    title_content = title["content"]

    return title_content

def get_description(soup):
    description = soup.find("meta", {"name": "DC.description"})
    description_content = description["content"]

    return clean_text(description_content)

def get_price(soup):
    spans = soup.find_all("span")
    price = re.search(r"\$[0-9]*[^<]*", str(spans[1])).group(0)

    return price

def create_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def main():
    url = input("Enter URL: ")
    shortened_url = re.search(r"(^.*)?\?", url).group(0)
    mobile_url = shortened_url.replace("www", "m")

    print("\nHow we feel about this listing: {}".format(sentiment_analysis(get_description(create_soup(url)))))
    print("Title: {}".format(get_title(create_soup(url))))
    print("Price: {}".format(get_price(create_soup(mobile_url))))

if __name__ == "__main__":
    main()