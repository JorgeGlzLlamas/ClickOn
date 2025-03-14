// Script mejorado para el panel de administrador
document.addEventListener('DOMContentLoaded', function() {
    // Manejo de pestañas
    const pestanas = document.querySelectorAll('.pestana');
    const contenidos = document.querySelectorAll('.contenido-pestana');

    // Función para cambiar entre pestañas con animación
    function cambiarPestana(pestanaId) {
        // Ocultar todos los contenidos
        contenidos.forEach(contenido => {
            contenido.style.display = 'none';
            contenido.classList.remove('fadeIn');
        });

        // Remover clase activa de todas las pestañas
        pestanas.forEach(p => p.classList.remove('activa'));

        // Activar la pestaña seleccionada
        const pestanaSeleccionada = document.querySelector(`[data-target="${pestanaId}"]`);
        if (pestanaSeleccionada) {
            pestanaSeleccionada.classList.add('activa');
        }

        // Mostrar el contenido correspondiente con animación
        const contenidoActivo = document.getElementById(pestanaId);
        if (contenidoActivo) {
            contenidoActivo.style.display = 'block';
            setTimeout(() => {
                contenidoActivo.classList.add('fadeIn');
            }, 10);
        }
    }

    // Asignar evento click a cada pestaña
    pestanas.forEach(pestana => {
        pestana.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            cambiarPestana(targetId);
            
            // Guardar la pestaña activa en localStorage
            localStorage.setItem('pestanaActivaAdmin', targetId);
        });
    });

    // Activar la primera pestaña por defecto o la última seleccionada
    const pestanaGuardada = localStorage.getItem('pestanaActivaAdmin');
    if (pestanaGuardada && document.getElementById(pestanaGuardada)) {
        cambiarPestana(pestanaGuardada);
    } else if (pestanas.length > 0) {
        const primeraPestana = pestanas[0].getAttribute('data-target');
        cambiarPestana(primeraPestana);
    }

    // Animaciones para tarjetas y elementos
    const tarjetas = document.querySelectorAll('.tarjeta-resumen, .tarjeta-producto, .tarjeta-promocion');
    
    tarjetas.forEach(tarjeta => {
        tarjeta.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 12px 30px rgba(0, 0, 0, 0.1)';
        });
        
        tarjeta.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'var(--card-shadow)';
        });
    });

    // Manejo del tema oscuro/claro
    const opcionesTema = document.querySelectorAll('.opcion-tema');
    
    opcionesTema.forEach(opcion => {
        opcion.addEventListener('click', function() {
            const tema = this.getAttribute('data-tema');
            
            // Quitar clase activa de todas las opciones
            opcionesTema.forEach(op => op.classList.remove('activa'));
            
            // Añadir clase activa a la opción seleccionada
            this.classList.add('activa');
            
            // Aplicar el tema seleccionado
            if (tema === 'oscuro') {
                document.body.classList.add('modo-oscuro');
                localStorage.setItem('temaAdmin', 'oscuro');
            } else if (tema === 'claro') {
                document.body.classList.remove('modo-oscuro');
                localStorage.setItem('temaAdmin', 'claro');
            } else if (tema === 'sistema') {
                // Detectar preferencia del sistema
                const prefiereModoOscuro = window.matchMedia('(prefers-color-scheme: dark)').matches;
                if (prefiereModoOscuro) {
                    document.body.classList.add('modo-oscuro');
                } else {
                    document.body.classList.remove('modo-oscuro');
                }
                localStorage.setItem('temaAdmin', 'sistema');
                
                // Escuchar cambios en la preferencia del sistema
                window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
                    if (localStorage.getItem('temaAdmin') === 'sistema') {
                        if (e.matches) {
                            document.body.classList.add('modo-oscuro');
                        } else {
                            document.body.classList.remove('modo-oscuro');
                        }
                    }
                });
            }
        });
    });
    
    // Cargar tema guardado
    const temaGuardado = localStorage.getItem('temaAdmin');
    if (temaGuardado) {
        const opcionTema = document.querySelector(`.opcion-tema[data-tema="${temaGuardado}"]`);
        if (opcionTema) {
            opcionTema.click();
        }
    }
    
    // Inicializar gráficos (ejemplo con Chart.js)
    function inicializarGraficos() {
        if (typeof Chart !== 'undefined') {
            // Ejemplo de gráfico de ventas
            const ctxVentas = document.getElementById('grafico-ventas-canvas');
            if (ctxVentas) {
                new Chart(ctxVentas, {
                    type: 'line',
                    data: {
                        labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                        datasets: [{
                            label: 'Ventas',
                            data: [1200, 1900, 1500, 2000, 2500, 3000, 2800],
                            borderColor: '#5AAA08',
                            backgroundColor: 'rgba(90, 170, 8, 0.1)',
                            tension: 0.3,
                            fill: true
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                display: false
                            },
                            tooltip: {
                                backgroundColor: 'rgba(0, 0, 0, 0.7)',
                                padding: 10,
                                cornerRadius: 6
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: {
                                    drawBorder: false,
                                    color: 'rgba(0, 0, 0, 0.05)'
                                }
                            },
                            x: {
                                grid: {
                                    display: false
                                }
                            }
                        }
                    }
                });
            }
            
            // Ejemplo de gráfico de productos
            const ctxProductos = document.getElementById('grafico-productos-canvas');
            if (ctxProductos) {
                new Chart(ctxProductos, {
                    type: 'doughnut',
                    data: {
                        labels: ['Pizzas', 'Hamburguesas', 'Bebidas', 'Postres', 'Otros'],
                        datasets: [{
                            data: [35, 25, 20, 15, 5],
                            backgroundColor: [
                                '#5AAA08', 
                                '#246B1A', 
                                '#9DE11A', 
                                '#36b9cc', 
                                '#f6c23e'
                            ],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: '70%',
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    padding: 20,
                                    usePointStyle: true,
                                    pointStyle: 'circle'
                                }
                            }
                        }
                    }
                });
            }
        }
    }
    
    // Cargar gráficos si Chart.js está disponible
    if (typeof Chart !== 'undefined') {
        inicializarGraficos();
    } else {
        // Si Chart.js no está disponible, mostrar placeholders
        const placeholders = document.querySelectorAll('.placeholder-grafico');
        placeholders.forEach(placeholder => {
            placeholder.innerHTML = `
                <div class="grafico-no-disponible">
                    <i class="bi bi-bar-chart"></i>
                    <p>Gráfico no disponible</p>
                </div>
            `;
        });
    }
    
    // Manejo de tamaño de fuente
    const botonesTamano = document.querySelectorAll('.btn-tamano');
    
    botonesTamano.forEach(boton => {
        boton.addEventListener('click', function() {
            const tamano = this.getAttribute('data-tamano');
            
            // Quitar clase activa de todos los botones
            botonesTamano.forEach(btn => btn.classList.remove('activo'));
            
            // Añadir clase activa al botón seleccionado
            this.classList.add('activo');
            
            // Aplicar tamaño de fuente
            document.documentElement.style.fontSize = tamano === 'pequeño' ? '14px' : 
                                                     tamano === 'grande' ? '18px' : '16px';
            
            // Guardar preferencia
            localStorage.setItem('tamanoFuenteAdmin', tamano);
        });
    });
    
    // Cargar tamaño de fuente guardado
    const tamanoGuardado = localStorage.getItem('tamanoFuenteAdmin');
    if (tamanoGuardado) {
        const botonTamano = document.querySelector(`.btn-tamano[data-tamano="${tamanoGuardado}"]`);
        if (botonTamano) {
            botonTamano.click();
        }
    }
    
    // Animaciones para botones de acción
    const botonesAccion = document.querySelectorAll('.btn-accion-tabla, .btn-accion-producto');
    
    botonesAccion.forEach(boton => {
        boton.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });
        
        boton.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Manejo de filtros
    const btnAplicarFiltro = document.querySelectorAll('.btn-aplicar-filtro');
    
    btnAplicarFiltro.forEach(btn => {
        btn.addEventListener('click', function() {
            // Aquí iría la lógica para aplicar filtros
            // Por ahora solo mostramos una animación
            this.classList.add('aplicando');
            this.textContent = 'Aplicando...';
            
            setTimeout(() => {
                this.classList.remove('aplicando');
                this.textContent = 'Aplicar filtros';
                
                // Mostrar notificación de éxito
                mostrarNotificacion('Filtros aplicados correctamente', 'success');
            }, 800);
        });
    });
    
    // Función para mostrar notificaciones
    function mostrarNotificacion(mensaje, tipo = 'info') {
        // Crear elemento de notificación
        const notificacion = document.createElement('div');
        notificacion.className = `notificacion ${tipo}`;
        
        // Icono según tipo
        let icono = 'info-circle';
        if (tipo === 'success') icono = 'check-circle';
        if (tipo === 'warning') icono = 'exclamation-triangle';
        if (tipo === 'error') icono = 'x-circle';
        
        notificacion.innerHTML = `
            <i class="bi bi-${icono}"></i>
            <p>${mensaje}</p>
            <button class="cerrar-notificacion"><i class="bi bi-x"></i></button>
        `;
        
        // Añadir al DOM
        document.body.appendChild(notificacion);
        
        // Mostrar con animación
        setTimeout(() => {
            notificacion.classList.add('visible');
        }, 10);
        
        // Ocultar automáticamente después de 5 segundos
        setTimeout(() => {
            notificacion.classList.remove('visible');
            setTimeout(() => {
                notificacion.remove();
            }, 300);
        }, 5000);
        
        // Cerrar al hacer clic en el botón
        notificacion.querySelector('.cerrar-notificacion').addEventListener('click', function() {
            notificacion.classList.remove('visible');
            setTimeout(() => {
                notificacion.remove();
            }, 300);
        });
    }
    
    // Inicializar tooltips si Bootstrap está disponible
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltips.forEach(tooltip => {
            new bootstrap.Tooltip(tooltip);
        });
    }
});