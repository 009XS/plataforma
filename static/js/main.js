/**
 * EduPlatform - Main JavaScript Library
 * Funciones unificadas para toda la aplicación
 */

// ====================================
// CONFIGURACIÓN GLOBAL
// ====================================
const EduPlatform = {
    apiBase: '',  // Base URL for API
    sweetAlert: typeof Swal !== 'undefined' ? Swal : null,

    // Configuración por defecto para fetch
    fetchConfig: {
        headers: {
            'Content-Type': 'application/json'
        }
    }
};

// ====================================
// NAVEGACIÓN
// ====================================

/**
 * Muestra una sección específica y oculta las demás
 * @param {string} sectionId - ID de la sección a mostrar (sin prefijo 'section-')
 */
function showSection(sectionId) {
    // Ocultar todas las secciones
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
        section.classList.add('hidden');
    });

    // Mostrar la sección solicitada
    const targetSection = document.getElementById('section-' + sectionId);
    if (targetSection) {
        targetSection.classList.remove('hidden');
        targetSection.classList.add('active');
    }

    // Actualizar navegación activa
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });

    // Marcar el nav-item actual como activo
    if (event && event.target) {
        const navItem = event.target.closest('.nav-item');
        if (navItem) navItem.classList.add('active');
    }

    // Actualizar título de página si existe
    const pageTitle = document.getElementById('page-title');
    if (pageTitle && window.pageTitles && window.pageTitles[sectionId]) {
        pageTitle.textContent = window.pageTitles[sectionId];
    }

    // Disparar evento personalizado
    document.dispatchEvent(new CustomEvent('sectionChanged', { detail: { section: sectionId } }));
}

/**
 * Toggle para sidebar móvil
 */
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('-translate-x-full');
    }
}

// ====================================
// MODALES
// ====================================

/**
 * Abre un modal por su ID
 * @param {string} modalId - ID del modal
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
    }
}

/**
 * Cierra un modal por su ID
 * @param {string} modalId - ID del modal
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
    }
}

/**
 * Cierra modal al hacer clic fuera del contenido
 */
function setupModalClose() {
    document.querySelectorAll('[data-modal-backdrop]').forEach(modal => {
        modal.addEventListener('click', function (e) {
            if (e.target === this) {
                closeModal(this.id);
            }
        });
    });
}

// ====================================
// API HELPERS
// ====================================

/**
 * Wrapper para fetch con manejo de errores
 * @param {string} url - URL del endpoint
 * @param {object} options - Opciones de fetch
 * @returns {Promise<object>} - Respuesta JSON
 */
async function apiFetch(url, options = {}) {
    try {
        const config = {
            ...EduPlatform.fetchConfig,
            ...options,
            headers: {
                ...EduPlatform.fetchConfig.headers,
                ...options.headers
            }
        };

        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * POST request helper
 */
async function apiPost(url, data) {
    return apiFetch(url, {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

/**
 * GET request helper
 */
async function apiGet(url) {
    return apiFetch(url, { method: 'GET' });
}

// ====================================
// NOTIFICACIONES
// ====================================

/**
 * Muestra una notificación usando SweetAlert2
 * @param {string} type - 'success', 'error', 'warning', 'info'
 * @param {string} title - Título de la notificación
 * @param {string} text - Texto opcional
 */
function showNotification(type, title, text = '') {
    if (EduPlatform.sweetAlert) {
        Swal.fire({
            icon: type,
            title: title,
            text: text,
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true
        });
    } else {
        alert(`${title}\n${text}`);
    }
}

/**
 * Muestra un diálogo de confirmación
 * @param {string} title - Título
 * @param {string} text - Texto
 * @param {string} confirmText - Texto del botón de confirmación
 * @returns {Promise<boolean>}
 */
async function showConfirm(title, text, confirmText = 'Sí, continuar') {
    if (EduPlatform.sweetAlert) {
        const result = await Swal.fire({
            title: title,
            text: text,
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#0284c7',
            cancelButtonColor: '#6b7280',
            confirmButtonText: confirmText,
            cancelButtonText: 'Cancelar'
        });
        return result.isConfirmed;
    }
    return confirm(`${title}\n${text}`);
}

/**
 * Muestra un loader
 * @param {string} message - Mensaje a mostrar
 */
function showLoader(message = 'Cargando...') {
    if (EduPlatform.sweetAlert) {
        Swal.fire({
            title: message,
            allowOutsideClick: false,
            didOpen: () => Swal.showLoading()
        });
    }
}

/**
 * Oculta el loader
 */
function hideLoader() {
    if (EduPlatform.sweetAlert) {
        Swal.close();
    }
}

// ====================================
// FLASHCARDS API
// ====================================

async function loadFlashcards() {
    try {
        const cards = await apiGet('/api/flashcards');
        return cards;
    } catch (error) {
        console.error('Error loading flashcards:', error);
        return [];
    }
}

async function createFlashcard(pregunta, respuesta) {
    try {
        const result = await apiPost('/api/flashcards', { pregunta, respuesta });
        showNotification('success', '¡Creada!', 'Tu tarjeta ha sido guardada');
        return result;
    } catch (error) {
        showNotification('error', 'Error', 'No se pudo guardar la tarjeta');
        throw error;
    }
}

// ====================================
// MENSAJES API
// ====================================

async function loadMessages() {
    try {
        return await apiGet('/api/messages');
    } catch (error) {
        console.error('Error loading messages:', error);
        return [];
    }
}

async function sendMessage(destinatarioId, asunto, contenido) {
    try {
        const result = await apiPost('/send_message', {
            destinatario_id: destinatarioId,
            asunto: asunto,
            contenido: contenido
        });
        showNotification('success', 'Enviado', 'Mensaje enviado correctamente');
        return result;
    } catch (error) {
        showNotification('error', 'Error', 'No se pudo enviar el mensaje');
        throw error;
    }
}

// ====================================
// PORTFOLIO API
// ====================================

async function loadPortfolio() {
    try {
        return await apiGet('/api/portfolio');
    } catch (error) {
        console.error('Error loading portfolio:', error);
        return [];
    }
}

async function uploadPortfolioFile(file, nombre, materia) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('nombre', nombre);
    formData.append('materia', materia);

    try {
        showLoader('Subiendo...');
        const response = await fetch('/api/portfolio/upload', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        hideLoader();

        if (result.success) {
            showNotification('success', 'Éxito', 'Archivo subido al portafolio');
        }
        return result;
    } catch (error) {
        hideLoader();
        showNotification('error', 'Error', 'No se pudo subir el archivo');
        throw error;
    }
}

// ====================================
// TEAMS API
// ====================================

async function loadTeams() {
    try {
        return await apiGet('/api/teams');
    } catch (error) {
        console.error('Error loading teams:', error);
        return [];
    }
}

async function createTeam(nombre) {
    try {
        const result = await apiPost('/api/teams/create', { nombre });
        showNotification('success', 'Creado', 'Equipo creado exitosamente');
        return result;
    } catch (error) {
        showNotification('error', 'Error', 'No se pudo crear el equipo');
        throw error;
    }
}

// ====================================
// TUTOR / AI CHAT API
// ====================================

async function sendAiMessage(message) {
    try {
        const result = await apiPost('/api/ai-chat', { message });
        return result.response || 'Lo siento, no pude procesar tu mensaje.';
    } catch (error) {
        console.error('AI Chat error:', error);
        return 'Error de conexión con el asistente IA.';
    }
}

async function loadTutorAppointments() {
    try {
        return await apiGet('/api/tutor/schedule');
    } catch (error) {
        console.error('Error loading tutor appointments:', error);
        return [];
    }
}

async function scheduleTutorSession(fechaHora, tutorId) {
    try {
        const result = await apiPost('/api/tutor/schedule', {
            fecha_hora: fechaHora,
            tutor_id: tutorId
        });
        showNotification('success', 'Agendado', 'Tu cita ha sido registrada');
        return result;
    } catch (error) {
        showNotification('error', 'Error', 'No se pudo agendar la cita');
        throw error;
    }
}

// ====================================
// VIDEO CALLS
// ====================================

/**
 * Inicia una videollamada usando Jitsi Meet
 * @param {string} roomType - Tipo de sala (ej: 'tutor', 'team')
 * @param {string|number} roomId - ID opcional para la sala
 */
function startVideoCall(roomType = 'general', roomId = '') {
    const roomName = `EduPlatform-${roomType}-${roomId || Date.now()}`;
    const url = `https://meet.jit.si/${roomName}`;
    window.open(url, '_blank');
}

async function joinVideoCall(type = 'tutor') {
    try {
        const data = await apiPost('/api/meet/join', { type });
        window.open(data.url, '_blank');
    } catch (error) {
        showNotification('error', 'Error', 'No se pudo iniciar la videollamada');
    }
}

// ====================================
// NOTIFICACIONES DEL SISTEMA
// ====================================

async function checkNotifications() {
    try {
        const data = await apiGet('/api/notifications');
        const badge = document.getElementById('notif-badge');
        if (badge) {
            if (data.count > 0) {
                badge.textContent = data.count;
                badge.classList.remove('hidden');
            } else {
                badge.classList.add('hidden');
            }
        }
        return data;
    } catch (error) {
        console.error('Error checking notifications:', error);
        return { count: 0 };
    }
}

function toggleNotificaciones() {
    const dropdown = document.getElementById('notif-dropdown');
    if (dropdown) {
        dropdown.classList.toggle('hidden');
    }
}

// ====================================
// ENCUESTAS DOCENTES API
// ====================================

async function loadEncuestasDocentes() {
    try {
        return await apiGet('/api/encuestas-docentes');
    } catch (error) {
        console.error('Error loading encuestas:', error);
        return { encuestas: [] };
    }
}

async function submitEncuestaDocente(data) {
    try {
        const result = await apiPost('/api/responder-encuesta-docente', data);
        if (result.success) {
            showNotification('success', '¡Gracias!', result.success);
        }
        return result;
    } catch (error) {
        showNotification('error', 'Error', 'No se pudo enviar la encuesta');
        throw error;
    }
}

// ====================================
// DOCENTE: TAREAS API
// ====================================

async function crearTarea(data) {
    try {
        const result = await apiPost('/api/docente/tareas', data);
        showNotification('success', 'Éxito', 'Tarea creada correctamente');
        return result;
    } catch (error) {
        showNotification('error', 'Error', 'No se pudo crear la tarea');
        throw error;
    }
}

async function eliminarTarea(tareaId) {
    const confirmed = await showConfirm(
        '¿Eliminar tarea?',
        'Esta acción no se puede deshacer. Se eliminarán también todas las entregas.',
        'Sí, eliminar'
    );

    if (confirmed) {
        try {
            const result = await apiPost('/api/eliminar-tarea', { tarea_id: tareaId });
            if (result.success) {
                showNotification('success', 'Eliminada', 'La tarea ha sido eliminada');
                location.reload();
            }
        } catch (error) {
            showNotification('error', 'Error', 'No se pudo eliminar la tarea');
        }
    }
}

async function calificarEntrega(entregaId, calificacion, comentarios) {
    try {
        const result = await apiPost('/api/calificar-tarea', {
            entrega_id: entregaId,
            calificacion: calificacion,
            comentarios: comentarios
        });
        showNotification('success', 'Éxito', 'Calificación guardada');
        return result;
    } catch (error) {
        showNotification('error', 'Error', 'No se pudo guardar la calificación');
        throw error;
    }
}

// ====================================
// DOCENTE: QR ASISTENCIA API
// ====================================

async function generarQRAsistencia(materiaId) {
    try {
        showLoader('Generando QR...');
        const result = await apiPost('/api/generar_qr_asistencia', { materia_id: materiaId });
        hideLoader();
        return result;
    } catch (error) {
        hideLoader();
        showNotification('error', 'Error', 'No se pudo generar el QR');
        throw error;
    }
}

// ====================================
// DOCENTE: RECURSOS API
// ====================================

async function loadRecursos() {
    try {
        return await apiGet('/api/resources');
    } catch (error) {
        console.error('Error loading resources:', error);
        return [];
    }
}

async function subirRecurso(formData) {
    try {
        showLoader('Subiendo recurso...');
        const response = await fetch('/api/resources', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        hideLoader();

        if (result.success) {
            showNotification('success', 'Éxito', 'Recurso subido correctamente');
        }
        return result;
    } catch (error) {
        hideLoader();
        showNotification('error', 'Error', 'No se pudo subir el recurso');
        throw error;
    }
}

async function eliminarRecurso(recursoId) {
    const confirmed = await showConfirm('¿Eliminar recurso?', 'Esta acción no se puede deshacer.');

    if (confirmed) {
        try {
            await apiPost('/api/eliminar-recurso', { recurso_id: recursoId });
            showNotification('success', 'Eliminado', 'Recurso eliminado');
            return true;
        } catch (error) {
            showNotification('error', 'Error', 'No se pudo eliminar');
            return false;
        }
    }
    return false;
}

// ====================================
// DOCENTE: RETOS DE CÓDIGO API
// ====================================

async function lanzarReto(data) {
    try {
        showLoader('Lanzando reto...');
        const result = await apiPost('/api/lanzar_reto', data);
        hideLoader();

        if (result.success) {
            showNotification('success', '¡Reto Lanzado!', 'El reto ha sido publicado');
        }
        return result;
    } catch (error) {
        hideLoader();
        showNotification('error', 'Error', 'No se pudo lanzar el reto');
        throw error;
    }
}

// ====================================
// DOCENTE: COMUNICADOS API
// ====================================

async function crearComunicado(formData) {
    try {
        showLoader('Publicando...');
        const response = await fetch('/api/announcements', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        hideLoader();

        if (result.success) {
            showNotification('success', 'Publicado', 'Comunicado publicado correctamente');
        }
        return result;
    } catch (error) {
        hideLoader();
        showNotification('error', 'Error', 'No se pudo publicar');
        throw error;
    }
}

// ====================================
// DOCENTE: EVALUACIONES AI
// ====================================

async function generarEvaluacionAI(materiaId, tema, cantidad = 10) {
    try {
        showLoader('Generando con IA...');
        const result = await apiPost('/examenes/generar-ai', {
            materia_id: materiaId,
            tema: tema,
            cantidad: cantidad
        });
        hideLoader();
        showNotification('success', '¡Listo!', 'Evaluación generada con IA');
        return result;
    } catch (error) {
        hideLoader();
        showNotification('error', 'Error', 'No se pudo generar con IA');
        throw error;
    }
}

// ====================================
// ADMIN: USUARIOS API
// ====================================

async function loadUsuarios() {
    try {
        return await apiGet('/api/usuarios');
    } catch (error) {
        console.error('Error loading usuarios:', error);
        return [];
    }
}

async function crearUsuario(data) {
    try {
        const result = await apiPost('/api/usuarios/crear', data);
        showNotification('success', 'Creado', 'Usuario creado exitosamente');
        return result;
    } catch (error) {
        showNotification('error', 'Error', 'No se pudo crear el usuario');
        throw error;
    }
}

async function eliminarUsuario(userId) {
    const confirmed = await showConfirm(
        '¿Eliminar usuario?',
        'Esta acción eliminará permanentemente al usuario y todos sus datos.',
        'Sí, eliminar'
    );

    if (confirmed) {
        try {
            const result = await apiPost('/api/usuarios/eliminar', { user_id: userId });
            if (result.success) {
                showNotification('success', 'Eliminado', 'Usuario eliminado');
                return true;
            }
        } catch (error) {
            showNotification('error', 'Error', 'No se pudo eliminar');
        }
    }
    return false;
}

// ====================================
// TIENDA / EDUCOINS
// ====================================

async function comprarItem(itemId, itemNombre, precio) {
    const confirmed = await showConfirm(
        `¿Comprar ${itemNombre}?`,
        `Esto costará ${precio} EduCoins`,
        'Sí, comprar'
    );

    if (confirmed) {
        try {
            showLoader('Procesando compra...');
            const result = await apiPost(`/api/tienda/comprar/${itemId}`, {});
            hideLoader();

            if (result.success) {
                showNotification('success', '¡Compra exitosa!', `Has adquirido ${itemNombre}`);
                location.reload();
            }
            return result;
        } catch (error) {
            hideLoader();
            showNotification('error', 'Error', 'No se pudo completar la compra');
        }
    }
    return null;
}

// ====================================
// CALENDARIO
// ====================================

async function loadCalendarEvents(month, year) {
    try {
        return await apiGet(`/api/calendar/events?month=${month}&year=${year}`);
    } catch (error) {
        console.error('Error loading calendar events:', error);
        return [];
    }
}

async function createCalendarEvent(titulo, fecha, descripcion, tipo = 'personal') {
    try {
        const result = await apiPost('/api/eventos-personales', {
            titulo,
            fecha,
            descripcion,
            tipo
        });
        showNotification('success', 'Creado', 'Evento guardado');
        return result;
    } catch (error) {
        showNotification('error', 'Error', 'No se pudo crear el evento');
        throw error;
    }
}

async function loadEventosPersonales(month, year) {
    try {
        return await apiGet(`/api/eventos-personales?month=${month}&year=${year}`);
    } catch (error) {
        console.error('Error loading eventos personales:', error);
        return [];
    }
}

// ====================================
// CALIFICAR ENTREGAS (Individual)
// ====================================

async function calificarEntregaIndividual(entregaId, calificacion, comentarios = '') {
    try {
        showLoader('Guardando calificación...');
        const result = await apiPost(`/api/calificar-entrega/${entregaId}`, {
            calificacion,
            comentarios
        });
        hideLoader();

        if (result.success) {
            showNotification('success', 'Calificado', result.message);
        }
        return result;
    } catch (error) {
        hideLoader();
        showNotification('error', 'Error', 'No se pudo guardar la calificación');
        throw error;
    }
}

// ====================================
// TIENDA: Cargar Items
// ====================================

async function loadTiendaItems(categoria = '') {
    try {
        let url = '/api/tienda/items';
        if (categoria) url += `?categoria=${categoria}`;
        return await apiGet(url);
    } catch (error) {
        console.error('Error loading tienda items:', error);
        return [];
    }
}

async function getUserEducoins() {
    try {
        const data = await apiGet('/api/user/me');
        return data.educoins || 0;
    } catch (error) {
        console.error('Error getting educoins:', error);
        return 0;
    }
}

// ====================================
// UTILIDADES
// ====================================

/**
 * Formatea una fecha para mostrar
 */
function formatDate(dateString, options = {}) {
    const date = new Date(dateString);
    const defaultOptions = {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    };
    return date.toLocaleDateString('es-MX', { ...defaultOptions, ...options });
}

/**
 * Formatea fecha y hora
 */
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('es-MX', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Escapa HTML para prevenir XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Filtrar elementos de una lista por texto
 */
function filterList(inputId, containerSelector, itemSelector) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener('keyup', debounce(function () {
        const filter = this.value.toLowerCase();
        const container = document.querySelector(containerSelector);
        const items = container.querySelectorAll(itemSelector);

        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(filter) ? '' : 'none';
        });
    }, 300));
}

// ====================================
// INICIALIZACIÓN
// ====================================

document.addEventListener('DOMContentLoaded', function () {
    // Setup modal click-outside-to-close
    setupModalClose();

    // Check notifications periodically
    checkNotifications();
    setInterval(checkNotifications, 60000);

    // Setup nav-item click handlers
    document.querySelectorAll('.nav-item').forEach(link => {
        link.addEventListener('click', function (e) {
            document.querySelectorAll('.nav-item').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', toggleSidebar);
    }

    console.log('EduPlatform JS initialized');
});

// Expose main functions to global scope for inline onclick handlers
window.showSection = showSection;
window.toggleSidebar = toggleSidebar;
window.openModal = openModal;
window.closeModal = closeModal;
window.showNotification = showNotification;
window.showConfirm = showConfirm;
window.showLoader = showLoader;
window.hideLoader = hideLoader;
window.apiFetch = apiFetch;
window.apiPost = apiPost;
window.apiGet = apiGet;
