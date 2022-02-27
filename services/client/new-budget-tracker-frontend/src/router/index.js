import { createWebHistory, createRouter } from "vue-router";
import RegisterPage from "../components/RegisterPage.vue";
import LoginPage from "../components/LoginPage.vue";
import ProfilePage from "../components/ProfilePage.vue";
import { useAuthStore } from "../stores/useAuth";
import TokenService from "../services/token.service";
import AuthService from "../services/auth.service";

const routes = [
  {
    path: "/",
    name: "Home",
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/login",
    name: "Login",
    component: LoginPage,
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterPage,
  },
  {
    path: "/profile",
    name: "Profile",
    component: ProfilePage,
    meta: {
      requiresAuth: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    const store = useAuthStore();
    if (!store.isLoggedIn) {
      const user = TokenService.getUser();
      if (user!==null) {
        AuthService.refresh(user);
        next();
      } else {
        next({ name: "Login" });
      }
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
