<script setup>
import { computed, ref } from "vue";

const username = ref("");
const email = ref("");
const password = ref("");
const password_confirm = ref("");
const isPwd = ref(true);
const confirmPwd = computed(() => {
  return password.value.length > 0 && password.value === password_confirm.value;
});
function handleRegister() {
  console.log(username.value);
  console.log(email.value);
  console.log(password.value);
}
</script>

<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-light-green text-black">
      <q-toolbar>
        <q-toolbar-title class="text-white"> Budget Tracker </q-toolbar-title>
        <q-space />
        <q-btn
          key="login-button"
          flat
          rounded
          color="dark"
          class="text-white"
          label="Login"
        ></q-btn>
        <q-btn
          key="register-button"
          flat
          rounded
          color="dark"
          class="text-white"
          label="Register"
        ></q-btn>
      </q-toolbar>
    </q-header>

    <q-page-container
      class="bg-cream-white window-height window-width row justify-center items-center"
    >
      <q-card flat class="bg-cream-white q-pa-lg shadow-1">
        <q-card-section>
          <q-form class="q-gutter-md">
            <q-input
              v-model="username"
              outlined
              standout="bg-white text-black"
              type="text"
              label="Username"
            >
              <template #prepend>
                <q-icon name="account_circle" />
              </template>
            </q-input>
            <q-input
              v-model="email"
              outlined
              standout="bg-white text-black"
              type="email"
              label="Email"
            >
              <template #prepend>
                <q-icon name="mail" />
              </template>
            </q-input>
            <q-input
              v-model="password"
              outlined
              standout="bg-white text-black"
              :type="isPwd ? 'password' : 'text'"
              label="Password"
            >
              <template #prepend>
                <q-icon name="lock" />
              </template>
              <template #append>
                <q-icon
                  :name="isPwd ? 'visibility_off' : 'visibility'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                />
              </template>
            </q-input>
            <q-input
              v-model="password_confirm"
              outlined
              standout="bg-white text-black"
              :type="isPwd ? 'password' : 'text'"
              label="Confirm Password"
            >
              <template #prepend>
                <q-icon name="lock" />
              </template>
              <template #append>
                <q-icon
                  :name="confirmPwd ? 'verified' : 'report_problem'"
                  :color="confirmPwd ? 'green' : 'default'"
                  class="cursor-pointer"
                  @click="isPwd = !isPwd"
                />
              </template>
            </q-input>
          </q-form>
        </q-card-section>
        <q-card-actions class="q-px-md">
          <q-btn
            unelevated
            color="light-green"
            size="lg"
            class="full-width"
            label="Register"
            @click="handleRegister"
          />
        </q-card-actions>
        <q-card-section class="text-center q-pa-none">
          <p class="text-grey-6">Already have an account? Login here.</p>
        </q-card-section>
      </q-card>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style scoped>
.bg-cream-white {
  background: #ffffea;
}
.q-card {
  width: 25rem;
}
</style>
