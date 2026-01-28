import gradio as gr
import subprocess
import threading
import time
import requests
from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'phase-2-fullstack-todo-app'))

from phase_2_fullstack_todo_app.backend.src.main import app as fastapi_app
import uvicorn
import os

def run_backend():
    """Function to run the FastAPI backend"""
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

def test_backend():
    """Test function to verify the backend is responding"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            return "✅ Backend is running and healthy"
        else:
            return f"❌ Backend responded with status: {response.status_code}"
    except Exception as e:
        return f"❌ Backend not accessible: {str(e)}"

with gr.Blocks(title="Todo App Backend") as demo:
    gr.Markdown("# Todo App Backend")
    gr.Markdown("This interface manages the backend API for the Todo application")
    
    with gr.Row():
        with gr.Column():
            status_btn = gr.Button("Check Backend Status")
            status_output = gr.Textbox(label="Status")
            
            status_btn.click(fn=test_backend, inputs=None, outputs=status_output)
    
    gr.Markdown("## API Endpoints")
    gr.Markdown("- `/auth/signup` - User registration")
    gr.Markdown("- `/auth/signin` - User authentication") 
    gr.Markdown("- `/tasks` - Task management")
    gr.Markdown("- `/health` - Health check endpoint")

# Start the backend in a separate thread
if __name__ == "__main__":
    # Start the FastAPI backend in a background thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Give the backend a moment to start
    time.sleep(2)
    
    # Launch the Gradio interface
    demo.launch(server_name="0.0.0.0", server_port=7860)