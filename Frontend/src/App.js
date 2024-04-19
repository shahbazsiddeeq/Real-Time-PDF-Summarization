import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [summaries, setSummaries] = useState({ gpt4: '', llama: '' });
  const [isLoading, setIsLoading] = useState(false); // State to track loading

  const handleFileChange = event => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      alert('Please select a PDF file first.');
      return;
    }

    setIsLoading(true); // Start loading
    const formData = new FormData();
    formData.append('file', file);

    fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      setSummaries({ gpt4: data.GPT4, llama: data.llama });
      setIsLoading(false); // Stop loading when data is received
    })
    .catch(error => {
      console.error('Error:', error);
      setIsLoading(false); // Stop loading on error
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        Real-Time PDF Summarization
      </header>
      <div className="upload-section">
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} accept="application/pdf" />
          <button type="submit" className='btn btn-primary'>Summarize PDF</button>
        </form>
        
      </div>
      <div className="summaries">
        <div className="summary-box">
          <h2>GPT4: <span>{isLoading && <div>Analyzing PDF...</div>}</span> {/* Loading indicator */}</h2>
          <pre>{summaries.gpt4}</pre>
        </div>
        <div className="summary-box">
          <h2>TinyLlama: <span>{isLoading && <div>Analyzing PDF...</div>}</span></h2>
          <pre>{summaries.llama}</pre>
        </div>
      </div>
      <footer className="App-footer">
        © 2024 Your Company Name
      </footer>
    </div>
  );
}

export default App;