// src/components/ChatWidget.jsx
'use client';

import { useChatKit, ChatKit } from '@openai/chatkit-react';

export function ChatWidget({ userId }) {
  // Official OpenAI ChatKit configuration
  // When using domainKey, pass workflow and user at top level
  const { control, error } = useChatKit({
    domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
    workflow: {
      id: process.env.NEXT_PUBLIC_CHATKIT_WORKFLOW_ID || 'wf_699350450ccc81908932f504ede340440b8b47cbb80e0405',
    },
    user: userId || 'default_user',
  });

  // Debug logging
  if (typeof window !== 'undefined') {
    console.log('ChatWidget Debug:', {
      userId,
      hasDomainKey: !!process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
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