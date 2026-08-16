// ==========================================================
// El Híbrido Ganador - Lógica de JavaScript Completa
// ==========================================================

document.addEventListener('DOMContentLoaded', () => {
    // 1. Selección de elementos del DOM
    const formulario = document.getElementById('formSolicitudes');
    const nombreCliente = document.getElementById('nombreCliente');
    const tipoServicio = document.getElementById('tipoServicio');
    const descripcionProblema = document.getElementById('descripcionProblema');
    const contenedorLista = document.getElementById('contenedorLista');
    const contadorSolicitudes = document.getElementById('contadorSolicitudes');
    const mensajeVacio = document.getElementById('mensajeVacio');

    // Elementos para el spinner y la alerta de Bootstrap
    const btnRegistrar = document.getElementById('btnRegistrar');
    const spinnerRegistrar = document.getElementById('spinnerRegistrar');
    const textoBtnRegistrar = document.getElementById('textoBtnRegistrar');
    const alertaExito = document.getElementById('alertaExito');
    const alertaExitoTexto = document.getElementById('alertaExitoTexto');

    // Instancias de los modales de Bootstrap (Verificando que existan en el HTML)
    const modalDetalleEl = document.getElementById('modalDetalle');
    const modalConfirmarEliminarEl = document.getElementById('modalConfirmarEliminar');
    
    const modalDetalle = modalDetalleEl ? new bootstrap.Modal(modalDetalleEl) : null;
    const modalConfirmarEliminar = modalConfirmarEliminarEl ? new bootstrap.Modal(modalConfirmarEliminarEl) : null;

    let totalRegistros = 0;
    let solicitudPendienteEliminarId = null; // Guarda el ID o índice de la tarjeta a eliminar

    // Cargar solicitudes guardadas al iniciar la página
    cargarSolicitudesAlmacenadas();

    // Función de validación mejorada
    function validarCampo(input, mostrarVerde = false) {
        if (!input) return false;
        let esValido = false;

        if (input.id === 'nombreCliente') {
            esValido = input.value.trim().length >= 5;
        } else if (input.id === 'tipoServicio') {
            esValido = input.value !== "";
        } else if (input.id === 'descripcionProblema') {
            esValido = input.value.trim().length >= 10;
        }

        if (!esValido) {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
        } else if (mostrarVerde) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        } else {
            input.classList.remove('is-invalid');
        }

        return esValido;
    }

    // 2. Eventos: Input y Blur para validación en tiempo real
    const campos = [nombreCliente, tipoServicio, descripcionProblema];

    campos.forEach(campo => {
        if (campo) {
            campo.addEventListener('input', () => validarCampo(campo, false));
            campo.addEventListener('blur', () => validarCampo(campo, true));
        }
    });

    // 3. Envío del formulario
    if (formulario) {
        formulario.addEventListener('submit', function(evento) {
            evento.preventDefault();

            const vNombre = validarCampo(nombreCliente, true);
            const vServicio = validarCampo(tipoServicio, true);
            const vDesc = validarCampo(descripcionProblema, true);

            if (!vNombre || !vServicio || !vDesc) {
                return;
            }

            const fechaRegistro = new Date().toLocaleString('es-EC', {
                dateStyle: 'medium',
                timeStyle: 'short'
            });

            const datosSolicitud = {
                id: Date.now().toString(), // ID único basado en tiempo
                nombre: nombreCliente.value.trim(),
                servicio: tipoServicio.value,
                descripcion: descripcionProblema.value.trim(),
                fecha: fechaRegistro
            };

            // --- Spinner Bootstrap: simula el procesamiento ---
            if (spinnerRegistrar) spinnerRegistrar.classList.remove('d-none');
            if (textoBtnRegistrar) textoBtnRegistrar.textContent = 'Registrando...';
            if (btnRegistrar) btnRegistrar.disabled = true;
            if (alertaExito) alertaExito.classList.add('d-none');

            setTimeout(() => {
                // Guardar en localStorage
                guardarEnLocalStorage(datosSolicitud);

                // Renderizar en pantalla
                crearTarjetaSolicitud(datosSolicitud);

                // Ocultar spinner y restaurar el botón
                if (spinnerRegistrar) spinnerRegistrar.classList.add('d-none');
                if (textoBtnRegistrar) textoBtnRegistrar.textContent = 'Registrar Solicitud';
                if (btnRegistrar) btnRegistrar.disabled = false;

                // Mostrar alerta Bootstrap de éxito
                if (alertaExitoTexto) alertaExitoTexto.textContent = `¡Solicitud de "${datosSolicitud.nombre}" registrada correctamente!`;
                if (alertaExito) {
                    alertaExito.classList.remove('d-none');
                    setTimeout(() => alertaExito.classList.add('d-none'), 3500);
                }

                // Resetear form y quitar validaciones verdes
                formulario.reset();
                campos.forEach(c => {
                    if (c) c.classList.remove('is-valid');
                });
            }, 900);
        });
    }

    // --- Lógica de creación de la tarjeta (Renderizado dinámico) ---
    function crearTarjetaSolicitud(datos) {
        if (totalRegistros === 0 && mensajeVacio) {
            mensajeVacio.style.display = 'none';
        }

        const colDiv = document.createElement('div');
        colDiv.className = 'col-12';
        colDiv.setAttribute('data-id', datos.id);

        colDiv.innerHTML = `
            <div class="card border-start border-primary border-4 p-3 bg-light shadow-sm">
                <h6 class="fw-bold text-dark mb-1">${datos.nombre}</h6>
                <span class="badge bg-primary text-wrap mb-2" style="max-width: fit-content;">${datos.servicio}</span>
                <p class="small text-muted mb-2">${datos.descripcion}</p>
                <div class="d-flex gap-2">
                    <button type="button" class="btn btn-sm btn-outline-primary btn-detalle">
                        <i class="bi bi-eye-fill"></i> Ver detalles
                    </button>
                    <button type="button" class="btn btn-sm btn-outline-danger btn-eliminar">
                        <i class="bi bi-trash-fill"></i> Eliminar
                    </button>
                </div>
            </div>
        `;

        // Botón "Ver detalles"
        colDiv.querySelector('.btn-detalle').addEventListener('click', function() {
            const elNombre = document.getElementById('detalleNombre');
            const elServicio = document.getElementById('detalleServicio');
            const elDesc = document.getElementById('detalleDescripcion');
            const elFecha = document.getElementById('detalleFecha');

            if (elNombre) elNombre.textContent = datos.nombre;
            if (elServicio) elServicio.textContent = datos.servicio;
            if (elDesc) elDesc.textContent = datos.descripcion;
            if (elFecha) elFecha.textContent = datos.fecha;
            
            if (modalDetalle) modalDetalle.show();
        });

        // Botón "Eliminar" -> abre el modal de confirmación
        colDiv.querySelector('.btn-eliminar').addEventListener('click', function() {
            solicitudPendienteEliminarId = datos.id;
            const nombreAEliminar = document.getElementById('nombreAEliminar');
            if (nombreAEliminar) nombreAEliminar.textContent = datos.nombre;
            if (modalConfirmarEliminar) modalConfirmarEliminar.show();
        });

        if (contenedorLista) {
            contenedorLista.appendChild(colDiv);
        }
        totalRegistros++;
        if (contadorSolicitudes) contadorSolicitudes.textContent = totalRegistros;
    }

    // Confirmar eliminación desde el modal Bootstrap
    const btnConfirmarEliminar = document.getElementById('btnConfirmarEliminar');
    if (btnConfirmarEliminar) {
        btnConfirmarEliminar.addEventListener('click', function() {
            if (solicitudPendienteEliminarId) {
                // Eliminar del DOM
                const tarjetaAEliminar = contenedorLista.querySelector(`[data-id="${solicitudPendienteEliminarId}"]`);
                if (tarjetaAEliminar) {
                    tarjetaAEliminar.remove();
                }

                // Eliminar de localStorage
                eliminarDeLocalStorage(solicitudPendienteEliminarId);

                totalRegistros--;
                if (contadorSolicitudes) contadorSolicitudes.textContent = totalRegistros;
                
                if (totalRegistros === 0 && mensajeVacio) {
                    mensajeVacio.style.display = 'block';
                }
                solicitudPendienteEliminarId = null;
            }
            if (modalConfirmarEliminar) modalConfirmarEliminar.hide();
        });
    }

    // --- Funciones auxiliares para LocalStorage ---
    function guardarEnLocalStorage(solicitud) {
        let solicitudes = JSON.parse(localStorage.getItem('solicitudes_hibrydo')) || [];
        solicitudes.push(solicitud);
        localStorage.setItem('solicitudes_hibrydo', JSON.stringify(solicitudes));
    }

    function cargarSolicitudesAlmacenadas() {
        let solicitudes = JSON.parse(localStorage.getItem('solicitudes_hibrydo')) || [];
        solicitudes.forEach(solicitud => {
            crearTarjetaSolicitud(solicitud);
        });
    }

    function eliminarDeLocalStorage(id) {
        let solicitudes = JSON.parse(localStorage.getItem('solicitudes_hibrydo')) || [];
        solicitudes = solicitudes.filter(solicitud => solicitud.id !== id);
        localStorage.setItem('solicitudes_hibrydo', JSON.stringify(solicitudes));
    }
});