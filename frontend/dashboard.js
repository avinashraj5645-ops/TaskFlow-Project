import { API } from './api.js';

// Auth Guard Check
if (localStorage.getItem('isLoggedIn') !== 'true' && !localStorage.getItem('taskflow_token')) {
  window.location.href = 'login.html';
}

document.addEventListener('DOMContentLoaded', () => {
  const projectForm = document.getElementById('project-form');
  const projectNameInput = document.getElementById('project-name');
  const projectNameError = document.getElementById('project-name-error');

  const taskForm = document.getElementById('task-form');
  const taskTitleInput = document.getElementById('task-title');
  const taskTitleError = document.getElementById('task-title-error');
  const taskDueInput = document.getElementById('task-due');
  const taskPrioritySelect = document.getElementById('task-priority');
  const taskProjectSelect = document.getElementById('task-project');

  const quickAddForm = document.getElementById('quick-add-form');
  const quickAddInput = document.getElementById('quick-add-input');
  const quickAddProjectSelect = document.getElementById('quick-add-project');
  const quickAddError = document.getElementById('quick-add-error');

  const taskListContainer = document.getElementById('task-list');
  const emptyState = document.getElementById('empty-state');
  const taskSearchInput = document.getElementById('task-search');
  const taskSortSelect = document.getElementById('task-sort');

  let tasks = [];
  let projects = [];

  async function init() {
    await fetchProjects();
    await fetchTasks();
  }

  async function fetchProjects() {
    try {
      projects = await API.getProjects();
      populateProjectDropdowns(projects);
    } catch (err) {
      console.error('Projects load error:', err);
    }
  }

  async function fetchTasks(search = '', sort = '') {
    try {
      tasks = await API.getTasks(search, sort);
      renderTasks(tasks);
    } catch (err) {
      console.error('Tasks load error:', err);
    }
  }

  // Populate ALL Project Dropdowns (Fixed Default Option Handling)
  function populateProjectDropdowns(projectList) {
    const dropdowns = [taskProjectSelect, quickAddProjectSelect];

    dropdowns.forEach(select => {
      if (!select) return;
      select.innerHTML = '';

      // Default option for "No Project / Optional"
      select.add(new Option('-- Select Project (Optional) --', ''));

      if (!projectList || projectList.length === 0) {
        return;
      }

      projectList.forEach(proj => {
        const pName = proj.name || proj.title || `Project #${proj.id}`;
        select.add(new Option(pName, proj.id));
      });
    });
  }

  // 1. Create Project Handler
  projectForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (projectNameError) projectNameError.textContent = '';
    const nameVal = projectNameInput.value.trim();

    if (!nameVal) {
      if (projectNameError) projectNameError.textContent = 'Project name required.';
      return;
    }

    try {
      await API.createProject(nameVal);
      projectNameInput.value = '';
      await fetchProjects();
    } catch (err) {
      console.error(err);
      if (projectNameError) projectNameError.textContent = err.message || 'Error creating project.';
    }
  });

  // 2. Add Standard Task Form Handler
  taskForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (taskTitleError) taskTitleError.textContent = '';

    const title = taskTitleInput.value.trim();
    if (!title) {
      if (taskTitleError) taskTitleError.textContent = 'Task title is required.';
      return;
    }

    const dueDateVal = taskDueInput?.value?.trim() || null;
    const projectIdVal = taskProjectSelect?.value || null;

    try {
      await API.createTask({
        title: title,
        due_date: dueDateVal,
        priority: taskPrioritySelect?.value || 'low',
        project_id: projectIdVal
      });

      taskForm.reset();
      fetchTasks(taskSearchInput?.value, taskSortSelect?.value);
    } catch (err) {
      console.error(err);
      if (taskTitleError) taskTitleError.textContent = err.message || 'Error creating task.';
    }
  });

  // 3. AI Quick-Add Form Handler
  quickAddForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (quickAddError) quickAddError.textContent = '';

    const inputVal = quickAddInput?.value.trim();
    if (!inputVal) {
      if (quickAddError) quickAddError.textContent = 'Please enter task description.';
      return;
    }

    try {
      await API.quickAddTask({
        text: inputVal,
        project_id: quickAddProjectSelect?.value || null
      });

      quickAddForm.reset();
      fetchTasks(taskSearchInput?.value, taskSortSelect?.value);
    } catch (err) {
      console.error(err);
      if (quickAddError) quickAddError.textContent = err.message || 'Error in quick-add task.';
    }
  });

  // 4. Search and Sort Event Listeners
  taskSearchInput?.addEventListener('input', (e) => {
    fetchTasks(e.target.value.trim(), taskSortSelect?.value);
  });

  taskSortSelect?.addEventListener('change', (e) => {
    fetchTasks(taskSearchInput?.value.trim(), e.target.value);
  });

  // Render Tasks Function
  function renderTasks(taskList) {
    if (!taskListContainer) return;
    taskListContainer.innerHTML = '';

    if (!taskList || taskList.length === 0) {
      if (emptyState) emptyState.hidden = false;
      return;
    }

    if (emptyState) emptyState.hidden = true;

    taskList.forEach(task => {
      const taskCard = document.createElement('div');
      taskCard.className = `task-item ${task.completed ? 'completed' : ''}`;
      taskCard.innerHTML = `
        <div class="task-info">
          <input type="checkbox" class="task-check" ${task.completed ? 'checked' : ''}>
          <div class="task-details">
            <span class="task-title-text">${escapeHTML(task.title || '')}</span>
            <div class="task-meta">
              ${task.due_date ? `<span class="due-tag">📅 ${escapeHTML(task.due_date)}</span>` : ''}
              <span class="priority-tag priority-${task.priority}">${task.priority || 'low'}</span>
            </div>
          </div>
        </div>
        <button class="btn-delete">&times;</button>
      `;

      taskCard.querySelector('.task-check').addEventListener('change', async (e) => {
        await API.toggleTask(task.id, e.target.checked);
        fetchTasks(taskSearchInput?.value, taskSortSelect?.value);
      });

      taskCard.querySelector('.btn-delete').addEventListener('click', async () => {
        await API.deleteTask(task.id);
        fetchTasks(taskSearchInput?.value, taskSortSelect?.value);
      });

      taskListContainer.appendChild(taskCard);
    });
  }

  function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag));
  }

  init();
});