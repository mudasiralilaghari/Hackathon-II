// src/components/ChatWidget.jsx
'use client';

import { useChatKit, ChatKit } from '@openai/chatkit-react';

export function ChatWidget({ userId }) {
  // Official OpenAI ChatKit configuration
  const { control } = useChatKit({
    workflow: {
      id: process.env.NEXT_PUBLIC_CHATKIT_WORKFLOW_ID || 'wf_699350450ccc81908932f504ede340440b8b47cbb80e0405',
    },
    user: userId || 'default_user',
    domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
  });

  return (
    <div className="h-full w-full">
      <ChatKit control={control} />
    </div>
  );
}

export default ChatWidget;