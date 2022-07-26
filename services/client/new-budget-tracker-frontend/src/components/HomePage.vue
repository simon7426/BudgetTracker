<script setup>
import { ref } from "vue";

import NavigationBar from "./NavigationBar.vue";
import LeftDrawer from "./LeftDrawer.vue";

const drawerOpen = ref(false)

function myTweak(offset) {
  return { minHeight: offset ? `calc(100vh - ${offset}px)` : "100vh" };
}
function drawerOpenFunc() {
  drawerOpen.value = true
}

function closeDrawerFunc(){
  drawerOpen.value = false
}

</script>

<template>
  <q-layout view="hHh lpR lFf">
    <NavigationBar @drawer-toggled="drawerOpenFunc"/>
    <LeftDrawer :drawer-open="drawerOpen" @drawer-closed="closeDrawerFunc"/>
    <q-page-container class="no-padding">
      <q-page
        :style-fn="myTweak"
        class="page-padding bg-cream-white row justify-center items-start"
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
