import praw
import csv
from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

def generate_summary(post_title, post_url, comments):
    all_posts=text_to_summarize = f"Post Title: {post_title}\nPost URL: {post_url}\nComments:\n" + "\n".join(comments)
    client=OpenAI()
    response = client.chat.completions.create(
      model="gpt-4",  # or another model name
      messages=[
        {
            "role": "user",
            "content": "Summarize the following Reddit posts and comments:\n\n" + all_posts,
        }
    ],
    )
    print(response)
    return response.choices[0].message.content.strip()



def summarize_data():
    df = pd.read_csv('wallstreet.csv')  # Update with your CSV file path

    # Concatenate all post titles, URLs, and comments into a single string
    df['summary'] = df.apply(lambda row: generate_summary(
        row['Post Title'], 
        row['Post URL'], 
        [row[f'Comment {i}'] for i in range(1, 21) if pd.notna(row[f'Comment {i}'])]
    ), axis=1)

    # Save or print summaries
    print(df[['Post Title', 'Post URL', 'summary']])
    # Optionally, save to a new CSV
    df.to_csv('summarized_reddit_data.csv', index=False)



def scrape_subreddit():
    reddit_read_only = praw.Reddit(client_id="4pRw10u11pxt7dnkZ198zw",         # your client id
                                   client_secret="tX3mckDAQ8-py4fHwdAR2yQ-Z70jWA",      # your client secret
                                   user_agent="example") 
    subreddit = reddit_read_only.subreddit("StockMarket")
    top_posts = subreddit.top('week', limit=20)

    # Create and open a CSV file in write mode
    with open(f'{"wallstreet"}.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(['Post Title', 'Post URL', 'Comment 1', 'Comment 2', 'Comment 3', 'Comment 4', 'Comment 5', 
                         'Comment 6', 'Comment 7', 'Comment 8', 'Comment 9', 'Comment 10', 'Comment 11', 'Comment 12', 
                         'Comment 13', 'Comment 14', 'Comment 15', 'Comment 16', 'Comment 17', 'Comment 18', 'Comment 19', 'Comment 20'])

        for post in top_posts:
            post_comments = []
            # Get the top 20 comments for each post
            post.comments.replace_more(limit=0)
            top_comments = post.comments.list()[:20]
            for comment in top_comments:
                post_comments.append(comment.body)

            # Pad the list of comments to ensure it always has 20 elements
            post_comments.extend([''] * (20 - len(post_comments)))

            # Write post details and comments to the CSV file
            writer.writerow([post.title, post.url] + post_comments)

def send_telegram():
    global TOKEN
    df=pd.read_csv("summarized_reddit_data.csv")
    summaries=df['summary']
    postTitles=df['Post Title']
    urls=df['Post URL']

    message_string=""
    chat_id = "981139073"
    for i in range(len(summaries)):
        message_string=""
        message_string+=postTitles[i]+"\n"
        message_string+=summaries[i]+"\n"
        message_string+=urls[i]+"\n\n"
        message_string=message_string.replace("&","and")
        #print(message_string)
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message_string}"

if __name__=="__main__":
    scrape_subreddit()
    summarize_data()
    send_telegram()








