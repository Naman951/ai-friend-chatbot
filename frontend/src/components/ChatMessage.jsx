'use client';

import React, { useEffect, useRef } from 'react';

export default function ChatMessage({ message, type }) {
  const messageRef = useRef(null);

  useEffect(() => {
    messageRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [message]);

  const isUser = type === 'user';

  return (
    <div ref={messageRef} className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-fade-in mb-4`}>
      <div
        className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl shadow-lg ${
          isUser
            ? 'bg-gradient-to-r from-primary to-secondary text-white rounded-br-none'
            : 'bg-gradient-to-r from-light to-accent text-gray-800 rounded-bl-none'
        }`}
      >
        <p className="text-sm lg:text-base break-words">{message}</p>
      </div>
    </div>
  );
}
