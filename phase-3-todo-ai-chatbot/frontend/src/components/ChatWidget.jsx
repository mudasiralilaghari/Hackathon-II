// src/components/ChatWidget.jsx
'use client';

import { useState, useEffect } from 'react';
import { useChatKit, ChatKit } from '@openai/chatkit-react';

export function ChatWidget({ userId }) {
  const [scriptStatus, setScriptStatus] = useState('pending');
  const [error, setError] = useState(null);

  // Wait for ChatKit web component to be defined
  useEffect(() => {
    if (typeof window === 'undefined') return;

    console.log('ChatWidget: Checking if ChatKit is available...');

    // Check if already loaded
    if (window.customElements?.get('openai-chatkit')) {
      console.log('ChatWidget: ChatKit already loaded');
      setScriptStatus('ready');
      return;
    }

    // Wait for component to be defined
    customElements.whenDefined('openai-chatkit')
      .then(() => {
        console.log('ChatWidget: ChatKit component defined');
        setScriptStatus('ready');
      })
      .catch((err) => {
        console.error('ChatWidget: Failed to load ChatKit:', err);
        setError(err);
        setScriptStatus('error');
      });
      
    // Timeout after 10 seconds
    setTimeout(() => {
      if (scriptStatus === 'pending') {
        console.warn('ChatWidget: ChatKit loading timeout');
        setScriptStatus('error');
        setError(new Error('ChatKit loading timeout'));
      }
    }, 10000);
  }, []);

  // Configure ChatKit with backend endpoint that creates sessions
  const { control, error: chatKitError } = useChatKit({
    api: {
      async getClientSecret(existing) {
        if (existing) {
          return existing;
        }

        try {
          const res = await fetch('http://localhost:8000/api/chatkit/session', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              workflow_id: 'wf_699350450ccc81908932f504ede340440b8b47cbb80e0405',
              user_id: userId || 'default_user',
            }),
          });

          if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.detail || `HTTP error! status: ${res.status}`);
          }

          const data = await res.json();
          console.log('ChatWidget: Got client_secret from backend');
          return data.client_secret;
        } catch (error) {
          console.error('ChatWidget: Error getting client secret:', error);
          throw error;
        }
      },
    },
  });
  
  // Log any ChatKit errors
  useEffect(() => {
    if (chatKitError) {
      console.error('ChatWidget: ChatKit error:', chatKitError);
      setError(chatKitError);
      setScriptStatus('error');
    }
  }, [chatKitError]);

  // Render based on script loading state
  if (scriptStatus === 'pending') {
    return (
      <div className="flex items-center justify-center h-full bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto mb-2"></div>
          <p className="text-gray-600">Loading ChatKit...</p>
          <p className="text-xs text-gray-400 mt-2">This may take a few seconds</p>
        </div>
      </div>
    );
  }

  if (scriptStatus === 'error') {
    return (
      <div className="flex items-center justify-center h-full bg-red-50 p-4">
        <div className="text-center text-red-600">
          <p className="font-semibold">Chat unavailable</p>
          <p className="text-sm mt-1">{error?.message || 'Failed to load ChatKit'}</p>
          <p className="text-xs mt-2 text-gray-500">Check browser console for details</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full w-full">
      <ChatKit control={control} />
    </div>
  );
}

export default ChatWidget;