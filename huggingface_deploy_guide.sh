#!/bin/bash
# Script to help with Hugging Face deployment

echo "To deploy to your Hugging Face Space, follow these steps:"

echo "1. Go to your Hugging Face Space: https://huggingface.co/spaces/FazalAhmed/full-stack-todo-app"
echo "2. Go to the 'Files' tab"
echo "3. Click on 'Duplicate Repo' or edit the existing one"
echo "4. In the Space settings, set the following:"
echo "   - SDK: Docker"
echo "   - Compute: CPU (Basic)"
echo ""
echo "5. Add these environment variables in your Space settings:"
echo "   - DATABASE_URL: Your Neon PostgreSQL connection string"
echo "   - SECRET_KEY: A strong secret key for JWT"
echo "   - ALGORITHM: HS256"
echo "   - ACCESS_TOKEN_EXPIRE_MINUTES: 30"
echo ""
echo "6. The Space will automatically use the Dockerfile and space.yaml in your repository"
echo ""
echo "Deployment files have been created in your hf-deployment branch."
echo "You can now merge this branch to main if you wish."