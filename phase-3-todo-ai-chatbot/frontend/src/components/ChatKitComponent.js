// src/components/ChatKitComponent.js
'use client';

import { useState, useEffect } from 'react';
import { ChatKit, useChatKit } from '@openai/chatkit-react';

const ChatKitComponent = ({ userId }) => {
  const [status, setStatus] = useState('Initializing...');
  const [hasError, setHasError] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Use ChatKit hook following official documentation pattern
  const { control, isLoading, error } = useChatKit({
    api: {
      async getClientSecret(existing) {
        // If we already have a secret, use it
        if (existing) {
          console.log('Using existing client secret');
          return existing;
        }

        try {
          console.log('Creating new ChatKit session...');
          const res = await fetch('http://localhost:8000/api/chatkit/session', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              workflow_id: 'wf_699350450ccc81908932f504ede340440b8b47cbb80e0405', // Your workflow ID
              user_id: userId || 'default_user',
            }),
          });

          if (!res.ok) {
            const errorText = await res.text();
            throw new Error(`HTTP error! status: ${res.status}, message: ${errorText}`);
          }

          const data = await res.json();
          console.log('Received session data:', data);

          setStatus('Connected to backend');
          return data.client_secret;
        } catch (err) {
          console.error('Error getting client secret:', err);
          const errorMsg = err instanceof Error ? err.message : String(err);
          setStatus(`Connection error: ${errorMsg}`);
          setErrorMessage(errorMsg);
          setHasError(true);
          throw err; // Re-throw to let ChatKit handle it
        }
      },
    },
  });

  // Update status based on ChatKit state
  useEffect(() => {
    if (isLoading) {
      setStatus('Loading ChatKit...');
    } else if (error) {
      const errorMsg = error.message || 'Unknown error';
      setStatus(`ChatKit error: ${errorMsg}`);
      setErrorMessage(errorMsg);
      setHasError(true);
    } else if (control) {
      setStatus('ChatKit loaded successfully');
    }
  }, [isLoading, error, control]);

  // Error state
  if (hasError || error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <h3 className="text-red-800 font-semibold">Chat Connection Error</h3>
        <p className="text-red-600">{status}</p>
        <p className="text-red-600 text-sm mt-2">Please ensure the backend server is running on http://localhost:8000</p>
      </div>
    );
  }

  // Loading state
  if (isLoading || status.includes('Loading')) {
    return (
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <p className="text-blue-800">Loading ChatKit... {status}</p>
      </div>
    );
  }

  // Main chat render with proper ChatKit component
  return (
    <div className="flex flex-col h-full" style={{ height: '500px' }}>
      <div className="mb-2 p-2 bg-gray-100 rounded">
        <p className="text-sm text-gray-600">{status}</p>
      </div>
      <div className="flex-grow border border-gray-300 rounded-lg overflow-hidden" style={{ height: '450px' }}>
        {control ? (
          <ChatKit
            control={control}
            style={{ width: '100%', height: '100%' }}
            className="chatkit-widget"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-gray-50">
            <p className="text-gray-500">Initializing ChatKit...</p>
          </div>
        )}
      </div>
      <div className="mt-2 text-xs text-gray-500 text-center">
        Powered by OpenAI ChatKit
      </div>
    </div>
  );
};

export default ChatKitComponent;