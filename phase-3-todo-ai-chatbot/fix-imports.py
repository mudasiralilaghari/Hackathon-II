# Fix imports for Hugging Face Spaces
import os

filepath = 'D:/hackathon-II/phase-3-todo-ai-chatbot/backend/src/main.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace relative imports with absolute
content = content.replace('from ..models', 'from models')
content = content.replace('from ..services', 'from services')
content = content.replace('from ..api', 'from api')
content = content.replace('from ..mcp', 'from mcp')
content = content.replace('from ..agents', 'from agents')
content = content.replace('from .models', 'from models')
content = content.replace('from .services', 'from services')
content = content.replace('from .api', 'from api')
content = content.replace('from .mcp', 'from mcp')
content = content.replace('from .agents', 'from agents')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('main.py imports FIXED')
