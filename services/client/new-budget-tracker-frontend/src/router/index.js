import { createWebHistory, createRouter } from "vue-router";
import HomePage from "../components/HomePage.vue";
import ProfilePage from "../components/ProfilePage.vue";
import RegisterPage from "../components/RegisterPage.vue";
import LoginPage from "../components/LoginPage.vue";
import LogoutPage from "../components/LogoutPage.vue";
import { useAuthStore } from "../stores/useAuth";
import TokenService from "../services/token.service";
import AuthService from "../services/auth.service";
import DashboardView from "../components/DashboardView.vue";

import AccountsView from "../components/Accounts/AccountsView.vue";
import CategoriesView from "../components/Categories/CategoriesView.vue";
import TransfersView from "../components/Transfers/TransfersView.vue";
import TransactionsView from "../components/Transactions/TransactionsView.vue";

const routes = [
  {
    path: "/",
    name: "Dashboard",
    component: DashboardView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/transactions",
    name: "Transactions",
    component: TransactionsView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/accounts",
    name: "Accounts",
    component: AccountsView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/transfers",
    name: "Transfers",
    component: TransfersView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/categories",
    name: "Category",
    component: CategoriesView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/login",
    name: "Login",
    component: LoginPage,
    meta: {
      requiresNotAuth: true,
    },
  },
  {
    path: "/register",
    name: "Register",
    component: RegisterPage,
    meta: {
      requiresNotAuth: true,
    },
  },
  {
    path: "/profile",
    name: "Profile",
    component: ProfilePage,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/logout",
    name: "Logout",
    component: LogoutPage,
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
      if (user !== null) {
        AuthService.refresh(user)
          .then(() => {
            next();
          })
          .catch((err) => {
            console.log(err);
            next({ name: "Login" });
          });
      } else {
        next({ name: "Login" });
      }
    } else {
      next();
    }
  } else if (to.matched.some((record) => record.meta.requiresNotAuth)) {
    const store = useAuthStore();
    if (store.isLoggedIn) {
      next({ name: "Profile" });
    } else {
      const user = TokenService.getUser();
      if (user !== null) {
        next({ name: "Profile" });
      } else {
        next();
      }
    }
  } else {
    next();
  }
});

export default router;
