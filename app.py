import re
from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
import markdownify
import io

app = Flask(__name__)

# Function to scrape and convert webpage to markdown, ignoring unnecessary elements
def scrape_and_convert(url, include_text=True, include_images=True):
    # Fetch the webpage content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove header, footer, navigation, sidebars, comments, and other unnecessary elements
    for tag in ['header', 'footer', 'nav', 'aside', 'script', 'style', 'noscript', 'iframe']:
        elements = soup.find_all(tag)
        for element in elements:
            element.decompose()  # Removes the element from the soup object

    # Remove metadata like JSON-LD (structured data)
    for tag in soup.find_all("script", {"type": "application/ld+json"}):
        tag.decompose()

    # Remove additional classes or ids that are unnecessary
    unwanted_classes = ['toc', 'ads', 'sponsored', 'related-posts', 'post-meta']
    for unwanted_class in unwanted_classes:
        for element in soup.find_all(class_=unwanted_class):
            element.decompose()

    # Remove empty elements to clean up the final output
    empty_tags = soup.find_all(lambda tag: not tag.contents or (tag.string and tag.string.strip() == ""))
    for empty_tag in empty_tags:
        empty_tag.decompose()

    # Handle content selection (text, images)
    if not include_images:
        for img in soup.find_all('img'):
            img.decompose()

    markdown_content = ""
    if include_text:
        markdown_content = markdownify.markdownify(str(soup), heading_style="ATX")

    # Remove excess blank lines (more than two consecutive newlines)
    cleaned_markdown_content = re.sub(r'\n\s*\n+', '\n\n', markdown_content)

    return cleaned_markdown_content, str(soup)

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the form submission and convert URL
@app.route('/convert', methods=['POST'])
def convert():
    url = request.form['url']
    include_text = 'includeText' in request.form
    include_images = 'includeImages' in request.form
    download_format = request.form['downloadFormat']

    # Automatically prepend 'http://' if no scheme is provided
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    if url:
        markdown_content, html_content = scrape_and_convert(url, include_text=include_text, include_images=include_images)

        # Download format selection
        if download_format == 'markdown':
            markdown_file = io.StringIO(markdown_content)
            markdown_file.seek(0)
            return send_file(io.BytesIO(markdown_file.getvalue().encode('utf-8')),
                             mimetype="text/markdown",
                             as_attachment=True,
                             download_name="converted.md")
        elif download_format == 'html':
            html_file = io.StringIO(html_content)
            html_file.seek(0)
            return send_file(io.BytesIO(html_file.getvalue().encode('utf-8')),
                             mimetype="text/html",
                             as_attachment=True,
                             download_name="converted.html")

    return "Error: Invalid URL"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
