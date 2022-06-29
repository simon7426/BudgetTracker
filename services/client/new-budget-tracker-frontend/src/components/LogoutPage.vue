<script setup>
import { ref } from "vue";
import AuthService from "../services/auth.service";
import { useRouter } from "vue-router";
const loading = ref(true);
AuthService.logout();
loading.value = false;
const time = ref(5);
const router = useRouter();

setInterval(() => {
  if (time.value === 0) {
    clearInterval(time.value);
  } else {
    time.value--;
  }
}, 1000);
setTimeout(() => {
  router.push({ name: "Login" });
}, 5000);
</script>

<template>
  <q-page-container class="bg-cream-white window-height window-width">
    <div v-if="loading" class="align-center">
      <q-spinner-bars color="purple" size="md" />
    </div>
    <q-card v-else tag="span" class="top-gap">
      <p class="center-text">
        You have been successfully logged out. Redirecting to Login Page in
        {{ time }} seconds.
      </p>
    </q-card>
  </q-page-container>
</template>

<style scoped>
.center-text {
  text-align: center;
}
.top-gap {
  margin: 2.5rem;
}
.align-center {
  display: flex;
  justify-content: center;
}
</style>
