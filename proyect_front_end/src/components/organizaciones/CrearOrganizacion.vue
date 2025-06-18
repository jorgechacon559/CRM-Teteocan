<template>
  <div class="main-content">
    <div class="header">
      <div>
        <h2>Crear organización</h2>
        <p>Registra una nueva empresa o negocio local en el sistema</p>
      </div>
      <div class="header-decoration">
        <div class="decoration-circle"></div>
        <div class="decoration-circle"></div>
        <div class="decoration-circle"></div>
      </div>
    </div>
    
    <div class="card-container">
      <div class="form-card">
        <!-- Selector de tipo de organización -->
        <div class="business-type">
          <h3 class="section-title"><i class="fas fa-store"></i> Tipo de Organización</h3>
          <div class="radio-group">
            <div class="radio-option" :class="{ active: form.tipo === 'empresa' }" @click="form.tipo = 'empresa'">
              <i class="fas fa-building"></i>
              <label for="empresa">Empresa</label>
            </div>
            <div class="radio-option" :class="{ active: form.tipo === 'negocio_local' }" @click="form.tipo = 'negocio_local'">
              <i class="fas fa-store-alt"></i>
              <label for="negocio_local">Negocio Local</label>
            </div>
          </div>
        </div>

        <form class="business-info" @submit.prevent="submitForm">
          <div class="form-section">
            <div class="form-title"><i class="fas fa-info-circle"></i> Información Básica</div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Nombre <span class="required">*</span></label>
                <div class="input-container">
                  <i class="fas fa-signature"></i>
                  <input class="form-input" v-model="form.nombre" required maxlength="255" placeholder="Nombre completo de la organización" />
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Ciudad <span class="required">*</span></label>
                <div class="input-container">
                  <i class="fas fa-city"></i>
                  <input class="form-input" v-model="form.ciudad" required maxlength="100" placeholder="Ciudad donde se ubica" />
                </div>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Estado <span class="required">*</span></label>
                <div class="input-container">
                  <i class="fas fa-map-marker-alt"></i>
                  <input class="form-input" v-model="form.ubicacion" required maxlength="100" placeholder="Ej. CDMX, Jalisco..." />
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Teléfono</label>
                <div class="input-container">
                  <i class="fas fa-phone-alt"></i>
                  <input class="form-input" v-model="form.telefono" maxlength="20" placeholder="(XXX) XXX-XXXX" />
                </div>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Dirección</label>
                <div class="input-container">
                  <i class="fas fa-map-marked-alt"></i>
                  <input class="form-input" v-model="form.direccion" maxlength="255" placeholder="Calle, número, colonia" />
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Código Postal</label>
                <div class="input-container">
                  <i class="fas fa-mail-bulk"></i>
                  <input class="form-input" v-model="form.codigo_postal" maxlength="10" placeholder="Código postal" />
                </div>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Email de contacto</label>
                <div class="input-container">
                  <i class="fas fa-envelope"></i>
                  <input class="form-input" v-model="form.email_contacto" type="email" maxlength="100" placeholder="contacto@organizacion.com" />
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Sitio web</label>
                <div class="input-container">
                  <i class="fas fa-globe"></i>
                  <input class="form-input" v-model="form.sitio_web" maxlength="255" placeholder="https://www.ejemplo.com" />
                </div>
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Notas</label>
                <div class="input-container">
                  <i class="fas fa-sticky-note"></i>
                  <input class="form-input" v-model="form.notas" maxlength="1000" placeholder="Información adicional relevante" />
                </div>
              </div>
            </div>
          </div>

          <!-- Campos dinámicos según tipo -->
          <div v-if="form.tipo === 'empresa'" class="form-section">
            <div class="form-title"><i class="fas fa-building"></i> Datos de Empresa</div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Sector <span class="required">*</span></label>
                <div class="input-container">
                  <i class="fas fa-industry"></i>
                  <input class="form-input" v-model="empresa.sector" required maxlength="100" placeholder="Sector empresarial" />
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Número de empleados</label>
                <div class="input-container">
                  <i class="fas fa-users"></i>
                  <input class="form-input" v-model.number="empresa.numero_empleados" type="number" min="1" placeholder="Cantidad de empleados" />
                </div>
              </div>
            </div>
          </div>
          <div v-else-if="form.tipo === 'negocio_local'" class="form-section">
            <div class="form-title"><i class="fas fa-store-alt"></i> Datos de Negocio Local</div>
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Categoría <span class="required">*</span></label>
                <div class="input-container">
                  <i class="fas fa-tags"></i>
                  <input class="form-input" v-model="negocio.categoria" required maxlength="100" placeholder="Ej. Cafetería, Restaurante..." />
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Horario apertura</label>
                <div class="input-container">
                  <i class="fas fa-door-open"></i>
                  <input class="form-input" v-model="negocio.horario_apertura" type="time" />
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">Horario cierre</label>
                <div class="input-container">
                  <i class="fas fa-door-closed"></i>
                  <input class="form-input" v-model="negocio.horario_cierre" type="time" />
                </div>
              </div>
            </div>
          </div>

          <div class="form-footer">
            <button class="btn btn-primary" type="submit">
              <i class="fas fa-save"></i> Guardar Organización
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
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import generalApi from '@/api/endpoints/general'

const form = ref({
  tipo: '',
  nombre: '',
  ciudad: '',
  ubicacion: '',
  telefono: '',
  direccion: '',
  codigo_postal: '',
  email_contacto: '',
  sitio_web: '',
  notas: ''
})

const empresa = ref({
  sector: '',
  numero_empleados: null
})

const negocio = ref({
  categoria: '',
  horario_apertura: '',
  horario_cierre: ''
})

const errorMsg = ref('')
const successMsg = ref('')

async function submitForm() {
  errorMsg.value = ''
  successMsg.value = ''
  // Validación básica
  if (!form.value.tipo || !form.value.nombre || !form.value.ciudad || !form.value.ubicacion) {
    errorMsg.value = 'Completa todos los campos obligatorios marcados con *'
    return
  }
  if (form.value.tipo === 'empresa' && !empresa.value.sector) {
    errorMsg.value = 'El sector es obligatorio para empresas'
    return
  }
  if (form.value.tipo === 'negocio_local' && !negocio.value.categoria) {
    errorMsg.value = 'La categoría es obligatoria para negocios locales'
    return
  }
  try {
    // 1. Crear organización principal
    const orgPayload = {
      ...form.value,
      sitio_web: form.value.sitio_web,
      sector: form.value.tipo === 'empresa' ? empresa.value.sector : null,
      categoria: form.value.tipo === 'negocio_local' ? negocio.value.categoria : null
    }
    const res = await generalApi.crearOrganizacion(orgPayload)
    const org = res.data.organizacion || res.data

    successMsg.value = '¡Organización creada con éxito!'
    // Limpia el formulario
    form.value = {
      tipo: '',
      nombre: '',
      ciudad: '',
      ubicacion: '',
      telefono: '',
      direccion: '',
      codigo_postal: '',
      email_contacto: '',
      sitio_web: '',
      notas: ''
    }
    empresa.value = { sector: '', numero_empleados: null }
    negocio.value = { categoria: '', horario_apertura: '', horario_cierre: '' }
    
    // Animación de éxito
    document.querySelector('.form-card').classList.add('success-animation')
    setTimeout(() => {
      document.querySelector('.form-card').classList.remove('success-animation')
    }, 2000)
  } catch (e) {
    errorMsg.value = e?.response?.data?.mensaje || 'Error al crear organización'
  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

:root {
  --primary-color: #2c3e50;
  --secondary-color: #3498db;
  --accent-color: #1abc9c;
  --light-gray: #f5f7fa;
  --medium-gray: #e2e8f0;
  --dark-gray: #718096;
  --white: #ffffff;
  --purple: #9b59b6;
  --dark-blue: #2980b9;
  --gold: #f1c40f;
  --red: #e74c3c;
}

.main-content {
  margin-left: 80px;
  width: calc(100% - 80px) !important;
  background: linear-gradient(135deg, #f0f4ff 0%, #f8f9ff 100%);
  min-height: 100vh;
  transition: all 0.3s ease;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  position: relative;
}

.header h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary-color);
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--dark-blue) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
}

.header p {
  color: var(--dark-gray);
  font-size: 1.2rem;
  margin-top: 10px;
  max-width: 600px;
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

.card-container {
  max-width: 900px;
  margin: 0 auto;
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.form-card {
  background: var(--white);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}

.form-card:hover {
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
}

.form-card.success-animation {
  animation: successPulse 2s;
}

@keyframes successPulse {
  0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.3); }
  50% { box-shadow: 0 0 0 15px rgba(34, 197, 94, 0); }
  100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
}

.business-type {
  background: linear-gradient(135deg, var(--secondary-color), var(--dark-blue));
  color: white;
  padding: 30px;
  position: relative;
  overflow: hidden;
}

.business-type::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  z-index: -1;
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.section-title {
  font-size: 1.6rem;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 15px;
  font-weight: 600;
}

.radio-group {
  display: flex;
  gap: 30px;
  margin-bottom: 10px;
}

.radio-option {
  display: flex;
  align-items: center;
  gap: 15px;
  cursor: pointer;
  padding: 15px 25px;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.15);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.radio-option:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-5px);
}

.radio-option.active {
  background: rgba(26, 188, 156, 0.4);
  border-color: var(--white);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.radio-option i {
  font-size: 1.8rem;
}

.radio-option label {
  font-size: 1.2rem;
  cursor: pointer;
  font-weight: 500;
}

.business-info {
  padding: 35px 30px;
}

.form-section {
  margin-bottom: 35px;
  padding-bottom: 25px;
  border-bottom: 1px solid var(--medium-gray);
}

.form-section:last-child {
  border-bottom: none;
}

.form-title {
  font-size: 1.4rem;
  color: var(--primary-color);
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
}

.form-title i {
  color: var(--accent-color);
  font-size: 1.3rem;
}

.form-row {
  display: flex;
  gap: 25px;
  margin-bottom: 25px;
}

.form-group {
  flex: 1;
}

.form-label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: var(--primary-color);
  display: flex;
  align-items: center;
  gap: 8px;
}

.required {
  color: var(--red);
  font-size: 1.2rem;
}

.input-container {
  position: relative;
}

.input-container i {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--dark-gray);
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.form-input {
  width: 75%;
  padding: 16px 20px 16px 50px;
  border: 2px solid var(--medium-gray);
  border-radius: 12px;
  font-size: 1.05rem;
  transition: all 0.3s ease;
  background: var(--light-gray);
  color: var(--primary-color);
}

.form-input:focus {
  outline: none;
  border-color: var(--accent-color);
  box-shadow: 0 0 0 4px rgba(26, 188, 156, 0.15);
  background: var(--white);
}

.form-input:focus + i {
  color: var(--accent-color);
  transform: translateY(-50%) scale(1.2);
}

.form-footer {
  padding: 20px 0 10px 0;
  display: flex;
  justify-content: center;
}

.btn-primary {
  background: linear-gradient(135deg, var(--accent-color), #16a085);
  color: var(--white);
  border: none;
  border-radius: 15px;
  padding: 16px 35px;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 5px 15px rgba(26, 188, 156, 0.3);
}

.btn-primary:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(26, 188, 156, 0.4);
}

.btn-primary:active {
  transform: translateY(-2px);
}

.error-msg {
  background: rgba(229, 62, 62, 0.1);
  color: var(--red);
  padding: 15px 20px;
  border-radius: 12px;
  margin-top: 25px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
  border-left: 4px solid var(--red);
  animation: shake 0.5s;
}

.success-msg {
  background: rgba(46, 204, 113, 0.1);
  color: #2ecc71;
  padding: 15px 20px;
  border-radius: 12px;
  margin-top: 25px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
  border-left: 4px solid #2ecc71;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-8px); }
  40%, 80% { transform: translateX(8px); }
}

/* Responsive design */
@media (max-width: 992px) {
  .main-content { 
    padding: 25px 20px 25px 90px; 
  }
  .card-container { 
    max-width: 100%; 
  }
  .radio-group {
    gap: 15px;
  }
  .radio-option {
    padding: 12px 15px;
  }
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  
  .header-decoration {
    position: absolute;
    top: 10px;
    right: 20px;
  }
  
  .form-row { 
    flex-direction: column; 
    gap: 20px; 
  }
  
  .main-content { 
    padding: 20px 15px; 
  }
  
  .business-type {
    padding: 25px 20px;
  }
  
  .section-title {
    font-size: 1.4rem;
  }
  
  .radio-option {
    flex: 1;
    justify-content: center;
  }
}

@media (max-width: 576px) {
  .main-content { 
    padding: 15px 10px; 
  }
  
  .business-type {
    padding: 20px 15px;
  }
  
  .business-info {
    padding: 25px 20px;
  }
  
  .radio-group {
    flex-direction: column;
    gap: 15px;
  }
  
  .form-title {
    font-size: 1.3rem;
  }
  
  .btn-primary {
    width: 100%;
    justify-content: center;
  }
}
</style>