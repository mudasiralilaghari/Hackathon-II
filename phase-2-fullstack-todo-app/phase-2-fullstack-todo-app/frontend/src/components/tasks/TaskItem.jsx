import React, { useState } from 'react';
import { updateTask, deleteTask, toggleTaskCompletion } from '../../services/api';

const TaskItem = ({ task, onTaskUpdated, onTaskDeleted, onToggleComplete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');

  const handleSave = async () => {
    try {
      const updatedTask = await updateTask(task.id, {
        title: editTitle,
        description: editDescription,
      });
      onTaskUpdated(updatedTask);
      setIsEditing(false);
    } catch (err) {
      alert(err.message);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(task.id);
        onTaskDeleted(task.id);
      } catch (err) {
        alert(err.message);
      }
    }
  };

  const handleToggleComplete = async () => {
    try {
      const updatedTask = await toggleTaskCompletion(task.id);
      onTaskUpdated(updatedTask);
    } catch (err) {
      console.error("Error toggling task completion:", err);
      alert(err.message);
    }
  };

  return (
    <li className={`border rounded-lg p-4 ${task.is_completed ? 'bg-green-50' : 'bg-white'}`}>
      {isEditing ? (
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
              onClick={handleSave}
              className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition"
            >
              Save
            </button>
            <button
              onClick={() => setIsEditing(false)}
              className="bg-gray-300 text-gray-700 py-2 px-4 rounded hover:bg-gray-400 transition"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3 flex-grow">
            <input
              type="checkbox"
              checked={task.is_completed}
              onChange={handleToggleComplete}
              className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-pointer"
            />
            <div className="flex-grow">
              <h3 className={`text-lg font-medium ${task.is_completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className={`mt-1 ${task.is_completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
                  {task.description}
                </p>
              )}
              <p className="text-xs text-gray-400 mt-2">
                Created: {new Date(task.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
          <div className="flex space-x-3 ml-4">
            <button
              onClick={() => setIsEditing(true)}
              className="text-blue-600 hover:text-blue-800 font-medium text-sm px-3 py-1 rounded hover:bg-blue-50 transition"
              title="Edit task"
            >
              ✏️ Edit
            </button>
            <button
              onClick={handleDelete}
              className="text-red-600 hover:text-red-800 font-medium text-sm px-3 py-1 rounded hover:bg-red-50 transition"
              title="Delete task"
            >
              🗑️ Delete
            </button>
          </div>
        </div>
      )}
    </li>
  );
};

export default TaskItem;