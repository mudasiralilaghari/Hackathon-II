import React, { useState, useEffect } from 'react';
import TaskItem from './TaskItem';
import TaskForm from './TaskForm';
import { fetchTasks, createTask, updateTask, deleteTask, toggleTaskCompletion } from '../../services/api';

const TaskList = ({ userId }) => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load tasks from API
  useEffect(() => {
    const loadTasks = async () => {
      try {
        const tasksData = await fetchTasks();
        setTasks(tasksData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadTasks();
  }, [userId]);

  const handleTaskAdded = (newTask) => {
    setTasks(prevTasks => [...prevTasks, newTask]);
  };

  const handleTaskUpdated = (updatedTask) => {
    setTasks(prevTasks => prevTasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (deletedTaskId) => {
    setTasks(prevTasks => prevTasks.filter(task => task.id !== deletedTaskId));
  };

  const handleToggleComplete = async (taskId) => {
    try {
      const updatedTask = await toggleTaskCompletion(taskId);
      setTasks(prevTasks => prevTasks.map(task => task.id === updatedTask.id ? updatedTask : task));
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div className="text-center py-10">Loading tasks...</div>;
  if (error) return <div className="text-center py-10 text-red-500">Error: {error}</div>;

  return (
    <div className="max-w-2xl mx-auto mt-8">
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Your Tasks</h2>
        <TaskForm onTaskAdded={handleTaskAdded} />
      </div>

      {tasks.length === 0 ? (
        <div className="text-center py-10 text-gray-500">
          No tasks yet. Add your first task above!
        </div>
      ) : (
        <ul className="space-y-4">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onTaskUpdated={handleTaskUpdated}
              onTaskDeleted={handleTaskDeleted}
              onToggleComplete={handleToggleComplete}
            />
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;