<template>
  <Toast :show="showToast" :message="toastMsg" :type="toastType" />
  <div class="auth-container">
    <div class="auth-left">
      <div class="logo">
        <i class="fas fa-chart-line logo-icon"></i>
        <span class="logo-text">Teteocan Technologies</span>
      </div>
      <h2>Desarrollo comercial</h2>
      <p>Plataforma profesional para el seguimiento y gestión de clientes. Accede a herramientas avanzadas para optimizar tus procesos comerciales.</p>
      <div class="features">
        <div class="feature-item">
          <i class="fas fa-search-location feature-icon"></i>
          <span>Seguimiento avanzado de prospectos</span>
        </div>
        <div class="feature-item">
          <i class="fas fa-chart-pie feature-icon"></i>
          <span>Reportes y análisis en tiempo real</span>
        </div>
        <div class="feature-item">
          <i class="fas fa-lock feature-icon"></i>
          <span>Protección de datos de nivel empresarial</span>
        </div>
      </div>
    </div>
    <!-- Panel derecho -->
    <div class="auth-right">
      <form class="login-form" @submit.prevent="login">
        <h2 class="form-title">Iniciar sesión</h2>
        <p class="form-subtitle">Ingresa tus credenciales para acceder a tu cuenta</p>
        <div v-if="errorMsg" class="error-msg">
          <i class="fas fa-exclamation-circle"></i>
          {{ errorMsg }}
        </div>
        <div class="form-group">
          <label class="form-label" for="email"><i class="fas fa-envelope"></i> Correo Electrónico</label>
          <input
            type="email"
            id="email"
            v-model="correo"
            placeholder="Tu correo electrónico"
            required
            :class="['form-input', { 'input-error': inputError }]"
          />
        </div>
        <div class="form-group">
          <label class="form-label" for="password"><i class="fas fa-lock"></i> Contraseña</label>
          <div class="password-container">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="password"
              placeholder="Tu contraseña"
              required
              :class="['form-input', { 'input-error': inputError }]"
            />
            <span class="toggle-password" @click="showPassword = !showPassword">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </span>
          </div>
        </div>
        <button type="submit" class="btn btn-primary">
          <i class="fas fa-sign-in-alt"></i> Ingresar
        </button>
        <div class="switch-form">
          ¿No tienes cuenta?
          <button type="button" class="btn-link" @click="$router.push('/register')">Regístrate ahora</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Toast from '@/components/Toast.vue'
import { useMessageStore } from '@/stores/message'

const messageStore = useMessageStore()
const showToast = ref(false)
const toastMsg = ref('')
const toastType = ref('success')

function mostrarToast(msg, tipo = 'success') {
  toastMsg.value = msg
  toastType.value = tipo
  showToast.value = true
  setTimeout(() => showToast.value = false, 3000)
}

onMounted(() => {
  if (messageStore.msg) {
    mostrarToast(messageStore.msg, messageStore.type)
    messageStore.clearMessage()
  }
})

const correo = ref('')
const password = ref('')
const errorMsg = ref('')
const authStore = useAuthStore()
const inputError = ref(false)
const showPassword = ref(false)

async function login() {
  errorMsg.value = ''
  inputError.value = false
  try {
    await authStore.login(correo.value, password.value)
  } catch (error) {
    errorMsg.value = 'Correo o contraseña incorrectos'
    inputError.value = true
  }
}
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.auth-container {
  display: flex;
  width: 100%;
  max-width: 1100px;
  min-height: 80vh;
  margin: 2rem auto;
  background: #fff;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(37, 99, 235, 0.15);
}
.auth-left {
  flex: 1;
  background: linear-gradient(135deg, #2563eb, #1e40af);
  color: #fff;
  padding: 50px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.logo {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 40px;
}
.logo-icon {
  font-size: 2.5rem;
  color: #1abc9c;
}
.logo-text {
  font-size: 1.8rem;
  font-weight: 700;
}
.auth-left h2 {
  font-size: 2.2rem;
  margin-bottom: 20px;
}
.auth-left p {
  font-size: 1.1rem;
  margin-bottom: 30px;
  opacity: 0.9;
}
.features {
  margin-top: 40px;
}
.feature-item {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}
.feature-icon {
  font-size: 1.3rem;
  color: #1abc9c;
  background: rgba(26, 188, 156, 0.2);
  border-radius: 50%;
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.auth-right {
  flex: 1;
  padding: 50px 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7f8fa;
}
.login-form {
  width: 100%;
  max-width: 400px;
  background: #fff;
  padding: 2.5rem 2rem;
  border-radius: 1.5rem;
  box-shadow: 0 8px 32px rgba(37,99,235,0.08);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.form-title {
  text-align: center;
  color: #2563eb;
  font-weight: 700;
  margin-bottom: 0.5rem;
  font-size: 2rem;
  letter-spacing: -1px;
}
.form-subtitle {
  color: #718096;
  text-align: center;
  margin-bottom: 1rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.form-label {
  color: #2563eb;
  font-weight: 600;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}
.form-input {
  width: 100%;
  box-sizing: border-box;
  padding: 0.9rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.7rem;
  font-size: 1rem;
  background-color: #f7f8fa;
  color: #222;
  transition: border 0.2s;
}
.form-input:focus {
  border-color: #1abc9c;
  outline: none;
  background: #fff;
}
.input-error {
  border-color: #d32f2f !important;
  background: #fff0f0 !important;
}
.password-container {
  position: relative;
}
.toggle-password {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #718096;
}
.btn {
  padding: 0.9rem 1.5rem;
  border-radius: 0.7rem;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  border: none;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: background 0.2s, color 0.2s, border 0.2s;
}
.btn-primary {
  background: #2563eb;
  color: #fff;
}
.btn-primary:hover {
  background: #1e40af;
}
.btn-link {
  background: none;
  color: #1abc9c;
  border: none;
  font-weight: 600;
  cursor: pointer;
  margin-left: 5px;
  font-size: 1rem;
  padding: 0;
}
.switch-form {
  text-align: center;
  margin-top: 1rem;
  color: #444;
  font-size: 0.98rem;
}
.error-msg {
  background: rgba(229, 62, 62, 0.1);
  color: #d32f2f;
  padding: 12px 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid rgba(229, 62, 62, 0.3);
  font-size: 1rem;
}
@media (max-width: 992px) {
  .auth-container {
    flex-direction: column;
    max-width: 600px;
    min-height: unset;
  }
  .auth-left, .auth-right {
    padding: 40px 20px;
  }
  .auth-left {
    text-align: center;
  }
  .feature-item {
    justify-content: center;
  }
}
@media (max-width: 576px) {
  .auth-container {
    border-radius: 0;
    min-height: 100vh;
  }
  .login-form {
    padding: 1.2rem 0.5rem;
    max-width: 98vw;
  }
}
</style>