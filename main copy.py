import logging
import os
import openai
import requests
from datetime import datetime
from rss_parser import parse_rss_feed
from wordpress_api import upload_image, create_post
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

openai.api_key = os.environ.get('OPENAI_API_KEY')

def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def generate_image_description(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

def save_image_description_to_file(image_description, output_file="prompts.txt"):
    with open(output_file, "a") as file:
        file.write(f"{image_description}, in the style of art deco, illustration by Yoshiyuki Sadamoto.\n")


rss_feed_list = parse_rss_feed("rss_feeds.txt")

for rss_feed in rss_feed_list:
    rss_title, rss_description, rss_url = rss_feed.values()

    article_prompt = f"You are a helpful assistant that summarizes articles about artificial intelligence in a funny and witty way. Start with a bulleted list containing a breakdown of the article's key points, and create closing two paragraphs with your \"<h3>Hot Take</h3>\". Include h1, h2, h3 tags in the final output where appropriate. {rss_description}"
    article_content = generate_text(article_prompt)
    article_content += f"\nTo learn more, check out the source here: {rss_url}"

    image_prompt = f"You are a helpful assistant that creates images based on articles titles. Create a brief visual description of what an image would look like for the title: {rss_title}"
    image_description = generate_text(image_prompt)

    # Save image_description to a text file
    save_image_description_to_file(image_description)

    title_prompt = f"You are a WordPress title generator. Create a concise title for the blog post that is catchy and optimized for search engines. Remove all HTML in the response and do not use quotes. {rss_title}"
    post_title = generate_text(title_prompt)

    image_url = generate_image_description(image_description)

    if image_url is None:
        logger.error("Skipping post creation due to the image generation issue.")
        continue

    uploaded_image_id = upload_image(image_url)

    create_post(post_title, article_content, uploaded_image_id)