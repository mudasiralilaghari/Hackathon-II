// src/services/api.js
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://fazalahmed-full-stack-todo-app.hf.space';

// Define the apiCall function properly
const apiCall = async (endpoint, options = {}) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  console.log('Making API call to:', `${API_BASE_URL}${endpoint}`); // Debug log
  console.log('With headers:', config.headers); // Debug log

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

  // Check if the response is HTML instead of JSON
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('text/html')) {
    const htmlResponse = await response.text();
    console.error('Received HTML response instead of JSON:', htmlResponse.substring(0, 100) + '...');
    throw new Error('Backend API is returning HTML instead of JSON. Check if the backend is properly deployed and accessible.');
  }

  if (response.status === 401) {
    // Token might be expired, redirect to signin
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      window.location.href = '/signin';
    }
    throw new Error('Unauthorized');
  }

  return response;
};

export const authAPI = {
  signup: async (userData) => {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });

    // Check if the response is HTML instead of JSON
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('text/html')) {
      const htmlResponse = await response.text();
      console.error('Received HTML response instead of JSON:', htmlResponse.substring(0, 100) + '...');
      throw new Error('Backend API is returning HTML instead of JSON. Check if the backend is properly deployed and accessible.');
    }

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Signup failed');
    }

    return response.json();
  },

  signin: async (email, password) => {
    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/signin`, {
      method: 'POST',
      body: formData,
    });

    // Check if the response is HTML instead of JSON
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('text/html')) {
      const htmlResponse = await response.text();
      console.error('Received HTML response instead of JSON:', htmlResponse.substring(0, 100) + '...');
      throw new Error('Backend API is returning HTML instead of JSON. Check if the backend is properly deployed and accessible.');
    }

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Signin failed');
    }

    return response.json();
  },

  getUser: async () => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    console.log('Getting user with token:', token ? token.substring(0, 20) + '...' : 'NO TOKEN'); // Debug logging

    const response = await apiCall('/auth/me');
    if (!response.ok) {
      // Check if the response is HTML instead of JSON
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('text/html')) {
        const htmlResponse = await response.text();
        console.error('Received HTML response instead of JSON:', htmlResponse.substring(0, 100) + '...');
        throw new Error('Backend API is returning HTML instead of JSON. Check if the backend is properly deployed and accessible.');
      }

      const errorText = await response.text();
      console.error('Get user error response:', errorText); // Debug logging
      throw new Error(`Failed to get user: ${response.status}`);
    }
    return response.json();
  },
};

export const taskAPI = {
  getTasks: async () => {
    const response = await apiCall('/tasks');
    // Check if the response is HTML instead of JSON
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('text/html')) {
      const htmlResponse = await response.text();
      console.error('Received HTML response instead of JSON:', htmlResponse.substring(0, 100) + '...');
      throw new Error('Backend API is returning HTML instead of JSON. Check if the backend is properly deployed and accessible.');
    }
    if (!response.ok) {
      throw new Error('Failed to get tasks');
    }
    return response.json();
  },

  createTask: async (taskData) => {
    const response = await apiCall('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
    // Check if the response is HTML instead of JSON
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('text/html')) {
      const htmlResponse = await response.text();
      console.error('Received HTML response instead of JSON:', htmlResponse.substring(0, 100) + '...');
      throw new Error('Backend API is returning HTML instead of JSON. Check if the backend is properly deployed and accessible.');
    }
    if (!response.ok) {
      throw new Error('Failed to create task');
    }
    return response.json();
  },

  updateTask: async (id, taskData) => {
    const response = await apiCall(`/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
    // Check if the response is HTML instead of JSON
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('text/html')) {
      const htmlResponse = await response.text();
      console.error('Received HTML response instead of JSON:', htmlResponse.substring(0, 100) + '...');
      throw new Error('Backend API is returning HTML instead of JSON. Check if the backend is properly deployed and accessible.');
    }
    if (!response.ok) {
      throw new Error('Failed to update task');
    }
    return response.json();
  },

  deleteTask: async (id) => {
    const response = await apiCall(`/tasks/${id}`, {
      method: 'DELETE',
    });
    // Check if the response is HTML instead of JSON
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('text/html')) {
      const htmlResponse = await response.text();
      console.error('Received HTML response instead of JSON:', htmlResponse.substring(0, 100) + '...');
      throw new Error('Backend API is returning HTML instead of JSON. Check if the backend is properly deployed and accessible.');
    }
    if (!response.ok) {
      throw new Error('Failed to delete task');
    }
    return response;
  },

  toggleTaskCompletion: async (id) => {
    const response = await apiCall(`/tasks/${id}/toggle`, {
      method: 'PATCH',
    });
    // Check if the response is HTML instead of JSON
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('text/html')) {
      const htmlResponse = await response.text();
      console.error('Received HTML response instead of JSON:', htmlResponse.substring(0, 100) + '...');
      throw new Error('Backend API is returning HTML instead of JSON. Check if the backend is properly deployed and accessible.');
    }
    if (!response.ok) {
      throw new Error('Failed to toggle task completion');
    }
    return response.json();
  },
};