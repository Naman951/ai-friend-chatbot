'use client';

import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ChatMessage from './ChatMessage';
import TypingIndicator from './TypingIndicator';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export default function ChatContainer() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId] = useState('default');
  const messagesEndRef = useRef(null);

  // Load chat history on mount
  useEffect(() => {
    loadChatHistory();
  }, []);

  const loadChatHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/history?conversation_id=${conversationId}`);
      if (response.data.messages) {
        setMessages(response.data.messages);
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    const userMessage = inputValue;
    setInputValue('');

    // Add user message to UI
    setMessages([...messages, { type: 'user', content: userMessage, timestamp: new Date().toISOString() }]);
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/api/chat`, {
        message: userMessage,
        conversation_id: conversationId,
      });

      const aiMessage = response.data.response;
      setMessages((prev) => [
        ...prev,
        { type: 'ai', content: aiMessage, timestamp: new Date().toISOString() },
      ]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        {
          type: 'ai',
          content: "Sorry, I couldn't process that. Please try again.",
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClearChat = async () => {
    try {
      await axios.post(`${API_URL}/api/clear`, { conversation_id: conversationId });
      setMessages([]);
    } catch (error) {
      console.error('Error clearing chat:', error);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-br from-blue-100 via-purple-100 to-pink-100">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary via-secondary to-accent p-6 shadow-lg">
        <h1 className="text-3xl font-bold text-white drop-shadow-lg">💜 AI Friend Chat</h1>
        <p className="text-white text-sm mt-1 opacity-90">Always here to chat with you!</p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 max-h-[calc(100vh-250px)]">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="text-6xl mb-4">👋</div>
              <p className="text-gray-600 text-lg font-semibold">Hey! I'm your AI friend</p>
              <p className="text-gray-500 mt-2">Start chatting with me below!</p>
            </div>
          </div>
        )}

        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg.content} type={msg.type} />
        ))}

        {isLoading && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="bg-white border-t-4 border-gradient-to-r from-primary to-secondary p-4 shadow-2xl">
        <form onSubmit={handleSendMessage} className="flex gap-3">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message... 💬"
            disabled={isLoading}
            className="flex-1 px-4 py-3 border-2 border-primary rounded-full focus:outline-none focus:border-secondary focus:shadow-lg transition"
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="bg-gradient-to-r from-primary to-secondary hover:shadow-lg disabled:opacity-50 text-white font-bold py-3 px-6 rounded-full transition transform hover:scale-105"
          >
            {isLoading ? '⏳' : '✨ Send'}
          </button>
          <button
            type="button"
            onClick={handleClearChat}
            className="bg-gray-400 hover:bg-gray-500 text-white font-bold py-3 px-4 rounded-full transition"
            title="Clear chat"
          >
            🗑️
          </button>
        </form>
      </div>
    </div>
  );
}
