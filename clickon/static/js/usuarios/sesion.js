document.addEventListener('DOMContentLoaded', function () {
    // Toggle password visibility
    const togglePassword = document.querySelector('.password-toggle');
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');

    togglePassword.addEventListener('click', function () {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        toggleIcon.classList.toggle('bi-eye');
        toggleIcon.classList.toggle('bi-eye-slash');
    });

    // Form validation
    const form = document.getElementById('loginForm');
    form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Por favor corrige los errores en el formulario.',
            });
        }
        form.classList.add('was-validated');
    }, false);
});