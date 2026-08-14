// api.js — Live Backend Fetch Service
const BASE_URL = "http://127.0.0.1:8000";

function getHeaders() {
  const token = localStorage.getItem("taskflow_token");
  return {
    "Content-Type": "application/json",
    ...(token ? { "Authorization": `Bearer ${token}` } : {})
  };
}

export const API = {
  // Auth & Profile
  async signup(userData) {
    const res = await fetch(`${BASE_URL}/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userData)
    });
    return res;
  },

  async login(credentials) {
    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(credentials)
    });
    return res;
  },

  async getProfile() {
    const res = await fetch(`${BASE_URL}/users/me`, { headers: getHeaders() });
    if (!res.ok) throw new Error("Failed to load user profile");
    return await res.json();
  },

  async updateProfile(profileData) {
    const res = await fetch(`${BASE_URL}/users/me`, {
      method: "PUT",
      headers: getHeaders(),
      body: JSON.stringify(profileData)
    });
    if (!res.ok) throw new Error("Failed to update profile");
    return await res.json();
  },

  async updatePassword({ currentPassword, newPassword }) {
    const response = await fetch(`${BASE_URL}/users/password`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Failed to update password');
    }

    return data;
  },

  // Projects
  async getProjects() {
    const res = await fetch(`${BASE_URL}/projects`, { headers: getHeaders() });
    if (!res.ok) throw new Error("Failed to fetch projects");
    return await res.json();
  },

  async createProject(name, ownerId = null) {
    const payload = { 
      name,
      owner_id: ownerId && String(ownerId).trim() !== "" ? String(ownerId) : null
    };

    const res = await fetch(`${BASE_URL}/projects`, {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify(payload)
    });
    
    if (res.status === 422) {
      const errData = await res.json();
      console.error("Project Validation Error:", errData);
      throw new Error(errData.detail?.[0]?.msg || "Invalid Project Data");
    }

    if (!res.ok) throw new Error("Failed to create project");
    return await res.json();
  },

  async deleteProject(id) {
    const res = await fetch(`${BASE_URL}/projects/${id}`, {
      method: "DELETE",
      headers: getHeaders()
    });
    if (!res.ok) throw new Error("Failed to delete project");
    return true;
  },

  async getProjectStats() {
    const res = await fetch(`${BASE_URL}/projects/stats`, { headers: getHeaders() });
    if (!res.ok) throw new Error("Failed to load project stats");
    return await res.json();
  },

  // Tasks CRUD
  async getTasks(search = "", sort = "") {
    let url = `${BASE_URL}/tasks`;
    const params = new URLSearchParams();
    if (search) params.append("search", search);
    if (sort) params.append("sort", sort);
    if (params.toString()) url += `?${params.toString()}`;

    const res = await fetch(url, { headers: getHeaders() });
    if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
    const data = await res.json();
    
    localStorage.setItem("taskflow_tasks_cache", JSON.stringify(data));
    return data;
  },

  async createTask(taskData) {
    const sanitizedData = {
      title: String(taskData.title).trim(),
      priority: (taskData.priority || "medium").toLowerCase(),
      due_date: taskData.due_date && String(taskData.due_date).trim() !== "" ? String(taskData.due_date).trim() : null,
      project_id: taskData.project_id && String(taskData.project_id).trim() !== "" ? String(taskData.project_id) : null
    };

    const res = await fetch(`${BASE_URL}/tasks`, {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify(sanitizedData)
    });
    
    if (res.status === 422) {
      const errData = await res.json();
      console.error("Task Validation Error:", errData);
      throw new Error(errData.detail?.[0]?.msg || "Validation Failed");
    }
    
    if (!res.ok) throw new Error("Failed to create task");
    return await res.json();
  },

  async quickAddTask(quickData) {
    const payload = {
      description: String(quickData.text || quickData.description).trim(),
      project_id: quickData.project_id && String(quickData.project_id).trim() !== "" ? String(quickData.project_id) : null
    };

    const res = await fetch(`${BASE_URL}/tasks/quick-add`, {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      return await this.createTask({
        title: payload.description,
        project_id: payload.project_id
      });
    }

    return await res.json();
  },

  async toggleTask(id, completed) {
    const res = await fetch(`${BASE_URL}/tasks/${id}`, {
      method: "PATCH",
      headers: getHeaders(),
      body: JSON.stringify({ completed: Boolean(completed) })
    });
    if (!res.ok) throw new Error("Failed to update task status");
    return await res.json();
  },

  async updateTask(id, updateData) {
    const res = await fetch(`${BASE_URL}/tasks/${id}`, {
      method: "PATCH",
      headers: getHeaders(),
      body: JSON.stringify(updateData)
    });
    if (!res.ok) throw new Error("Failed to update task");
    return await res.json();
  },

  async deleteTask(id) {
    const res = await fetch(`${BASE_URL}/tasks/${id}`, {
      method: "DELETE",
      headers: getHeaders()
    });
    if (!res.ok) throw new Error("Failed to delete task");
    return true;
  }
};