// src/app/dashboard/page.js
'use client';

import { useState, useEffect } from 'react';
import { authAPI, taskAPI } from '../../services/api';
import ChatWidget from '../../components/ChatWidget';

export default function DashboardPage() {
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newTask, setNewTask] = useState({ title: '', description: '' });
  const [error, setError] = useState('');
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('access_token');
    if (!token) {
      // Redirect to signin if not authenticated
      window.location.href = '/signin';
      return;
    }

    // Get user info
    const fetchUserData = async () => {
      try {
        const userData = await authAPI.getUser();
        setUser(userData);
        fetchTasks();
      } catch (err) {
        setError('Failed to load user data');
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  const fetchTasks = async () => {
    try {
      const tasksData = await taskAPI.getTasks();
      setTasks(tasksData);
    } catch (err) {
      setError('Failed to load tasks: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    window.location.href = '/signin';
  };

  const handleAddTask = async (e) => {
    e.preventDefault();

    try {
      const createdTask = await taskAPI.createTask({
        title: newTask.title,
        description: newTask.description
      });
      setTasks([...tasks, createdTask]);
      setNewTask({ title: '', description: '' });
    } catch (err) {
      setError('Failed to create task: ' + err.message);
    }
  };

  const toggleTaskCompletion = async (taskId) => {
    try {
      const updatedTask = await taskAPI.toggleTaskCompletion(taskId);
      setTasks(tasks.map(task =>
        task.id === updatedTask.id ? updatedTask : task
      ));
    } catch (err) {
      setError('Failed to update task: ' + err.message);
    }
  };

  const deleteTask = async (taskId) => {
    try {
      await taskAPI.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      setError('Failed to delete task: ' + err.message);
    }
  };

  const updateTask = async (taskId, updatedData) => {
    try {
      const updatedTask = await taskAPI.updateTask(taskId, updatedData);
      setTasks(tasks.map(task =>
        task.id === updatedTask.id ? updatedTask : task
      ));
      // Exit edit mode
      setEditingTaskId(null);
      setEditTitle('');
      setEditDescription('');
    } catch (err) {
      setError('Failed to update task: ' + err.message);
    }
  };

  const handleSaveEdit = async (taskId) => {
    try {
      await updateTask(taskId, {
        title: editTitle,
        description: editDescription
      });
    } catch (err) {
      setError('Failed to save task: ' + err.message);
    }
  };

  const cancelEdit = () => {
    setEditingTaskId(null);
    setEditTitle('');
    setEditDescription('');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl">Loading dashboard...</div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-red-500">Access denied. Redirecting...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Todo Dashboard</h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">Welcome, {user.username}!</span>
            <button
              onClick={handleLogout}
              className="bg-red-600 text-white py-1 px-3 rounded hover:bg-red-700"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Task Management */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Add New Task</h2>
              <form onSubmit={handleAddTask} className="space-y-4">
                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                    Title *
                  </label>
                  <input
                    id="title"
                    type="text"
                    value={newTask.title}
                    onChange={(e) => setNewTask({...newTask, title: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="What needs to be done?"
                    required
                  />
                </div>

                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    id="description"
                    value={newTask.description}
                    onChange={(e) => setNewTask({...newTask, description: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Additional details (optional)"
                    rows="3"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  Add Task
                </button>
              </form>
            </div>

            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Your Tasks</h2>

              {tasks.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  No tasks yet. Add your first task above!
                </div>
              ) : (
                <ul className="space-y-4">
                  {tasks.map((task) => (
                    editingTaskId === task.id ? (
                      // Editing mode
                      <li key={task.id} className="border rounded-lg p-4 bg-blue-50">
                        <div className="space-y-3">
                          <input
                            type="text"
                            value={editTitle}
                            onChange={(e) => setEditTitle(e.target.value)}
                            className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 border-blue-300"
                            placeholder="Task title"
                          />
                          <textarea
                            value={editDescription}
                            onChange={(e) => setEditDescription(e.target.value)}
                            className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 border-blue-300"
                            placeholder="Task description"
                            rows="3"
                          />
                          <div className="flex space-x-2">
                            <button
                              onClick={() => handleSaveEdit(task.id)}
                              className="bg-blue-600 text-white py-1 px-3 rounded hover:bg-blue-700 transition"
                            >
                              Save
                            </button>
                            <button
                              onClick={cancelEdit}
                              className="bg-gray-300 text-gray-700 py-1 px-3 rounded hover:bg-gray-400 transition"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      </li>
                    ) : (
                      // Viewing mode
                      <li key={task.id} className={`border rounded-lg p-4 ${task.is_completed ? 'bg-green-50' : 'bg-white'}`}>
                        <div className="flex items-start justify-between">
                          <div className="flex items-start space-x-3">
                            <input
                              type="checkbox"
                              checked={task.is_completed}
                              onChange={() => toggleTaskCompletion(task.id)}
                              className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                            />
                            <div>
                              <h3 className={`text-lg ${task.is_completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                                {task.title}
                              </h3>
                              {task.description && (
                                <p className={`${task.is_completed ? 'line-through text-gray-500' : 'text-gray-600'} mt-1`}>
                                  {task.description}
                                </p>
                              )}
                              <p className="text-xs text-gray-400 mt-2">
                                Created: {new Date(task.created_at).toLocaleDateString()}
                              </p>
                            </div>
                          </div>
                          <div className="flex space-x-3">
                            <button
                              onClick={() => {
                                // Set up editing state for this task
                                setEditingTaskId(task.id);
                                setEditTitle(task.title);
                                setEditDescription(task.description || '');
                              }}
                              className="text-blue-600 hover:text-blue-800 font-medium text-sm px-3 py-1 rounded hover:bg-blue-50 transition"
                            >
                              ✏️ Edit
                            </button>
                            <button
                              onClick={() => deleteTask(task.id)}
                              className="text-red-600 hover:text-red-800 font-medium text-sm px-3 py-1 rounded hover:bg-red-50 transition"
                            >
                              Delete
                            </button>
                          </div>
                        </div>
                      </li>
                    )
                  ))}
                </ul>
              )}
            </div>
          </div>

          {/* Right Column - AI Chat Assistant */}
          <div className="lg:col-span-1">
            <div className="bg-white shadow rounded-lg p-6 h-full">
              <h2 className="text-xl font-semibold mb-4">AI Todo Assistant</h2>
              <p className="text-gray-600 mb-4">Ask me to help manage your tasks!</p>
              
              <div className="h-[calc(100%-80px)]" style={{ minHeight: '500px' }}>
                {user ? (
                  <ChatWidget userId={user.id || user.email || user.username} />
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <p className="text-gray-500">Loading user info...</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}