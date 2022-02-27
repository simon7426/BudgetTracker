<script setup>
import { ref } from "vue";
import authService from "../services/auth.service";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref("");
const isLoading = ref(false);
const isPwd = ref(true);

const router = useRouter()
// function checkInput(username) {
//   if(!!username){
//     return "This field is required!"
//   }
// }

const checkInput = [val => !!val || 'Field is required']

function handleLogin() {
  isLoading.value = true
  const inp_username= username.value.trim()
  const inp_password = password.value.trim()
  const user = {
    "username": inp_username,
    "password": inp_password,
  }
  authService.login(user).then(
    (data) => {
      console.log("Login Success")
      router.push({ name: "Profile" })
    },
    (error) => {
      isLoading.value = false
      console.log("error")
    }
  )
}
</script>

<template>
  <q-page-container
    class="bg-cream-white window-height window-width row justify-center items-center"
  >
    <q-card flat class="bg-cream-white q-pa-lg shadow-1">
      <q-card-section class="card-header">
        <q-img
          :ratio="16 / 9"
          fit="fill"
          class="card-header-img"
          src="../assets/logo16.png"
          alt="logo"
        />
      </q-card-section>
      <q-card-section>
        <q-form class="q-gutter-md">
          <q-input
            v-model="username"
            outlined
            standout="bg-white text-black"
            type="text"
            label="Username"
            :rules="checkInput"
          >
            <template #prepend>
              <q-icon name="account_circle" />
            </template>
          </q-input>
          <q-input
            v-model="password"
            outlined
            standout="bg-white text-black"
            :type="isPwd ? 'password' : 'text'"
            label="Password"
            :rules="checkInput"
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
        </q-form>
      </q-card-section>
      <q-card-actions class="q-px-md">
        <q-btn
          unelevated
          color="light-green"
          size="lg"
          class="full-width"
          label="Login"
          :loading="isLoading"
          @click="handleLogin"
        />
      </q-card-actions>
      <q-card-section class="text-center q-pa-none">
        <p class="text-grey-6">Don't have an account? Register here.</p>
      </q-card-section>
    </q-card>
    <router-view />
  </q-page-container>
</template>

<style scoped></style>
