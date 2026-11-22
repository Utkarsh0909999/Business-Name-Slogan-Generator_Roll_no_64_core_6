# PS64 – Business Name & Slogan Generator

## Problem Statement
Startups struggle with branding. Given a business idea, target audience and style, this app generates 10 business names with slogans and a 3-line pitch, and lets the user mark favourite options.

## Features
- Inputs: business idea, target audience, style (Modern, Playful, Premium, Traditional, Techy, Minimal)
- Generates 10 names + slogans and a 3-line pitch
- Mark options as favourites and download them as a text file

## Tech Stack
- Python
- Streamlit (UI)
- Groq API with GPT-OSS 20B (LLM)
- python-dotenv

## How to Run
1. Clone the repo and open the folder
2. Get a free API key from https://console.groq.com/keys
3. Create a `.env` file in the project folder:
   ```
   GROQ_API_KEY=your_key_here
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Start the app:
   ```
   streamlit run app.py
   ```

## Screenshots
![Output 1](screenshots/output1.png)
![Output 2](screenshots/output2.png)

## Author
Name: <Utkarsh Suroshe>
Roll No: 64
Class: LY CORE 6
