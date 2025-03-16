// Función para alternar la visibilidad de la contraseña
function togglePassword(fieldId) {
    const passwordField = document.getElementById(fieldId);
    const toggleIcon = document.getElementById('toggleIcon' + fieldId.replace('password', ''));
    
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('bi-eye');
        toggleIcon.classList.add('bi-eye-slash');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('bi-eye-slash');
        toggleIcon.classList.add('bi-eye');
    }
}

// Validación del formulario de registro
document.addEventListener('DOMContentLoaded', function() {
    const registroForm = document.getElementById('registroForm');
    
    if (registroForm) {
        registroForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validar nombre de usuario
            const username = document.getElementById('username');
            if (username.value.trim().length < 4) {
                showError(username, 'El nombre de usuario debe tener al menos 4 caracteres');
                isValid = false;
            } else {
                removeError(username);
            }
            
            // Validar correo electrónico
            const email = document.getElementById('email');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email.value.trim())) {
                showError(email, 'Por favor ingresa un correo electrónico válido');
                isValid = false;
            } else {
                removeError(email);
            }
            
            // Validar nombre
            const firstName = document.getElementById('first_name');
            if (firstName.value.trim().length < 2) {
                showError(firstName, 'Por favor ingresa tu nombre');
                isValid = false;
            } else {
                removeError(firstName);
            }
            
            // Validar apellido
            const lastName = document.getElementById('last_name');
            if (lastName.value.trim().length < 2) {
                showError(lastName, 'Por favor ingresa tu apellido');
                isValid = false;
            } else {
                removeError(lastName);
            }
            
            // Validar teléfono
            const phone = document.getElementById('phone');
            const phoneRegex = /^[0-9]{10}$/;
            if (!phoneRegex.test(phone.value.trim())) {
                showError(phone, 'Por favor ingresa un número de teléfono válido (10 dígitos)');
                isValid = false;
            } else {
                removeError(phone);
            }
            
            // Validar contraseña
            const password1 = document.getElementById('password1');
            const password2 = document.getElementById('password2');
            
            if (password1.value.length < 8) {
                showError(password1, 'La contraseña debe tener al menos 8 caracteres');
                isValid = false;
            } else if (!/[A-Z]/.test(password1.value)) {
                showError(password1, 'La contraseña debe contener al menos una letra mayúscula');
                isValid = false;
            } else if (!/[a-z]/.test(password1.value)) {
                showError(password1, 'La contraseña debe contener al menos una letra minúscula');
                isValid = false;
            } else if (!/[0-9]/.test(password1.value)) {
                showError(password1, 'La contraseña debe contener al menos un número');
                isValid = false;
            } else {
                removeError(password1);
            }
            
            // Validar que las contraseñas coincidan
            if (password1.value !== password2.value) {
                showError(password2, 'Las contraseñas no coinciden');
                isValid = false;
            } else if (password2.value.length > 0) {
                removeError(password2);
            }
            
            // Validar términos y condiciones
            const terms = document.getElementById('terms');
            if (!terms.checked) {
                showError(terms, 'Debes aceptar los términos y condiciones');
                isValid = false;
            } else {
                removeError(terms);
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Función para mostrar mensajes de error
    function showError(input, message) {
        const formGroup = input.closest('.mb-3') || input.closest('.mb-4');
        let errorDiv = formGroup.querySelector('.error-message');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-danger mt-1';
            formGroup.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
        input.classList.add('is-invalid');
    }
    
    // Función para eliminar mensajes de error
    function removeError(input) {
        const formGroup = input.closest('.mb-3') || input.closest('.mb-4');
        const errorDiv = formGroup.querySelector('.error-message');
        
        if (errorDiv) {
            errorDiv.remove();
        }
        
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    }
    
    // Validación en tiempo real para el campo de contraseña
    const password1 = document.getElementById('password1');
    if (password1) {
        password1.addEventListener('input', function() {
            const strengthMeter = document.getElementById('password-strength');
            const val = password1.value;
            let strength = 0;
            
            // Si la contraseña tiene más de 8 caracteres, suma 1 punto
            if (val.length >= 8) strength += 1;
            
            // Si la contraseña tiene al menos una letra minúscula, suma 1 punto
            if (/[a-z]/.test(val)) strength += 1;
            
            // Si la contraseña tiene al menos una letra mayúscula, suma 1 punto
            if (/[A-Z]/.test(val)) strength += 1;
            
            // Si la contraseña tiene al menos un número, suma 1 punto
            if (/[0-9]/.test(val)) strength += 1;
            
            // Si la contraseña tiene al menos un carácter especial, suma 1 punto
            if (/[^a-zA-Z0-9]/.test(val)) strength += 1;
            
            // Actualizar la barra de progreso
            strengthMeter.style.width = (strength * 20) + '%';
            
            // Cambiar el color de la barra según la fortaleza
            if (strength <= 2) {
                strengthMeter.className = 'progress-bar bg-danger';
                strengthMeter.textContent = 'Débil';
            } else if (strength <= 3) {
                strengthMeter.className = 'progress-bar bg-warning';
                strengthMeter.textContent = 'Media';
            } else {
                strengthMeter.className = 'progress-bar bg-success';
                strengthMeter.textContent = 'Fuerte';
            }
        });
    }
});

// Validación en tiempo real para el campo de correo electrónico
document.addEventListener('DOMContentLoaded', function() {
    const emailField = document.getElementById('email');
    
    if (emailField) {
        emailField.addEventListener('blur', function() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailField.value.trim()) && emailField.value.trim() !== '') {
                showError(emailField, 'Por favor ingresa un correo electrónico válido');
            } else if (emailField.value.trim() !== '') {
                removeError(emailField);
            }
        });
    }
    
    // Validación en tiempo real para el campo de teléfono
    const phoneField = document.getElementById('phone');
    
    if (phoneField) {
        phoneField.addEventListener('input', function(e) {
            // Permitir solo números
            this.value = this.value.replace(/[^0-9]/g, '');
            
            // Limitar a 10 dígitos
            if (this.value.length > 10) {
                this.value = this.value.slice(0, 10);
            }
        });
        
        phoneField.addEventListener('blur', function() {
            const phoneRegex = /^[0-9]{10}$/;
            if (!phoneRegex.test(phoneField.value.trim()) && phoneField.value.trim() !== '') {
                showError(phoneField, 'Por favor ingresa un número de teléfono válido (10 dígitos)');
            } else if (phoneField.value.trim() !== '') {
                removeError(phoneField);
            }
        });
    }
    
    // Validación en tiempo real para confirmar contraseña
    const password2Field = document.getElementById('password2');
    const password1Field = document.getElementById('password1');
    
    if (password2Field && password1Field) {
        password2Field.addEventListener('input', function() {
            if (password1Field.value !== password2Field.value) {
                showError(password2Field, 'Las contraseñas no coinciden');
            } else {
                removeError(password2Field);
            }
        });
    }
    
    // Función para mostrar mensajes de error (ya definida anteriormente)
    function showError(input, message) {
        const formGroup = input.closest('.mb-3') || input.closest('.mb-4');
        let errorDiv = formGroup.querySelector('.error-message');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-danger mt-1';
            formGroup.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
        input.classList.add('is-invalid');
    }
    
    // Función para eliminar mensajes de error (ya definida anteriormente)
    function removeError(input) {
        const formGroup = input.closest('.mb-3') || input.closest('.mb-4');
        const errorDiv = formGroup.querySelector('.error-message');
        
        if (errorDiv) {
            errorDiv.remove();
        }
        
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    }
});

// Función para validar el formulario de inicio de sesión
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validar nombre de usuario o correo
            const username = document.getElementById('username');
            if (username && username.value.trim() === '') {
                showError(username, 'Por favor ingresa tu nombre de usuario o correo electrónico');
                isValid = false;
            } else if (username) {
                removeError(username);
            }
            
            // Validar contraseña
            const password = document.getElementById('password');
            if (password && password.value.trim() === '') {
                showError(password, 'Por favor ingresa tu contraseña');
                isValid = false;
            } else if (password) {
                removeError(password);
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Funciones para mostrar/eliminar errores (reutilizadas)
    function showError(input, message) {
        const formGroup = input.closest('.mb-3') || input.closest('.mb-4');
        let errorDiv = formGroup.querySelector('.error-message');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-danger mt-1';
            formGroup.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
        input.classList.add('is-invalid');
    }
    
    function removeError(input) {
        const formGroup = input.closest('.mb-3') || input.closest('.mb-4');
        const errorDiv = formGroup.querySelector('.error-message');
        
        if (errorDiv) {
            errorDiv.remove();
        }
        
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    }
});

// Función para validar el formulario de recuperación de contraseña
document.addEventListener('DOMContentLoaded', function() {
    const recoveryForm = document.getElementById('recoveryForm');
    
    if (recoveryForm) {
        recoveryForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validar correo electrónico
            const email = document.getElementById('recovery_email');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (email && !emailRegex.test(email.value.trim())) {
                showError(email, 'Por favor ingresa un correo electrónico válido');
                isValid = false;
            } else if (email) {
                removeError(email);
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Funciones para mostrar/eliminar errores (reutilizadas)
    function showError(input, message) {
        const formGroup = input.closest('.mb-3') || input.closest('.mb-4');
        let errorDiv = formGroup.querySelector('.error-message');
        
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message text-danger mt-1';
            formGroup.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
        input.classList.add('is-invalid');
    }
    
    function removeError(input) {
        const formGroup = input.closest('.mb-3') || input.closest('.mb-4');
        const errorDiv = formGroup.querySelector('.error-message');
        
        if (errorDiv) {
            errorDiv.remove();
        }
        
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    }
});

// Animación para mensajes de alerta
document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todos los mensajes de alerta
    const alerts = document.querySelectorAll('.alert');
    
    // Añadir animación de entrada
    alerts.forEach(alert => {
        // Añadir clase para animación de entrada
        alert.classList.add('fade-in');
        
        // Configurar desaparición automática después de 5 segundos
        if (!alert.classList.contains('alert-danger')) {
            setTimeout(() => {
                alert.classList.add('fade-out');
                setTimeout(() => {
                    alert.remove();
                }, 500);
            }, 5000);
        }
        
        // Añadir botón de cierre si no existe
        if (!alert.querySelector('.btn-close')) {
            const closeButton = document.createElement('button');
            closeButton.type = 'button';
            closeButton.className = 'btn-close';
            closeButton.setAttribute('data-bs-dismiss', 'alert');
            closeButton.setAttribute('aria-label', 'Close');
            
            alert.classList.add('alert-dismissible');
            alert.appendChild(closeButton);
        }
    });
});