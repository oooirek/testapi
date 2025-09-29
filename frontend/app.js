const API_URL = 'http://127.0.0.1:8000';

async function addTask() {
  const title = document.getElementById('taskTitle').value.trim();
  if (!title) return alert('Введите задачу');
  const res = await fetch(`${API_URL}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title })
  });
  if (res.ok) {
    document.getElementById('taskTitle').value = '';
    getAllTasks();
  }
}

async function getAllTasks() {
  const res = await fetch(`${API_URL}/tasks`);
  const tasks = await res.json();
  const listNew = document.getElementById('tasksNew');
  const listDone = document.getElementById('tasksDone');
  listNew.innerHTML = '';
  listDone.innerHTML = '';

  tasks.forEach(t => {
    const li = document.createElement('li');
    li.innerHTML = `
      <input type="checkbox" ${t.done ? 'checked' : ''} onchange="toggleTask(${t.id}, this)">
      <span ${t.done ? 'style="text-decoration: line-through;"' : ''}>${t.title}</span>
      <button onclick="deleteTask(${t.id})">Удалить</button>
    `;
    if (t.done) {
      listDone.appendChild(li);
    } else {
      listNew.appendChild(li);
    }
  });
}

async function toggleTask(id, checkbox) {
  const res = await fetch(`${API_URL}/tasks/${id}`, { method: 'PATCH' });
  if (!res.ok) {
    alert('Ошибка при изменении статуса');
    checkbox.checked = !checkbox.checked;
    return;
  }
  // сразу обновляем отображение
  const span = checkbox.nextElementSibling;
  if (checkbox.checked) {
    span.style.textDecoration = "line-through";
    document.getElementById('tasksDone').appendChild(checkbox.parentElement);
  } else {
    span.style.textDecoration = "none";
    document.getElementById('tasksNew').appendChild(checkbox.parentElement);
  }
}

async function deleteTask(id) {
  const res = await fetch(`${API_URL}/tasks/${id}`, { method: 'DELETE' });
  if (res.ok) getAllTasks();
}

async function resetDatabase() {
  const res = await fetch(`${API_URL}/data/setup_db`, { method: 'POST' });
  if (res.ok) getAllTasks();
}

document.addEventListener('DOMContentLoaded', getAllTasks);
