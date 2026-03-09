// src/components/ChatWidget.jsx
'use client';

import { useState, useEffect } from 'react';
import { useChatKit, ChatKit } from '@openai/chatkit-react';

export function ChatWidget({ userId }) {
  const [scriptStatus, setScriptStatus] = useState('pending');
  const [error, setError] = useState(null);
  const [showFallback, setShowFallback] = useState(false);

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
        setShowFallback(true);
      });

    // Timeout after 5 seconds - show fallback UI
    setTimeout(() => {
      if (scriptStatus === 'pending') {
        console.warn('ChatWidget: ChatKit loading timeout - showing fallback');
        setShowFallback(true);
        setScriptStatus('ready');
      }
    }, 5000);
  }, []);

  // Configure ChatKit with domain key (official OpenAI way)
  const { control, error: chatKitError } = useChatKit({
    workflow: {
      id: process.env.NEXT_PUBLIC_CHATKIT_WORKFLOW_ID || 'wf_699350450ccc81908932f504ede340440b8b47cbb80e0405',
    },
    user: userId || 'default_user',
    domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
  });

  // If ChatKit fails to get client secret, show fallback message
  useEffect(() => {
    if (chatKitError || !control) {
      console.error('ChatWidget: ChatKit error:', chatKitError);
      setShowFallback(true);
    }
  }, [chatKitError, control]);

  // Show fallback UI if ChatKit fails
  if (showFallback) {
    return (
      <div className="flex flex-col items-center justify-center h-full bg-gray-50 p-4">
        <div className="text-center">
          <div className="text-4xl mb-4">🤖</div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">AI Todo Assistant</h3>
          <p className="text-sm text-gray-600 mb-4">
            ChatKit is currently unavailable. This usually happens when using OpenRouter API keys.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-left">
            <p className="text-xs text-blue-800 font-medium mb-2">To enable ChatKit:</p>
            <ol className="text-xs text-blue-700 space-y-1 list-decimal list-inside">
              <li>Get an official OpenAI API key from <a href="https://platform.openai.com/api-keys" target="_blank" className="underline">platform.openai.com</a></li>
              <li>Update your backend .env file with the new key</li>
              <li>Redeploy your backend</li>
            </ol>
          </div>
          <p className="text-xs text-gray-500 mt-4">
            Note: Your task management features (add, list, update, delete) are still working perfectly!
          </p>
        </div>
      </div>
    );
  }

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