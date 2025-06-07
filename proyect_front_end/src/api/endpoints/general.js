import api from "../axios";

export default {
    // --- ORGANIZACIONES ---
    getOrganizaciones(params = {}) {
        // GET /api/organizaciones/
        return api.get('/organizaciones/', { params });
    },
    getOrganizacionById(id) {
        // GET /api/organizaciones/<id>
        return api.get(`/organizaciones/${id}`);
    },
    crearOrganizacion(data) {
        // POST /api/organizaciones/
        return api.post('/organizaciones/', data);
    },
    editarOrganizacion(id, data) {
        // PUT /api/organizaciones/<id>
        return api.put(`/organizaciones/${id}`, data);
    },

    // --- SEGUIMIENTOS ---
    // Solo existen:
    // POST /api/seguimientos/registrar
    // GET /api/seguimientos/organizacion/<organizacion_id>
    // GET /api/seguimientos/usuario/<usuario_id>
    // PUT /api/seguimientos/<seguimiento_id>
    // DELETE /api/seguimientos/<seguimiento_id>
getSeguimientosPorUsuario(usuario_id) {
    // GET /api/seguimientos/usuario/<usuario_id>
    return api.get(`/seguimientos/usuario/${usuario_id}`);
},

getUsuarios(item = {}) {
    const token = sessionStorage.getItem('access_token');
    // Si item es string, úsalo como endpoint; si es objeto, usa como params
    if (typeof item === 'string') {
        return api.get(`/usuarios/${item}`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
    }
    // Si es objeto (filtros), usa como params
    return api.get('/usuarios/usuarios', {
        params: item,
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
},

getSeguimientos(params = {}) {
    // Si hay filtros, usa los endpoints específicos
    if (params.organizacion_id) {
        return this.getSeguimientosPorOrganizacion(params.organizacion_id)
    }
    if (params.usuario_id) {
        return this.getSeguimientosPorUsuario(params.usuario_id)
    }
    // Si no hay filtros, pide todos los seguimientos
    return api.get('/seguimientos/', { params })
},
    crearSeguimiento(data) {
        // POST /api/seguimientos/registrar
        return api.post('/seguimientos/registrar', data);
    },
    editarSeguimiento(id, data) {
        // PUT /api/seguimientos/<id>
        return api.put(`/seguimientos/${id}`, data);
    },
    eliminarSeguimiento(id) {
        // DELETE /api/seguimientos/<id>
        return api.delete(`/seguimientos/${id}`);
    },

    // --- HISTORIAL DE ASIGNACIONES ---
    // GET /api/organizaciones/<organizacion_id>/historial-asignaciones
    getHistorialAsignaciones(organizacion_id) {
        return api.get(`/organizaciones/${organizacion_id}/historial-asignaciones`);
    },

    // --- REPORTES ---
    // Ejemplo de reportes disponibles
    getResumenOrganizaciones() {
        // GET /api/reportes/resumen-organizaciones
        return api.get('/reportes/resumen-organizaciones');
    },
    getOrganizacionesNivelDigital() {
        // GET /api/reportes/organizaciones-nivel-digital
        return api.get('/reportes/organizaciones-nivel-digital');
    },
    getSeguimientosPorUsuarioReporte() {
        // GET /api/reportes/seguimientos-por-usuario
        return api.get('/reportes/seguimientos-por-usuario');
    },
    getConversiones() {
        // GET /api/reportes/conversiones
        return api.get('/reportes/conversiones');
    }
}
