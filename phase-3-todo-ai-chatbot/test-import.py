import sys
print('Script started')
print('Python:', sys.version[:50])

sys.path.insert(0, 'D:/hackathon-II/phase-3-todo-ai-chatbot/backend/src')
print('Path added')

try:
    from api import task_routes
    print('SUCCESS: task_routes imported')
    print('Router:', task_routes.router)
except Exception as e:
    print('FAIL:', e)
    import traceback
    traceback.print_exc()

print('Script ended')
