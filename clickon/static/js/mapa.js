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

const TARIFA_BASE = 20; // Tarifa base en pesos
const TARIFA_POR_KM = 5; // Pesos adicionales por kilómetro

// Inicializar el mapa cuando el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si el elemento del mapa existe en la página actual
    const mapaContainer = document.getElementById('mapa-estatico');
    if (!mapaContainer) return;

    // Inicializar el mapa
    let mapa = L.map('mapa-estatico', {
        center: PUNTO_FIJO,
        zoom: 15,
        dragging: true,  // Deshabilitar arrastre
        touchZoom: true, // Deshabilitar zoom táctil
        doubleClickZoom: true, // Deshabilitar zoom con doble clic
        scrollWheelZoom: true, // Deshabilitar zoom con rueda del ratón
        boxZoom: true,   // Deshabilitar zoom con caja
        keyboard: true,  // Deshabilitar teclado
        zoomControl: true // Ocultar controles de zoom
    });

    // Añadir capa de mapa de OpenStreetMap (gratuito)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mapa);

    // Crear icono personalizado para el establecimiento (punto de inicio)
    const iconoEstablecimiento = L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/512/3170/3170733.png', // Icono de tienda/establecimiento
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [50, 50],
        iconAnchor: [25, 50],
        popupAnchor: [0, -45],
        shadowSize: [41, 41]
    });

    // Crear icono personalizado para la casa del cliente (destino)
    const iconoCasaCliente = L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/512/8059/8059355.png', // Icono de casa
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [45, 45],
        iconAnchor: [22, 45],
        popupAnchor: [0, -40],
        shadowSize: [41, 41]
    });

    // Añadir marcador para el establecimiento con el icono correspondiente
    const marcadorFijo = L.marker(PUNTO_FIJO, {icon: iconoEstablecimiento}).addTo(mapa);
    marcadorFijo.bindPopup("<div class='popup-content'><strong>Click On</strong><p>Nuestra ubicación</p></div>").openPopup();

    // Variables para almacenar la ruta actual y el marcador de destino
    let rutaActual = null;
    let marcadorDestino = null;

    // Manejar el envío del formulario
    const formulario = document.getElementById('direccionForm');
    
    if (formulario) {
        formulario.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const direccion = document.getElementById('direccionInput').value;
            
            if (!direccion) {
                alert("Por favor, ingresa una dirección");
                return;
            }
            
            try {
                // Mostrar indicador de carga
                document.getElementById('direccionInput').disabled = true;
                
                // Geocodificar la dirección
                const coordenadas = await geocodificarDireccion(direccion);
                
                // Calcular la ruta
                await calcularRuta(coordenadas, mapa);
            } catch (error) {
                alert("No se pudo encontrar la dirección. Por favor, intenta con otra.");
            } finally {
                // Ocultar indicador de carga
                document.getElementById('direccionInput').disabled = false;
            }
        });
    }

    // Función para calcular ruta usando OSRM (Open Source Routing Machine)
    async function calcularRuta(destino, mapa) {
        try {
            // Si ya existe una ruta, eliminarla
            if (rutaActual) {
                mapa.removeLayer(rutaActual);
            }
            
            // Si ya existe un marcador de destino, eliminarlo
            if (marcadorDestino) {
                mapa.removeLayer(marcadorDestino);
            }
            
            // Crear marcador para el destino con el icono de casa
            marcadorDestino = L.marker(destino, {icon: iconoCasaCliente}).addTo(mapa);
            marcadorDestino.bindPopup("<div class='popup-content'><strong>Tu ubicación</strong><p>Destino de entrega</p></div>").openPopup();
            
            // Obtener ruta usando OSRM (que sigue las calles)
            const url = `https://router.project-osrm.org/route/v1/driving/${PUNTO_FIJO[1]},${PUNTO_FIJO[0]};${destino[1]},${destino[0]}?overview=full&geometries=polyline&steps=true`;
            
            const respuesta = await fetch(url);
            const datos = await respuesta.json();
            
            if (datos.code !== 'Ok' || !datos.routes || datos.routes.length === 0) {
                throw new Error('No se pudo calcular la ruta');
            }
            
            // Obtener la ruta y decodificar la geometría
            const ruta = datos.routes[0];
            const coordenadasRuta = decodePolyline(ruta.geometry);
            
            // Dibujar la ruta con estilo mejorado
            rutaActual = L.polyline(coordenadasRuta, {
                color: 'var(--dark-green)',
                weight: 6,
                opacity: 0.8,
                lineCap: 'round',
                lineJoin: 'round',
                dashArray: '10, 10', // Línea punteada para mejor visibilidad
                className: 'animated-route' // Para animación CSS
            }).addTo(mapa);
            
            // Ajustar la vista para mostrar toda la ruta
            mapa.fitBounds(rutaActual.getBounds(), { padding: [50, 50] });
            
            // Calcular distancia en kilómetros
            const distanciaKm = ruta.distance / 1000;
            
            // Calcular tarifa
            const tarifa = TARIFA_BASE + (distanciaKm * TARIFA_POR_KM);
            
                       // Mostrar resultados en el elemento superior con diseño mejorado
                       const resultadoEnvio = document.getElementById('resultadoEnvio');
                       resultadoEnvio.innerHTML = `
                           <div class="tarifa-container">
                               <h3 class="tarifa-titulo">Detalles de Envío</h3>
                               <div class="tarifa-grid">
                                   <div class="tarifa-item">
                                       <i class="bi bi-geo-alt-fill"></i>
                                       <p><strong>Distancia:</strong> ${distanciaKm.toFixed(2)} km</p>
                                   </div>
                                   <div class="tarifa-item">
                                       <i class="bi bi-cash-coin"></i>
                                       <p><strong>Tarifa base:</strong> $${TARIFA_BASE.toFixed(2)} MXN</p>
                                   </div>
                                   <div class="tarifa-item">
                                       <i class="bi bi-plus-circle-fill"></i>
                                       <p><strong>Tarifa por km:</strong> $${(distanciaKm * TARIFA_POR_KM).toFixed(2)} MXN</p>
                                   </div>
                                   <div class="tarifa-item tarifa-total">
                                       <i class="bi bi-check-circle-fill"></i>
                                       <p><strong>Tarifa total:</strong> $${tarifa.toFixed(2)} MXN</p>
                                   </div>
                               </div>
                           </div>
                       `;
                       resultadoEnvio.style.display = 'block';
            
            return {
                distancia: distanciaKm,
                tarifa: tarifa
            };
        } catch (error) {
            console.error("Error al calcular la ruta:", error);
            
            // Si falla OSRM, mostrar un mensaje de error en el elemento superior
            const resultadoEnvio = document.getElementById('resultadoEnvio');
            resultadoEnvio.innerHTML = `
                <div class="alert-danger p-2 rounded">
                    <p class="mb-0">No se pudo calcular la ruta. Por favor, intenta con otra dirección.</p>
                </div>
            `;
            resultadoEnvio.style.display = 'block';
            
            return null;
        }
    }
});

// Función para geocodificar una dirección usando la API gratuita de Nominatim
async function geocodificarDireccion(direccion) {
    try {
        const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(direccion)}`;
        const respuesta = await fetch(url);
        const datos = await respuesta.json();
        
        if (datos && datos.length > 0) {
            return [parseFloat(datos[0].lat), parseFloat(datos[0].lon)];
        } else {
            throw new Error("No se encontró la dirección");
        }
    } catch (error) {
        console.error("Error al geocodificar:", error);
        throw error;
    }
}

// Función para decodificar polyline
function decodePolyline(encoded) {
    let points = [];
    let index = 0, len = encoded.length;
    let lat = 0, lng = 0;

    while (index < len) {
        let b, shift = 0, result = 0;
        do {
            b = encoded.charAt(index++).charCodeAt(0) - 63;
            result |= (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);
        let dlat = ((result & 1) ? ~(result >> 1) : (result >> 1));
        lat += dlat;

        shift = 0;
        result = 0;
        do {
            b = encoded.charAt(index++).charCodeAt(0) - 63;
            result |= (b & 0x1f) << shift;
            shift += 5;
        } while (b >= 0x20);
        let dlng = ((result & 1) ? ~(result >> 1) : (result >> 1));
        lng += dlng;

        points.push([lat * 1e-5, lng * 1e-5]);
    }
    return points;
}