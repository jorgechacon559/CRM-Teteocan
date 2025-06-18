<script setup>
import { reactive, onMounted, computed, ref, watch, onBeforeUnmount } from 'vue';
import { useUsuariosStore } from '@/stores/usuarios';
import api from '@/api/axios';

const usuarios = useUsuariosStore();
const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('success')

function showSuccessToast(msg) {
  toastMessage.value = msg
  toastType.value = 'success'
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 2500)
}

function showErrorToast(msg) {
  toastMessage.value = msg
  toastType.value = 'error'
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 2500)
}

const headers = reactive(['Nombre', 'Apellido', 'Correo', 'Rol', 'Estado', 'Acciones']);
const paginadorData = reactive({
    currentPage: 1,
    totalPages: undefined,
    itemsPerPage: 10,
});

function mostrarRol(rol) {
  if (rol === 'admin') return 'Admin';
  if (rol === 'agente') return 'Agente';
  return rol;
}

const pageInput = ref('');
watch(() => paginadorData.currentPage, (val) => {
  pageInput.value = val ? val.toString() : '';
});
const searchText = ref('');
watch(searchText, () => {
  paginadorData.currentPage = 1;
});

const usuariosData = computed(() => {
    const data = usuarios.data;
    if(!data) return [];
    // Filtrar por búsqueda
    let filtered = data;
    if (searchText.value.trim()) {
        const txt = searchText.value.trim().toLowerCase();
        filtered = data.filter(u =>
            (u.nombre && u.nombre.toLowerCase().includes(txt)) ||
            (u.apellido && u.apellido.toLowerCase().includes(txt)) ||
            (u.email && u.email.toLowerCase().includes(txt)) ||
            (u.rol && u.rol.toLowerCase().includes(txt))
        );
    }
    paginadorData.totalPages = Math.max(1, Math.ceil(filtered.length / paginadorData.itemsPerPage));
    const start = (paginadorData.currentPage - 1) * paginadorData.itemsPerPage;
    const end = start + paginadorData.itemsPerPage;
    return filtered.slice(start, end);
});
watch(() => paginadorData.currentPage,
(newVal) => {
    if((newVal === null || newVal === undefined || newVal === '') || newVal < 1) {
        paginadorData.currentPage = 1;
    } else if (newVal > paginadorData.totalPages) {
        paginadorData.currentPage = paginadorData.totalPages;
    }
});
const paginatorState = (toRight) => {
    paginadorData.currentPage = toRight ?
        Math.min(paginadorData.totalPages, ++paginadorData.currentPage) :
        Math.max(1, --paginadorData.currentPage);
};
const validateAndGoToPage = () => {
    let page = parseInt(pageInput.value, 10);
    if (isNaN(page) || page < 1) page = 1;
    if (page > paginadorData.totalPages) page = paginadorData.totalPages;
    paginadorData.currentPage = page;
    pageInput.value = page.toString();
};
let identity = sessionStorage.getItem('user');
identity = identity ? JSON.parse(identity) : null;
const getInfo = async () => {
    await usuarios.getAllInfoUsr('usuarios');
};
onMounted(async () => {
  await getInfo();
  console.log('Usuarios cargados:', usuarios.data);
});

// Modal para upgrade
const showUpgradeModal = ref(false);
const usuarioUpgradeId = ref(null);
const adminPassword = ref('');
const upgradeError = ref('');

const confirmarUpgrade = (usuario_id) => {
    usuarioUpgradeId.value = usuario_id;
    adminPassword.value = '';
    upgradeError.value = '';
    showUpgradeModal.value = true;
    setTimeout(() => {
      document.addEventListener('keydown', handleEsc);
    }, 0);
};

const cancelarUpgrade = () => {
    showUpgradeModal.value = false;
    usuarioUpgradeId.value = null;
    adminPassword.value = '';
    upgradeError.value = '';
    document.removeEventListener('keydown', handleEsc);
};

const handleEsc = (e) => {
    if (e.key === 'Escape') cancelarUpgrade();
};

const modalOverlayClick = (e) => {
    if (e.target.classList.contains('modal-overlay')) cancelarUpgrade();
};

onBeforeUnmount(() => {
    document.removeEventListener('keydown', handleEsc);
});

const realizarUpgrade = async () => {
    upgradeError.value = '';
    try {
        const adminEmail = identity.email;
        if (!adminEmail) {
            upgradeError.value = 'No se encontró el correo del administrador actual.';
            return;
        }
        const response = await api.post('/usuarios/login', {
            email: adminEmail,
            password: adminPassword.value
        });
        if (response.data && response.data.access_token) {
            await api.put(`/usuarios/${usuarioUpgradeId.value}/hacer-admin`, {}, {
                headers: { Authorization: `Bearer ${response.data.access_token}` }
            });
            await getInfo();
            cancelarUpgrade();
            showSuccessToast('Usuario ascendido a Administrador correctamente');
        } else {
            upgradeError.value = 'Contraseña incorrecta';
        }
    } catch (e) {
        upgradeError.value = 'Contraseña incorrecta o error de autenticación';
    }
};

const eliminarUsuario = async (usuario_id) => {
    try {
        const token = sessionStorage.getItem("token");
        await api.put(`/usuarios/${usuario_id}/baja`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        });
        await getInfo();
        showErrorToast('Usuario dado de baja');
    } catch (e) {
        showErrorToast('No se pudo eliminar al usuario');
    }
};
</script>

<template>
  <div class="admin-users-container">
    <div class="admin-header">
      <div class="header-content">
        <h1><i class="fas fa-users-cog"></i> Gestión de usuarios</h1>
        <p>Administra todos los usuarios del sistema. Solo administradores pueden realizar cambios.</p>
      </div>
      <div class="header-stats">
        <div class="stat-card">
          <i class="fas fa-user"></i>
          <div>
            <span>Total de usuarios</span>
            <strong>{{ usuarios.data ? usuarios.data.length : 0 }}</strong>
          </div>
        </div>
        <div class="stat-card">
          <i class="fas fa-user-shield"></i>
          <div>
            <span>Número de administradores</span>
            <strong>{{ usuarios.data ? usuarios.data.filter(u => u.rol === 'admin').length : 0 }}</strong>
          </div>
        </div>
      </div>
    </div>

    <div class="users-table-container">
      <div class="table-header">
        <div class="search-container">
          <i class="fas fa-search"></i>
          <input
            type="text"
            placeholder="Buscar usuarios..."
            class="search-input"
            v-model="searchText"
          >
        </div>
        <div class="pagination-info">
          Página {{ paginadorData.currentPage }} de {{ paginadorData.totalPages }}
        </div>
      </div>

      <div class="users-table">
        <div class="table-header-row">
          <div v-for="(head, index) in headers" :key="index" class="table-header-cell">
            {{ head }}
          </div>
        </div>

        <div class="table-body">
          <div 
            v-for="(item, index) in usuariosData" 
            :key="index" 
            class="table-row"
            :class="{ 'inactive-user': item.baja }"
          >
            <div class="table-cell">
              <div class="user-info">
                <div class="user-avatar">
                  <i class="fas fa-user"></i>
                </div>
                <span>{{ item.nombre }}</span>
              </div>
            </div>
            <div class="table-cell">
              <span>{{ item.apellido }}</span>
            </div>
            <div class="table-cell">
              <span>{{ item.email }}</span>
            </div>
            <div class="table-cell">
              <span class="user-role" :class="item.rol">{{ mostrarRol(item.rol) }}</span>
            </div>
            <div class="table-cell">
              <span class="user-status" :class="item.baja ? 'inactive' : 'active'">
                {{ item.baja ? 'Inactivo' : 'Activo' }}
              </span>
            </div>
            <div class="table-cell actions-cell">
              <!-- Botón upgrade a admin -->
              <button
                v-if="identity && identity.rol === 'admin' && item.rol !== 'admin' && !item.baja"
                class="btn-action btn-upgrade"
                @click="confirmarUpgrade(item.usuario_id)"
                title="Hacer admin"
              >
                <i class="fas fa-user-shield"></i>
              </button>
              <!-- Botón eliminar -->
              <button
                v-if="identity && identity.rol === 'admin' && !item.baja && item.usuario_id !== identity.usuario_id"
                class="btn-action btn-delete"
                @click="eliminarUsuario(item.usuario_id)"
                title="Dar de baja"
              >
                <i class="fas fa-user-slash"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="table-footer">
        <div class="pagination-controls">
          <button 
            class="pagination-btn" 
            @click="paginatorState(false)"
            :disabled="paginadorData.currentPage === 1"
          >
            <i class="fas fa-chevron-left"></i>
          </button>
          
          <div class="page-input-container">
            <input
              type="text"
              placeholder="Ir a página"
              v-model="pageInput"
              @keyup.enter="validateAndGoToPage"
              @blur="validateAndGoToPage"
              class="page-input"
            >
          </div>
          
          <button 
            class="pagination-btn" 
            @click="paginatorState(true)"
            :disabled="paginadorData.currentPage === paginadorData.totalPages"
          >
            <i class="fas fa-chevron-right"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de confirmación para upgrade -->
    <transition name="modal-fade">
      <div v-if="showUpgradeModal" class="modal-overlay" @mousedown="modalOverlayClick">
        <div class="modal-content" @mousedown.stop>
          <div class="modal-header">
            <i class="fas fa-user-shield"></i>
            <h3>Confirmar ascenso a Administrador</h3>
          </div>
          <div class="modal-body">
            <p>Para confirmar esta acción, por favor ingrese su contraseña de administrador:</p>
            <div class="password-input-container">
              <i class="fas fa-lock"></i>
              <input 
                type="password" 
                v-model="adminPassword" 
                placeholder="Contraseña actual" 
                class="modal-input"
              />
            </div>
            <p v-if="upgradeError" class="error-message">{{ upgradeError }}</p>
          </div>
          <div class="modal-actions">
            <button @click="cancelarUpgrade" class="modal-btn cancel-btn">
              <i class="fas fa-times"></i> Cancelar
            </button>
            <button @click="realizarUpgrade" class="modal-btn confirm-btn">
              <i class="fas fa-check"></i> Confirmar
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Toast Notification -->
    <div v-if="showToast" class="toast" :class="toastType">
      <i class="fas" :class="toastType === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'"></i>
      <span>{{ toastMessage }}</span>
    </div>
  </div>
</template>

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
  font-family: 'Poppins', sans-serif;
}

.admin-users-container {
  margin-left: 80px;
  min-height: 100vh;
  width: calc(100% - 80px) !important;
  background-color: #f5f7fa;
}

.admin-header {
  margin-bottom: 30px;
}

.header-content h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 10px;
  background: linear-gradient(to right, var(--primary), var(--primary-dark));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  display: flex;
  align-items: center;
  gap: 15px;
}

.header-content p {
  font-size: 1.1rem;
  color: var(--gray);
  max-width: 700px;
  line-height: 1.6;
}

.header-stats {
  display: flex;
  gap: 20px;
  margin-top: 25px;
}

.stat-card {
  background: #fff;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  min-width: 250px;
}

.stat-card i {
  font-size: 2.5rem;
  width: 60px;
  height: 60px;
  background: rgba(67, 97, 238, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
}

.stat-card div {
  display: flex;
  flex-direction: column;
}

.stat-card span {
  font-size: 0.95rem;
  color: var(--gray);
}

.stat-card strong {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--dark);
}

.users-table-container {
  background: #fff;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  background: var(--light);
  border-bottom: 1px solid var(--light-gray);
}

.search-container {
  position: relative;
  width: 300px;
}

.search-container i {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--gray);
}

.search-input {
  width: 100%;
  padding: 12px 15px 12px 45px;
  border: 2px solid var(--light-gray);
  border-radius: 12px;
  font-size: 1rem;
  transition: var(--transition);
  background: #fff;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
}

.pagination-info {
  font-weight: 500;
  color: var(--gray);
}

.users-table {
  width: 100%;
}

.table-header-row {
  display: grid;
  grid-template-columns: 1.5fr 1.5fr 2fr 1fr 1fr 1fr;
  padding: 15px 30px;
  background: #f8fafc;
  font-weight: 600;
  color: var(--dark);
  border-bottom: 1px solid var(--light-gray);
}

.table-body {
  min-height: 400px;
}

.table-row {
  display: grid;
  grid-template-columns: 1.5fr 1.5fr 2fr 1fr 1fr 1fr;
  padding: 15px 30px;
  border-bottom: 1px solid var(--light-gray);
  transition: var(--transition);
}

.table-row:hover {
  background-color: rgba(67, 97, 238, 0.03);
}

.table-cell {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--light);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
  font-size: 1.1rem;
}

.user-role {
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 500;
  font-size: 0.9rem;
}

.user-role.admin {
  background: rgba(67, 97, 238, 0.1);
  color: var(--primary);
}

.user-role.agente {
  background: rgba(76, 201, 240, 0.1);
  color: var(--secondary);
}

.user-role.usuario {
  background: rgba(114, 114, 114, 0.1);
  color: var(--dark);
}

.user-status {
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 500;
  font-size: 0.9rem;
}

.user-status.active {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success);
}

.user-status.inactive {
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger);
}

.inactive-user {
  opacity: 0.7;
  background-color: rgba(229, 231, 235, 0.3);
}

.actions-cell {
  display: flex;
  gap: 10px;
}

.btn-action {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  transition: var(--transition);
  font-size: 1.1rem;
}

.btn-upgrade {
  background: rgba(46, 204, 113, 0.1);
  color: var(--success);
}

.btn-upgrade:hover {
  background: var(--success);
  color: white;
}

.btn-delete {
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger);
}

.btn-delete:hover {
  background: var(--danger);
  color: white;
}

.table-footer {
  padding: 20px 30px;
  display: flex;
  justify-content: center;
  border-top: 1px solid var(--light-gray);
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.pagination-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--primary);
  color: var(--primary);
  background: transparent;
  cursor: pointer;
  transition: var(--transition);
  font-size: 1rem;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  border-color: var(--light-gray);
  color: var(--light-gray);
}

.pagination-btn:not(:disabled):hover {
  background: var(--primary);
  color: white;
}

.page-input-container {
  position: relative;
}

.page-input {
  width: 120px;
  padding: 10px 15px 10px 40px;
  border: 2px solid var(--light-gray);
  border-radius: 30px;
  font-size: 0.95rem;
  transition: var(--transition);
}

.page-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
}

.page-input-container::before {
  content: "\f35a";
  font-family: "Font Awesome 5 Free";
  font-weight: 900;
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--gray);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  width: 100%;
  max-width: 500px;
  overflow: hidden;
}

.modal-header {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  padding: 25px;
  text-align: center;
}

.modal-header i {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.modal-header h3 {
  font-size: 1.8rem;
  font-weight: 600;
}

.modal-body {
  padding: 30px;
}

.modal-body p {
  margin-bottom: 20px;
  color: var(--gray);
  text-align: center;
}

.password-input-container {
  position: relative;
  margin-bottom: 25px;
}

.password-input-container i {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--gray);
}

.modal-input {
  width: 100%;
  padding: 15px 20px 15px 50px;
  border: 2px solid var(--light-gray);
  border-radius: 12px;
  font-size: 1rem;
  transition: var(--transition);
}

.modal-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
}

.error-message {
  color: var(--danger);
  text-align: center;
  margin-top: 15px;
  font-weight: 500;
}

.modal-actions {
  display: flex;
  gap: 15px;
  padding: 0 30px 30px;
}

.modal-btn {
  flex: 1;
  padding: 15px;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border: none;
  transition: var(--transition);
}

.cancel-btn {
  background: #f8f9fa;
  color: var(--gray);
  border: 2px solid var(--light-gray);
}

.cancel-btn:hover {
  background: #e2e8f0;
}

.confirm-btn {
  background: linear-gradient(to right, var(--success), #1d9b5c);
  color: white;
  box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3);
}

.confirm-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(46, 204, 113, 0.4);
}

/* Toast Notification */
.toast {
  position: fixed;
  bottom: 30px;
  right: 30px;
  padding: 15px 25px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 500;
  z-index: 1000;
  animation: slideIn 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.toast.success {
  background: var(--success);
  color: white;
}

.toast.error {
  background: var(--danger);
  color: white;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 992px) {
  .users-table-container {
    overflow-x: auto;
  }
  
  .users-table {
    min-width: 900px;
  }
  
  .header-stats {
    flex-wrap: wrap;
  }
}

@media (max-width: 768px) {
  .admin-header {
    padding: 20px;
  }
  
  .modal-content {
    width: 95%;
  }
  
  .modal-actions {
    flex-direction: column;
  }
}

@media (max-width: 576px) {
  .admin-users-container {
    padding: 15px;
  }
  
  .table-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .search-container {
    width: 100%;
  }
}
</style>