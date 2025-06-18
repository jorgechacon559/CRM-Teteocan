import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL || '/'),
  routes: [
    {
      path: "/",
      component: () => import("@/layouts/PublicLayout.vue"),
      children: [
        {
          path: 'login',
          name: 'login',
          component: () => import("@/components/inicio/Login.vue")
        },
        {
          path: 'register',
          name: 'register',
          component: () => import("@/components/inicio/Register.vue")
        },
        {
          path: '',
          redirect: { name: 'login' }
        }
      ],
    },
    {
      path: "/inicio",
      component: () => import("@/layouts/UsuarioLayout.vue"),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'inicio',
          component: () => import("@/components/inicio/Home.vue"),
          meta: { requiresAuth: true }
        },
        {
          path: '/organizaciones/crear',
          name: 'crear-organizacion',
          component: () => import("@/components/organizaciones/CrearOrganizacion.vue"),
          meta: { requiresAuth: true }
        },
        {
          path: '/seguimientos',
          name: 'realizar-seguimiento',
          component: () => import("@/components/seguimientos/RealizarSeguimiento.vue"),
          meta: { requiresAuth: true }
        },
        {
          path: '/seguimientos/historial',
          name: 'historial-seguimientos',
          // Carga dinámica para code splitting
          component: () => import('@/components/seguimientos/HistorialSeguimientos.vue'),
          meta: { requiresAuth: true }
        },
        {
          path: '/usuarios',
          name: 'usuarios',
          component: () => import("@/components/usuario/AllUsers.vue"),
          meta: { requiresAuth: true, requiresAdmin: true }
        }
      ]
    },
    {
      path: '/:catchAll(.*)',
      redirect: { name: 'inicio' }
    }
  ]
});

// Protección de rutas y roles
router.beforeEach(async (to, from, next) => {
  const user = sessionStorage.getItem('user');
  const token = sessionStorage.getItem('token');
  const refreshToken = sessionStorage.getItem('refresh_token');
  const authStore = useAuthStore();

  // Solo admin puede acceder a /usuarios
  if ((to.path === '/usuarios' || to.name === 'usuarios' || to.meta.requiresAdmin)) {
    if (!user) {
      next({ name: 'login' });
      return;
    }
    const userObj = JSON.parse(user);
    if (userObj.rol !== 'admin') {
      next({ name: 'inicio' });
      return;
    }
  }

  if (to.meta.requiresAuth) {
    if (!user) {
      next({ name: 'login' });
    } else if (!token && refreshToken) {
      const refreshed = await authStore.refreshAccessToken();
      if (refreshed) {
        next();
      } else {
        next({ name: 'login' });
      }
    } else if (!token && !refreshToken) {
      next({ name: 'login' });
    } else {
      next();
    }
  } else if (user && (to.name === 'login' || to.name === 'register')) {
    next({ name: 'inicio' });
  } else {
    next();
  }
});

export default router;