# Webpage to Markdown Converter

A simple Flask-based web application that allows users to input a URL and convert the content of the webpage into Markdown format. The application strips unnecessary elements such as headers, footers, navigation bars, and sidebars, focusing primarily on the article content. Users can download the converted Markdown or HTML file.

## Features

- Converts webpage content to Markdown format.
- Strips unnecessary elements like headers, footers, sidebars, and navigation bars.
- Option to include or exclude images and text content.
- Download converted content as either Markdown (`.md`) or HTML (`.html`).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Running with Docker](#running-with-docker)
- [Contributing](#contributing)
- [License](#license)

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/webpage-to-markdown.git
   cd webpage-to-markdown
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   flask run --host=0.0.0.0
   ```

4. Access the application in your browser at `http://localhost:5000`.

## Usage

1. Open the web application.
2. Enter the URL of the webpage you want to convert.
3. Choose whether you want to include text, images, or both.
4. Select the format you want to download (Markdown or HTML).
5. Click "Convert" to process the webpage and download the result.


## Running with Docker

You can also run the application using Docker.

1. **Build the Docker Image**:

   ```bash
   docker build -t webpage-to-markdown .
   ```

2. **Run the Docker Container**:

   ```bash
   docker run -p 5000:5000 webpage-to-markdown
   ```

3. **Access the Application**:

   Visit `http://localhost:5000` in your browser.

### Running with Docker Compose

You can use Docker Compose for easier management:

1. **Create a `docker-compose.yml`** (already included in the project).
2. **Run the Application**:

   ```bash
   docker-compose up --build
   ```

3. **Access the Application**:

   Visit `http://localhost:5000`.

