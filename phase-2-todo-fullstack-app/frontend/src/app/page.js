// src/app/page.js
'use client';

import { useState } from 'react';

export default function Home() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch(activeTab) {
      case 'dashboard':
        return (
          <div className="text-center py-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-4">🚀 Multi-User Todo App</h1>
            <p className="text-lg text-gray-600 mb-8">
              A secure and intuitive todo application to help you organize your daily tasks
            </p>
            
            <div className="flex flex-col sm:flex-row justify-center gap-4 mb-12">
              <a 
                href="/signup" 
                className="px-6 py-3 bg-green-600 text-white font-semibold rounded-lg shadow-md hover:bg-green-700 transition duration-200 text-center"
              >
                Get Started
              </a>
              <a 
                href="/signin" 
                className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition duration-200 text-center"
              >
                Sign In
              </a>
              <a 
                href="/dashboard" 
                className="px-6 py-3 bg-purple-600 text-white font-semibold rounded-lg shadow-md hover:bg-purple-700 transition duration-200 text-center"
              >
                View Dashboard
              </a>
            </div>
            
            <div className="mt-12">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Application Features</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="bg-blue-50 p-6 rounded-xl border border-blue-100">
                  <h3 className="text-xl font-semibold text-blue-800 mb-2">🔐 Secure Authentication</h3>
                  <p className="text-gray-600">JWT-based authentication with secure signup and signin processes</p>
                </div>
                
                <div className="bg-green-50 p-6 rounded-xl border border-green-100">
                  <h3 className="text-xl font-semibold text-green-800 mb-2">📋 Task Management</h3>
                  <p className="text-gray-600">Create, read, update, and delete tasks with ease</p>
                </div>
                
                <div className="bg-yellow-50 p-6 rounded-xl border border-yellow-100">
                  <h3 className="text-xl font-semibold text-yellow-800 mb-2">✅ Completion Tracking</h3>
                  <p className="text-gray-600">Mark tasks as complete/incomplete with simple toggle</p>
                </div>
                
                <div className="bg-red-50 p-6 rounded-xl border border-red-100">
                  <h3 className="text-xl font-semibold text-red-800 mb-2">👤 User Isolation</h3>
                  <p className="text-gray-600">Each user sees only their own tasks and data</p>
                </div>
                
                <div className="bg-indigo-50 p-6 rounded-xl border border-indigo-100">
                  <h3 className="text-xl font-semibold text-indigo-800 mb-2">📱 Responsive Design</h3>
                  <p className="text-gray-600">Works seamlessly on desktop, tablet, and mobile devices</p>
                </div>
                
                <div className="bg-purple-50 p-6 rounded-xl border border-purple-100">
                  <h3 className="text-xl font-semibold text-purple-800 mb-2">⚡ Fast Performance</h3>
                  <p className="text-gray-600">Optimized for speed and efficiency</p>
                </div>
              </div>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Todo Application</h1>
          <nav>
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`mr-4 px-4 py-2 rounded-lg ${
                activeTab === 'dashboard' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Dashboard
            </button>
          </nav>
        </div>
      </header>

      <main className="py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {renderContent()}
        </div>
      </main>

      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 text-center text-gray-600">
          <p>Multi-User Todo App © {new Date().getFullYear()} | Full-Stack Application</p>
        </div>
      </footer>
    </div>
  );
}