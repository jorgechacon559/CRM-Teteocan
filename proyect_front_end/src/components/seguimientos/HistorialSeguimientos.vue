<template>
  <div class="main-container">
    <div class="header-section">
      <div class="header-content">
        <div class="header-text">
          <h1><i class="fas fa-history"></i> Historial de seguimientos</h1>
          <p>Consulta el historial completo de interacciones y cambios de estado de una organización o agente.</p>
        </div>
      </div>
    </div>
    
    <div class="content-wrapper">
      <div class="filters-card">
        <div class="filters-header">
          <i class="fas fa-filter"></i>
          <h3>Filtros de búsqueda</h3>
        </div>
        <div class="filters-grid">
          <div class="filter-group" v-if="esAdmin">
            <label class="filter-label"><i class="fas fa-industry"></i> Tipo de organización</label>
            <div class="select-container">
              <select class="filter-select" v-model="filtroTipoOrg">
                <option value="">Todas</option>
                <option value="empresa">Empresa</option>
                <option value="negocio_local">Negocio local</option>
              </select>
              <i class="fas fa-chevron-down"></i>
            </div>
          </div>

          <div class="filter-group" v-if="esAdmin">
            <label class="filter-label"><i class="fas fa-user"></i> Agente</label>
            <div class="select-container">
              <select class="filter-select" v-model="filtroAgente">
                <option value="">Todos los agentes</option>
                <option v-for="user in listaUsuarios" :key="user.usuario_id" :value="user.usuario_id">
                  {{ user.nombre }}
                </option>
              </select>
              <i class="fas fa-chevron-down"></i>
            </div>
          </div>
          
          <div class="filter-group">
            <label class="filter-label"><i class="fas fa-tag"></i> Estado</label>
            <div class="select-container">
              <select class="filter-select" v-model="filtroEstado" @change="buscarHistorial">
                <option value="">Todos los estados</option>
                <option value="prospecto">Prospecto</option>
                <option value="cliente">Cliente</option>
                <option value="descartado">Descartado</option>
              </select>
              <i class="fas fa-chevron-down"></i>
            </div>
          </div>
          <div class="filter-group">
            <label class="filter-label"><i class="fas fa-calendar"></i> Fecha</label>
            <div class="input-container">
              <i class="fas fa-calendar-day"></i>
              <input 
                class="filter-input" 
                type="date" 
                v-model="filtroFecha" 
                @change="buscarHistorial" 
              />
            </div>
          </div>
          <div class="filter-group">
            <label class="filter-label"><i class="fas fa-signal"></i> Nivel digitalización</label>
            <div class="select-container">
              <select class="filter-select" v-model="filtroNivelDigital" @change="buscarHistorial">
                <option value="">Todos los niveles</option>
                <option value="1">Nada</option>
                <option value="2">Solo RS/WA</option>
                <option value="3">Solo Website</option>
                <option value="4">Combinación</option>
                <option value="5">Completo</option>
              </select>
              <i class="fas fa-chevron-down"></i>
            </div>
          </div>
        </div>
      </div>
      
      <div class="results-container">
        <div class="results-header">
          <h3>Resultados: {{ historialFiltrado.length }} seguimientos</h3>
          <div class="pagination-controls" v-if="totalPaginas > 1">
            <button class="page-btn" :disabled="paginaActual === 1" @click="paginaActual--">
              <i class="fas fa-chevron-left"></i>
            </button>
            <span class="page-info">Página {{ paginaActual }} de {{ totalPaginas }}</span>
            <button class="page-btn" :disabled="paginaActual === totalPaginas" @click="paginaActual++">
              <i class="fas fa-chevron-right"></i>
            </button>
          </div>
        </div>
        
        <div v-if="paginatedHistorial.length" class="timeline">
          <div v-for="item in paginatedHistorial" :key="item.seguimiento_id" class="timeline-item">
            <div class="timeline-date">
              <i class="fas fa-calendar-day"></i> {{ formatFecha(item.fecha) }}
            </div>
            
            <div class="timeline-content">
              <div class="timeline-header">
                <div class="timeline-badge" :class="tipoBadge(item.tipo)">
                  <i :class="iconoTipo(item.tipo)"></i> {{ tipoLabel(item.tipo) }}
                </div>
                
                <div class="timeline-status">
                  <div v-if="item.estado" class="status-badge" :class="badgeEstado(item.estado)">
                    {{ estadoLabel(item.estado) }}
                  </div>
                  <div v-if="item.nivel_digitalizacion !== null" class="level-badge">
                    <i class="fas fa-signal"></i> 
                    {{ nivelLabel(item.nivel_digitalizacion) }}
                  </div>
                </div>
              </div>
              
              <div class="timeline-body">
                <div class="timeline-org">
                  <i class="fas fa-building"></i>
                  <strong>{{ item.organizacion_nombre }}</strong>
                </div>
                
                <div class="timeline-comment">
                  <i class="fas fa-comment-alt"></i>
                  <p>{{ item.comentarios }}</p>
                </div>
              </div>
              
              <div class="timeline-footer">
                <div class="timeline-user">
                  <i class="fas fa-user-circle"></i>
                  <span>{{ item.usuario_nombre }}</span>
                </div>
                <div class="timeline-method">
                  <i :class="metodoIcon(item.metodo_contacto)"></i>
                  <span>{{ metodoLabel(item.metodo_contacto) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="no-results">
          <i class="fas fa-inbox"></i>
          <h4>No hay seguimientos para los filtros seleccionados</h4>
          <p>Intenta ajustar tus filtros o selecciona diferentes parámetros</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import generalApi from '@/api/endpoints/general'
import dayjs from 'dayjs'
import { useUsuariosStore } from '@/stores/usuarios'
const usuariosStore = useUsuariosStore()
const usuarioActual = JSON.parse(sessionStorage.getItem('user') || '{}')
const historial = ref([])
const filtroAgente = ref('')
const filtroEstado = ref('')
const filtroFecha = ref('')
const listaUsuarios = ref([])
const filtroNivelDigital = ref('')
const paginaActual = ref(1)
const elementosPorPagina = 8
const filtroEmpresa = ref('')
const filtroTipoOrg = ref('')
const listaOrganizaciones = ref([])

const esAdmin = usuarioActual.rol === 'admin'

const totalPaginas = computed(() =>
  Math.ceil(historialFiltrado.value.length / elementosPorPagina)
)

const paginatedHistorial = computed(() => {
  const start = (paginaActual.value - 1) * elementosPorPagina
  return historialFiltrado.value.slice(start, start + elementosPorPagina)
})

// Cargar historial al montar
onMounted(async () => {
  if (esAdmin) {
    const usuarios = await usuariosStore.getAllInfoUsr({});
    console.log('Respuesta getAllInfoUsr:', usuarios);
    // Agrega este log para ver si usuarios.data existe y qué contiene
    if (usuarios && usuarios.data) {
      console.log('usuarios.data:', usuarios.data);
    }
    listaUsuarios.value = Array.isArray(usuarios) ? usuarios : (usuarios.data || []);
    const res = await generalApi.getOrganizaciones();
    listaOrganizaciones.value = res.data.organizaciones || [];
    console.log('Usuarios:', listaUsuarios.value);
    console.log('Organizaciones:', listaOrganizaciones.value);
    await cargarHistorial();
  } else {
    await cargarHistorialPersonal();
  }
});

async function cargarHistorial() {
  let params = {};
  if (filtroTipoOrg.value) params.tipo = filtroTipoOrg.value;
  if (filtroAgente.value) params.usuario_id = filtroAgente.value;
  if (filtroEstado.value) params.estado = filtroEstado.value;
  if (filtroFecha.value) params.fecha = filtroFecha.value;
  if (filtroNivelDigital.value) params.nivel_digitalizacion = filtroNivelDigital.value;
  const res = await generalApi.getSeguimientos(params);
  historial.value = res.data.seguimientos || res.data || [];
  console.log('Seguimientos cargados:', historial.value); // <-- aquí
}

async function cargarHistorialPersonal() {
  const res = await generalApi.getSeguimientosPorUsuario(usuarioActual.usuario_id);
  historial.value = res.data.seguimientos || res.data || [];
  console.log('Seguimientos personales cargados:', historial.value); // <-- aquí
}
// Watchers para recargar historial al cambiar filtros
if (esAdmin) {
  watch([filtroTipoOrg, filtroAgente, filtroEstado, filtroFecha, filtroNivelDigital], () => {
    paginaActual.value = 1;
    cargarHistorial();
  });
}

// Watchers para recargar historial al cambiar filtros
if (esAdmin) {
  watch([filtroEmpresa, filtroAgente, filtroEstado, filtroFecha, filtroNivelDigital], () => {
    paginaActual.value = 1;
    cargarHistorial();
  });
} else {
  watch([filtroEstado, filtroFecha, filtroNivelDigital], () => {
    paginaActual.value = 1;
    cargarHistorialPersonal();
  });
}

// Filtros computados
const historialFiltrado = computed(() => {
  return historial.value.filter(item => {
    const coincideTipo = !filtroTipoOrg.value ||
      (item.organizacion_tipo && item.organizacion_tipo.replace(/\s/g, '_').toLowerCase() === filtroTipoOrg.value);
    // El filtro de agente ya lo hace el backend, así que siempre es true aquí:
    const coincideAgente = true;
    const coincideEstado = !filtroEstado.value || item.estado === filtroEstado.value
    const coincideFecha = !filtroFecha.value || dayjs(item.fecha).format('YYYY-MM-DD') === filtroFecha.value
    const coincideNivel = !filtroNivelDigital.value || String(item.nivel_digitalizacion) === String(filtroNivelDigital.value)
    return coincideTipo && coincideAgente && coincideEstado && coincideFecha && coincideNivel
  })
})

function buscarHistorial() {
  // Solo reactivo, no hace falta recargar
}

function formatFecha(fecha) {
  return dayjs(fecha).format('DD MMM YYYY')
}

function estadoLabel(estado) {
  if (!estado) return '';
  return estado.charAt(0).toUpperCase() + estado.slice(1).toLowerCase();
}

function tipoLabel(tipo) {
  if (tipo === 'prospeccion') return 'Primer contacto'
  if (tipo === 'seguimiento') return 'Seguimiento'
  if (tipo === 'cierre') return 'Cierre'
  return tipo
}

function iconoTipo(tipo) {
  if (tipo === 'prospeccion') return 'fas fa-handshake'
  if (tipo === 'seguimiento') return 'fas fa-sync-alt'
  if (tipo === 'cierre') return 'fas fa-flag-checkered'
  return 'fas fa-question-circle'
}

function tipoBadge(tipo) {
  if (tipo === 'prospeccion') return 'badge-prospeccion'
  if (tipo === 'seguimiento') return 'badge-seguimiento'
  if (tipo === 'cierre') return 'badge-cierre'
  return 'badge-default'
}

function badgeEstado(estado) {
  if (!estado) return 'badge-default';
  if (estado.toLowerCase() === 'cliente') return 'badge-cliente';
  if (estado.toLowerCase() === 'descartado') return 'badge-descartado';
  if (estado.toLowerCase() === 'prospecto') return 'badge-prospecto';
  return 'badge-default';
}

function nivelLabel(n) {
  return [
    'Sin información',
    'Nada',
    'Solo RS/WA',
    'Solo Website',
    'Combinación',
    'Completo'
  ][n] || 'Sin información'
}

function metodoLabel(metodo) {
  if (metodo === 'whatsapp') return 'WhatsApp'
  if (metodo === 'email') return 'Correo electrónico'
  if (metodo === 'llamada') return 'Llamada telefónica'
  if (metodo === 'visita') return 'Visita en persona'
  if (metodo === 'otro') return 'Otro método'
  return 'Sin especificar'
}

function metodoIcon(metodo) {
  if (metodo === 'whatsapp') return 'fab fa-whatsapp'
  if (metodo === 'email') return 'fas fa-envelope'
  if (metodo === 'llamada') return 'fas fa-phone-alt'
  if (metodo === 'visita') return 'fas fa-map-marker-alt'
  return 'fas fa-comments'
}
</script>

<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {
  --primary: #4361ee;
  --primary-dark: #3a0ca3;
  --secondary: #4cc9f0;
  --success: #2ecc71;
  --warning: #f39c12;
  --danger: #e74c3c;
  --light: #f8f9fa;
  --dark: #2c3e50;
  --gray: #718096;
  --light-gray: #e2e8f0;
  --border-radius: 16px;
  --box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  --transition: all 0.3s ease;
}
</style>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {
  --primary: #4361ee;
  --primary-dark: #3a0ca3;
  --secondary: #4cc9f0;
  --success: #2ecc71;
  --warning: #f39c12;
  --danger: #e74c3c;
  --light: #f8f9fa;
  --dark: #2c3e50;
  --gray: #718096;
  --light-gray: #e2e8f0;
  --border-radius: 16px;
  --box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  --transition: all 0.3s ease;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Poppins', sans-serif;
  background-color: #f5f7fa;
  color: var(--dark);
}

.main-container {
  margin-left: 80px;
  width: calc(100% - 80px) !important;
  padding: 30px;
  min-height: 100vh;
}

.header-section {
  margin-bottom: 30px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.header-text h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 10px;
  background: linear-gradient(to right, var(--primary), var(--primary-dark));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.header-text h1 i {
  margin-right: 15px;
}

.header-text p {
  font-size: 1.1rem;
  color: var(--gray);
  max-width: 700px;
  line-height: 1.6;
}

.btn-back {
  background: none;
  border: 2px solid var(--primary);
  color: var(--primary);
  border-radius: var(--border-radius);
  padding: 14px 25px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  transition: var(--transition);
}

.btn-back:hover {
  background: rgba(67, 97, 238, 0.05);
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.filters-card {
  background: #fff;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
  margin-bottom: 30px;
}

.filters-header {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 25px 30px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
}

.filters-header h3 {
  font-size: 1.6rem;
  font-weight: 600;
}

.filters-header i {
  font-size: 1.8rem;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 25px;
  padding: 30px;
}

.filter-group {
  margin-bottom: 15px;
}

.filter-label {
  display: block;
  margin-bottom: 12px;
  font-weight: 600;
  color: var(--dark);
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 10px;
}

.input-container, .select-container {
  position: relative;
  width: 100%;
}

.input-container i, .select-container i {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--gray);
  font-size: 1.1rem;
}

.filter-input, .filter-select {
  width: 100%;
  padding: 16px 20px 16px 50px;
  border: 2px solid var(--light-gray);
  border-radius: 12px;
  font-size: 1.1rem;
  transition: var(--transition);
  background: var(--light);
  font-family: 'Poppins', sans-serif;
}

.filter-input:focus, .filter-select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(67, 97, 238, 0.2);
}

.filter-select {
  appearance: none;
  padding-right: 50px;
}

.select-container i.fa-chevron-down {
  left: auto;
  right: 20px;
}

.results-container {
  background: #fff;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 30px;
  background: var(--light);
  border-bottom: 1px solid var(--light-gray);
}

.results-header h3 {
  font-size: 1.5rem;
  color: var(--dark);
  font-weight: 600;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.page-btn {
  background: #fff;
  border: 2px solid var(--primary);
  color: var(--primary);
  border-radius: 8px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition);
}

.page-btn:hover:not(:disabled) {
  background: rgba(67, 97, 238, 0.1);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-weight: 500;
  color: var(--gray);
}

.timeline {
  padding: 30px;
}

.timeline-item {
  position: relative;
  padding: 0 0 30px 30px;
  border-left: 2px solid var(--light-gray);
  margin-bottom: 30px;
}

.timeline-item:last-child {
  padding-bottom: 0;
  margin-bottom: 0;
  border-left: 2px solid transparent;
}

.timeline-item::before {
  content: '';
  position: absolute;
  left: -8px;
  top: 0;
  width: 14px;
  height: 14px;
  background: var(--primary);
  border-radius: 50%;
  z-index: 1;
}

.timeline-date {
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
}

.timeline-content {
  background: var(--light);
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.timeline-badge {
  padding: 10px 20px;
  border-radius: 30px;
  font-size: 1.1rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.badge-prospeccion {
  background: rgba(67, 97, 238, 0.1);
  color: var(--primary);
}

.badge-seguimiento {
  background: rgba(76, 201, 240, 0.1);
  color: var(--secondary);
}

.badge-cierre {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success);
}

.badge-default {
  background: rgba(114, 114, 114, 0.1);
  color: var(--dark);
}

.timeline-status {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.status-badge {
  padding: 8px 16px;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 600;
}

.badge-prospecto {
  background: rgba(243, 156, 18, 0.1);
  color: var(--warning);
}

.badge-cliente {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success);
}

.badge-descartado {
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger);
}

.level-badge {
  padding: 8px 16px;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 600;
  background: rgba(67, 97, 238, 0.1);
  color: var(--primary);
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.timeline-body {
  margin-bottom: 20px;
}

.timeline-org {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--dark);
}

.timeline-comment {
  display: flex;
  gap: 15px;
}

.timeline-comment i {
  color: var(--primary);
  font-size: 1.2rem;
  margin-top: 5px;
}

.timeline-comment p {
  line-height: 1.6;
  color: var(--dark);
}

.timeline-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 15px;
  border-top: 1px solid var(--light-gray);
}

.timeline-user, .timeline-method {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--gray);
  font-size: 1rem;
}

.timeline-method i {
  color: var(--primary);
}

.no-results {
  text-align: center;
  padding: 60px 30px;
  color: var(--gray);
}

.no-results i {
  font-size: 4rem;
  margin-bottom: 20px;
  color: var(--light-gray);
}

.no-results h4 {
  font-size: 1.8rem;
  margin-bottom: 15px;
  color: var(--dark);
}

@media (max-width: 1200px) {
  .main-container {
    margin-left: 70px;
  }
}

@media (max-width: 992px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 25px;
  }
  
  .results-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }
  
  .timeline-footer {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
}

@media (max-width: 768px) {
  .main-container {
    padding: 20px;
  }
  
  .filters-grid {
    grid-template-columns: 1fr;
  }
  
  .timeline-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 576px) {
  .main-container {
    padding: 15px;
    margin-left: 0;
  }
  
  .header-text h1 {
    font-size: 2rem;
  }
  
  .timeline-content {
    padding: 20px;
  }
}
</style>