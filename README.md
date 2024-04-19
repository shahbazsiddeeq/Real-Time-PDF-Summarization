# Real-Time PDF Summarization Web Application

## Overview
This web application allows users to upload PDF files and receive real-time summarizations of their contents. It features a chatbot-style user interface, providing a seamless experience for users to interact with the application. The summarization process is powered by Language Learning Models (LLMs), specifically, the Llama and GPT-4 models.

## Features
User-friendly Interface: The application offers a chatbot-style interface, making it intuitive for users to interact with.
PDF Upload: Users can easily upload PDF files directly within the application.
Real-time Summarization: Summaries of uploaded PDFs are generated in real-time and displayed in a conversational style.
Dual Display Area: The application includes two distinct display boxes, each showing summaries generated by different LLMs simultaneously.
## Frontend
The frontend of the application is built using the React framework. It includes the following components:

Header and Footer: Designed to facilitate basic navigation and provide essential information.
Body: Contains functionality for users to upload PDF files.
Display Area: Situated below the upload feature, this area displays real-time summarizations from both LLMs.
## Backend
The backend of the application is implemented using Python, with the FastAPI framework serving as the server-side framework. It fulfills the following requirements:

API Development: The backend includes an API that supports real-time interactions, potentially utilizing WebSockets or Socket.IO.
LLM Integration: It integrates two LLM models: Llama and GPT-4, for text generation and summarization.
Testing: The backend is thoroughly tested to ensure its functionality and reliability.

## Installation
To run the application locally, follow these steps:
1. Clone the repository or download diorectly from the browser:
   ```bash
   git clone https://github.com/shahbazsiddeeq/Real-Time-PDF-Summarization.git

2. First go to Frontend directory:
    ```bash
    cd Frontend
    npm install
    npm start

3. Backend:
    ```bash
    cd Backend
    pip install -r requirements.txt
    uvicorn server:app --reload
or 
   ```bash
      cd Backend
      pip install fastapi uvicorn starlette python-multipart pdfplumber aiofiles monsterapi cors
      uvicorn server:app --reload
