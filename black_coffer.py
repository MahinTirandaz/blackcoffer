import numpy as np 
import re 
import os 
import pandas as pd
from nltk.tokenize import RegexpTokenizer , sent_tokenize
from urllib.request import urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import urllib.request,sys,time ,requests

import pandas as pd

# Correct file path for reading the Excel file
file_path = r'C:\Users\Mahin Tirandaz\Downloads\Input.xlsx'

# Read the Excel file
input_df = pd.read_excel(file_path)

def get_article_names(urls):
    titles = []
    for url in urls:
        # Extract the part of the URL after "insights.blackcoffer.com/"
        title_part = url.split("insights.blackcoffer.com/")[1]
        # Clean the title part by replacing hyphens with spaces and removing trailing slash if present
        title_clean = title_part.replace('-', ' ').strip('/')
        titles.append(title_clean)
    return titles

# Extract URLs from the dataframe
urls = input_df["URL"]

# Get the cleaned article names
urlsTitleDF = get_article_names(urls)
print(urlsTitleDF)

import zipfile
# Paths
zip_path = r'C:\Users\Mahin Tirandaz\Downloads\MasterDictionary-20240609T171450Z-001.zip'
extract_dir = r'C:\Users\Mahin Tirandaz\Downloads\MasterDictionary'
positiveWordsFile = r'C:\Users\Mahin Tirandaz\Downloads\positive-words.txt'

# Extract the ZIP file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Path to the extracted negative words file
negativeWordsFile = os.path.join(extract_dir, 'MasterDictionary', 'negative-words.txt')

# Loading positive words
with open(positiveWordsFile, 'r') as posfile:
    positivewords = posfile.read().lower()
positiveWordList = positivewords.split('\n')

# Loading negative words
with open(negativeWordsFile, 'r') as negfile:
    negativewords = negfile.read().lower()
negativeWordList = negativewords.split('\n')

print("Positive Words:", positiveWordList)
print("Negative Words:", negativeWordList)

url = "https://insights.blackcoffer.com/rising-it-cities-and-its-impact-on-the-economy-environment-infrastructure-and-city-life-by-the-year-2040-2"

page=requests.get(url , headers={"User-Agent": "XY"})  
soup = BeautifulSoup(page.text , 'html.parser')
#get title
title = soup . find("h1",attrs = { 'class' : 'entry-title'}).get_text()

#get article text
text = soup . find(attrs = { 'class' : 'td-post-content'}).get_text()
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

# Assuming you have defined the file paths somewhere in your code
positiveWordsFile = r'C:\Users\Mahin Tirandaz\Downloads\positive-words.txt'
negativeWordsFile = r'C:\Users\Mahin Tirandaz\Downloads\negative-words.txt'
stopWordsFile = r'C:\Users\Mahin Tirandaz\Downloads\StopWords_Generic.txt'

# Loading positive words
with open(positiveWordsFile, 'r') as posfile:
    positivewords = posfile.read().lower()
positiveWordList = positivewords.split('\n')

# Loading negative words
with open(negativeWordsFile, 'r', encoding="ISO-8859-1") as negfile:
    negativeword = negfile.read().lower()
negativeWordList = negativeword.split('\n')

# Loading stop words dictionary for removing stop words
with open(stopWordsFile, 'r') as stop_words:
    stopWords = stop_words.read().lower()
stopWordList = stopWords.split('\n')
stopWordList[-1:] = []

# Displaying the first 6 elements of each list
print(positiveWordList[:6], negativeWordList[:6], stopWordList[:6])

#tokenizeing module and filtering tokens using stop words list, removing punctuations
def tokenizer(text):
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    filtered_words = list(filter(lambda token: token not in stopWordList, tokens))
    return filtered_words

def positive_score (text):
  posword=0
  tokenphrase = tokenizer(text)
  for word in tokenphrase :
    if word in positiveWordList:
       posword+=1
      
    retpos = posword
    return retpos 

def negative_score (text):
  negword=0
  tokenphrase = tokenizer(text)
  for word in tokenphrase :
    if word in negativeWordList : negword +=1

    retneg = negword 
    return retneg

def polarity_score (positive_score , negative_score) :
  return (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
#################################################
def total_word_count(text):
    tokens = tokenizer(text)
    return len(tokens)
#############################################
def AverageSentenceLenght (text):
  Wordcount = len(tokenizer (text))
  SentenceCount = len (sent_tokenize(text))
  if SentenceCount > 0 : Average_Sentence_Lenght = Wordcount / SentenceCount

  avg = Average_Sentence_Lenght

  return round(avg)


# Counting complex words
def complex_word_count(text):
    tokens = tokenizer(text)
    complexWord = 0
    
    for word in tokens:
        vowels=0
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if(w=='a' or w=='e' or w=='i' or w=='o' or w=='u'):
                    vowels += 1
            if(vowels > 2):
                complexWord += 1
    return complexWord

def percentage_complex_word(text):
    tokens = tokenizer(text)
    complexWord = 0
    complex_word_percentage = 0
    
    for word in tokens:
        vowels=0
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if(w=='a' or w=='e' or w=='i' or w=='o' or w=='u'):
                    vowels += 1
            if(vowels > 2):
                complexWord += 1
    if len(tokens) != 0:
        complex_word_percentage = complexWord/len(tokens)
    
    return complex_word_percentage

def fog_index(averageSentenceLength, percentageComplexWord):
    fogIndex = 0.4 * (averageSentenceLength + percentageComplexWord)
    return fogIndex

URLS = input("Enter the URL: ")
URLS

import requests
from bs4 import BeautifulSoup

URLS = ["https://insights.blackcoffer.com/rising-it-cities-and-its-impact-on-the-economy-environment-infrastructure-and-city-life-by-the-year-2040-2/"]

corps = []
for url in URLS:
    page = requests.get(url, headers={"User-Agent": "XY"})
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Get title
    title = soup.find("h1", attrs={'class': 'entry-title'}).get_text()
    
    # Get article text
    text = soup.find(attrs={'class': 'td-post-content'}).get_text()
    
    # Process text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    corps.append(text)

print(corps)

# Functions to be defined for processing
def total_word_count(text):
    return len(text.split())

def percentage_complex_word(text):
    # Example function for percentage of complex words
    words = text.split()
    complex_words = [word for word in words if len(word) > 6]
    return len(complex_words) / len(words) * 100

def complex_word_count(text):
    words = text.split()
    return len([word for word in words if len(word) > 6])

def AverageSentenceLenght(text):
    sentences = text.split('.')
    words = text.split()
    return len(words) / len(sentences)

def positive_score(text):
    # Placeholder function for positive score
    return sum(1 for word in text.split() if word in ['good', 'great', 'positive', 'excellent'])

def negative_score(text):
    # Placeholder function for negative score
    return sum(1 for word in text.split() if word in ['bad', 'poor', 'negative', 'terrible'])

def polarity_score(pos, neg):
    return (pos - neg) / (pos + neg + 1)

# List of URLs to scrape
URLS = ["https://insights.blackcoffer.com/rising-it-cities-and-its-impact-on-the-economy-environment-infrastructure-and-city-life-by-the-year-2040-2/"]

corps = []
urlsTitleDF = []

for url in URLS:
    page = requests.get(url, headers={"User-Agent": "XY"})
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Get title
    title = soup.find("h1", attrs={'class': 'entry-title'}).get_text()
    urlsTitleDF.append(title)
    
    # Get article text
    text = soup.find(attrs={'class': 'td-post-content'}).get_text()
    
    # Process text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    corps.append(text)

# Check if both lists have the same length
assert len(corps) == len(urlsTitleDF), "The lengths of corps and urlsTitleDF do not match."

# Create DataFrame
df = pd.DataFrame({'title': urlsTitleDF, 'corps': corps})

# Apply functions to the DataFrame
df["total word count"] = df["corps"].apply(total_word_count)
df["percentage_complex_word"] = df["corps"].apply(percentage_complex_word)
df["complex_word_count"] = df["corps"].apply(complex_word_count)
df["AverageSentenceLenght"] = df["corps"].apply(AverageSentenceLenght)
df["positive_score"] = df["corps"].apply(positive_score)
df["negative_score"] = df["corps"].apply(negative_score)
df["polarity_score"] = np.vectorize(polarity_score)(df['positive_score'], df['negative_score'])

df

final = df.drop("corps" , 1)
final 