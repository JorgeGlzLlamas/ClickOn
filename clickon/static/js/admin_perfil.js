// Script mejorado para el panel de administrador
document.addEventListener('DOMContentLoaded', function() {
    console.log("Admin perfil: Script cargado");
    
    // Manejo de pestañas para perfil admin
    const pestanasAdmin = document.querySelectorAll('.contenedor-perfil-admin .pestana');
    const contenidosAdmin = document.querySelectorAll('.contenedor-perfil-admin .contenido-pestana');
    
    console.log("Pestañas encontradas:", pestanasAdmin.length);
    console.log("Contenidos encontrados:", contenidosAdmin.length);
    
    // Función para cambiar entre pestañas con animación
    function cambiarPestanaAdmin(pestanaId) {
        console.log("Cambiando a pestaña admin:", pestanaId);
        
        // Ocultar todos los contenidos
        contenidosAdmin.forEach(contenido => {
            contenido.style.display = 'none';
        });
        
        // Remover clase activa de todas las pestañas
        pestanasAdmin.forEach(p => {
            p.classList.remove('activa');
        });
        
        // Activar la pestaña seleccionada
        const pestanaSeleccionada = document.querySelector(`.contenedor-perfil-admin .pestana[data-pestana="${pestanaId}"]`);
        if (pestanaSeleccionada) {
            pestanaSeleccionada.classList.add('activa');
            console.log("Pestaña activada:", pestanaId);
        } else {
            console.log("No se encontró la pestaña:", pestanaId);
        }
        
        // Mostrar el contenido correspondiente
        const contenidoActivo = document.getElementById(`${pestanaId}-contenido`);
        if (contenidoActivo) {
            contenidoActivo.style.display = 'block';
            console.log("Contenido mostrado:", pestanaId);
        } else {
            console.log("No se encontró el contenido:", pestanaId);
        }
    }
    
    // Asignar evento click a cada pestaña
    pestanasAdmin.forEach(pestana => {
        pestana.addEventListener('click', function() {
            const targetId = this.getAttribute('data-pestana');
            if (targetId) {
                cambiarPestanaAdmin(targetId);
                
                // Guardar la pestaña activa en localStorage
                localStorage.setItem('pestanaActivaAdmin', targetId);
            } else {
                console.error("Esta pestaña no tiene atributo data-pestana");
            }
        });
    });
    
    // Activar la primera pestaña por defecto o la última seleccionada
    const pestanaGuardada = localStorage.getItem('pestanaActivaAdmin');
    if (pestanaGuardada && document.getElementById(`${pestanaGuardada}-contenido`)) {
        cambiarPestanaAdmin(pestanaGuardada);
    } else if (pestanasAdmin.length > 0) {
        const primeraPestana = pestanasAdmin[0].getAttribute('data-pestana');
        if (primeraPestana) {
            cambiarPestanaAdmin(primeraPestana);
        }
    }
    
    // Manejo del tema oscuro
    const modoOscuroToggle = document.getElementById('modo-oscuro-toggle');
    if (modoOscuroToggle) {
        // Verificar si hay una preferencia guardada
        const temaGuardado = localStorage.getItem('temaAdmin');
        if (temaGuardado === 'oscuro') {
            document.body.classList.add('modo-oscuro');
            modoOscuroToggle.checked = true;
        }
        
        modoOscuroToggle.addEventListener('change', function() {
            if (this.checked) {
                document.body.classList.add('modo-oscuro');
                localStorage.setItem('temaAdmin', 'oscuro');
            } else {
                document.body.classList.remove('modo-oscuro');
                localStorage.setItem('temaAdmin', 'claro');
            }
        });
    }
    
    // Manejo del tamaño de texto
    const botonesTamano = document.querySelectorAll('.btn-tamano');
    if (botonesTamano.length > 0) {
        // Verificar si hay una preferencia guardada
        const tamanoGuardado = localStorage.getItem('tamanoTextoAdmin');
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
                localStorage.setItem('tamanoTextoAdmin', tamano);
            });
        });
    }
    
    // Inicializar gráficos si Chart.js está disponible
    if (typeof Chart !== 'undefined') {
        try {
            // Gráfico de ventas
            const ctxVentas = document.getElementById('grafico-ventas');
            if (ctxVentas) {
                new Chart(ctxVentas, {
                    type: 'line',
                    data: {
                        labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                        datasets: [{
                            label: 'Ventas',
                            data: [12000, 15000, 18000, 14000, 19000, 22000, 21000, 25000, 23000, 26000, 28000, 30000],
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
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            }
            
            // Gráfico de productos
            const ctxProductos = document.getElementById('grafico-productos');
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
                        maintainAspectRatio: false
                    }
                });
            }
        } catch (error) {
            console.error("Error al inicializar gráficos:", error);
        }
    } else {
        console.log("Chart.js no está disponible");
    }
    
    // Manejo de filtros
    const btnAplicarFiltro = document.querySelectorAll('.btn-aplicar-filtro');
    btnAplicarFiltro.forEach(btn => {
        btn.addEventListener('click', function() {
            console.log("Aplicando filtros...");
            // Aquí iría la lógica para aplicar filtros
        });
    });
    
    // Manejo de botones de acción
    const botonesAccion = document.querySelectorAll('.btn-accion-producto, .btn-editar, .btn-eliminar');
    botonesAccion.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log("Acción:", this.getAttribute('data-accion') || this.className);
            // Aquí iría la lógica para cada acción
        });
    });
});