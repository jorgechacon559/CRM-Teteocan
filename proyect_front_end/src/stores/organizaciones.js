import { defineStore } from "pinia";
import general from "@/api/endpoints/general";
import { reactive, toRefs } from "vue";

export const useOrganizacionesStore = defineStore('organizaciones', () => {
    const state = reactive({
        data: [],                // Lista de organizaciones (todas o filtradas)
        current: null,           // Organización seleccionada
        detallesEmpresa: null,   // Detalles de empresa (si aplica)
        detallesNegocio: null,   // Detalles de negocio local (si aplica)
        asignaciones: [],        // Historial de asignaciones (si aplica)
        loading: false,
        error: null,
        paginacion: {
            page: 1,
            totalPages: 1,
            perPage: 15,
        }
    });

    // --- ORGANIZACIONES ---
    const setData = (arr) => { state.data = arr || []; };
    const setCurrent = (item) => { state.current = item; };

    // Obtener todas las organizaciones (con filtros y paginación)
    const getOrganizaciones = async (params = {}) => {
        state.loading = true;
        state.error = null;
        try {
            const response = await general.getOrganizaciones(params);
            setData(response.data || []);
            // Si tu backend soporta paginación, actualiza aquí
            // state.paginacion.totalPages = response.data.totalPages || 1;
            return response.data;
        } catch (error) {
            state.error = error?.message || 'Error al obtener organizaciones';
            setData([]);
            return [];
        } finally {
            state.loading = false;
        }
    };

    // Obtener organización por ID (incluye detalles y asignaciones)
    const getOrganizacionById = async (id) => {
        state.loading = true;
        state.error = null;
        try {
            const response = await general.getOrganizacionById(id);
            setCurrent(response.data);
            // Cargar detalles según tipo
            if (response.data?.tipo === 'empresa') {
                await getDetallesEmpresa(id);
            } else if (response.data?.tipo === 'negocio_local') {
                await getDetallesNegocio(id);
            }
            // Cargar historial de asignaciones
            await getAsignaciones({ organizacion_id: id });
            return response.data;
        } catch (error) {
            state.error = error?.message || 'Error al obtener la organización';
            setCurrent(null);
            return null;
        } finally {
            state.loading = false;
        }
    };

    // Crear organización (empresa o negocio local)
    const crearOrganizacion = async (data) => {
        state.loading = true;
        state.error = null;
        try {
            const response = await general.crearOrganizacion(data);
            setCurrent(response.data);
            return response.data;
        } catch (error) {
            state.error = error?.message || 'Error al crear organización';
            return { success: false, message: state.error, status: error?.status || 500 };
        } finally {
            state.loading = false;
        }
    };

    // Editar organización
    const editarOrganizacion = async (id, data) => {
        state.loading = true;
        state.error = null;
        try {
            const response = await general.editarOrganizacion(id, data);
            setCurrent(response.data);
            return response.data;
        } catch (error) {
            state.error = error?.message || 'Error al editar organización';
            return { success: false, message: state.error, status: error?.status || 500 };
        } finally {
            state.loading = false;
        }
    };

    // Eliminar organización (si aplica)
    const eliminarOrganizacion = async (id) => {
        state.loading = true;
        state.error = null;
        try {
            const response = await general.eliminarOrganizacion(id);
            return response.data;
        } catch (error) {
            state.error = error?.message || 'Error al eliminar organización';
            return { success: false, message: state.error, status: error?.status || 500 };
        } finally {
            state.loading = false;
        }
    };

    // --- DETALLES EMPRESA ---
    const getDetallesEmpresa = async (organizacion_id) => {
        try {
            const response = await general.getDetalleEmpresaByOrgId(organizacion_id);
            state.detallesEmpresa = response.data;
            return response.data;
        } catch (error) {
            state.detallesEmpresa = null;
            return null;
        }
    };
    const crearDetalleEmpresa = async (data) => {
        try {
            const response = await general.crearDetalleEmpresa(data);
            state.detallesEmpresa = response.data;
            return response.data;
        } catch (error) {
            return { success: false, message: error?.message || 'Error al crear detalle', status: error?.status || 500 };
        }
    };
    const editarDetalleEmpresa = async (id, data) => {
        try {
            const response = await general.editarDetalleEmpresa(id, data);
            state.detallesEmpresa = response.data;
            return response.data;
        } catch (error) {
            return { success: false, message: error?.message || 'Error al editar detalle', status: error?.status || 500 };
        }
    };

    // --- DETALLES NEGOCIO LOCAL ---
    const getDetallesNegocio = async (organizacion_id) => {
        try {
            const response = await general.getDetalleNegocioByOrgId(organizacion_id);
            state.detallesNegocio = response.data;
            return response.data;
        } catch (error) {
            state.detallesNegocio = null;
            return null;
        }
    };
    const crearDetalleNegocio = async (data) => {
        try {
            const response = await general.crearDetalleNegocio(data);
            state.detallesNegocio = response.data;
            return response.data;
        } catch (error) {
            return { success: false, message: error?.message || 'Error al crear detalle', status: error?.status || 500 };
        }
    };
    const editarDetalleNegocio = async (id, data) => {
        try {
            const response = await general.editarDetalleNegocio(id, data);
            state.detallesNegocio = response.data;
            return response.data;
        } catch (error) {
            return { success: false, message: error?.message || 'Error al editar detalle', status: error?.status || 500 };
        }
    };

    // --- ASIGNACIONES (Historial de prospectos) ---
    const getAsignaciones = async (params = {}) => {
        try {
            const response = await general.getAsignaciones(params);
            state.asignaciones = response.data || [];
            return response.data;
        } catch (error) {
            state.asignaciones = [];
            return [];
        }
    };

    // --- UTILIDADES ---
    const limpiarEstado = () => {
        setCurrent(null);
        state.detallesEmpresa = null;
        state.detallesNegocio = null;
        state.asignaciones = [];
        state.error = null;
    };

    return {
        ...toRefs(state),
        setData,
        setCurrent,
        getOrganizaciones,
        getOrganizacionById,
        crearOrganizacion,
        editarOrganizacion,
        eliminarOrganizacion,
        getDetallesEmpresa,
        crearDetalleEmpresa,
        editarDetalleEmpresa,
        getDetallesNegocio,
        crearDetalleNegocio,
        editarDetalleNegocio,
        getAsignaciones,
        limpiarEstado,
    };
});