// Simulating a logged-in user
const userName = 'Hello, John Doe';
document.getElementById('userName').textContent = userName;
document.getElementById('userNameDropdown').textContent = userName;

function logout() {
     window.location.href = '/login';
} 