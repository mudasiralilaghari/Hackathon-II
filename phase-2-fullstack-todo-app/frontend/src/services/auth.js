// API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://fazalahmed-full-stack-todo-app.hf.space';

/**
 * Signs up a new user
 */
export const signup = async (userData) => {
  try {
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

    return await response.json();
  } catch (error) {
    console.error('Signup error:', error);
    throw error;
  }
};

/**
 * Signs in a user
 */
export const signin = async (credentials) => {
  try {
    // Create form data for the request
    const formData = new FormData();
    formData.append('email', credentials.email);
    formData.append('password', credentials.password);

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

    return await response.json();
  } catch (error) {
    console.error('Signin error:', error);
    throw error;
  }
};

/**
 * Gets the current user's profile
 */
export const getCurrentUser = async () => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      throw new Error('No access token found');
    }

    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
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
      throw new Error(errorData.detail || 'Failed to get user profile');
    }

    return await response.json();
  } catch (error) {
    console.error('Get user error:', error);
    throw error;
  }
};

/**
 * Checks if the user is authenticated
 */
export const isAuthenticated = () => {
  const token = localStorage.getItem('access_token');
  return !!token;
};

/**
 * Logs out the current user
 */
export const logout = () => {
  localStorage.removeItem('access_token');
};