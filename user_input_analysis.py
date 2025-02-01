import tkinter as tk
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize the sentiment analyzer
sid = SentimentIntensityAnalyzer()

# get the sentiment from user input
def get_sentiment(review):
    
    # determine the sentiment category based on compound score
    score = sid.polarity_scores(review)
    compound_score = score['compound']
    
    if compound_score >= 0.05:
        sentiment =  "Positive"
    
    elif compound_score <= -0.05:
        sentiment = "Negative"
    
    else:
        sentiment = "Neutral"
        
    # return the user's sentiment and score
    return sentiment, compound_score

def submit():
    
    # store the user input from the textbox
    review = textbox.get("1.0", tk.END).strip()
    
    if review:
        
        sentiment,compound_score = get_sentiment(review)
        result_label.config(text=f"Sentiment: {sentiment}\nScore: {compound_score:.2f}\n\n Scores range from 1 (Positive) to -1 (Negative)")
        
    else:
        result_label.config(text="Please enter a review.", fg="red")

# call constructor
root = tk.Tk()

# set GUI dimensions 
root.geometry("600x350")

# set title
root.title("The Mirage Hotel Review Form")

# create and set label 
label = tk.Label(root, text= "Thank you for staying at The Mirage Hotel. Please leave us a review below:", font=('Arial', 12))
label.pack(padx=20, pady=20)

# create and set user input text box
textbox = tk.Text(root, height=10, font=('Arial', 10))
textbox.pack(padx=10)

# create and set submit button
button = tk.Button(root, text="Submit", command = submit)
button.place(x=260, y = 205)

# Label to display sentiment result
result_label = tk.Label(root, text="", font=('Arial', 12, 'bold'))
result_label.place(x=165, y=250)

# run the GUI until the user closes the window
root.mainloop()