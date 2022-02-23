<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import HelloWorld from "./components/HelloWorld.vue";
import LoginPage from "./components/LoginPage.vue";
import RegisterPage from "./components/RegisterPage.vue";
import NavigationBar from "./components/NavigationBar.vue";
</script>

<template>
  <q-layout view="hHh lpR fFf">
    <NavigationBar />
    <RegisterPage />
  </q-layout>
</template>

<style>
.bg-cream-white {
  background: #ffffea;
}
.q-card {
  width: 25rem;
}
.card-header {
  display: flex;
  justify-content: center;
}
.card-header-img {
  width: 100%;
}
</style>
