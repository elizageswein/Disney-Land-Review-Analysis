# -*- coding: utf-8 -*-

# Eliza Geswein
# 11/23/22


from textblob import TextBlob
import pandas as pd
import seaborn as sns

#reads csv file into dataframe
reviews_df = pd.read_csv('DisneylandReviews.csv', header = 1, encoding = 'latin-1')

def calc_rating(star_num):
    #groups based on num of stars in review
    ratings = ['positive', 'neutral', 'negative']    
    #star thresholds for rating groups        
    thresholds = [4, 3, 1]                                    
    
    #starts as negative by default
    rating = 'negative'                                       
    
    i = 0
    
    while i < len(thresholds) and star_num < thresholds[i]:   
        i += 1
    
    #assigns appropriate rating based on threshold
    if i < len(thresholds):                                   
        rating = ratings[i]
    
    return rating
   

def calc_sentiment(polarity):
    #groups based on review's calculated polarity
    sentiments = ['positive', 'neutral', 'negative']
    #polarity thresholds for sentiment groups
    thresholds = [0.05, -0.05, -1]                            
    
    #starts as negative by default
    sentiment = 'negative'
    
    i = 0
    
    while i < len(thresholds) and polarity < thresholds[i]:
        i += 1
    
    #assigns appropriate sentiment based on threshold
    if i < len(thresholds):
        sentiment = sentiments[i]
    
    return sentiment

#empty list for rating strings
ratings_column = []
#empty list for sentiment strings
sentiments_column = []
#empty list for True/False whether or not rating = sentiment
agree_column = []                                             

#initialize counter variables
agree_count = 0                                               
disagree_count = 0
five_star_agree = 0
four_star_agree = 0
five_star_disagree = 0
four_star_disagree = 0


for r in range(len(reviews_df)):   
    #stars variable of num of stars in specified column of df                         
    stars = reviews_df.iat[r, 1]    

    #calculate record's rating based on num of stars                          
    review_star_rating = calc_rating(stars)
    
    ratings_column.append(review_star_rating)                 
    
    #TextBlob variable of record's review text in specified column of df
    review_blob = TextBlob(reviews_df.iat[r, 4])    

    #polarity from sentiment analysis on TextBlob object
    #polarity on [-1, 1] scale from negative-positive        
    review_polarity = review_blob.sentiment.polarity   

    #calculates record's sentiment based on its polarity (negative/positive)       
    review_sentiment_rating = calc_sentiment(review_polarity) 
    
    #list of sentiment rating values
    sentiments_column.append(review_sentiment_rating)         
    
    #determines if rating returned by star value and rating returned by polarity value match or not
    if review_star_rating == review_sentiment_rating:      
        agree = 'True'                                       
        agree_count += 1   

        #if row's review was 5 or 4 stars, adds to 5 or 4 star agree count
        #used later for tables of 5 and 4 star reviews                                   
        if stars == 5:
            five_star_agree += 1

                                 
        if stars == 4:
            four_star_agree += 1                              
   
    else:
        agree = 'False'                                       
        disagree_count += 1 

        #if row's review was 5 or 4 stars, adds to 5 or 4 star agree count
        #used later for tables of 5 and 4 star reviews                                   
        if stars == 5:
            five_star_disagree += 1     
                      
        if stars == 4:
            four_star_disagree += 1 
    
    #list of agree True/False values                     
    agree_column.append(agree)                              
    
    
#assigns lists made to corresponding columns in df
reviews_df['Rating'] = ratings_column                                             
reviews_df['Sentiment'] = sentiments_column
reviews_df['Rating = Sentiment?'] = agree_column

#pct of reviews whose star rating and review sentiment agree/disagree
agree_percent = round((agree_count/(agree_count+disagree_count)*100),2)
disagree_percent = round((disagree_count/(agree_count+disagree_count)*100), 2)

#print frequency table with counts and pcts of agree vs. disagree
print("Star-Text Sentiment Agreement Table")
print(f'{" ":12} {"Number":<12} {"Percentage":<12}')
print(f'{" ":12} {"-"*12} {"-"*12}')
print(f'{"Agree":>12} {agree_count:<12} {agree_percent:<12}')
print(f'{"Disagree":>12} {disagree_count:<12} {disagree_percent:<12}')

#pct of 5 star reviews whose star rating and review sentiment agree/disagree
five_agree_percent = round((five_star_agree/(five_star_agree+five_star_disagree)*100), 2)
five_disagree_percent = round((five_star_disagree/(five_star_agree+five_star_disagree)*100), 2)

#print frequency table with counts and pcts of agree vs. disagree for 5 star reviews
print("\nFive Star Star-Text Sentiment Agreement Table")
print(f'{" ":12} {"Number":<12} {"Percentage":<12}')
print(f'{" ":12} {"-"*12} {"-"*12}')
print(f'{"Agree":>12} {five_star_agree:<12} {five_agree_percent:<12}')
print(f'{"Disagree":>12} {five_star_disagree:<12} {five_disagree_percent:<12}')


#repeat above for 4 star reviews
four_agree_percent = round((four_star_agree/(four_star_agree+four_star_disagree)*100), 2)
four_disagree_percent = round((four_star_disagree/(four_star_agree+four_star_disagree)*100), 2)

print("\nFour Star Star-Text Sentiment Agreement Table")
print(f'{" ":12} {"Number":<12} {"Percentage":<12}')
print(f'{" ":12} {"-"*12} {"-"*12}')
print(f'{"Agree":>12} {four_star_agree:<12} {four_agree_percent:<12}')
print(f'{"Disagree":>12} {four_star_disagree:<12} {four_disagree_percent:<12}')


#categories for bar chart based on star rating
values = ['Overall', 'Five Star', 'Four Star']

#values for bar chart 
#pct of reviews whose star rating and review sentiment agree
counts = [agree_percent, five_agree_percent, four_agree_percent]

sns.set_style('whitegrid')   

#sets x and y variables for bar chart                 
axes = sns.barplot(x=values, y=counts, palette='bright')      
axes.set_title('Star-Text Sentiment Agreement Table')            
axes.set(xlabel='', ylabel='% Agree')                           

axes.set_ylim(top=max(counts) * 1.10)                            

#displays frequency for corresponding bar
for bar, count in zip(axes.patches, counts):                     
    text_x = bar.get_x() + bar.get_width() / 2.0
    text_y = bar.get_height()
    text = f'{count:,}'
    axes.text(text_x, text_y, text, fontsize=11, ha='center', va='bottom')

    




    
    
