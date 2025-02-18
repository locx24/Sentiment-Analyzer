## Setup Instructions

1. Install required Python libraries:  
   Open command line or a terminal within IDE
   Download Python3 from https://www.python.org/downloads/ or in the terminal run the commands below to confirm it's already installed: 

    python --version
    pip --version

2. In the terminal run the command below to install the pandas, nltk, scikit-learn, matplotlib, and wordcloud libraries:

   pip install pandas nltk scikit-learn matplotlib wordcloud

3. In the terminal run the command below to install the SSL certificate for Python:

    /Applications/Python\ 3.12/Install\ Certificates.command

4. Create a separate python file then copy and paste the code below. Then run this file to download the necessary NLTK datasets:

    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('punkt_tab')
    nltk.download('vader_lexicon')

5. The file created in step 4 can now be deleted as the "punkt" and "stopwords" libraries have successfully downloaded

6. Run the user_input_analysis.py file and leave a review of any sentiment

7. Your review will be evaluated and given a polarity sore. Additionally, the review will be classified as either Positive, Neutral, or Negative.
    

