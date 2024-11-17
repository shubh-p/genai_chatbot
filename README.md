# Chatbot Application README

## Project Overview
This project is a chatbot that retrieves contextual information from GitLab's Handbook and Direction pages, embedding the data using a pre-trained model and responding to user queries using Google's Gemini API.

## Prerequisites
- Python 3.8 or higher
- Access to the internet for downloading dependencies and accessing APIs

## Getting Started

### 1. Clone the Repository
Start by cloning this repository to your local machine:
```bash
git clone <https://github.com/shubh-p/genai_chatbot.git>
cd genai_chatbot
```

## 2. Create a Virtual Environment

Create a virtual environment to isolate the project dependencies:

```bash
python -m venv venv
```
## 3. Activate the Virtual Environment
```
Activate the virtual environment:

Windows:

.\venv\Scripts\activate

MacOS/Linux:

source venv/bin/activate
```
## 4. Install Dependencies

Install the required Python packages from requirements.txt:
```
pip install -r requirements.txt
```

## 5. Add your api key to env
Get your gemini api ley refer: https://aistudio.google.com/ and export it into your environment using 
```
export GEMINI_API_KEY='YOUR API KEY'
```
## 6. Run the App

Start the app using Streamlit, which will create the vectors and run the app on your local port:
```
streamlit run app.py
```
The app will be available at http://localhost:8501 (or another port if specified by Streamlit).
Usage

    Interact with the app by entering queries.
    The chatbot will provide answers based on the context retrieved from the embedded handbook and direction data.


## Data scraping and structuring 
The following steps have been done to extract data from the relevant webpages and markdown files and are not needed to be done again
## 1. Prepare the Handbook Data

Copy the handbook directory from GitLab's Handbook repository into the handbook directory inside your project folder.
```
https://gitlab.com/gitlab-com/content-sites/handbook-/tree/main/content/handbook
``` 

## 2. Generate JSON Data from Handbook

Run the following script to create JSON data from the handbook:
```
python core/data_retrieval_handbook.py
```
## 3. Generate JSON Data from the Direction Page

Run the following script to create JSON data from the GitLab Direction page:
```
python core/data_retrieval_direction.py
```
