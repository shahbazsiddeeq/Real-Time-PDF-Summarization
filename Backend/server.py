from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pdfplumber
import asyncio
import requests
import os
import json
import re
from monsterapi.nextGenLLMClient import LLMClient, GenerateRequest
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Function to split text into chunks of approximately 3000 tokens each
# Function to split text into chunks based on paragraphs without exceeding a specified token count
import pdfplumber
import re

def utf8_word_count(s):
    return len(s.split())
def split_into_chunks_by_paragraphs(text, max_tokens=3000):
    paragraphs = text.split('\n')  # Split the text into paragraphs based on newlines
    chunks = []
    current_chunk = []
    current_length = 0

    for paragraph in paragraphs:
        paragraph_length = utf8_word_count(paragraph)
        if current_length + paragraph_length > max_tokens:
            chunks.append("\n".join(current_chunk))
            current_chunk = [paragraph]
            current_length = paragraph_length
        else:
            current_chunk.append(paragraph)
            current_length += paragraph_length

    # Add the last chunk if it has any content
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    return chunks
def call_chat_gpt_api(previous_summary, next_paragraph):
        system_prompt = f"""
        You are tasked with progressively summarizing a document. Begin with the summary provided and then incorporate the next paragraph into this existing summary.
        Your job is to update the summary with each new paragraph without increasing its length unnecessarily. Keep the summary concise, focused on main points, and under 500 words.
        Previous summary:
        {previous_summary}
        Next paragraph:
        {next_paragraph}
        """
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
        
        # Fetch the last five Q&A pairs and append them to the messages
        
        # Append the user's latest question
        messages.append({
            "role": "user",
            "content": "Please update the summary with the information from the next paragraph."
        })

        # Adding the user's question to the prompt
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer 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',
            'Content-Type': 'application/json',
        }

        payload = {
            'model': 'gpt-3.5-turbo-16k',
            'messages': messages,
            'temperature': 0.7,  # Customizable
            'max_tokens': 2000  # Customizable
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=50)
        response_json = response.json()
        completion_content = response_json['choices'][0]['message']['content']
        return completion_content
def call_chat_gpt_api_full_text(content):
        # Adjust the prompt according to the validity of the polygon area
        system_prompt = f"""
        Create a concise summary focusing on main points and key information, with a word limit of 500 words. 
        Instructions: Identify crucial themes, data, and emphasized text. Condense these elements into a coherent 
        summary that maintains the logical flow of the original article. The summary should be clear and well-structured,
        providing a comprehensive overview without personal interpretation. Review for accuracy and clarity, ensuring no 
        critical information is omitted.
        """

        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
        
        # Fetch the last five Q&A pairs and append them to the messages
        
        # Append the user's latest question
        messages.append({
            "role": "user",
            "content": content
        })

        # Adding the user's question to the prompt
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer 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',
            'Content-Type': 'application/json',
        }

        payload = {
            'model': 'gpt-3.5-turbo-16k',
            'messages': messages,
            'temperature': 0.7,  # Customizable
            'max_tokens': 1000  # Customizable
        }
        
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=50)
        response_json = response.json()
        completion_content = response_json['choices'][0]['message']['content']
        return completion_content
def call_tinyllama_api(content):
    api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjQ3OGExNDFkYjRhZTU0MDhhMGUyNjg3ZmIxMWVkNmUyIiwiY3JlYXRlZF9hdCI6IjIwMjQtMDQtMTlUMTY6MzU6MDAuNTEyNTc2In0.J_dXW_mQUssZw8BvWXwbhLOc85Dr1XPtuZh6CAOPy-g'  # Replace 'your-api-key' with your actual Monster API key
    # Initialize the LLMClient with your API key
    client = LLMClient(api_key=api_key)
    # Specify the model you want to use and the input data
    model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    input_data = {
        'messages': [
            {"role": "user", "content": content}
        ],
        'top_k': 10,
        'top_p': 0.9,
        'temperature': 0.9,
        'max_length': 1000,
        'beam_size': 1,
        'system_prompt': 'Create a concise summary focusing on main points and key information, with a word limit of 500 words.  Instructions: Identify crucial themes, data, and emphasized text. Condense these elements into a coherent  summary that maintains the logical flow of the original article. The summary should be clear and well-structured, providing a comprehensive overview without personal interpretation. Review for accuracy and clarity, ensuring no  critical information is omitted.',
        'repetition_penalty': 1.2,
    }

    # Create a GenerateRequest object with the model and input data
    request = GenerateRequest(
        model=model,
        messages=input_data['messages'],
        top_k=input_data['top_k'],
        top_p=input_data['top_p'],
        temperature=input_data['temperature'],
        max_length=input_data['max_length'],
        beam_size=input_data['beam_size'],
        system_prompt=input_data['system_prompt'],
        repetition_penalty=input_data['repetition_penalty']
    )

    # Make the API call and fetch the response
    response = client.generate(request)

    # Convert the response to JSON and print
     # Extracting the assistant's response text from the JSON structure
    if 'response' in response and 'text' in response['response']:
        assistant_response = response['response']['text'][0].replace('\n', ' ').strip()
    else:
        assistant_response = "No response generated."

    return assistant_response
def summarize_text_chunks(text_chunks):
    cumulative_summary = ""

    for i, paragraph in enumerate(text_chunks):
        # Send the current summary and the next paragraph to the API
        summary_response = call_chat_gpt_api(cumulative_summary, paragraph)
        
        # Update the cumulative summary with the new summary provided by the API
        cumulative_summary = summary_response

    return cumulative_summary
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Ensure the file is a pdf
    if file.content_type != 'application/pdf':
        return JSONResponse(status_code=400, content={"message": "Invalid file type."})

    # Read file content as bytes
    content = await file.read()

    # Use pdfplumber to extract text from the PDF
    with pdfplumber.open(file.file) as pdf:
        all_text = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:  # This check is to avoid adding None if text extraction fails
                all_text.append(text)

        full_text = "\n".join(all_text)

    # Check if the text exceeds 5000 tokens, split into smaller chunks if needed
    if len(full_text.split()) >6000:
        # Normalize whitespace and strip HTML tags (if any)

        # Split the extracted text into manageable chunks based on paragraphs and punctuation
        # Assuming 'file.file' is the path to your PDF
        # Split the extracted text into manageable chunks based on paragraphs
        text_chunks = split_into_chunks_by_paragraphs(full_text, 4000)
        complete_summary = summarize_text_chunks(text_chunks)
    else:
        complete_summary = call_chat_gpt_api_full_text(full_text)
    # You can now process each chunk as needed or return it
    
    gpt4 = complete_summary  # Simulated summary from model 1
    llama = call_tinyllama_api(full_text)  # Simulated summary from model 2
    # llama = 'hi'  # Simulated summary from model 2
    return {"GPT4": gpt4, "llama": llama}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)