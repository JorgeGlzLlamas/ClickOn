// Función para manejar el cambio de modo oscuro/claro
document.addEventListener('DOMContentLoaded', function() {
    const modoOscuroToggle = document.getElementById('modo-oscuro-toggle');
    const animacionesToggle = document.getElementById('animaciones-toggle');
    const botonesTexto = document.querySelectorAll('.btn-tamano');
    
    // Verificar si hay preferencias guardadas
    const modoOscuro = localStorage.getItem('modoOscuro') === 'true';
    const animacionesActivas = localStorage.getItem('animaciones') !== 'false';
    const tamanoTexto = localStorage.getItem('tamanoTexto') || 'normal';
    
    // Aplicar preferencias guardadas
    if (modoOscuro) {
        document.body.classList.add('modo-oscuro');
        modoOscuroToggle.checked = true;
    }
    
    animacionesToggle.checked = animacionesActivas;
    if (!animacionesActivas) {
        document.body.classList.add('sin-animaciones');
    }
    
    // Aplicar tamaño de texto guardado
    document.body.classList.add(`texto-${tamanoTexto}`);
    botonesTexto.forEach(btn => {
        if (btn.getAttribute('data-tamano') === tamanoTexto) {
            btn.classList.add('activo');
        } else {
            btn.classList.remove('activo');
        }
    });
    
    // Manejar cambio de modo oscuro
    modoOscuroToggle.addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.add('modo-oscuro');
            localStorage.setItem('modoOscuro', 'true');
        } else {
            document.body.classList.remove('modo-oscuro');
            localStorage.setItem('modoOscuro', 'false');
        }
    });
    
    // Manejar cambio de animaciones
    animacionesToggle.addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.remove('sin-animaciones');
            localStorage.setItem('animaciones', 'true');
        } else {
            document.body.classList.add('sin-animaciones');
            localStorage.setItem('animaciones', 'false');
        }
    });
    
    // Manejar cambio de tamaño de texto
    botonesTexto.forEach(btn => {
        btn.addEventListener('click', function() {
            const tamano = this.getAttribute('data-tamano');
            
            // Quitar clases de tamaño anteriores
            document.body.classList.remove('texto-pequeño', 'texto-normal', 'texto-grande');
            
            // Agregar nueva clase de tamaño
            document.body.classList.add(`texto-${tamano}`);
            
            // Actualizar botones
            botonesTexto.forEach(b => b.classList.remove('activo'));
            this.classList.add('activo');
            
            // Guardar preferencia
            localStorage.setItem('tamanoTexto', tamano);
        });
    });
});