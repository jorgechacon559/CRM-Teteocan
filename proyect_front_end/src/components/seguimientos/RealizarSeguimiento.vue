<template>
  <div class="main-container">
    <div class="header-container">
      <div class="header-content">
        <h1 class="page-title">Realizar seguimiento</h1>
        <p class="page-description">
          Gestiona el proceso completo desde la prospección hasta el seguimiento de clientes con herramientas avanzadas.
        </p>
      </div>
      <div class="header-decoration">
        <div class="decoration-circle"></div>
        <div class="decoration-circle"></div>
        <div class="decoration-circle"></div>
      </div>
    </div>
    <div class="content-wrapper">
      <div class="search-section">
        <div class="search-card">
          <div class="search-header">
            <i class="fas fa-search-location icon-primary"></i>
            <h3>Seleccionar organización</h3>
          </div>
          <div class="search-controls">
            <div class="radio-group">
              <div class="radio-option">
                <input type="radio" id="empresa" value="empresa" v-model="tipoBusqueda" class="custom-radio" />
                <label for="empresa" class="radio-label">
                  <i class="fas fa-building"></i> Empresa
                </label>
              </div>
              <div class="radio-option">
                <input type="radio" id="negocio_local" value="negocio_local" v-model="tipoBusqueda" class="custom-radio" />
                <label for="negocio_local" class="radio-label">
                  <i class="fas fa-store"></i> Negocio Local
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="results-section">
        <div class="results-container">
        <div class="results-group">
          <div class="results-header">
            <i class="fas fa-unlock icon-disponible"></i>
            <h4>Disponibles</h4>
          </div>
<div v-if="paginadasDisponibles.length" class="results-grid">
  <div
    v-for="org in paginadasDisponibles"
    :key="org.organizacion_id"
    class="result-card"
    @click="seleccionarOrganizacion(org)"
    :class="{ selected: org.organizacion_id === seleccionada?.organizacion_id }"
  >
    <div class="org-name">{{ org.nombre }}</div>
    <div v-if="org.masivo" class="badge badge-masivo">
      Contactado por correo masivo
    </div>
    <div v-if="org.prospecto_id && org.prospecto_id !== usuarioActual.usuario_id" class="badge badge-asignada">
      Asignada a {{ org.asignado_nombre || 'otro agente' }}
    </div>
    <div v-else class="badge badge-disponible">
      Disponible
    </div>
  </div>
</div>
<div v-else class="no-results">
  <i class="fas fa-info-circle"></i> No hay organizaciones disponibles
</div>
<div v-if="totalPaginasDisponibles > 1" class="pagination-compact">
  <button
    class="pagination-control"
    :disabled="paginaDisponibles === 1"
    @click="paginaDisponibles = 1"
    aria-label="Primera página"
  >
    <i class="fas fa-angle-double-left"></i>
  </button>
  <button
    class="pagination-control"
    :disabled="paginaDisponibles === 1"
    @click="paginaDisponibles--"
    aria-label="Página anterior"
  >
    <i class="fas fa-angle-left"></i>
  </button>
  <button
    v-for="n in paginasVisibles(paginaDisponibles, totalPaginasDisponibles)"
    :key="n"
    :class="['pagination-item', { active: paginaDisponibles === n, dots: n === '...' }]"
    @click="typeof n === 'number' && (paginaDisponibles = n)"
    :disabled="n === '...'"
  >{{ n }}</button>
  <button
    class="pagination-control"
    :disabled="paginaDisponibles === totalPaginasDisponibles"
    @click="paginaDisponibles++"
    aria-label="Página siguiente"
  >
    <i class="fas fa-angle-right"></i>
  </button>
  <button
    class="pagination-control"
    :disabled="paginaDisponibles === totalPaginasDisponibles"
    @click="paginaDisponibles = totalPaginasDisponibles"
    aria-label="Última página"
  >
    <i class="fas fa-angle-double-right"></i>
  </button>
</div>

        </div>
          <div class="results-group">
            <div class="results-header">
              <i class="fas fa-user-check icon-asignada"></i>
              <h4>Asignadas a ti</h4>
            </div>
<div v-if="paginadasAsignadas.length" class="results-grid">
  <div
    v-for="org in paginadasAsignadas"
    :key="org.organizacion_id"
    class="result-card"
    @click="seleccionarOrganizacion(org)"
    :class="{ selected: org.organizacion_id === seleccionada?.organizacion_id }"
  >
    <div class="org-name">{{ org.nombre }}</div>
    <div v-if="org.masivo" class="badge badge-masivo">
      Contactado por correo masivo
    </div>
    <div class="badge badge-asignada">Asignada</div>
    <div class="badge" :class="badgeEstado(org.estado_organizacion)">
      {{ org.estado_organizacion }}
    </div>
  </div>
</div>
<div v-else class="no-results">
  <i class="fas fa-info-circle"></i> No tienes prospectos asignados
</div>
<div v-if="totalPaginasAsignadas > 1" class="pagination-compact">
  <button
    class="pagination-control"
    :disabled="paginaAsignadas === 1"
    @click="paginaAsignadas = 1"
    aria-label="Primera página"
  >
    <i class="fas fa-angle-double-left"></i>
  </button>
  <button
    class="pagination-control"
    :disabled="paginaAsignadas === 1"
    @click="paginaAsignadas--"
    aria-label="Página anterior"
  >
    <i class="fas fa-angle-left"></i>
  </button>
  <button
    v-for="n in paginasVisibles(paginaAsignadas, totalPaginasAsignadas)"
    :key="n"
    :class="['pagination-item', { active: paginaAsignadas === n, dots: n === '...' }]"
    @click="typeof n === 'number' && (paginaAsignadas = n)"
    :disabled="n === '...'"
  >{{ n }}</button>
  <button
    class="pagination-control"
    :disabled="paginaAsignadas === totalPaginasAsignadas"
    @click="paginaAsignadas++"
    aria-label="Página siguiente"
  >
    <i class="fas fa-angle-right"></i>
  </button>
  <button
    class="pagination-control"
    :disabled="paginaAsignadas === totalPaginasAsignadas"
    @click="paginaAsignadas = totalPaginasAsignadas"
    aria-label="Última página"
  >
    <i class="fas fa-angle-double-right"></i>
  </button>
</div>
          </div>
        </div>
      </div>
      <div class="detail-section" v-if="seleccionada">
        <div class="detail-card">
          <div class="org-header">
            <div class="org-info">
              <h2 class="org-name">{{ seleccionada.nombre }}</h2>
              <div class="org-meta">
                <div class="meta-item">
                  <i class="fas fa-phone"></i>
                  <span>{{ seleccionada.telefono || 'Sin teléfono' }}</span>
                </div>
                <div class="meta-item">
                  <i class="fas fa-envelope"></i>
                  <span>{{ seleccionada.email_contacto || 'Sin email' }}</span>
                </div>
              </div>
<div class="meta-item" v-if="seleccionada.sitio_web">
  <i class="fas fa-globe"></i>
  <template v-if="seleccionada.sitio_web !== 'Sin sitio web'">
    <a
      :href="formateaSitioWeb(seleccionada.sitio_web)"
      target="_blank"
      style="color:inherit;text-decoration:underline;"
    >
      {{ seleccionada.sitio_web }}
    </a>
  </template>
  <template v-else>
    {{ seleccionada.sitio_web }}
  </template>
</div>
            </div>
            <div class="org-status">
              <div class="level-badges">
                <span
                  class="level-pill"
                  :class="'level-' + (seleccionada.nivel_digitalizacion || 0)"
                >
                  <i :class="nivelIcon(seleccionada.nivel_digitalizacion)"></i>
                  Nivel {{ seleccionada.nivel_digitalizacion || 0 }}
                </span>
                <span
                  class="estado-pill"
                  :class="'estado-' + (seleccionada.estado_organizacion || 'prospecto')"
                >
                  {{ seleccionada.estado_organizacion }}
                </span>
              </div>
            </div>
          </div>
          <div class="org-content">
            <div class="org-tabs">
              <button class="tab-btn" :class="{ active: activeTab === 'edicion' }" @click="activeTab = 'edicion'">
                <i class="fas fa-edit"></i> Editar datos
              </button>
              <button class="tab-btn" :class="{ active: activeTab === 'seguimiento' }" @click="activeTab = 'seguimiento'">
                <i class="fas fa-tasks"></i> Registrar seguimiento
              </button>
            </div>
            <div class="tab-content">
              <!-- Edición de datos -->
              <div v-if="activeTab === 'edicion' && esAsignado" class="edit-form">
                <h3 class="form-title"><i class="fas fa-edit"></i> Editar datos generales</h3>
                <div class="form-grid">
                  <div class="form-group">
                    <label class="form-label">Teléfono</label>
                    <input class="form-input" v-model="seleccionada.telefono" maxlength="20" />
                  </div>
                  <div class="form-group">
                    <label class="form-label">Dirección</label>
                    <input class="form-input" v-model="seleccionada.direccion" maxlength="255" />
                  </div>
                  <div class="form-group">
                    <label class="form-label">Email</label>
                    <input class="form-input" v-model="seleccionada.email_contacto" maxlength="100" />
                  </div>
                  <div class="form-group">
                    <label class="form-label">Sitio web</label>
                    <input class="form-input" v-model="seleccionada.sitio_web" maxlength="255" placeholder="https://www.ejemplo.com" />
                  </div>
                  <div class="form-actions">
                    <button class="btn btn-outline" @click="guardarEdicion">
                      <i class="fas fa-save"></i> Guardar cambios
                    </button>
                  </div>
                </div>
              </div>
              <div v-else-if="activeTab === 'edicion'" class="not-assigned">
                <i class="fas fa-user-lock"></i>
                <p>Solo el agente asignado puede editar estos datos</p>
              </div>
              <!-- Formulario de seguimiento -->
              <div v-if="activeTab === 'seguimiento'" class="followup-form">
                <h3 class="form-title"><i class="fas fa-tasks"></i> Registrar seguimiento</h3>
                <form @submit.prevent="registrarSeguimiento">
                  <div class="form-grid">
                    <div class="form-group">
                      <label class="form-label">Tipo de seguimiento</label>
                      <div class="form-input" style="background:#f8f9fa;">{{ tipoLabel(seleccionada?.prospecto_id ? 'seguimiento' : 'prospeccion') }}</div>
                    </div>
                    <div class="form-group">
                      <label class="form-label">Método de contacto <span class="required">*</span></label>
                      <select class="form-select" v-model="seguimiento.metodo_contacto" required>
                        <option value="">Selecciona...</option>
                        <option value="whatsapp">WhatsApp</option>
                        <option value="email">Correo electrónico</option>
                        <option value="llamada">Llamada telefónica</option>
                        <option value="otro">Otro</option>
                      </select>
                    </div>
                    <div class="form-group">
                      <label class="form-label">Fecha</label>
                      <input class="form-input" type="date" v-model="seguimiento.fecha" />
                    </div>
                    <div class="form-group">
                      <label class="form-label">Estado <span class="required">*</span></label>
                      <select class="form-select" v-model="seguimiento.estadoVisual">
                        <option value="">Sin cambio</option>
                        <option value="prospecto">Prospecto</option>
                        <option value="contactado">Contactado</option>
                        <option value="no_responde">No responde</option>
                        <option value="interesado">Interesado</option>
                        <option value="cliente">Cliente</option>
                        <option value="descartado">Descartado</option>
                      </select>
                    </div>
                    <div
                      class="form-group"
                      v-if="!seleccionada.prospecto_id && seleccionada.estado_organizacion === 'prospecto'"
                    >
                      <label class="form-label">Nivel de digitalización <span class="required">*</span></label>
                      <div class="nivel-btn-group">
                        <button
                          v-for="n in 5"
                          :key="n"
                          type="button"
                          :class="['nivel-btn', 'level-' + n, { active: seguimiento.nivel_digitalizacion == n }]"
                          @click="seguimiento.nivel_digitalizacion = n"
                        >
                          <i :class="nivelIcon(n)"></i>
                          {{ nivelLabel(n) }} (Nivel {{ n }})
                        </button>
                      </div>
                    </div>
                    <div class="form-group" v-else>
                      <label class="form-label">Nivel de digitalización</label>
                      <div class="digital-pill active" style="pointer-events:none;">
                        <i :class="nivelIcon(seleccionada.nivel_digitalizacion)"></i>
                        {{ nivelLabel(seleccionada.nivel_digitalizacion) }}
                      </div>
                    </div>
                    <div class="form-group full-width">
                      <label class="form-label">Comentarios <span class="required">*</span></label>
                      <textarea class="comments-input" v-model="seguimiento.comentarios" required maxlength="1000" placeholder="Detalla la interacción..." />
                    </div>
                  </div>
                  <div class="form-actions">
                    <button class="btn btn-primary" type="submit">
                      <i class="fas fa-paper-plane"></i> Guardar seguimiento
                    </button>
                  </div>
                  <div v-if="errorMsg" class="error-msg">
                    <i class="fas fa-exclamation-circle"></i> {{ errorMsg }}
                  </div>
                  <div v-if="successMsg" class="success-msg">
                    <i class="fas fa-check-circle"></i> {{ successMsg }}
                  </div>
                </form>
              </div>
              <!-- Historial de interacciones -->
              <div v-if="activeTab === 'historial'" class="history-section">
                <h3 class="form-title"><i class="fas fa-history"></i> Historial de Interacciones</h3>
                <div class="timeline">
                  <div v-for="item in historial" :key="item.seguimiento_id" class="timeline-item">
                    <div class="timeline-badge" :class="tipoBadge(item.tipo)">
                      <i :class="tipoIcon(item.tipo)"></i>
                    </div>
                    <div class="timeline-content">
                      <div class="timeline-header">
                        <div class="timeline-date">{{ formatFecha(item.fecha) }}</div>
                        <div class="timeline-meta">
                          <div class="timeline-user">
                            <i class="fas fa-user"></i> {{ item.usuario_nombre }}
                          </div>
                          <div class="timeline-method">
                            <i class="fas fa-comments"></i> {{ item.metodo_contacto }}
                          </div>
                        </div>
                      </div>
                      <div class="timeline-body">
                        {{ item.comentarios }}
                      </div>
                      <div class="form-group">
                        <label class="form-label">Nivel digitalización</label>
                        <div class="digital-pill active" style="pointer-events:none;">
                          <i :class="nivelIcon(item.nivel_digitalizacion)"></i>
                          {{ nivelLabel(item.nivel_digitalizacion) }}
                        </div>
                      </div>
                      </div>
                  </div>
                  <div v-if="!historial.length" class="no-history">
                    <i class="fas fa-inbox"></i>
                    <p>No hay historial de interacciones aún</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import generalApi from '@/api/endpoints/general'
import dayjs from 'dayjs'

const tipoBusqueda = ref('empresa')
const organizacionesDisponibles = ref([])
const organizacionesAsignadas = ref([])
const seleccionada = ref(null)
const historial = ref([])
const seguimiento = ref({
  tipo: '',
  metodo_contacto: '',
  fecha: dayjs().format('YYYY-MM-DD'),
  comentarios: '',
  estado: '',
  estadoVisual: '',
  nivel_digitalizacion: ''
})
const errorMsg = ref('')
const successMsg = ref('')
const activeTab = ref('seguimiento')

// Simula obtener el usuario actual desde sessionStorage
const usuarioActual = JSON.parse(sessionStorage.getItem('user') || '{}')
const esAsignado = computed(() =>
  seleccionada.value && seleccionada.value.prospecto_id === usuarioActual.usuario_id
)

onMounted(() => {
  cargarOrganizaciones()
})

watch(tipoBusqueda, () => {
  cargarOrganizaciones()
  paginaAsignadas.value = 1
  paginaDisponibles.value = 1
})

async function cargarOrganizaciones() {
  seleccionada.value = null
  historial.value = []
  paginaDisponibles.value = 1
  paginaAsignadas.value = 1
  if (usuarioActual.rol === 'admin') {
    const res = await generalApi.getOrganizaciones({ tipo: tipoBusqueda.value })
    const todas = res.data.organizaciones || []
    // Asignadas a mí
    organizacionesAsignadas.value = todas.filter(
      org => org.prospecto_id === usuarioActual.usuario_id
    )
    // Disponibles: las que no están asignadas a mí
    organizacionesDisponibles.value = todas.filter(
      org => org.prospecto_id !== usuarioActual.usuario_id
    )
  }
}

const elementosPorPagina = 20
const paginaDisponibles = ref(1)
const paginaAsignadas = ref(1)

const totalPaginasDisponibles = computed(() =>
  Math.ceil(organizacionesDisponibles.value.length / elementosPorPagina)
)
const totalPaginasAsignadas = computed(() =>
  Math.ceil(organizacionesAsignadas.value.length / elementosPorPagina)
)

const paginadasDisponibles = computed(() => {
  const start = (paginaDisponibles.value - 1) * elementosPorPagina
  return organizacionesDisponibles.value.slice(start, start + elementosPorPagina)
})
const paginadasAsignadas = computed(() => {
  const start = (paginaAsignadas.value - 1) * elementosPorPagina
  return organizacionesAsignadas.value.slice(start, start + elementosPorPagina)
})

// Seleccionar organización y cargar historial
async function seleccionarOrganizacion(org) {
  seleccionada.value = { ...org }
  errorMsg.value = ''
  successMsg.value = ''
  activeTab.value = 'seguimiento'
  // Cargar historial de seguimientos
  try {
    const res = await generalApi.getSeguimientos({ organizacion_id: org.organizacion_id })
    historial.value = res.data || []
  } catch {
    historial.value = []
  }
}

// Guardar edición de datos básicos
async function guardarEdicion() {
  try {
    await generalApi.editarOrganizacion(seleccionada.value.organizacion_id, {
      telefono: seleccionada.value.telefono,
      direccion: seleccionada.value.direccion,
      email_contacto: seleccionada.value.email_contacto,
      sitio_web: seleccionada.value.sitio_web
    })
    successMsg.value = 'Datos actualizados correctamente'
    setTimeout(() => (successMsg.value = ''), 3000)
  } catch {
    errorMsg.value = 'Error al guardar los cambios'
  }
}

function mapEstado(visual) {
  if (visual === 'cliente') return 'cliente'
  if (visual === 'descartado') return 'descartado'
  // Todo lo demás es prospecto
  return 'prospecto'
}

// Registrar seguimiento
async function registrarSeguimiento() {
  errorMsg.value = ''
  successMsg.value = ''
  seguimiento.value.tipo = seleccionada.value?.prospecto_id ? 'seguimiento' : 'prospeccion'

  if (
    !seguimiento.value.tipo ||
    !seguimiento.value.metodo_contacto ||
    !seguimiento.value.comentarios ||
    (!seleccionada.value.prospecto_id && seleccionada.value.estado_organizacion === 'prospecto' && !seguimiento.value.nivel_digitalizacion)
  ) {
    errorMsg.value = 'Por favor complete todos los campos obligatorios'
    return
  }
  try {
    await generalApi.crearSeguimiento({
      organizacion_id: seleccionada.value.organizacion_id,
      tipo: seguimiento.value.tipo,
      metodo_contacto: seguimiento.value.metodo_contacto,
      fecha: seguimiento.value.fecha,
      comentarios: seguimiento.value.comentarios,
      estado: seguimiento.value.estadoVisual ? mapEstado(seguimiento.value.estadoVisual) : undefined,
      nivel_digitalizacion: seguimiento.value.nivel_digitalizacion || undefined
    })
    successMsg.value = 'Seguimiento registrado exitosamente'
    await seleccionarOrganizacion(seleccionada.value)
    await cargarOrganizaciones()
    // Limpia el formulario
    seguimiento.value = {
      tipo: '',
      metodo_contacto: '',
      fecha: dayjs().format('YYYY-MM-DD'),
      comentarios: '',
      estado: '',
      estadoVisual: '',
      nivel_digitalizacion: ''
    }
    setTimeout(() => (successMsg.value = ''), 3000)
  } catch (e) {
    errorMsg.value = e?.response?.data?.mensaje || 'Error al registrar el seguimiento'
  }
}


// Utilidades visuales
function badgeEstado(estado) {
  if (estado === 'cliente') return 'badge-cliente'
  if (estado === 'descartado') return 'badge-descartado'
  return 'badge-prospecto'
}

function tipoLabel(tipo) {
  if (tipo === 'prospeccion') return 'Primer contacto'
  if (tipo === 'seguimiento') return 'Seguimiento'
  if (tipo === 'cierre') return 'Cierre'
  return tipo
}

function tipoIcon(tipo) {
  if (tipo === 'prospeccion') return 'fas fa-handshake'
  if (tipo === 'seguimiento') return 'fas fa-sync-alt'
  if (tipo === 'cierre') return 'fas fa-check-circle'
  return 'fas fa-comment'
}

function tipoBadge(tipo) {
  if (tipo === 'prospeccion') return 'badge-prospeccion'
  if (tipo === 'seguimiento') return 'badge-seguimiento'
  if (tipo === 'cierre') return 'badge-cierre'
  return ''
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

function formatFecha(fecha) {
  return dayjs(fecha).format('DD MMM YYYY, HH:mm')
}

function nivelIcon(n) {
  switch (n) {
    case 1: return 'fas fa-ban'
    case 2: return 'fab fa-whatsapp'
    case 3: return 'fas fa-globe'
    case 4: return 'fas fa-link'
    case 5: return 'fas fa-check-circle'
    default: return 'fas fa-question'
  }
}

function paginasVisibles(paginaActual, totalPaginas) {
  const paginas = []
  if (totalPaginas <= 7) {
    for (let i = 1; i <= totalPaginas; i++) paginas.push(i)
  } else {
    if (paginaActual <= 4) {
      paginas.push(1, 2, 3, 4, 5, '...', totalPaginas)
    } else if (paginaActual >= totalPaginas - 3) {
      paginas.push(1, '...', totalPaginas - 4, totalPaginas - 3, totalPaginas - 2, totalPaginas - 1, totalPaginas)
    } else {
      paginas.push(1, '...', paginaActual - 1, paginaActual, paginaActual + 1, '...', totalPaginas)
    }
  }
  return paginas
}

function formateaSitioWeb(url) {
  if (!url) return ''
  if (/^https?:\/\//i.test(url)) return url
  return 'https://' + url
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

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  position: relative;
}

.header-content {
  max-width: 900px;
}

.header-decoration {
  display: flex;
  gap: 15px;
}

.decoration-circle {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--accent-color);
  opacity: 0.7;
  animation: float 3s ease-in-out infinite;
}

.decoration-circle:nth-child(2) {
  background: var(--secondary-color);
  animation-delay: 0.5s;
}

.decoration-circle:nth-child(3) {
  background: var(--purple);
  animation-delay: 1s;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--dark);
  margin-bottom: 10px;
  background: linear-gradient(to right, var(--primary), var(--primary-dark));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.page-description {
  font-size: 1.1rem;
  color: var(--gray);
  max-width: 700px;
  line-height: 1.6;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.search-section {
  margin-bottom: 30px;
}

.search-card {
  background: #fff;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
  padding: 25px;
}

.search-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
}

.search-header h3 {
  font-size: 1.5rem;
  color: var(--dark);
  font-weight: 600;
}

.icon-primary {
  font-size: 1.8rem;
  color: var(--primary);
  background: rgba(67, 97, 238, 0.1);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-controls {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.radio-group {
  display: flex;
  gap: 25px;
}

.radio-option {
  display: flex;
  align-items: center;
}

.custom-radio {
  width: 20px;
  height: 20px;
  accent-color: var(--primary);
  cursor: pointer;
  margin-right: 10px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  font-weight: 500;
  color: var(--dark);
  transition: var(--transition);
}

.radio-label:hover {
  color: var(--primary);
}


.search-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--gray);
  font-size: 1.1rem;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(67, 97, 238, 0.2);
}

.results-section {
  margin-bottom: 30px;
}

.results-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 25px;
}

.results-group {
  background: #fff;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
}

.results-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 25px;
  background: var(--light);
  border-bottom: 1px solid var(--light-gray);
}

.results-header h4 {
  font-size: 1.2rem;
  color: var(--dark);
  font-weight: 600;
}

.icon-disponible {
  color: var(--primary);
  font-size: 1.2rem;
}

.icon-asignada {
  color: var(--success);
  font-size: 1.2rem;
}

.results-grid {
  padding: 15px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
  max-height: 400px;
  overflow-y: auto;
}

.result-card {
  background: var(--light);
  border-radius: 12px;
  padding: 10px 12px;
  cursor: pointer;
  transition: var(--transition);
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-height: 48px;
}

.result-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border-color: var(--primary);
}

.result-card.selected {
  background: rgba(67, 97, 238, 0.05);
  border-color: var(--primary);
}

.org-name {
  font-weight: 600;
  font-size: 1rem;
  color: var(--dark);
  margin-bottom: 2px;
}

.badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: none;
}

.badge-disponible { 
  background: rgba(67, 97, 238, 0.1); 
  color: var(--primary);
  align-self: flex-start;
}

.badge-asignada { 
  background: rgba(46, 204, 113, 0.1); 
  color: var(--success);
  align-self: flex-start;
  text-transform: capitalize;
}

.badge-prospecto { 
  background: rgba(243, 156, 18, 0.15); 
  color: #b45309;
  text-transform: capitalize;
  align-self: flex-start;
}

.badge-cliente { 
  background: rgba(46, 204, 113, 0.1); 
  color: var(--success);
  align-self: flex-start;
  text-transform: capitalize;
}

.badge-descartado { 
  background: rgba(231, 76, 60, 0.1); 
  color: var(--danger);
  align-self: flex-start;
  text-transform: capitalize;
}

.no-results {
  padding: 30px 20px;
  text-align: center;
  color: var(--gray);
  font-size: 1.1rem;
}

.no-results i {
  font-size: 2rem;
  margin-bottom: 15px;
  display: block;
  color: var(--light-gray);
}

.detail-section {
  margin-top: 30px;
}

.detail-card {
  background: #fff;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
}

.org-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px;
  background: linear-gradient(135deg, var(--success), var(--secondary));
  color: white;
}

.org-info {
  flex: 1;
}

.org-name {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 15px;
}

.org-meta {
  display: flex;
  gap: 25px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
}

.org-status {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 15px;
}

.digital-level {
  background: rgba(255, 255, 255, 0.1);
  padding: 10px 15px;
  border-radius: 30px;
  font-size: 1.1rem;
  font-weight: 600;
  text-align: center;
  min-width: 180px;
}

.level-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  margin-top: 8px;
  overflow: hidden;
}

.level-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.level-0 .level-fill { background: #95a5a6; width: 0%; }
.level-1 .level-fill { background: #e74c3c; width: 20%; }
.level-2 .level-fill { background: #f39c12; width: 40%; }
.level-3 .level-fill { background: #f1c40f; width: 60%; }
.level-4 .level-fill { background: #2ecc71; width: 80%; }
.level-5 .level-fill { background: #3498db; width: 100%; }

.status-badge {
  padding: 8px 20px;
  border-radius: 30px;
  font-size: 1.1rem;
  font-weight: 600;
}

.status-prospecto { background-color: #fef3c7; color: #b45309; }
.status-cliente { background-color: #d1fae5; color: #065f46; }
.status-descartado { background-color: #fee2e2; color: #b91c1c; }

.org-content {
  padding: 30px;
}

.org-tabs {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  border-bottom: 2px solid var(--light-gray);
  padding-bottom: 15px;
}

.tab-btn {
  background: none;
  border: none;
  padding: 12px 25px;
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--gray);
  cursor: pointer;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: var(--transition);
}

.tab-btn:hover {
  background: rgba(67, 97, 238, 0.05);
  color: var(--primary);
}

.tab-btn.active {
  background: var(--primary);
  color: white;
}

.tab-content {
  padding: 20px 0;
}

.form-title {
  font-size: 1.5rem;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 15px;
  color: var(--dark);
}

.form-title i {
  color: var(--primary);
  background: rgba(67, 97, 238, 0.1);
  width: 45px;
  height: 45px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 25px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group.full-width {
  grid-column: span 2;
}

.form-label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: var(--dark);
  font-size: 1.1rem;
}

.required {
  color: var(--danger);
}

.form-input, .form-select, .comments-input {
  width: 100%;
  padding: 16px 20px;
  border: 2px solid var(--light-gray);
  border-radius: 12px;
  font-size: 1.1rem;
  transition: var(--transition);
  background: var(--light);
  font-family: 'Poppins', sans-serif;
}

.form-input:focus, .form-select:focus, .comments-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(67, 97, 238, 0.2);
}

.comments-input {
  min-height: 120px;
  resize: vertical;
}

.form-actions {
  grid-column: span 2;
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}

.btn {
  padding: 16px 35px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  align-items: center;
  gap: 12px;
  border: none;
  font-family: 'Poppins', sans-serif;
}

.btn-primary {
  background: linear-gradient(to right, var(--primary), var(--primary-dark));
  color: white;
  box-shadow: 0 5px 20px rgba(67, 97, 238, 0.3);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(67, 97, 238, 0.4);
}

.btn-outline {
  background: transparent;
  border: 2px solid var(--primary);
  color: var(--primary);
}

.btn-outline:hover {
  background: var(--primary);
  color: white;
}

.error-msg, .success-msg {
  padding: 16px 20px;
  border-radius: 12px;
  margin-top: 25px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 12px;
}

.error-msg {
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger);
  border-left: 4px solid var(--danger);
}

.success-msg {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success);
  border-left: 4px solid var(--success);
}

.timeline {
  position: relative;
  padding-left: 30px;
  border-left: 2px solid var(--light-gray);
}

.timeline-item {
  position: relative;
  margin-bottom: 35px;
  padding-left: 30px;
}

.timeline-badge {
  position: absolute;
  left: -40px;
  top: 0;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.badge-prospeccion { background: linear-gradient(135deg, #4361ee, #3a0ca3); }
.badge-seguimiento { background: linear-gradient(135deg, #4cc9f0, #4895ef); }
.badge-cierre { background: linear-gradient(135deg, #2ecc71, #1d9b5c); }
.badge-masivo {
  background: #e0e7ff;
  color: #3b82f6;
  align-self: flex-start;
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
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--light-gray);
}

.timeline-date {
  font-weight: 600;
  color: var(--primary);
  font-size: 1.1rem;
}

.timeline-meta {
  display: flex;
  gap: 20px;
  color: var(--gray);
  font-size: 0.95rem;
}

.timeline-user, .timeline-method {
  display: flex;
  align-items: center;
  gap: 8px;
}

.timeline-body {
  margin-bottom: 15px;
  line-height: 1.6;
}

.timeline-footer {
  display: flex;
  gap: 15px;
  padding-top: 15px;
  border-top: 1px solid var(--light-gray);
}

.timeline-status, .timeline-level {
  display: flex;
  align-items: center;
  gap: 8px;
}

.timeline-status span, .timeline-level span {
  color: var(--gray);
  font-size: 0.95rem;
}

.no-history {
  text-align: center;
  padding: 40px 20px;
  color: var(--gray);
}

.no-history i {
  font-size: 3rem;
  margin-bottom: 20px;
  display: block;
  color: var(--light-gray);
}

.not-assigned {
  text-align: center;
  padding: 50px 20px;
  color: var(--gray);
}

.not-assigned i {
  font-size: 3rem;
  margin-bottom: 20px;
  display: block;
  color: var(--light-gray);
}

@media (max-width: 1200px) {
  .main-container {
    margin-left: 80px;
  }
}

@media (max-width: 992px) {
  .results-container {
    grid-template-columns: 1fr;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-group.full-width {
    grid-column: span 1;
  }
}

@media (max-width: 768px) {
  .main-container {
    padding: 20px;
  }
  
  .org-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 25px;
  }
  
  .org-status {
    align-items: flex-start;
    width: 100%;
  }
  
  .org-tabs {
    flex-wrap: wrap;
  }
  
  .form-actions {
    justify-content: center;
  }
}

@media (max-width: 576px) {
  .main-container {
    margin-left: 80px;
  }
  
  .radio-group {
    flex-direction: column;
    gap: 15px;
  }
  
  .results-grid {
    grid-template-columns: 1fr;
  }
  
  .timeline-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}

.digital-pill-group {
  display: flex;
  gap: 8px;
  margin-top: 8px;
  flex-wrap: wrap;
}

.digital-pill {
  border: 2px solid var(--primary);
  background: white;
  color: var(--primary);
  border-radius: 999px;
  padding: 8px 18px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: none;
  outline: none;
}

.digital-pill.active,
.digital-pill:hover {
  background: linear-gradient(to right, var(--primary), var(--primary-dark));
  color: #fff;
  border-color: var(--primary-dark);
}

.digital-pill i {
  font-size: 1.1em;
}

.level-badges {
  display: flex;
  gap: 12px;
  margin-bottom: 10px;
}

.level-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 22px;
  border-radius: 18px;
  font-weight: 700;
  font-size: 1.05rem;
  background: #f5f7fa;
  color: #333;
}

.level-1 { background: #e74c3c; color: #fff; }
.level-2 { background: #1abc9c; color: #fff; }
.level-3 { background: #f1c40f; color: #222; }
.level-4 { background: #2ecc71; color: #fff; }
.level-5 { background: #3498db; color: #fff; }
.level-0 { background: #95a5a6; color: #fff; }

.estado-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 22px;
  border-radius: 18px;
  font-weight: 700;
  font-size: 1.05rem;
  background: #f5f7fa;
  color: #b45309;
  text-transform: capitalize;
}

.estado-prospecto { background: #f39c12; color: #fff; }
.estado-cliente { background: #2ecc71; color: #fff; }
.estado-descartado { background: #e74c3c; color: #fff; }

/* Botones de selección de nivel */
.nivel-btn-group {
  display: flex;
  gap: 16px;
  margin-top: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin: 18px 0 0 0;
}

.pagination button {
  background: #fff;
  color: #3a0ca3;
  border: 1.5px solid #3a0ca3;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.pagination button.active,
.pagination button:hover:not(:disabled) {
  background: linear-gradient(135deg, #4361ee, #3a0ca3);
  color: #fff;
}

.pagination button:disabled {
  background: #e2e8f0;
  color: #b0b0b0;
  cursor: not-allowed;
}

.pagination-compact {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  margin: 18px 0 0 0;
  flex-wrap: wrap;
}

.pagination-item,
.pagination-control {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 38px;
  height: 38px;
  border-radius: 10px;
  font-size: 1.05rem;
  font-weight: 500;
  cursor: pointer;
  background: #fff;
  color: #3a0ca3;
  border: 1.5px solid #3a0ca3;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(67, 97, 238, 0.06);
  margin: 0 1px;
  outline: none;
}

.pagination-item.active {
  background: linear-gradient(135deg, #4361ee, #3a0ca3);
  color: #fff;
  font-weight: 700;
  border-color: #3a0ca3;
  box-shadow: 0 0 10px #3a0ca333;
  transform: scale(1.08);
}

.pagination-item.dots {
  background: transparent;
  color: #b0b0b0;
  border: none;
  cursor: default;
  font-size: 1.2rem;
  width: auto;
  min-width: 18px;
}

.pagination-control:disabled,
.pagination-item:disabled {
  background: #e2e8f0;
  color: #b0b0b0;
  cursor: not-allowed;
  border-color: #e2e8f0;
}

.pagination-control:hover:not(:disabled),
.pagination-item:hover:not(.active):not(:disabled):not(.dots) {
  background: #f3f0ff;
  color: #3a0ca3;
  box-shadow: 0 2px 8px #3a0ca322;
}

.nivel-btn {
  border: 2px solid #e2e8f0;
  background: #fff;
  color: #222;
  border-radius: 14px;
  padding: 18px 28px;
  font-size: 1.08rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(44, 62, 80, 0.04);
}

.nivel-btn.level-1 { border-color: #e74c3c; }
.nivel-btn.level-2 { border-color: #1abc9c; }
.nivel-btn.level-3 { border-color: #f1c40f; }
.nivel-btn.level-4 { border-color: #2ecc71; }
.nivel-btn.level-5 { border-color: #3498db; }

.nivel-btn.active,
.nivel-btn:hover {
  color: #fff;
}

.nivel-btn.active.level-1,
.nivel-btn.level-1:hover { background: #e74c3c; }
.nivel-btn.active.level-2,
.nivel-btn.level-2:hover { background: #1abc9c; }
.nivel-btn.active.level-3,
.nivel-btn.level-3:hover { background: #f1c40f; color: #222; }
.nivel-btn.active.level-4,
.nivel-btn.level-4:hover { background: #2ecc71; }
.nivel-btn.active.level-5,
.nivel-btn.level-5:hover { background: #3498db; }
</style>