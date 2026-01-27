# Todo App Frontend

This is the frontend for the Multi-User Todo Application, built with Next.js (App Router) and deployed on Vercel.

## Deployment

This project is set up for deployment on Vercel:

1. Connect your GitHub repository to Vercel
2. During the import process:
   - Set the Root Directory to `frontend`
   - Framework preset: Next.js
3. Add the following environment variables:
   - `NEXT_PUBLIC_API_URL`: https://fazalahmed-full-stack-todo-app.hf.space
   - `NEXT_PUBLIC_JWT_SECRET`: 2f2f99a85c2ae5b883522a98cea7b0ae95a264af9a949a8a3a4e4bea2cae3942
4. Deploy!

## Features

- User authentication (signup/signin)
- Task management (create, read, update, delete)
- Task completion toggling
- Responsive design with Tailwind CSS
- Secure JWT-based authentication

## Tech Stack

- Next.js (App Router)
- React
- Tailwind CSS
- Vercel for deployment

## Environment Variables

This project uses the following environment variables:

- `NEXT_PUBLIC_API_URL`: The URL of the backend API
- `NEXT_PUBLIC_JWT_SECRET`: The secret used for JWT validation (should match the backend)

## Scripts

- `npm run dev`: Starts the development server
- `npm run build`: Builds the application for production
- `npm run start`: Starts the production server
- `npm run lint`: Runs ESLint to check for code issues