import tkinter as tk
from nltk.sentiment import SentimentIntensityAnalyzer

# initialize the sentiment analyzer
sid = SentimentIntensityAnalyzer()

# get the sentiment from user input
def get_sentiment(review):
    
    score = sid.polarity_scores(review)
    
    compound_score = score['compound']
    
    if compound_score >= 0.05:
        
        sentiment = "Positive"
        
    elif compound_score <= -0.05:
        
        sentiment = "Negative"
        
    else:
        
        sentiment = "Neutral"
        
    return sentiment, compound_score

def submit():
    
    review = textbox.get("1.0", tk.END).strip()
    
    if review:
        
        sentiment, compound_score = get_sentiment(review)
        
        result_label.config(
            text=f"Sentiment: {sentiment}\nScore: {compound_score:.2f}\n\nScores range from 1 (Positive) to -1 (Negative)"
        )
        
    else:
        
        result_label.config(text="Please enter a review.")
    
    # Ensure the label is centered below the submit button
    result_label.place(x=300, y=250, anchor="center")

# call constructor
root = tk.Tk()

# set dimensions
root.geometry("600x350")

# set title
root.title("The Mirage Hotel Review Form")

# set label 
label = tk.Label(root, text="Thank you for staying at The Mirage Hotel. Please leave us a review below:", font=('Arial', 12))
label.pack(padx=20, pady=20)

# set user input text box
textbox = tk.Text(root, height=10, font=('Arial', 10))
textbox.pack(padx=10)

# set submit button
button = tk.Button(root, text="Submit", command=submit)
button.place(x=300, y=205, anchor="center")  # Centered horizontally

# display sentiment result
result_label = tk.Label(root, text="", font=('Arial', 12))
result_label.place(x=300, y=250, anchor="center")  # Centered below the button

# run the GUI until the user closes the window
root.mainloop()