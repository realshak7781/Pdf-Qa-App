import React, { useState } from "react";
import axios from "axios";
import { Upload, Send } from "lucide-react";

const API_URL = "http://localhost:8000"; 

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [currentFile, setCurrentFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Handle File Upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) {
      alert("Please select a file.");
      return;
    }
  
    if (file.type !== "application/pdf") {
      alert("Only PDF files are allowed.");
      return;
    }
  
    setCurrentFile(file);
    const formData = new FormData();
    formData.append("file", file);
  
    try {
      const response = await axios.post(`${API_URL}/upload/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
  
      if (response.status === 200) {
        console.log(response.data);
        alert("PDF uploaded successfully!");
      } else {
        alert("Upload failed: " + response.data.error);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to upload PDF.");
    }
  };
  

  // Handle Sending Message
  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = {
      text: inputMessage,
      type: "user",
      initial: inputMessage[0].toUpperCase(),
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputMessage("");
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/ask/`, {
        question: inputMessage,
      });

      const aiResponse = {
        text: response.data.answer || "I couldn't find an answer to that.",
        type: "ai",
      };

      setMessages((prevMessages) => [...prevMessages, aiResponse]);
    } catch (error) {
      console.error("Error getting answer:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: "Error retrieving response.", type: "ai" },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="p-4 border-b bg-white">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white">
              ai
            </div>
            <span className="font-semibold text-gray-800">planet</span>
            {currentFile && (
              <div className="ml-4 text-sm text-gray-600 flex items-center gap-2">
                <span>{currentFile.name}</span>
                <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                  <Upload size={16} />
                </div>
              </div>
            )}
          </div>

          <label className="cursor-pointer">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              className="hidden"
            />
            <div className="px-4 py-2 rounded-lg border border-gray-300 flex items-center gap-2 hover:bg-gray-50">
              <Upload size={16} />
              <span>Upload PDF</span>
            </div>
          </label>
        </div>
      </header>

      {/* Chat Area */}
      <main className="max-w-4xl mx-auto p-4 mb-20">
        <div className="space-y-6">
          {messages.map((message, index) => (
            <div key={index} className="flex gap-4">
              {message.type === "user" ? (
                <div className="w-8 h-8 rounded-full bg-purple-200 flex items-center justify-center">
                  {message.initial}
                </div>
              ) : (
                <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-white">
                  ai
                </div>
              )}
              <div className="flex-1">
                <p className="text-gray-800">{message.text}</p>
              </div>
            </div>
          ))}
          {isLoading && <p className="text-gray-500">Processing...</p>}
        </div>
      </main>

      {/* Message Input */}
      <footer className="fixed bottom-0 left-0 right-0 bg-white border-t p-4">
        <form onSubmit={handleSendMessage} className="max-w-4xl mx-auto">
          <div className="relative">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask a question..."
              className="w-full p-4 pr-12 rounded-lg bg-gray-100 focus:outline-none focus:ring-2 focus:ring-green-500"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="absolute right-4 top-1/2 -translate-y-1/2"
              disabled={isLoading}
            >
              <Send 
                size={20} 
                className={`text-gray-400 ${isLoading ? "opacity-50" : "hover:text-green-500"}`} 
              />
            </button>
          </div>
        </form>
      </footer>
    </div>
  );
};

export default ChatInterface;