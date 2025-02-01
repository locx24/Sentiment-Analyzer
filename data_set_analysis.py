import pandas as pd  
import nltk  
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize  
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("tripadvisor_hotel_reviews.csv")

# Sample a subset of the data (100 rows)
df_sample = df.sample(n=100, random_state=42)

# Display the first few rows
print(df_sample.head())

# Check for missing values
print(df_sample.isnull().sum())

# Text Preprocessing: Tokenization and removal of stopwords
stop_words = set(stopwords.words("english"))

# Function to preprocess the reviews
def preprocess_text(text):
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords and non-alphabetical words
    tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]
    
    return tokens

# Apply preprocessing to the 'Review' column
df_sample['processed_review'] = df_sample['Review'].apply(preprocess_text)

# Check the results
print(df_sample[['Review', 'processed_review']].head())

#------------------------------------------------------------------------------------------------------DATA NOW PREPROCESSED 

# Initialize the Sentiment Intensity Analyzer to perform sentiment analysis
sid = SentimentIntensityAnalyzer()

# Function to categorize sentiment
def categorize_sentiment(text):
    
    # Get the sentiment scores for the text
    scores = sid.polarity_scores(' '.join(text))  # Join the tokens back into a single string for analysis
    
    # Extract the compound score
    compound_score = scores['compound']
    
    # Categorize sentiment based on the compound score
    if compound_score >= 0.05:
        
        return 'Positive'
    elif compound_score <= -0.05:
        
        return 'Negative'
    
    else:
        
        return 'Neutral'

# Apply sentiment categorization to the 'processed_review' column
df_sample['sentiment'] = df_sample['processed_review'].apply(categorize_sentiment)

# Check the results
print(df_sample[['Review', 'processed_review', 'sentiment']].head())

# ---------------------------------------------------------------------------------------------------------------DESCRIPTIVE METHODS

# Sentiment distribution
sentiment_counts = df_sample['sentiment'].value_counts()

# 1. Bar Chart - Sentiment Distribution
plt.figure(figsize=(6, 4))
sentiment_counts.plot(kind='bar', color=['#4CAF50', '#FFC107', '#F44336'])
plt.title('Sentiment Distribution of Reviews')
plt.xlabel('Sentiment')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# 2. Line Graph - Average Review Rating Over Time 

# If 'Date' is missing, using the index as a proxy for time
df_sample['ReviewIndex'] = df_sample.index

# Plotting average rating over 'ReviewIndex' (or 'Date' if available)
plt.figure(figsize=(8, 6))
df_sample.groupby('ReviewIndex')['Rating'].mean().plot(kind='line', color='blue')
plt.title('Average Review Rating Over Time')
plt.xlabel('Review Index')
plt.ylabel('Average Rating')
plt.tight_layout()
plt.show()

# 3. Word Cloud - Most Common Words

# Combine all processed reviews into a single string
all_reviews = ' '.join(df_sample['processed_review'].apply(lambda x: ' '.join(x)))

# Generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_reviews)

# Display the word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in Reviews')
plt.tight_layout()
plt.show()