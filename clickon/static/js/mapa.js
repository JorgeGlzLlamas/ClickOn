// Convertir coordenadas de formato DMS a decimal
function dmsToDecimal(degrees, minutes, seconds, direction) {
    let decimal = degrees + (minutes / 60) + (seconds / 3600);
    if (direction === 'S' || direction === 'W') {
        decimal = -decimal;
    }
    return decimal;
}

// Coordenadas del punto fijo (21°25'27.3"N 104°53'51.1"W)
const latDMS = { degrees: 21, minutes: 25, seconds: 27.3, direction: 'N' };
const lngDMS = { degrees: 104, minutes: 53, seconds: 51.1, direction: 'W' };

const PUNTO_FIJO = [
    dmsToDecimal(latDMS.degrees, latDMS.minutes, latDMS.seconds, latDMS.direction),
    dmsToDecimal(lngDMS.degrees, lngDMS.minutes, lngDMS.seconds, lngDMS.direction)
];

// Inicializar el mapa cuando el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si el elemento del mapa existe en la página actual
    const mapaContainer = document.getElementById('mapa-estatico');
    if (!mapaContainer) return;

    // Asegurar que el contenedor del mapa sea visible
    mapaContainer.style.display = 'block';
    mapaContainer.style.height = '610px';
    mapaContainer.style.position = 'relative';
    
    // Inicializar el mapa
    let mapa = L.map('mapa-estatico', {
        center: PUNTO_FIJO,
        zoom: 15,
        dragging: true,
        touchZoom: true, 
        doubleClickZoom: true,
        scrollWheelZoom: true,
        boxZoom: true,
        keyboard: true,
        zoomControl: true
    });

    // Añadir capa de mapa de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mapa);

    // Crear icono personalizado para el establecimiento
    const iconoEstablecimiento = L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/512/3170/3170733.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [50, 50],
        iconAnchor: [25, 50],
        shadowSize: [41, 41]
    });
    
    // Crear icono personalizado para la ubicación del usuario
    const iconoUsuario = L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/512/25/25694.png', // Icono de casa
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [40, 40],
        iconAnchor: [20, 40],
        shadowSize: [41, 41]
    });

    // Añadir marcador para el establecimiento
    L.marker(PUNTO_FIJO, {icon: iconoEstablecimiento}).addTo(mapa);
    
    // Variables para almacenar la ruta y el marcador del usuario
    let rutaUsuario = null;
    let marcadorUsuario = null;
    
    // Función para dibujar ruta desde punto fijo hasta ubicación del usuario
    async function dibujarRutaUsuario(coordenadasUsuario) {
        try {
            // Si ya existe una ruta, eliminarla
            if (rutaUsuario) {
                mapa.removeLayer(rutaUsuario);
            }
            
            // Si ya existe un marcador de usuario, eliminarlo
            if (marcadorUsuario) {
                mapa.removeLayer(marcadorUsuario);
            }
            
            // Añadir marcador para la ubicación del usuario
            marcadorUsuario = L.marker(coordenadasUsuario, {icon: iconoUsuario}).addTo(mapa);
            
            // Obtener la mejor ruta usando OSRM con optimización
            const url = `https://router.project-osrm.org/route/v1/driving/${PUNTO_FIJO[1]},${PUNTO_FIJO[0]};${coordenadasUsuario[1]},${coordenadasUsuario[0]}?overview=full&geometries=geojson&steps=true`;
            const respuesta = await fetch(url);
            const datos = await respuesta.json();
            
            if (datos.code !== 'Ok' || !datos.routes || datos.routes.length === 0) {
                throw new Error("No se pudo calcular la ruta");
            }
            
            // Seleccionar la mejor ruta (la primera es la recomendada por OSRM)
            const mejorRuta = datos.routes[0];
            
            // Usar directamente las coordenadas GeoJSON en lugar de decodificar polyline
            const puntos = mejorRuta.geometry.coordinates.map(coord => [coord[1], coord[0]]);
            
            // Crear una ruta que siga las calles con estilo mejorado y más visible
            rutaUsuario = L.polyline(puntos, {
                color: '#28a745',
                weight: 8,
                opacity: 1,
                lineJoin: 'round',
                lineCap: 'round'
            }).addTo(mapa);
            
            // Ajustar el mapa para mostrar toda la ruta
            mapa.fitBounds(rutaUsuario.getBounds(), {
                padding: [50, 50]
            });
            
            // Mostrar distancia y tiempo estimado
            const distanciaKm = (mejorRuta.distance / 1000).toFixed(2);
            const tiempoMinutos = Math.ceil(mejorRuta.duration / 60);
            
            // Calcular costo de envío (ejemplo: $10 por kilómetro)
            const costoPorKm = 10;
            const costoEnvio = (distanciaKm * costoPorKm).toFixed(2);
            
            // Obtener la dirección del usuario mediante geocodificación inversa
            const obtenerDireccion = async (lat, lng) => {
                try {
                    const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`;
                    const respuesta = await fetch(url);
                    const datos = await respuesta.json();
                    return datos.display_name || "Ubicación no disponible";
                } catch (error) {
                    console.error("Error al obtener dirección:", error);
                    return "Ubicación no disponible";
                }
            };
            
            // Obtener la dirección y mostrar la información
            const direccionUsuario = await obtenerDireccion(coordenadasUsuario[0], coordenadasUsuario[1]);
            
            // Crear un control de información con detalles de la mejor ruta
            const infoControl = L.control({position: 'bottomleft'});
            infoControl.onAdd = function() {
                const div = L.DomUtil.create('div', 'info-route');
                div.innerHTML = `
                    <div style="background: white; padding: 12px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); z-index: 1000; min-width: 220px; max-width: 350px;">
                        <h4 style="margin: 0 0 8px 0; color: #28a745; font-weight: bold;">Detalles del envío</h4>
                        <p style="margin: 0 0 5px 0;"><strong>Ubicación:</strong> <span style="font-size: 0.9em;">${direccionUsuario}</span></p>
                        <p style="margin: 0 0 5px 0;"><strong>Distancia:</strong> ${distanciaKm} km</p>
                        <p style="margin: 0 0 5px 0;"><strong>Tiempo estimado:</strong> ${tiempoMinutos} min</p>
                        <p style="margin: 0 0 5px 0;"><strong>Costo por km:</strong> $${costoPorKm}.00 MXN</p>
                        <p style="margin: 0; font-weight: bold; color: #28a745;"><strong>Costo de envío:</strong> $${costoEnvio} MXN</p>
                    </div>
                `;
                return div;
            };
            infoControl.addTo(mapa);
            
        } catch (error) {
            console.error("Error al dibujar ruta:", error);
            // Mostrar solo el marcador del usuario si no se puede dibujar la ruta
            if (!marcadorUsuario) {
                marcadorUsuario = L.marker(coordenadasUsuario, {icon: iconoUsuario}).addTo(mapa);
                mapa.setView(coordenadasUsuario, 15);
            }
            
            // Mostrar mensaje de error al usuario
            const errorControl = L.control({position: 'bottomleft'});
            errorControl.onAdd = function() {
                const div = L.DomUtil.create('div', 'error-route');
                div.innerHTML = `
                    <div style="background: white; padding: 10px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); z-index: 1000;">
                        <h4 style="margin: 0 0 5px 0; color: #dc3545;">No se pudo calcular la ruta</h4>
                        <p style="margin: 0;">Intente nuevamente más tarde</p>
                    </div>
                `;
                return div;
            };
            errorControl.addTo(mapa);
        }
    }
    
    // Solicitar ubicación del usuario cuando cargue la página
    let permisoDenegado = false;
    
    function solicitarUbicacion() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                // Éxito
                function(position) {
                    const coordenadasUsuario = [position.coords.latitude, position.coords.longitude];
                    dibujarRutaUsuario(coordenadasUsuario);
                    permisoDenegado = false;
                },
                // Error - Mostrar formulario para ingresar dirección manualmente
                function(error) {
                    console.log("Error al obtener ubicación:", error.message);
                    mostrarFormularioDireccion();
                    
                    // Marcar que el permiso fue denegado para solicitar nuevamente más tarde
                    if (error.code === error.PERMISSION_DENIED) {
                        permisoDenegado = true;
                        
                        // Programar recordatorios periódicos para solicitar ubicación
                        programarRecordatorioUbicacion();
                    }
                },
                // Opciones
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                }
            );
        } else {
            // Navegador no soporta geolocalización
            mostrarFormularioDireccion();
        }
    }
    
    // Función para mostrar alerta y solicitar ubicación nuevamente
    function mostrarAlertaUbicacion() {
        if (permisoDenegado) {
            const confirmar = confirm("Para una mejor experiencia, ¿nos permites acceder a tu ubicación para calcular la ruta de entrega?");
            if (confirmar) {
                solicitarUbicacion();
            }
        }
    }
    
    // Programar recordatorios periódicos para solicitar ubicación
    function programarRecordatorioUbicacion() {
        // Mostrar el primer recordatorio después de 2 minutos
        setTimeout(() => {
            mostrarAlertaUbicacion();
            
            // Después mostrar cada 5 minutos si sigue denegado
            const intervaloRecordatorio = setInterval(() => {
                if (!permisoDenegado) {
                    clearInterval(intervaloRecordatorio);
                } else {
                    mostrarAlertaUbicacion();
                }
            }, 5 * 60 * 1000); // 5 minutos
            
        }, 2 * 60 * 1000); // 2 minutos
    }
    
    // Iniciar solicitud de ubicación con un pequeño retraso
    setTimeout(solicitarUbicacion, 1000);
    
    // Función para mostrar formulario de dirección manual
    function mostrarFormularioDireccion() {
        // Crear control para el formulario
        const direccionControl = L.control({position: 'topright'});
        
        direccionControl.onAdd = function() {
            const div = L.DomUtil.create('div', 'direccion-form');
            div.innerHTML = `
                <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); z-index: 1000; margin-top: 10px; width: 280px;">
                    <h4 style="margin: 0 0 10px 0; color: #28a745;">Ingresa tu ubicación</h4>
                    <input type="text" id="direccion-input" placeholder="Ej: Av. México 123, Tepic" 
                           style="width: 100%; padding: 8px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px;">
                    <button id="buscar-direccion" 
                            style="background: #28a745; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; width: 100%;">
                        Buscar
                    </button>
                    <p id="error-direccion" style="color: #dc3545; margin: 5px 0 0 0; font-size: 0.9em; display: none;">
                        No se encontró la dirección. Intenta con otra.
                    </p>
                </div>
            `;
            return div;
        };
        
        direccionControl.addTo(mapa);
        
        // Agregar evento al botón de búsqueda
        setTimeout(() => {
            const botonBuscar = document.getElementById('buscar-direccion');
            const inputDireccion = document.getElementById('direccion-input');
            const errorDireccion = document.getElementById('error-direccion');
            
            if (botonBuscar && inputDireccion) {
                botonBuscar.addEventListener('click', function() {
                    buscarDireccion(inputDireccion.value);
                });
                
                inputDireccion.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        buscarDireccion(inputDireccion.value);
                    }
                });
            }
            
            // Función para buscar dirección usando Nominatim (OpenStreetMap)
            async function buscarDireccion(direccion) {
                if (!direccion.trim()) return;
                
                try {
                    errorDireccion.style.display = 'none';
                    botonBuscar.innerHTML = 'Buscando...';
                    botonBuscar.disabled = true;
                    
                    // Añadir "Nayarit" a la búsqueda si no se especifica una ciudad
                    if (!direccion.toLowerCase().includes('nayarit')) {
                        direccion += ', Nayarit, México';
                    } else if (!direccion.toLowerCase().includes('méxico') && !direccion.toLowerCase().includes('mexico')) {
                        direccion += ', México';
                    }
                    
                    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(direccion)}&limit=1`;
                    const respuesta = await fetch(url);
                    const datos = await respuesta.json();
                    
                    if (datos && datos.length > 0) {
                        const coordenadas = [parseFloat(datos[0].lat), parseFloat(datos[0].lon)];
                        dibujarRutaUsuario(coordenadas);
                    } else {
                        errorDireccion.style.display = 'block';
                    }
                } catch (error) {
                    console.error("Error al buscar dirección:", error);
                    errorDireccion.style.display = 'block';
                } finally {
                    botonBuscar.innerHTML = 'Buscar';
                    botonBuscar.disabled = false;
                }
            }
        }, 100);
    }

    // Añadir estilos adicionales al mapa
    const estilosMapa = document.createElement('style');
    estilosMapa.textContent = `
        #mapa-estatico {
            position: absolute;
            top: 122px;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }
        
        @media (max-width: 768px) {
            #mapa-estatico {
                border-width: 5px;
            }
        }
    `;
    document.head.appendChild(estilosMapa);
});