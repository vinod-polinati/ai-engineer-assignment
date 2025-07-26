import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

interface Message {
  sender: 'user' | 'bot';
  text: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([
    { sender: 'bot', text: "Hi, I'm your AI Excel interviewer. Type anything to begin." }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => crypto.randomUUID());
  const [interviewCompleted, setInterviewCompleted] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    setIsLoading(true);

    // Add user message
    setMessages(prev => [...prev, { sender: 'user', text: userMessage }]);

    try {
      console.log('Sending request to:', 'https://ai-engineer-assignment.onrender.com/chat');
      console.log('Request data:', { session_id: sessionId, message: userMessage });
      
      const response = await axios.post('https://ai-engineer-assignment.onrender.com/chat', {
        session_id: sessionId,
        message: userMessage
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
        timeout: 30000 // 30 second timeout
      });

      console.log('Response received:', response.data);
      const botReply = response.data.response;
      setMessages(prev => [...prev, { sender: 'bot', text: botReply }]);
      
      // Check if interview is completed
      if (botReply.includes("Interview completed") || botReply.includes("Overall impression")) {
        setInterviewCompleted(true);
      }
      
    } catch (error: any) {
      console.error('Error details:', error);
      console.error('Error response:', error.response?.data);
      console.error('Error status:', error.response?.status);
      
      let errorMessage = 'Sorry, there was an error. Please try again.';
      
      if (error.response?.status === 429) {
        errorMessage = 'Too many requests. Please wait a moment and try again.';
      } else if (error.code === 'ECONNABORTED') {
        errorMessage = 'Request timed out. Please try again.';
      } else if (error.response?.status >= 500) {
        errorMessage = 'Server error. Please try again in a moment.';
      }
      
      setMessages(prev => [...prev, { 
        sender: 'bot', 
        text: errorMessage 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestart = () => {
    setMessages([{ sender: 'bot', text: "Hi, I'm your AI Excel interviewer. Type anything to begin." }]);
    setInterviewCompleted(false);
  };

  const handleDownloadTranscript = async () => {
    try {
      const response = await axios.get(`https://ai-engineer-assignment.onrender.com/download-transcript/${sessionId}`, {
        responseType: 'blob',
        timeout: 30000
      });
      
      // Create a download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `excel_interview_transcript_${sessionId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error('Error downloading transcript:', error);
      alert('Error downloading transcript. Please try again.');
    }
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="header">
          <h1>Excel Mock Interview</h1>
          <div className="header-buttons">
            {interviewCompleted && (
              <button onClick={handleDownloadTranscript} className="download-btn">
                Download Transcript
              </button>
            )}
            <button onClick={handleRestart} className="restart-btn">
              Restart Interview
            </button>
          </div>
        </div>
        
        <div className="messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <div className="message-content">
                {message.text}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message bot">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your response here..."
            disabled={isLoading}
            className="message-input"
          />
          <button type="submit" disabled={isLoading || !inputValue.trim()} className="send-btn">
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
