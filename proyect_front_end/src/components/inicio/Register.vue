<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useMessageStore } from '@/stores/message'

const messageStore = useMessageStore()
const router = useRouter()
const name = ref('')
const apellido = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const errorMsg = ref('')
const successMsg = ref('')
const emailError = ref(false)
const passwordError = ref(false)
const authStore = useAuthStore()

const minLength = computed(() => password.value.length >= 8)
const hasUpper = computed(() => /[A-Z]/.test(password.value))
const hasLower = computed(() => /[a-z]/.test(password.value))
const hasNumber = computed(() => /\d/.test(password.value))
const hasSymbol = computed(() => /[!@#$%^&*()_\-+=\[\]{};':"\\|,.<>/?`~]/.test(password.value))

const passwordStrength = computed(() => {
  let score = 0
  if (minLength.value) score++
  if (hasUpper.value) score++
  if (hasLower.value) score++
  if (hasNumber.value) score++
  if (hasSymbol.value) score++
  if (password.value.length >= 16 && hasSymbol.value && hasUpper.value && hasLower.value && hasNumber.value) score++
  return score
})

const strengthLabel = computed(() => {
  switch (passwordStrength.value) {
    case 0: case 1: return 'Débil'
    case 2: return 'Regular'
    case 3: return 'Fuerte'
    case 4: return 'Muy fuerte'
    case 5: return 'Excelente'
    case 6: return 'Irrompible'
    default: return ''
  }
})

const barColor = computed(() => {
  switch (passwordStrength.value) {
    case 0: case 1: return '#e53e3e'
    case 2: return '#f59e42'
    case 3: return '#fbbf24'
    case 4: return '#22c55e'
    case 5: return '#15803d'
    case 6: return '#065f46'
    default: return '#e5e7eb'
  }
})

const canRegister = computed(() =>
  minLength.value && hasUpper.value && hasLower.value && hasNumber.value && hasSymbol.value && password.value === password2.value
)

async function register() {
  errorMsg.value = ''
  successMsg.value = ''
  emailError.value = false
  passwordError.value = false

  if (!canRegister.value) {
    errorMsg.value = "La contraseña no cumple los requisitos o no coincide."
    passwordError.value = true
    return
  }
  try {
    const response = await authStore.register(name.value, apellido.value, email.value, password.value);
    const res = response.data

    if (
      res?.usuario ||
      res?.mensaje?.toLowerCase().includes('éxito') ||
      res?.mensaje?.toLowerCase().includes('exito')
    ) {
      messageStore.setMessage('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
      router.push({ path: '/login' })
    } else if (res?.mensaje?.toLowerCase().includes('existe')) {
      errorMsg.value = "El correo ya está registrado"
      emailError.value = true
    } else {
      errorMsg.value = "Error al registrar. Verifica tus datos."
    }
  } catch (error) {
    const msg =
      error?.response?.data?.msg ||
      error?.response?.data?.message ||
      error?.response?.data?.mensaje ||
      error?.message ||
      '';
    if (msg.toLowerCase().includes('correo') || msg.toLowerCase().includes('existe')) {
      errorMsg.value = "El correo ya está registrado";
      emailError.value = true;
    } else {
      errorMsg.value = "Error al registrar. Verifica tus datos.";
    }
  }
}
</script>

<template>
  <div class="register-container">
    <!-- Panel izquierdo optimizado -->
    <div class="register-left">
      <div class="logo">
        <i class="fas fa-gem logo-icon"></i>
        <span class="logo-text">Teteocan Technologies</span>
      </div>
      <h2>¡Regístrate ahora!</h2>
      <p>Accede a la plataforma profesional para el seguimiento y gestión de clientes. Crea tu cuenta y comienza a potenciar tu desarrollo comercial.</p>
      
      <div class="features">
        <div class="feature-item">
          <i class="fas fa-user-plus feature-icon"></i>
          <span>Registro rápido y seguro</span>
        </div>
        <div class="feature-item">
          <i class="fas fa-shield-alt feature-icon"></i>
          <span>Tus datos están protegidos</span>
        </div>
        <div class="feature-item">
          <i class="fas fa-chart-line feature-icon"></i>
          <span>Herramientas avanzadas de CRM</span>
        </div>
      </div>
    </div>

    <!-- Panel derecho: Formulario optimizado -->
    <div class="register-right">
      <form class="register-form" @submit.prevent="register">
        <h2 class="form-title">Crear cuenta</h2>
        <p class="form-subtitle">Completa tus datos para comenzar</p>
        
        <div v-if="errorMsg" class="error-msg">
          <i class="fas fa-exclamation-circle"></i>
          {{ errorMsg }}
        </div>
        <div v-if="successMsg" class="success-msg">
          <i class="fas fa-check-circle"></i>
          {{ successMsg }}
        </div>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label" for="name">
              <i class="fas fa-user"></i> Nombre
            </label>
            <div class="input-container">
              <input
                type="text"
                id="name"
                v-model="name"
                placeholder="Tu nombre"
                class="form-input"
                required
              />
              <i class="fas fa-user input-icon"></i>
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-label" for="apellido">
              <i class="fas fa-user"></i> Apellido
            </label>
            <div class="input-container">
              <input
                type="text"
                id="apellido"
                v-model="apellido"
                placeholder="Apellido"
                class="form-input"
                required
              />
              <i class="fas fa-user input-icon"></i>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label" for="email">
            <i class="fas fa-envelope"></i> Correo Electrónico
          </label>
          <div class="input-container">
            <input
              type="email"
              id="email"
              v-model="email"
              placeholder="Tu correo electrónico"
              :class="['form-input', { 'input-error': emailError }]"
              required
            />
            <i class="fas fa-envelope input-icon"></i>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label" for="password">
            <i class="fas fa-lock"></i> Contraseña
          </label>
          <div class="input-container">
            <input
              type="password"
              id="password"
              v-model="password"
              placeholder="Crea una contraseña"
              :class="['form-input', { 'input-error': passwordError }]"
              required
              autocomplete="new-password"
            />
            <i class="fas fa-lock input-icon"></i>
          </div>
          
          <div class="password-strength">
            <div class="strength-title">Requisitos de contraseña:</div>
            <div class="strength-rules">
              <div class="rule-item">
                <i :class="['fas', minLength ? 'fa-check-circle valid' : 'fa-circle rule-icon']"></i>
                <span>Mínimo 8 caracteres</span>
              </div>
              <div class="rule-item">
                <i :class="['fas', hasUpper ? 'fa-check-circle valid' : 'fa-circle rule-icon']"></i>
                <span>Una mayúscula</span>
              </div>
              <div class="rule-item">
                <i :class="['fas', hasLower ? 'fa-check-circle valid' : 'fa-circle rule-icon']"></i>
                <span>Una minúscula</span>
              </div>
              <div class="rule-item">
                <i :class="['fas', hasNumber ? 'fa-check-circle valid' : 'fa-circle rule-icon']"></i>
                <span>Un número</span>
              </div>
              <div class="rule-item">
                <i :class="['fas', hasSymbol ? 'fa-check-circle valid' : 'fa-circle rule-icon']"></i>
                <span>Un símbolo especial</span>
              </div>
            </div>
            
            <div class="bar-container">
              <div class="bar">
                <div
                  class="bar-fill"
                  :style="{
                    width: (passwordStrength * 16.66) + '%',
                    background: barColor
                  }"
                ></div>
              </div>
              <span class="label" :style="{ color: barColor }">{{ strengthLabel }}</span>
            </div>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label" for="password2">
            <i class="fas fa-lock"></i> Confirmar contraseña
          </label>
          <div class="input-container">
            <input
              type="password"
              id="password2"
              v-model="password2"
              placeholder="Confirma tu contraseña"
              :class="['form-input', { 'input-error': password2 && password !== password2 }]"
              required
              autocomplete="new-password"
            />
            <i class="fas fa-lock input-icon"></i>
          </div>
          <div v-if="password2 && password !== password2" class="password-mismatch">
            <i class="fas fa-exclamation-circle"></i>
            Las contraseñas no coinciden.
          </div>
        </div>

        <button type="submit" class="btn btn-primary" :disabled="!canRegister">
          <i class="fas fa-user-plus"></i> Registrarse
        </button>
        
        <div class="register-switch">
          ¿Ya tienes una cuenta?
          <button class="btn-link" type="button" @click="$router.push('/login')">Iniciar sesión</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style>
:root {
  --primary-gradient: linear-gradient(135deg, #6a11cb, #2575fc);
  --secondary-gradient: linear-gradient(to right, #6a11cb, #2575fc);
  --error-color: #e53e3e;
  --success-color: #2ecc71;
  --input-bg: #f8f9ff;
  --input-border: #e0e7ff;
  --text-primary: #2d3748;
  --text-secondary: #4a5568;
  --shadow-primary: 0 20px 50px rgba(37, 99, 235, 0.15);
  --shadow-secondary: 0 8px 32px rgba(37, 99, 235, 0.08);
  --border-radius: 24px;
}
</style>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

:root {
  --primary-gradient: linear-gradient(135deg, #6a11cb, #2575fc);
  --secondary-gradient: linear-gradient(to right, #6a11cb, #2575fc);
  --error-color: #e53e3e;
  --success-color: #2ecc71;
  --input-bg: #f8f9ff;
  --input-border: #e0e7ff;
  --text-primary: #2d3748;
  --text-secondary: #4a5568;
  --shadow-primary: 0 20px 50px rgba(37, 99, 235, 0.15);
  --shadow-secondary: 0 8px 32px rgba(37, 99, 235, 0.08);
  --border-radius: 24px;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Poppins', sans-serif;
  background-color: #f7f8fa;
}

.register-container {
  display: flex;
  width: 100%;
  max-width: 1200px;
  min-height: 80vh;
  margin: 2rem auto;
  background: #fff;
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: var(--shadow-primary);
}

.register-left {
  flex: 1.2;
  background: var(--primary-gradient);
  color: #fff;
  padding: 50px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.register-left::before {
  content: "";
  position: absolute;
  top: -50px;
  right: -50px;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.register-left::after {
  content: "";
  position: absolute;
  bottom: -80px;
  left: -80px;
  width: 250px;
  height: 250px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
}

.logo {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 40px;
  position: relative;
  z-index: 2;
}

.logo-icon {
  font-size: 2.8rem;
  color: #1abc9c;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.logo-text {
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.register-left h2 {
  font-size: 2.4rem;
  margin-bottom: 20px;
  position: relative;
  z-index: 2;
  line-height: 1.3;
}

.register-left p {
  font-size: 1.15rem;
  margin-bottom: 30px;
  opacity: 0.9;
  position: relative;
  z-index: 2;
  line-height: 1.6;
}

.features {
  margin-top: 40px;
  position: relative;
  z-index: 2;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  padding: 10px 15px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(4px);
  transition: transform 0.3s ease;
}

.feature-item:hover {
  transform: translateX(5px);
}

.feature-icon {
  font-size: 1.5rem;
  color: #1abc9c;
  background: rgba(26, 188, 156, 0.2);
  border-radius: 50%;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.register-right {
  flex: 1;
  padding: 50px 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f7f8fa;
}

.register-form {
  width: 100%;
  max-width: 480px;
  background: #fff;
  padding: 2.8rem 2.5rem;
  border-radius: 1.8rem;
  box-shadow: var(--shadow-secondary);
  display: flex;
  flex-direction: column;
  gap: 1.8rem;
}

.form-title {
  text-align: center;
  color: #6a11cb;
  font-weight: 700;
  margin-bottom: 0.5rem;
  font-size: 2.2rem;
  letter-spacing: -1px;
}

.form-subtitle {
  color: var(--text-secondary);
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.05rem;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 28px;
  position: relative;
  flex: 1;
}

.form-label {
  display: block;
  margin-bottom: 10px;
  color: #6a11cb;
  font-weight: 500;
  font-size: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.input-container {
  position: relative;
}

.form-input {
  width: 100%;
  padding: 16px 20px 16px 50px;
  border: 2px solid var(--input-border);
  border-radius: 14px;
  font-size: 16px;
  background-color: var(--input-bg);
  color: var(--text-primary);
  transition: all 0.3s ease;
  font-family: 'Poppins', sans-serif;
}

.form-input:focus {
  outline: none;
  border-color: #6a11cb;
  box-shadow: 0 0 0 4px rgba(106, 17, 203, 0.15);
  background-color: #ffffff;
}

.input-icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  color: #718096;
  font-size: 18px;
  transition: color 0.3s ease;
  pointer-events: none;
}

.form-input:focus + .input-icon {
  color: #6a11cb;
}

.input-error {
  border-color: var(--error-color) !important;
  background: rgba(229, 62, 62, 0.05) !important;
}

.input-error + .input-icon {
  color: var(--error-color) !important;
}

.btn {
  padding: 18px;
  border-radius: 14px;
  font-size: 17px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border: none;
  width: 100%;
  font-family: 'Poppins', sans-serif;
}

.btn-primary {
  background: var(--secondary-gradient);
  color: white;
  box-shadow: 0 5px 18px rgba(106, 17, 203, 0.25);
  position: relative;
  overflow: hidden;
}

.btn-primary::after {
  content: "";
  position: absolute;
  top: -50%;
  left: -60%;
  width: 20px;
  height: 200%;
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(25deg);
  transition: all 0.6s;
}

.btn-primary:hover:enabled::after {
  left: 140%;
}

.btn-primary:disabled {
  background: #cbd5e0;
  color: #718096;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-primary:hover:enabled {
  transform: translateY(-3px);
  box-shadow: 0 8px 22px rgba(106, 17, 203, 0.35);
}

.btn-link {
  background: none;
  color: #6a11cb;
  border: none;
  font-weight: 600;
  cursor: pointer;
  margin-left: 5px;
  font-size: 1rem;
  padding: 0;
  transition: all 0.3s ease;
  position: relative;
}

.btn-link::after {
  content: "";
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: #6a11cb;
  transition: width 0.3s ease;
}

.btn-link:hover::after {
  width: 100%;
}

.register-switch {
  margin-top: 25px;
  text-align: center;
  font-size: 16px;
  color: var(--text-secondary);
}

.error-msg {
  background: rgba(229, 62, 62, 0.1);
  color: var(--error-color);
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 25px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 12px;
  border-left: 4px solid var(--error-color);
  animation: fadeIn 0.4s;
}

.success-msg {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success-color);
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 25px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 12px;
  border-left: 4px solid var(--success-color);
  animation: fadeIn 0.4s;
}

.password-strength {
  margin-top: 18px;
  background: #f8f9ff;
  border-radius: 12px;
  padding: 22px;
  border: 2px solid var(--input-border);
}

.strength-title {
  font-size: 15px;
  margin-bottom: 18px;
  color: var(--text-secondary);
  font-weight: 500;
}

.strength-rules {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 24px;
}

.rule-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  color: var(--text-secondary);
}

.rule-icon {
  font-size: 14px;
  color: #cbd5e0;
  transition: all 0.3s ease;
}

.valid {
  color: var(--success-color) !important;
}

.bar-container {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-top: 14px;
}

.bar {
  height: 10px;
  border-radius: 5px;
  transition: all 0.5s ease;
  flex-grow: 1;
  background: #e2e8f0;
  overflow: hidden;
  position: relative;
}

.bar-fill {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 0%;
  transition: width 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.label {
  font-size: 15px;
  font-weight: 600;
  min-width: 100px;
  text-align: right;
}

.password-mismatch {
  color: var(--error-color);
  font-size: 15px;
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive Design */
@media (max-width: 1100px) {
  .register-container {
    max-width: 95%;
  }
}

@media (max-width: 992px) {
  .register-container {
    flex-direction: column;
    max-width: 700px;
    min-height: unset;
  }
  
  .register-left, .register-right {
    padding: 40px 30px;
  }
  
  .register-left {
    text-align: center;
    padding: 50px 30px;
  }
  
  .feature-item {
    justify-content: center;
    max-width: 400px;
    margin: 0 auto 20px;
  }
  
  .register-form {
    max-width: 100%;
    padding: 2.5rem 2rem;
  }
  
  .form-row {
    flex-direction: column;
    gap: 0;
  }
}

@media (max-width: 600px) {
  .register-container {
    border-radius: 0;
    min-height: 100vh;
    margin: 0;
    box-shadow: none;
  }
  
  .register-form {
    padding: 1.8rem 1.5rem;
    border-radius: 1.2rem;
  }
  
  .logo {
    margin-bottom: 30px;
  }
  
  .logo-text {
    font-size: 1.7rem;
  }
  
  .register-left h2 {
    font-size: 2rem;
  }
  
  .form-title {
    font-size: 1.9rem;
  }
  
  .strength-rules {
    grid-template-columns: 1fr;
  }
  
  .password-strength {
    padding: 18px;
  }
  
  .btn {
    padding: 17px;
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .register-left, .register-right {
    padding: 35px 20px;
  }
  
  .register-form {
    padding: 1.5rem 1.2rem;
  }
  
  .form-input {
    padding: 14px 16px 14px 45px;
  }
  
  .input-icon {
    left: 15px;
  }
}
</style>