from datetime import datetime, timedelta
from google_play_scraper import Sort, reviews
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import nltk
from nltk.corpus import stopwords

# Downloading the NLTK stopwords 
nltk.download('stopwords')

# Defining a function to preprocess the text
def preprocess(text):
    # Add your custom preprocessing here (e.g., removing special characters, lowercasing)
    # For simplicity, we'll just lowercase the text in this example
    return text.lower()

package_name = "money.jupiter"

today = datetime.now()
date_threshold = today - timedelta(days=30)

# Fetching reviews for the app
review_results, continuation_token = reviews(
    package_name,
    lang='en',
    country='in',
    sort=Sort.NEWEST,
    count=5000,  # You can adjust the number of reviews to fetch
    filter_score_with=None  # Remove this line if you want to fetch all scores
)

# Creating a DataFrame from the reviews
df = pd.DataFrame(review_results)

# Filtering reviews with scores 1, 2, and 3
filtered_df = df[df['score'].isin([1, 2, 3])]

# Preprocessing the text
filtered_df['content'] = filtered_df['content'].apply(preprocess)

# Initializing the TF-IDF vectorizer with English stopwords
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Creating a TF-IDF matrix
tfidf_matrix = tfidf_vectorizer.fit_transform(filtered_df['content'])

# Performing NMF (Topic Modeling)
num_topics = 5
nmf_model = NMF(n_components=num_topics, random_state=42)
topics = nmf_model.fit_transform(tfidf_matrix)

# Adding a new column to the DataFrame to indicate the topic for each review
filtered_df['topic'] = topics.argmax(axis=1) + 1  # +1 to match topic indexing (1-based)

# Printing the top words for each topic
feature_names = tfidf_vectorizer.get_feature_names_out()
# Creating a dictionary to store reviews by topic
reviews_by_topic = {}

# Grouping reviews by topic
for topic_idx in range(1, num_topics + 1):
    topic_reviews = filtered_df[filtered_df['topic'] == topic_idx]
    reviews_by_topic[f"Topic {topic_idx}"] = topic_reviews[['score', 'content']]

# Calculating the percentage of reviews for each topic
total_reviews = len(filtered_df)
topic_percentages = {}

for topic_idx in range(1, num_topics + 1):
    topic_reviews_count = len(filtered_df[filtered_df['topic'] == topic_idx])
    percentage = (topic_reviews_count / total_reviews) * 100
    topic_percentages[f"Topic {topic_idx}"] = percentage

# Defining headers for each topic bracket
topic_headers = {
    1: "Customer Issues",
    2: "App Usage and Transactions",
    3: "Access and Permissions",
    4: "Mobile App Problems",
    5: "Account and Banking"
}

# Creating a Pandas Excel writer using XlsxWriter as the engine
excel_file_path = r"C:\Users\saket\Downloads\12Nov_reviews_by_topic.xlsx"
with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
    # Writing each group of reviews to a separate sheet in the Excel file with headers
    for topic, reviews in reviews_by_topic.items():
        # Get the header for the current topic or use a default header if not found
        header = topic_headers.get(int(topic.split()[-1]), f" {topic}")

        # Creating a DataFrame for the reviews
        df = pd.DataFrame(reviews)

        # Creating a new DataFrame with the header and percentage as the first rows
        header_df = pd.DataFrame([[header, f"Percentage: {topic_percentages[topic]:.2f}%"]],
                                 columns=['Header', ''])

        # Concatenating the header DataFrame, percentage DataFrame, and reviews DataFrame
        final_df = pd.concat([header_df, df], axis=0, ignore_index=True)

        # Writing the DataFrame to the Excel sheet
        final_df.to_excel(writer, sheet_name=f" {topic}", index=False)

print(f"Reviews by topic have been saved to {excel_file_path}")
