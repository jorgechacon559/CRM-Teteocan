import { defineStore } from "pinia";
import general from "@/api/endpoints/general";
import { reactive, toRefs } from "vue";

export const useSeguimientosStore = defineStore('seguimientos', () => {
    const state = reactive({
        data: [],              // Lista de seguimientos (historial)
        current: null,         // Seguimiento seleccionado
        loading: false,
        error: null,
        paginacion: {
            page: 1,
            totalPages: 1,
            perPage: 15,
        }
    });

    // --- SETTERS ---
    const setData = (arr) => { state.data = arr || []; };
    const setCurrent = (item) => { state.current = item; };

    // --- OBTENER HISTORIAL DE SEGUIMIENTOS ---
    // params puede incluir: organizacion_id, usuario_id, tipo, estado, fecha, etc.
    const getSeguimientos = async (params = {}) => {
        state.loading = true;
        state.error = null;
        try {
            const response = await general.getSeguimientos(params);
            setData(response.data || []);
            // Si tu backend soporta paginación, actualiza aquí
            // state.paginacion.totalPages = response.data.totalPages || 1;
            return response.data;
        } catch (error) {
            state.error = error?.message || 'Error al obtener seguimientos';
            setData([]);
            return [];
        } finally {
            state.loading = false;
        }
    };

    // --- OBTENER SEGUIMIENTO POR ID ---
    const getSeguimientoById = async (id) => {
        state.loading = true;
        state.error = null;
        try {
            const response = await general.getSeguimientoById(id);
            setCurrent(response.data);
            return response.data;
        } catch (error) {
            state.error = error?.message || 'Error al obtener seguimiento';
            setCurrent(null);
            return null;
        } finally {
            state.loading = false;
        }
    };

    // --- CREAR SEGUIMIENTO ---
    // data: { organizacion_id, usuario_id, tipo, comentarios, metodo_contacto, estado, nivel_digitalizacion, fecha }
    const crearSeguimiento = async (data) => {
        state.loading = true;
        state.error = null;
        try {
            const response = await general.crearSeguimiento(data);
            // Triggers del backend actualizan prospecto_id, estado_organizacion y nivel_digitalizacion automáticamente
            setCurrent(response.data);
            return response.data;
        } catch (error) {
            state.error = error?.message || 'Error al crear seguimiento';
            return { success: false, message: state.error, status: error?.status || 500 };
        } finally {
            state.loading = false;
        }
    };

    // --- EDITAR SEGUIMIENTO (solo admin o para correcciones) ---
    // data: { ...campos editables }
    const editarSeguimiento = async (id, data) => {
        state.loading = true;
        state.error = null;
        try {
            const response = await general.editarSeguimiento(id, data);
            setCurrent(response.data);
            return response.data;
        } catch (error) {
            state.error = error?.message || 'Error al editar seguimiento';
            return { success: false, message: state.error, status: error?.status || 500 };
        } finally {
            state.loading = false;
        }
    };

    // --- FILTROS AVANZADOS ---
    // Puedes agregar métodos para filtrar por tipo, estado, usuario, fecha, etc.
    const filtrarSeguimientos = (filtros = {}) => {
        // Esto es solo para filtrar en frontend si ya tienes todos los datos cargados
        return state.data.filter(seg => {
            return Object.entries(filtros).every(([key, val]) => {
                if (val === undefined || val === null || val === '') return true;
                return seg[key] === val;
            });
        });
    };

    // --- LIMPIAR ESTADO ---
    const limpiarEstado = () => {
        setCurrent(null);
        setData([]);
        state.error = null;
    };

    return {
        ...toRefs(state),
        setData,
        setCurrent,
        getSeguimientos,
        getSeguimientoById,
        crearSeguimiento,
        editarSeguimiento,
        filtrarSeguimientos,
        limpiarEstado,
    };
});