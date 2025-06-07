<template>
  <div class="home-bg">
    <div class="home-container">
      <div class="welcome-section">
        <div class="crown">
          <i class="fas fa-crown"></i>
        </div>
        <h1 class="main-title">
          ¡Bienvenido{{ userName ? ', ' + userName : '' }}!
        </h1>
        <p class="subtitle">
          Plataforma de gestión comercial <span class="brand">Teteocan</span>
        </p>
        <p class="description">
          Lleva el control de tus organizaciones, prospectos y clientes con la máxima elegancia y eficiencia.<br>
          <span class="highlight">¡Tú eres el protagonista de tu éxito!</span>
        </p>
      </div>

      <div class="quick-guide">
        <h2><i class="fas fa-magic"></i> ¿Cómo empezar?</h2>
        <div class="steps">
          <div class="step">
            <div class="icon"><i class="fas fa-building"></i></div>
            <div class="step-content">
              <h3>1. Crea una organización</h3>
              <p>Registra empresas o negocios locales desde el menú lateral.</p>
            </div>
          </div>
          <div class="step">
            <div class="icon"><i class="fas fa-search-location"></i></div>
            <div class="step-content">
              <h3>2. Realiza seguimientos</h3>
              <p>Haz contacto, registra avances y gana prospectos automáticamente.</p>
            </div>
          </div>
          <div class="step">
            <div class="icon"><i class="fas fa-history"></i></div>
            <div class="step-content">
              <h3>3. Consulta historial</h3>
              <p>Visualiza el historial de interacciones y el avance de cada organización.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="home-footer">
        <div class="quote">
          <i class="fas fa-quote-left"></i>
          <span>
            La excelencia no es un acto, es un hábito. <b>¡Hazlo con estilo!</b>
          </span>
        </div>
        <div class="brand-logo">
          <i class="fas fa-gem"></i> Teteocan Technologies
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const userName = ref('')
onMounted(() => {
  const user = sessionStorage.getItem('user')
  if (user) {
    const parsed = JSON.parse(user)
    userName.value = parsed.nombre ? parsed.nombre : ''
  }
})
</script>
<style>
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
  --orange: #f39c12;
  --gold: #f1c40f;
}
</style>
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
  --orange: #f39c12;
  --gold: #f1c40f;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.home-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a2530 0%, #2c3e50 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.home-container {
  width: 100%;
  margin-left: 80px;
  max-width: 900px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(245, 247, 250, 0.95) 100%);
  border-radius: 25px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
  padding: 40px;
  position: relative;
  overflow: hidden;
  z-index: 1;
}
.home-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(26, 188, 156, 0.1) 0%, transparent 70%);
  z-index: -1;
  animation: rotate 20s linear infinite;
}
@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
  padding: 0 20px;
}
.crown {
  font-size: 3.5rem;
  color: var(--gold);
  margin-bottom: 20px;
  animation: crownPop 1.5s cubic-bezier(.68,-0.55,.27,1.55) forwards;
  display: inline-block;
  background: linear-gradient(135deg, rgba(241, 196, 15, 0.1) 0%, transparent 70%);
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}
@keyframes crownPop {
  0% { transform: scale(0.3) rotate(-30deg); opacity: 0; }
  70% { transform: scale(1.2) rotate(15deg); opacity: 1; }
  100% { transform: scale(1) rotate(0); opacity: 1; }
}
.main-title {
  font-size: 2.8rem;
  font-weight: 800;
  color: var(--primary-color);
  margin-bottom: 10px;
  letter-spacing: -1px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--dark-blue) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  opacity: 0;
  animation: fadeInUp 0.8s 0.4s forwards;
}
.subtitle {
  color: var(--accent-color);
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 15px;
  opacity: 0;
  animation: fadeInUp 0.8s 0.6s forwards;
}
.brand {
  color: var(--purple);
  font-weight: 700;
  letter-spacing: 1px;
  position: relative;
}
.brand::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--accent-color);
  border-radius: 10px;
  transform: scaleX(0.8);
}
.description {
  color: var(--dark-gray);
  font-size: 1.2rem;
  margin: 20px auto;
  max-width: 80%;
  line-height: 1.6;
  opacity: 0;
  animation: fadeInUp 0.8s 0.8s forwards;
}
.highlight {
  color: var(--dark-blue);
  font-weight: 700;
  position: relative;
  display: inline-block;
}
.highlight::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--orange);
  border-radius: 10px;
  transform: scaleX(0.9);
}
.quick-guide {
  background: var(--light-gray);
  border-radius: 20px;
  padding: 35px 30px;
  margin-bottom: 30px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--medium-gray);
  opacity: 0;
  animation: fadeInUp 0.8s 1s forwards;
}
.quick-guide h2 {
  color: var(--primary-color);
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 15px;
  justify-content: center;
}
.steps {
  display: flex;
  flex-direction: column;
  gap: 25px;
}
.step {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  text-align: left;
  padding: 20px;
  border-radius: 18px;
  background: var(--white);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 1px solid transparent;
}
.step:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
  border-color: var(--accent-color);
}
.step .icon {
  font-size: 2.2rem;
  color: var(--white);
  background: linear-gradient(135deg, var(--secondary-color), var(--dark-blue));
  border-radius: 50%;
  padding: 18px;
  min-width: 70px;
  min-height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.step-content {
  flex-grow: 1;
}
.step h3 {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 10px;
}
.step p {
  color: var(--dark-gray);
  font-size: 1.1rem;
  margin: 0;
  line-height: 1.5;
}
.home-footer {
  margin-top: 40px;
  display: flex;
  flex-direction: column;
  gap: 25px;
  align-items: center;
  opacity: 0;
  animation: fadeInUp 0.8s 1.2s forwards;
}
.quote {
  color: var(--primary-color);
  font-size: 1.4rem;
  font-style: italic;
  display: flex;
  align-items: center;
  gap: 15px;
  max-width: 90%;
  padding: 20px;
  background: rgba(255, 255, 255, 0.7);
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}
.quote i {
  color: var(--accent-color);
  font-size: 2rem;
}
.brand-logo {
  color: var(--accent-color);
  font-weight: 700;
  font-size: 1.3rem;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(26, 188, 156, 0.1);
  padding: 15px 30px;
  border-radius: 50px;
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
/* Floating animation for steps */
.step:nth-child(1) {
  animation: float 6s ease-in-out 1.2s infinite;
}
.step:nth-child(2) {
  animation: float 6s ease-in-out 1.4s infinite;
}
.step:nth-child(3) {
  animation: float 6s ease-in-out 1.6s infinite;
}
@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}
/* Responsive design */
@media (max-width: 768px) {
  .home-container {
    padding: 30px 20px;
    max-width: 95%;
  }
  .main-title {
    font-size: 2.2rem;
  }
  .subtitle {
    font-size: 1.2rem;
  }
  .description {
    font-size: 1rem;
    max-width: 95%;
  }
  .quick-guide {
    padding: 25px 20px;
  }
  .step {
    gap: 15px;
    padding: 15px;
  }
  .step .icon {
    min-width: 55px;
    min-height: 55px;
    font-size: 1.7rem;
    padding: 12px;
  }
  .step h3 {
    font-size: 1.2rem;
  }
  .step p {
    font-size: 0.95rem;
  }
  .quote {
    font-size: 1.1rem;
  }
  .brand-logo {
    font-size: 1.1rem;
  }
}
@media (max-width: 480px) {
  .step {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .step .icon {
    margin-bottom: 15px;
  }
}
</style>