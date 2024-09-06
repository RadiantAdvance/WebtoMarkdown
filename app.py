import re
from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
import markdownify
import io

app = Flask(__name__)

# Function to scrape and convert webpage to markdown, ignoring unnecessary elements
def scrape_and_convert(url, include_text=True, include_images=True):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove header, footer, navigation, sidebars, comments, TOC, and tags
    for tag in ['header', 'footer', 'nav', 'aside']:
        elements = soup.find_all(tag)
        for element in elements:
            element.decompose()  # Removes the element from the soup object

    # Remove elements by common sidebar, navbar, TOC, and comments class names
    remove_classes = ['sidebar', 'aside', 'navbar', 'menu', 'related', 'toc', 'tags', 'tag-list', 'post-tags']
    for remove_class in remove_classes:
        for element in soup.find_all(class_=remove_class):
            element.decompose()

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
