<script setup>
import { useAuthStore } from "../stores/useAuth";
const store = useAuthStore();
</script>

<template>
  <q-header elevated class="nav-color text-black">
    <q-toolbar>
      <router-link class="no-decoration" :to="{ name: 'Dashboard' }">
        <q-avatar square size="2.5rem">
          <img src="../assets/logoalter.png" />
        </q-avatar>
      </router-link>
      <q-toolbar-title class="text-white"> Budget Tracker </q-toolbar-title>
      <q-space />
      <div v-if="store.isLoggedIn" class="q-gutter-sm">
        <router-link class="no-decoration" :to="{ name: 'Profile' }">
          <q-btn
            key="profile-button"
            flat
            rounded
            color="dark"
            class="text-white q-mt-sm"
            label="Profile"
          ></q-btn
        ></router-link>
        <router-link class="no-decoration" :to="{ name: 'Logout' }">
          <q-btn
            key="logout-button"
            flat
            rounded
            color="dark"
            class="text-white q-mt-sm"
            label="Logout"
          ></q-btn
        ></router-link>
      </div>
      <div v-else class="q-gutter-sm">
        <router-link class="no-decoration" :to="{ name: 'Login' }"
          ><q-btn
            key="login-button"
            flat
            rounded
            color="dark"
            class="text-white q-mt-sm"
            label="Login"
          ></q-btn
        ></router-link>
        <router-link class="no-decoration" :to="{ name: 'Register' }">
          <q-btn
            key="register-button"
            flat
            rounded
            color="dark"
            class="text-white q-mt-sm"
            label="Register"
          ></q-btn
        ></router-link>
      </div>
    </q-toolbar>
  </q-header>
</template>
<style scoped lang="scss">
.no-decoration {
  text-decoration: none;
  color: inherit;
}

.nav-color {
  background-color: $secondary;
}
</style>
