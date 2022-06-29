<script setup>
import { ref } from "vue";

import NavigationBar from "./NavigationBar.vue";
import LeftDrawer from "./LeftDrawer.vue";
</script>

<template>
  <q-layout view="hHh lpR lFf">
    <NavigationBar />
    <LeftDrawer />
    <q-page-container class="no-padding">
      <q-page
        class="page-padding bg-cream-white window-height row justify-center items-start"
      >
        <router-view
      /></q-page>
    </q-page-container>
  </q-layout>
</template>

<style lang="scss">
.bg-cream-white {
  background: $primary;
}

.card-header {
  display: flex;
  justify-content: center;
}

.card-header-img {
  width: 100%;
}

.no-padding {
  padding: 0;
}

.page-padding {
  padding: 4rem 0rem;
}

@media (min-width: 768px) {
  .page-padding {
    padding: 5rem 250px;
  }
}
</style>
