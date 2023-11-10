# jupiter-googleplay-reviews
Google Play Reviews Analysis for Jupiter App

Author: Saketh Kilaru 
Last Updated: [11/10/2023]  

Introduction

This document outlines the analysis of Google Play reviews for the Jupiter app over the last 30 days. The objective is to categorize and analyze user feedback, providing insights into different topics and their percentages.

Code Overview

The analysis is conducted using a Python script (`topic_modelling.py`). The following libraries and tools are utilised:

- `google_play_scraper` for fetching Google Play reviews.
- `pandas` for data manipulation and analysis.
- `sklearn` for TF-IDF Vectorization and NMF.
- `nltk` for natural language processing (stopwords).

Steps

1. Fetching Reviews

Google Play reviews are fetched using the `google_play_scraper` library. The parameters used for fetching include the package name, language, country, sorting by newest, and fetching a count of 5000 reviews.

2. Preprocessing

Text preprocessing is applied to lowercase the text, ensuring uniformity in the subsequent analysis steps.

3. Topic Modeling

TF-IDF Vectorization and Non-negative Matrix Factorization (NMF) are employed for topic modelling. The script categorizes reviews into five topics based on content.

4. Topic Naming and Percentage Calculation

Topics are named according to identified themes, and the percentage of reviews for each topic is calculated.

5. Excel Export

Results are exported to an Excel file. Each sheet corresponds to a specific topic, with headers indicating the topic name and the percentage of reviews.

Topics and Headers

Topics are named as follows:

1. Customer Issues
2. App Usage and Transactions
3. Access and Permissions
4. Mobile App Problems
5. Account and Banking

Percentage Calculation

The percentage of reviews for each topic is calculated relative to the total number of filtered reviews.

Conclusion

This document provides a structured overview of the Google Play reviews analysis, from fetching to categorization and export. The Excel file serves as a reference for detailed analysis and insights.

Next Steps

Future improvements may involve reviewing and adjusting the topic modelling approach, changing the topics to be more specific, and increasing the amount of reviews we collect.



