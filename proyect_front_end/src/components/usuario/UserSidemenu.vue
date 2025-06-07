<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const user = ref(null)
if (sessionStorage.getItem('user')) {
  user.value = JSON.parse(sessionStorage.getItem('user'))
}

const buttons = [
  { title: 'Inicio', icon: 'fa-home', link: '/inicio' },
  { title: 'Crear organización', icon: 'fa-building', link: '/organizaciones/crear' },
  { title: 'Realizar seguimiento', icon: 'fa-search-location', link: '/seguimientos' },
  { title: 'Historial', icon: 'fa-history', link: '/seguimientos/historial' }
]
if (user.value && user.value.rol === 'admin') {
  buttons.push({ title: 'Usuarios', icon: 'fa-users-cog', link: '/usuarios' })
}

function logout() {
  sessionStorage.clear()
  router.push('/login')
}

// Esta función compara la ruta actual con el link del botón
function isActive(link) {
  // Si es inicio, solo cuando es exactamente /inicio
  if (link === '/inicio') return route.path === '/inicio';
  // Si es historial, solo cuando es exactamente /seguimientos/historial
  if (link === '/seguimientos/historial') return route.path === '/seguimientos/historial';
  // Para los demás, activo si es exactamente igual o si empieza con el link + '/' (pero no para historial)
  return route.path === link || (route.path.startsWith(link + '/') && link !== '/seguimientos');
}
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1>
        <i class="fas fa-chart-line"></i>
        <span>Panel de navegación</span>
      </h1>
    </div>
    <div class="user-info" v-if="user">
      <div class="user-avatar">
        {{ user.nombre ? user.nombre[0].toUpperCase() : 'U' }}
      </div>
      <div class="user-details">
        <div class="user-name">{{ user.nombre }}{{ user.apellido ? ' ' + user.apellido : '' }}</div>
        <div class="user-role">{{ user.rol === 'admin' ? 'Administrador' : 'Agente' }}</div>
      </div>
    </div>
  <nav class="nav-links">
      <router-link
        v-for="button in buttons"
        :key="button.link"
        :to="button.link"
        class="nav-item"
        :class="{ active: isActive(button.link) }"
      >
        <i :class="['fas', button.icon]"></i>
        <span>{{ button.title }}</span>
      </router-link>
  </nav>
    <div class="logout-section">
      <button class="logout-btn" @click="logout">
        <i class="fas fa-sign-out-alt"></i>
        <span>Cerrar sesión</span>
      </button>
    </div>
  </aside>
</template>

<style>
:root {
  --sidebar-width: 280px;
  --primary-color: #2c3e50;
  --secondary-color: #3498db;
  --accent-color: #1abc9c;
  --light-gray: #f5f7fa;
  --dark-gray: #718096;
  --white: #ffffff;
  --purple: #9b59b6;
  --dark-blue: #2980b9;
  --gold: #f1c40f;
  --sidebar-bg: linear-gradient(135deg, #1a2530 0%, #2c3e50 100%);
  --sidebar-link-hover: rgba(255, 255, 255, 0.05);
  --sidebar-link-active: rgba(26, 188, 156, 0.15);
  --sidebar-border-active: #1abc9c;
}

</style>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.sidebar {
  width: var(--sidebar-width);
  background: var(--sidebar-bg)!important;
  color: var(--white);
  min-height: 100vh;
  position: sticky;
  top: 0;
  left: 0;
  box-shadow: 3px 0 15px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
  z-index: 100;
  overflow: hidden;
}
.sidebar::before {
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

.sidebar-header {
  padding: 30px 25px 20px 25px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  justify-content: center;
  z-index: 2;
}
.sidebar-header h1 {
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  color: var(--white);
  letter-spacing: -0.5px;
}
.sidebar-header i {
  color: var(--accent-color);
  font-size: 1.8rem;
  background: rgba(26, 188, 156, 0.1);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
}

.user-info {
  padding: 25px;
  display: flex;
  align-items: center;
  gap: 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 2;
}
.user-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--secondary-color), var(--dark-blue));
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  color: var(--white);
  font-weight: 600;
}
.user-details {
  flex: 1;
}
.user-name {
  font-weight: 600;
  font-size: 1.2rem;
  margin-bottom: 5px;
  color: var(--white);
}
.user-role {
  background: rgba(26, 188, 156, 0.2);
  color: var(--accent-color);
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  display: inline-block;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 25px 0;
  position: relative;
  z-index: 2;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 18px 30px;
  border-left: 4px solid transparent;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
  font-size: 1.1rem;
  text-decoration: none;
  background: transparent;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.nav-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 100%;
  background: linear-gradient(to right, rgba(26, 188, 156, 0.2), transparent);
  transition: width 0.4s ease;
  z-index: -1;
}
.nav-item i {
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
  min-width: 25px;
  text-align: center;
}
.nav-item span {
  transition: all 0.3s ease;
}
.nav-item:hover {
  color: var(--white);
  transform: translateX(8px);
}
.nav-item:hover::before {
  width: 100%;
}
.nav-item:hover i {
  color: var(--accent-color);
  transform: scale(1.2);
}
.nav-item.active {
  background: var(--sidebar-link-active);
  border-left: 4px solid var(--sidebar-border-active);
  color: var(--accent-color);
  font-weight: 600;
  transform: translateX(0);
}
.nav-item.active i {
  color: var(--accent-color);
  animation: iconPulse 1.5s infinite;
}
.nav-item.active::before {
  width: 100%;
  background: rgba(26, 188, 156, 0.15);
}
@keyframes iconPulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.logout-section {
  margin-top: auto;
  padding: 20px 25px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  z-index: 2;
}
.logout-btn {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px 20px;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
  font-size: 1.1rem;
  text-decoration: none;
  background: transparent;
  transition: all 0.3s ease;
  cursor: pointer;
  border-radius: 12px;
  border: none;
}
.logout-btn:hover {
  background: rgba(231, 76, 60, 0.2);
  color: var(--white);
}
.logout-btn i {
  font-size: 1.3rem;
  transition: all 0.3s ease;
}
.logout-btn:hover i {
  color: #e74c3c;
  transform: rotate(-10deg);
}

@media (max-width: 992px) {
  .sidebar {
    width: 80px;
  }
  .sidebar-header h1 span,
  .user-name,
  .user-role,
  .nav-item span,
  .logout-btn span {
    display: none;
  }
  .sidebar-header, .nav-item, .logout-btn {
    padding: 20px 15px;
    justify-content: center;
  }
  .user-info {
    justify-content: center;
    padding: 25px 15px;
  }
  .nav-links {
    padding: 20px 0;
  }
}
@media (max-width: 768px) {
  .sidebar {
    width: 100%;
    height: auto;
  }
}
</style>