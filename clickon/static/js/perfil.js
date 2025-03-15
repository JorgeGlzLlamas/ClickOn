// Script para el perfil de cliente
document.addEventListener('DOMContentLoaded', function() {
    console.log("Perfil cliente: Script cargado");
    
    // Manejo de pestañas para perfil cliente
    const pestanas = document.querySelectorAll('.pestana');
    const contenidos = document.querySelectorAll('.contenido-pestana');
    
    // Función para cambiar entre pestañas
    function cambiarPestana(pestanaId) {
        console.log("Cambiando a pestaña:", pestanaId);
        
        // Ocultar todos los contenidos
        contenidos.forEach(contenido => {
            contenido.style.display = 'none';
            contenido.classList.add('oculto');
        });
        
        // Remover clase activa de todas las pestañas
        pestanas.forEach(p => {
            p.classList.remove('activa');
        });
        
        // Activar la pestaña seleccionada
        const pestanaSeleccionada = document.querySelector(`[data-pestana="${pestanaId}"]`);
        if (pestanaSeleccionada) {
            pestanaSeleccionada.classList.add('activa');
        }
        
        // Mostrar el contenido correspondiente
        const contenidoActivo = document.getElementById(`${pestanaId}-contenido`);
        if (contenidoActivo) {
            contenidoActivo.style.display = 'block';
            contenidoActivo.classList.remove('oculto');
        }
    }
    
    // Asignar evento click a cada pestaña
    pestanas.forEach(pestana => {
        pestana.addEventListener('click', function() {
            const targetId = this.getAttribute('data-pestana');
            cambiarPestana(targetId);
        });
    });
    
    // Activar la primera pestaña por defecto
    if (pestanas.length > 0) {
        const primeraPestana = pestanas[0].getAttribute('data-pestana');
        cambiarPestana(primeraPestana);
    }
    
    // Manejo del tema oscuro
    const modoOscuroToggle = document.getElementById('modo-oscuro-toggle');
    if (modoOscuroToggle) {
        // Verificar si hay una preferencia guardada
        const temaGuardado = localStorage.getItem('tema');
        if (temaGuardado === 'oscuro') {
            document.body.classList.add('modo-oscuro');
            modoOscuroToggle.checked = true;
        }
        
        modoOscuroToggle.addEventListener('change', function() {
            if (this.checked) {
                document.body.classList.add('modo-oscuro');
                localStorage.setItem('tema', 'oscuro');
            } else {
                document.body.classList.remove('modo-oscuro');
                localStorage.setItem('tema', 'claro');
            }
        });
    }
    
    // Manejo del tamaño de texto
    const botonesTamano = document.querySelectorAll('.btn-tamano');
    if (botonesTamano.length > 0) {
        // Verificar si hay una preferencia guardada
        const tamanoGuardado = localStorage.getItem('tamanoTexto');
        if (tamanoGuardado) {
            document.body.classList.remove('texto-pequeño', 'texto-normal', 'texto-grande');
            document.body.classList.add(`texto-${tamanoGuardado}`);
            
            botonesTamano.forEach(btn => {
                btn.classList.remove('activo');
                if (btn.getAttribute('data-tamano') === tamanoGuardado) {
                    btn.classList.add('activo');
                }
            });
        }
        
        botonesTamano.forEach(boton => {
            boton.addEventListener('click', function() {
                const tamano = this.getAttribute('data-tamano');
                
                // Quitar todas las clases de tamaño
                document.body.classList.remove('texto-pequeño', 'texto-normal', 'texto-grande');
                document.body.classList.add(`texto-${tamano}`);
                
                // Actualizar botones
                botonesTamano.forEach(btn => btn.classList.remove('activo'));
                this.classList.add('activo');
                
                // Guardar preferencia
                localStorage.setItem('tamanoTexto', tamano);
            });
        });
    }
    
    // Manejo de animaciones
    const animacionesToggle = document.getElementById('animaciones-toggle');
    if (animacionesToggle) {
        // Verificar si hay una preferencia guardada
        const animacionesGuardadas = localStorage.getItem('animaciones');
        if (animacionesGuardadas === 'desactivadas') {
            document.body.classList.add('sin-animaciones');
            animacionesToggle.checked = false;
        }
        
        animacionesToggle.addEventListener('change', function() {
            if (this.checked) {
                document.body.classList.remove('sin-animaciones');
                localStorage.setItem('animaciones', 'activadas');
            } else {
                document.body.classList.add('sin-animaciones');
                localStorage.setItem('animaciones', 'desactivadas');
            }
        });
    }
});
