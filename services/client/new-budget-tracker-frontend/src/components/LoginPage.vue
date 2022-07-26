<script setup>
import { ref } from "vue";
import authService from "../services/auth.service";
import { useRouter } from "vue-router";
import { useQuasar } from "quasar";
import { VueReCaptcha, useReCaptcha } from "vue-recaptcha-v3";

const username = ref("");
const usernameRef = ref(null);
const password = ref("");
const passwordRef = ref(null);
const isLoading = ref(false);
const isPwd = ref(true);

const router = useRouter();

const checkInput = [(val) => !!val || "Field is required"];

const q = useQuasar();
const { executeRecaptcha, recaptchaLoaded } = useReCaptcha();

function showNotif() {
  q.notify({
    type: "negative",
    message: "Invalid Username/Password.",
    position: "bottom-right",
  });
}

async function handleLogin() {
  const inp_username = username.value.trim();
  const inp_password = password.value.trim();
  if (inp_username.length !== 0 && inp_password.length !== 0) {
    isLoading.value = true;
    await recaptchaLoaded();

    const token = await executeRecaptcha("login");
    const user = {
      username: inp_username,
      password: inp_password,
      token: token,
    };

    await authService.login(user).then(
      (data) => {
        console.log(data);
        router.push({ name: "Dashboard" });
      },
      (error) => {
        isLoading.value = false;
        username.value = "";
        password.value = "";
        showNotif();
      }
    );
  } else {
    usernameRef.value.validate();
    passwordRef.value.validate();
  }
}
</script>

<template>
  <q-card flat class="bg-cream-white q-pa-lg shadow-1">
    <q-card-section class="card-header">
      <q-img
        :ratio="1 / 1"
        fit="fill"
        class="card-header-img"
        src="../assets/logoalter2.png"
        alt="logo"
      />
    </q-card-section>
    <q-card-section>
      <q-form class="q-gutter-md">
        <q-input
          ref="usernameRef"
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
          ref="passwordRef"
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
</template>
