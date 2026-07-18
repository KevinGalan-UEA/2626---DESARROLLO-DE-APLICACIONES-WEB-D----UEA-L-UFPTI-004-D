// 1. Selección de elementos del DOM
const formulario = document.getElementById('formSolicitudes');
const nombreCliente = document.getElementById('nombreCliente');
const tipoServicio = document.getElementById('tipoServicio');
const descripcionProblema = document.getElementById('descripcionProblema');
const contenedorLista = document.getElementById('contenedorLista');
const contadorSolicitudes = document.getElementById('contadorSolicitudes');
const mensajeVacio = document.getElementById('mensajeVacio');

// Elementos nuevos para el spinner y la alerta de Bootstrap
const btnRegistrar = document.getElementById('btnRegistrar');
const spinnerRegistrar = document.getElementById('spinnerRegistrar');
const textoBtnRegistrar = document.getElementById('textoBtnRegistrar');
const alertaExito = document.getElementById('alertaExito');
const alertaExitoTexto = document.getElementById('alertaExitoTexto');

// Instancias de los modales de Bootstrap
const modalDetalle = new bootstrap.Modal(document.getElementById('modalDetalle'));
const modalConfirmarEliminar = new bootstrap.Modal(document.getElementById('modalConfirmarEliminar'));

let totalRegistros = 0;
let colDivPendienteEliminar = null; // Guarda la tarjeta que se quiere eliminar mientras se confirma

// Función de validación mejorada (se conserva igual que en la Semana 6)
function validarCampo(input, mostrarVerde = false) {
    let esValido = false;

    // Lógica de validación
    if (input.id === 'nombreCliente') {
        esValido = input.value.trim().length >= 5;
    } else if (input.id === 'tipoServicio') {
        esValido = input.value !== "";
    } else if (input.id === 'descripcionProblema') {
        esValido = input.value.trim().length >= 10;
    }

    // Lógica de estilos
    if (!esValido) {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
    } else if (mostrarVerde) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    } else {
        // Solo quitamos el error mientras escribe, no forzamos el verde
        input.classList.remove('is-invalid');
    }

    return esValido;
}

// 2. Eventos: Input (limpieza) y Blur (validación final)
const campos = [nombreCliente, tipoServicio, descripcionProblema];

campos.forEach(campo => {
    // Mientras escribe, solo limpiamos el error si se corrige
    campo.addEventListener('input', () => validarCampo(campo, false));

    // Al salir, ahí sí validamos y mostramos el check verde
    campo.addEventListener('blur', () => validarCampo(campo, true));
});

// 3. Envío del formulario
formulario.addEventListener('submit', function(evento) {
    evento.preventDefault();

    // Validar todo al hacer click en enviar
    const vNombre = validarCampo(nombreCliente, true);
    const vServicio = validarCampo(tipoServicio, true);
    const vDesc = validarCampo(descripcionProblema, true);

    if (!vNombre || !vServicio || !vDesc) {
        return;
    }

    // Guardamos los valores antes de que el formulario se resetee
    const datosSolicitud = {
        nombre: nombreCliente.value.trim(),
        servicio: tipoServicio.value,
        descripcion: descripcionProblema.value.trim()
    };

    // --- Spinner Bootstrap: simula el envío/procesamiento de la solicitud ---
    spinnerRegistrar.classList.remove('d-none');
    textoBtnRegistrar.textContent = 'Registrando...';
    btnRegistrar.disabled = true;
    alertaExito.classList.add('d-none');

    setTimeout(() => {
        crearTarjetaSolicitud(datosSolicitud);

        // Ocultar spinner y restaurar el botón
        spinnerRegistrar.classList.add('d-none');
        textoBtnRegistrar.textContent = 'Registrar Solicitud';
        btnRegistrar.disabled = false;

        // Mostrar alerta Bootstrap de éxito
        alertaExitoTexto.textContent = `¡Solicitud de "${datosSolicitud.nombre}" registrada correctamente!`;
        alertaExito.classList.remove('d-none');
        setTimeout(() => alertaExito.classList.add('d-none'), 3500);

        // Resetear form y quitar validaciones verdes
        formulario.reset();
        campos.forEach(c => c.classList.remove('is-valid'));
    }, 900); // simula ~0.9s de procesamiento
});

// --- Lógica de creación de la tarjeta (renderizado dinámico, Semana 7) ---
function crearTarjetaSolicitud(datos) {
    if (totalRegistros === 0) {
        mensajeVacio.style.display = 'none';
    }

    const fechaRegistro = new Date().toLocaleString('es-EC', {
        dateStyle: 'medium',
        timeStyle: 'short'
    });

    const colDiv = document.createElement('div');
    colDiv.className = 'col-12';

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

    // Botón "Ver detalles" -> abre el modal Bootstrap con la información completa
    colDiv.querySelector('.btn-detalle').addEventListener('click', function() {
        document.getElementById('detalleNombre').textContent = datos.nombre;
        document.getElementById('detalleServicio').textContent = datos.servicio;
        document.getElementById('detalleDescripcion').textContent = datos.descripcion;
        document.getElementById('detalleFecha').textContent = fechaRegistro;
        modalDetalle.show();
    });

    // Botón "Eliminar" -> abre el modal de confirmación en lugar de borrar directo
    colDiv.querySelector('.btn-eliminar').addEventListener('click', function() {
        colDivPendienteEliminar = colDiv;
        document.getElementById('nombreAEliminar').textContent = datos.nombre;
        modalConfirmarEliminar.show();
    });

    contenedorLista.appendChild(colDiv);
    totalRegistros++;
    contadorSolicitudes.textContent = totalRegistros;
}

// Confirmar eliminación desde el modal Bootstrap
document.getElementById('btnConfirmarEliminar').addEventListener('click', function() {
    if (colDivPendienteEliminar) {
        colDivPendienteEliminar.remove();
        totalRegistros--;
        contadorSolicitudes.textContent = totalRegistros;
        if (totalRegistros === 0) {
            mensajeVacio.style.display = 'block';
        }
        colDivPendienteEliminar = null;
    }
    modalConfirmarEliminar.hide();
});