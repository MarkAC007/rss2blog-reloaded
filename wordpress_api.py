# wordpress_api.py

import requests
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods.media import UploadFile

WP_URL = "https://siteurl/xmlrpc.php"
WP_USERNAME = ""
WP_PASSWORD = ""

client = Client(WP_URL, WP_USERNAME, WP_PASSWORD)

def upload_image(image_url):
    response = requests.get(image_url)
    image_data = response.content
    image_name = "generated_image.jpg"

    data = {
        "name": image_name,
        "type": "image/jpeg",
        "bits": image_data
    }

    response = client.call(UploadFile(data))
    return response["id"]

def create_post(title, content, featured_image_id):
    post = WordPressPost()
    post.title = title
    post.content = content
    post.post_status = "draft"  # Changed this line from "publish" to "draft"
    post.thumbnail = featured_image_id

    post_id = client.call(NewPost(post))
    return post_id
