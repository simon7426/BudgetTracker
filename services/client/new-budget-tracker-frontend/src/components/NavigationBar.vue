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
      </div>
    </q-toolbar>
  </q-header>
</template>
