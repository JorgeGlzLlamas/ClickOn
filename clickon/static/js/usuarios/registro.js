document.addEventListener('DOMContentLoaded', function () {

    // Restrict phone input to numbers only
    const phoneInput = document.getElementById('phone');
    phoneInput.addEventListener('input', function () {
        this.value = this.value.replace(/[^0-9]/g, '');
    });

    // Form validation
    const form = document.getElementById('registroForm');
    form.addEventListener('submit', function (event) {
        let valid = true;

        // Validate first name and last name (letters and accented characters)
        const nameFields = ['first_name', 'last_name'];
        nameFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (!/^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+$/.test(field.value)) {
                field.setCustomValidity('Por favor ingresa solo letras (con o sin acentos).');
                valid = false;
            } else {
                field.setCustomValidity('');
            }
        });

        // Validate username (at least 4 characters, no spaces)
        const username = document.getElementById('username');
        if (!/^\S{4,}$/.test(username.value)) {
            username.setCustomValidity('El nombre de usuario debe tener al menos 4 caracteres y no puede contener espacios.');
            valid = false;
        } else {
            username.setCustomValidity('');
        }

        // Validate email format
        const email = document.getElementById('email');
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
            email.setCustomValidity('Ingresa un correo electrónico válido.');
            valid = false;
        } else {
            email.setCustomValidity('');
        }

        // Validate password (at least 8 characters, including uppercase, lowercase, and numbers)
        const password1 = document.getElementById('password1');
        if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}/.test(password1.value)) {
            password1.setCustomValidity('La contraseña debe tener al menos 8 caracteres, incluyendo mayúsculas, minúsculas y números.');
            valid = false;
        } else {
            password1.setCustomValidity('');
        }

        // Validate password confirmation
        const password2 = document.getElementById('password2');
        if (password1.value !== password2.value) {
            password2.setCustomValidity('Las contraseñas no coinciden.');
            valid = false;
        } else {
            password2.setCustomValidity('');
        }

        if (!valid || !form.checkValidity()) {
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