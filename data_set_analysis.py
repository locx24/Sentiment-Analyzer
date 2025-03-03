import pandas as pd  
import nltk  
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize  
from nltk.sentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# load the dataset
df = pd.read_csv("tripadvisor_hotel_reviews.csv")

# sample a subset of the data (1000 rows. dataset contains a total 20,491 reviews)
df_sample = df.sample(n=1000, random_state=42)

# generate time interval
df_sample['Date'] = pd.date_range(start='2022-01-01', periods=len(df_sample), freq='D')

# text preprocessing performing tokenization and removal of stopwords
stop_words = set(stopwords.words("english"))

# function to preprocess the reviews
def preprocess_text(text):
    
    # tokenize the text
    tokens = word_tokenize(text)
    
    # remove stopwords and non-alphabetical words
    tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]
    
    return tokens

# apply preprocessing to the Review column
df_sample['processed_review'] = df_sample['Review'].apply(preprocess_text)

#-------------------------------------------------------------------------------------------------------------DATA NOW PREPROCESSED 

# initialize the sentiment intensity analyzer to perform sentiment analysis
sid = SentimentIntensityAnalyzer()

# function to categorize sentiment
def categorize_sentiment(text):
    
    # get the sentiment scores for the text
    scores = sid.polarity_scores(' '.join(text))  # Join the tokens back into a single string for analysis
    
    # get the compound score
    compound_score = scores['compound']
    
    # categorize sentiment based on the compound score
    if compound_score >= 0.05:
        
        return 'Positive'
    elif compound_score <= -0.05:
        
        return 'Negative'
    
    else:
        
        return 'Neutral'

# apply sentiment categorization to the 'processed_review' column
df_sample['sentiment'] = df_sample['processed_review'].apply(categorize_sentiment)

# ---------------------------------------------------------------------------------------------------------------ACCURACY METRIC

# map sentiment labels to integers
df_sample['sentiment_label'] = df_sample['sentiment'].map({'Positive': 1, 'Neutral': 0, 'Negative': -1})

# limit features to 500 most relevant words
vectorizer = TfidfVectorizer(max_features=500)  

# convert the processed review text into a numerical value
X = vectorizer.fit_transform(df_sample['processed_review'].apply(lambda x: ' '.join(x)))

# get the sentiment labels
y = df_sample['sentiment_label']

# split the dataset and train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# initialize a logistic regression model
log_model = LogisticRegression(random_state=0, max_iter=500)

# train the logistic regression model using the training dataset
log_model.fit(X_train, y_train)

# make predictions on the test dataset
y_pred = log_model.predict(X_test)

# calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)

# print the model's accuracy to the console
print(f'Logistic Regression Accuracy: {accuracy:.2f}')

# ---------------------------------------------------------------------------------------------------------------DESCRIPTIVE METHODS


# sentiment distribution
sentiment_counts = df_sample['sentiment'].value_counts()

# 1. bar chart for sentiment distribution

plt.figure(figsize=(6, 4))
sentiment_counts.plot(kind='bar', color=['#4CAF50', '#FFC107', '#F44336'])

# set chart titles
plt.title('Sentiment Distribution of Reviews')
plt.xlabel('Sentiment')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

# 2. line graph for Average Review Rating Over Time 

plt.figure(figsize=(10, 6))
df_sample.groupby(df_sample['Date'].dt.to_period("M"))['Rating'].mean().plot(kind='line', marker='o', color='blue')

# set chart titles
plt.title('Average Review Rating Over Time')
plt.xlabel('Date')
plt.ylabel('Average Rating')

# format chart
plt.xticks(rotation=45)

# Set y-axis scale from 1 to 5
plt.ylim(1, 5)

plt.tight_layout()
plt.show()

# 3. word cloud for most common words

# combine all processed reviews into a single string
all_reviews = ' '.join(df_sample['processed_review'].apply(lambda x: ' '.join(x)))

# generate the word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_reviews)

# set chart titles and display the word cloud
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Common Words in Reviews')
plt.tight_layout()
plt.show()