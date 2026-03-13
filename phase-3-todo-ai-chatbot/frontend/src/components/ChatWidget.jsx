// src/components/ChatWidget.jsx
'use client';

import { useChatKit, ChatKit } from '@openai/chatkit-react';

export function ChatWidget({ userId }) {
  // Official OpenAI ChatKit configuration with HostedApiConfig
  const { control, error } = useChatKit({
    api: {
      // Use backend to get client secret
      getClientSecret: async (currentClientSecret) => {
        console.log('ChatWidget: Getting client secret...');
        
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chatkit/session`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              workflow_id: process.env.NEXT_PUBLIC_CHATKIT_WORKFLOW_ID || 'wf_699350450ccc81908932f504ede340440b8b47cbb80e0405',
              user_id: userId || 'default_user',
            }),
          });

          if (!response.ok) {
            const errorText = await response.text();
            console.error('ChatWidget: Backend error:', response.status, errorText);
            throw new Error(`Backend error ${response.status}: ${errorText}`);
          }

          const data = await response.json();
          console.log('ChatWidget: Got client_secret:', data.client_secret ? 'YES' : 'NO');
          return data.client_secret;
        } catch (err) {
          console.error('ChatWidget: Error getting client secret:', err.message);
          throw err;
        }
      },
    },
  });

  // Debug logging
  if (typeof window !== 'undefined') {
    console.log('ChatWidget Debug:', {
      userId,
      hasControl: !!control,
      error: error
    });
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 text-red-700 rounded-lg">
        <p className="font-semibold">ChatKit Error:</p>
        <p className="text-sm">{error.message || 'Failed to initialize ChatKit'}</p>
      </div>
    );
  }

  if (!control) {
    return (
      <div className="p-4 bg-blue-50 text-blue-700 rounded-lg">
        <p>Loading ChatKit...</p>
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