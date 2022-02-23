<script setup></script>

<template>
  <q-header elevated class="bg-light-green text-black">
    <q-toolbar>
      <q-avatar square size="2.5rem">
        <img src="../assets/logo-transperant.png" />
      </q-avatar>
      <q-toolbar-title class="text-white"> Budget Tracker </q-toolbar-title>
      <q-space />
      <div class="q-gutter-sm">
        <router-link class="no-decoration" to="/login"
          ><q-btn
            key="login-button"
            flat
            rounded
            color="dark"
            class="text-white"
            label="Login"
          ></q-btn
        ></router-link>
        <router-link class="no-decoration" to="/register">
          <q-btn
            key="register-button"
            flat
            rounded
            color="dark"
            class="text-white"
            label="Register"
          ></q-btn
        ></router-link>
      </div>
    </q-toolbar>
  </q-header>
</template>
<style scoped>
.no-decoration {
  text-decoration: none;
  color: inherit;
}
</style>
