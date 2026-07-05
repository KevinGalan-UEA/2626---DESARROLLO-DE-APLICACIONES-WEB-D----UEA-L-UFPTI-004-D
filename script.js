// 1. Selección de elementos del DOM
const formulario = document.getElementById('formSolicitudes');
const nombreCliente = document.getElementById('nombreCliente');
const tipoServicio = document.getElementById('tipoServicio');
const descripcionProblema = document.getElementById('descripcionProblema');
const contenedorLista = document.getElementById('contenedorLista');
const contadorSolicitudes = document.getElementById('contadorSolicitudes');
const mensajeVacio = document.getElementById('mensajeVacio');

let totalRegistros = 0;

// Función de validación mejorada
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

    // --- Lógica de creación ---
    if (totalRegistros === 0) {
        mensajeVacio.style.display = 'none';
    }

    const colDiv = document.createElement('div');
    colDiv.className = 'col-12';

    colDiv.innerHTML = `
        <div class="card border-start border-primary border-4 p-3 bg-light shadow-sm position-relative">
            <h6 class="fw-bold text-dark mb-1">${nombreCliente.value.trim()}</h6>
            <span class="badge bg-primary text-wrap mb-2" style="max-width: fit-content;">${tipoServicio.value}</span>
            <p class="small text-muted mb-2">${descripcionProblema.value.trim()}</p>
            <button class="btn btn-sm btn-outline-danger btn-eliminar position-absolute top-50 end-0 translate-middle-y me-3">
                <i class="bi bi-trash-fill"></i> Eliminar
            </button>
        </div>
    `;

    const botonEliminar = colDiv.querySelector('.btn-eliminar');
    botonEliminar.addEventListener('click', function() {
        colDiv.remove();
        totalRegistros--;
        contadorSolicitudes.textContent = totalRegistros;
        if (totalRegistros === 0) {
            mensajeVacio.style.display = 'block';
        }
    });

    contenedorLista.appendChild(colDiv);
    totalRegistros++;
    contadorSolicitudes.textContent = totalRegistros;

    // Resetear form y quitar validaciones verdes
    formulario.reset();
    campos.forEach(c => c.classList.remove('is-valid'));
});