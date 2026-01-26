import gradio as gr
import subprocess
import threading
import time
import requests
from fastapi import FastAPI
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
import os

from backend.src.main import app as fastapi_app

def run_backend():
    """Function to run the FastAPI backend"""
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)

def launch_gradio_interface():
    """Gradio interface to interact with your backend"""
    
    def signup_user(username, email, password):
        try:
            response = requests.post("http://localhost:8000/auth/signup", json={
                "username": username,
                "email": email,
                "password": password
            })
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def signin_user(username, password):
        try:
            response = requests.post("http://localhost:8000/auth/signin", json={
                "username": username,
                "password": password
            })
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def create_task(title, description, token):
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post("http://localhost:8000/tasks", json={
                "title": title,
                "description": description,
                "completed": False
            }, headers=headers)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_tasks(token):
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get("http://localhost:8000/tasks", headers=headers)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    with gr.Blocks(title="Todo App Backend") as demo:
        gr.Markdown("# Todo App Backend Interface")
        gr.Markdown("Use this interface to interact with the backend API")
        
        with gr.Tab("User Signup"):
            signup_username = gr.Textbox(label="Username")
            signup_email = gr.Textbox(label="Email")
            signup_password = gr.Textbox(label="Password", type="password")
            signup_btn = gr.Button("Signup")
            signup_output = gr.Textbox(label="Response", interactive=False)
            
            signup_btn.click(
                fn=signup_user,
                inputs=[signup_username, signup_email, signup_password],
                outputs=signup_output
            )
        
        with gr.Tab("User Signin"):
            signin_username = gr.Textbox(label="Username")
            signin_password = gr.Textbox(label="Password", type="password")
            signin_btn = gr.Button("Signin")
            signin_output = gr.Textbox(label="Response", interactive=False)
            
            signin_btn.click(
                fn=signin_user,
                inputs=[signin_username, signin_password],
                outputs=signin_output
            )
        
        with gr.Tab("Create Task"):
            task_title = gr.Textbox(label="Task Title")
            task_description = gr.Textbox(label="Task Description")
            task_token = gr.Textbox(label="Auth Token")
            create_task_btn = gr.Button("Create Task")
            task_output = gr.Textbox(label="Response", interactive=False)
            
            create_task_btn.click(
                fn=create_task,
                inputs=[task_title, task_description, task_token],
                outputs=task_output
            )
        
        with gr.Tab("View Tasks"):
            view_token = gr.Textbox(label="Auth Token")
            view_btn = gr.Button("Get Tasks")
            view_output = gr.Textbox(label="Tasks", interactive=False)
            
            view_btn.click(
                fn=get_tasks,
                inputs=[view_token],
                outputs=view_output
            )
    
    return demo

# Start the backend in a separate thread
if __name__ == "__main__":
    # Start the FastAPI backend in a background thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a bit for the backend to start
    time.sleep(2)
    
    # Launch the Gradio interface
    demo = launch_gradio_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)