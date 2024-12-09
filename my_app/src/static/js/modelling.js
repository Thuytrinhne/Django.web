$(document).ready(function() {
    // Initialize Selectize for dropdown fields
    $('select').selectize({
        sortField: 'text'
    });
});

// Handle range input changes
document.querySelectorAll('input[type="range"]').forEach(range => {
    const output = range.parentElement.querySelector('output');
    range.addEventListener('input', (e) => {
        output.textContent = e.target.value;
    });
});

// Form submission handler
document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);
    console.log('Form data:', data);
    // Here you would send the data to your backend
    alert('Form submitted successfully!');
}); 