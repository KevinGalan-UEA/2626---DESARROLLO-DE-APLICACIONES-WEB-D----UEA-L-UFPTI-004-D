// 1. Selección de elementos del DOM
const formulario = document.getElementById('formSolicitudes');
const nombreCliente = document.getElementById('nombreCliente');
const tipoServicio = document.getElementById('tipoServicio');
const descripcionProblema = document.getElementById('descripcionProblema');
const contenedorLista = document.getElementById('contenedorLista');
const contadorSolicitudes = document.getElementById('contadorSolicitudes');
const mensajeVacio = document.getElementById('mensajeVacio');

// Contador global para rastrear las solicitudes creadas
let totalRegistros = 0;

// 2. Manejo de Eventos: Evento 'submit' del formulario
formulario.addEventListener('submit', function(evento) {
    // Uso de preventDefault() para evitar que se recargue el navegador
    evento.preventDefault();

    // Obtener valores de los campos limpiando espacios sobrantes
    const nombreVal = nombreCliente.value.trim();
    const servicioVal = tipoServicio.value;
    const descripcionVal = descripcionProblema.value.trim();

    // 3. Validación básica para verificar que los campos no estén vacíos
    if (nombreVal === "" || servicioVal === "" || descripcionVal === "") {
        alert("Por favor, complete todos los campos para registrar la solicitud.");
        return; // Detiene la ejecución
    }

    // Ocultar mensaje por defecto si existe la primera tarjeta
    if (totalRegistros === 0) {
        mensajeVacio.style.display = 'none';
    }

    // 4. Manipulación del DOM: Uso de createElement()
    const colDiv = document.createElement('div');
    colDiv.className = 'col-12';

    // Inserción estructurada aplicando clases y estilos responsivos de Bootstrap
    colDiv.innerHTML = `
        <div class="card border-start border-primary border-4 p-3 bg-light shadow-sm position-relative">
            <h6 class="fw-bold text-dark mb-1">${nombreVal}</h6>
            <span class="badge bg-primary text-wrap mb-2" style="max-width: fit-content;">${servicioVal}</span>
            <p class="small text-muted mb-2">${descripcionVal}</p>
            <button class="btn btn-sm btn-outline-danger btn-eliminar position-absolute top-50 end-0 translate-middle-y me-3">
                <i class="bi bi-trash-fill"></i> Eliminar
            </button>
        </div>
    `;

    // 5. Manejo de Eventos: Eliminar registros mediante el evento 'click'
    const botonEliminar = colDiv.querySelector('.btn-eliminar');
    botonEliminar.addEventListener('click', function() {
        colDiv.remove(); // Remueve el nodo del DOM
        
        // Actualizar contador decreciente
        totalRegistros--;
        contadorSolicitudes.textContent = totalRegistros;

        // Mostrar el mensaje original si ya no quedan registros
        if (totalRegistros === 0) {
            mensajeVacio.style.display = 'block';
        }
    });

    // 6. Manipulación del DOM: Uso de appendChild() para inyectar la tarjeta
    contenedorLista.appendChild(colDiv);

    // 7. Mostrar en pantalla el total de registros creados actualizando el contador
    totalRegistros++;
    contadorSolicitudes.textContent = totalRegistros;

    // Limpiar el formulario para un nuevo ingreso de datos
    formulario.reset();
});