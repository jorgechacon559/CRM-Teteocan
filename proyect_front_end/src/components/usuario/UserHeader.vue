<template>
  <header class="user-header">
    <div class="container">
      <div class="brand">
        <div class="logo">
          <i class="fas fa-gem"></i>
        </div>
        <div class="brand-text">
          <h1 class="title">Desarrollo comercial</h1>
          <span class="subtitle">Teteocan Technologies</span>
        </div>
      </div>
      <div class="header-icons">
        <div class="header-badge">
          <i class="fas fa-crown"></i>
          <span>¡Bienvenido!</span>
        </div>
        <div class="header-magic">
          <i class="fas fa-magic"></i>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
// No necesitas lógica aquí si no hay interacción
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

:root {
  --primary-color: #2c3e50;
  --secondary-color: #3498db;
  --accent-color: #1abc9c;
  --light-gray: #f5f7fa;
  --dark-gray: #718096;
  --white: #ffffff;
  --purple: #9b59b6;
  --dark-blue: #2980b9;
  --gold: #f1c40f;
}

.user-header {
  background: linear-gradient(135deg, var(--primary-color) 0%, #1a2530 100%) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.13);
  padding: 0.8rem 0;
  position: relative;
  z-index: 100;
}

.user-header::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(to right, rgba(26, 188, 156, 0.08) 0%, transparent 60%);
  z-index: -1;
}

.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  max-width: 1600px;
  margin: 0 auto;
}

.brand {
  display: flex;
  align-items: center;
  gap: 18px;
}

.logo {
  width: 52px;
  height: 52px;
  background: linear-gradient(135deg, var(--accent-color), var(--dark-blue));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: var(--white);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.18);
  transition: all 0.3s ease;
}

.logo:hover {
  transform: rotate(-10deg) scale(1.08);
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
  margin-bottom: 20px;

}

.title {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--white);
  letter-spacing: -0.5px;
  margin-bottom: 2px;
}

.subtitle {
  font-size: 1rem;
  font-weight: 600;
  color: var(--accent-color);
  letter-spacing: 1px;
  margin-left: 2px;
}

.header-icons {
  display: flex;
  align-items: center;
  gap: 25px;
}

.header-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(241, 196, 15, 0.13);
  color: var(--gold);
  font-weight: 700;
  font-size: 1.08rem;
  padding: 7px 18px 7px 14px;
  border-radius: 30px;
  box-shadow: 0 2px 8px rgba(241, 196, 15, 0.07);
  animation: badgePop 1.2s cubic-bezier(.68,-0.55,.27,1.55);
}
.header-badge i {
  font-size: 1.3rem;
  color: var(--gold);
}

@keyframes badgePop {
  0% { transform: scale(0.7) rotate(-10deg); opacity: 0; }
  70% { transform: scale(1.15) rotate(8deg); opacity: 1; }
  100% { transform: scale(1) rotate(0); opacity: 1; }
}

.header-magic {
  background: linear-gradient(135deg, var(--purple), var(--accent-color));
  color: var(--white);
  border-radius: 50%;
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  box-shadow: 0 2px 8px rgba(155, 89, 182, 0.13);
  animation: magicFloat 2.5s ease-in-out infinite;
}

@keyframes magicFloat {
  0% { transform: translateY(0);}
  50% { transform: translateY(-7px);}
  100% { transform: translateY(0);}
}

@media (max-width: 992px) {
  .container {
    padding: 0 1.2rem;
  }
  .brand-text .title {
    font-size: 1.2rem;
  }
  .subtitle {
    font-size: 0.85rem;
  }
  .header-badge {
    font-size: 0.95rem;
    padding: 6px 12px 6px 10px;
  }
  .header-magic {
    width: 36px;
    height: 36px;
    font-size: 1.1rem;
  }
}

@media (max-width: 600px) {
  .container {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
    padding: 0 0.5rem;
  }
  .header-icons {
    gap: 10px;
  }
}
</style>