// src/app/layout.js
import './globals.css';

export const metadata = {
  title: 'Multi-User Todo App',
  description: 'A full-featured todo application with authentication',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-50 min-h-screen">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </body>
    </html>
  );
}