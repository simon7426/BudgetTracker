<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../stores/useAuth";
const store = useAuthStore();
const router = useRouter();

const leftDrawerOpen = ref(true);
const miniState = ref(true);

const menuList = [
  {
    icon: "dashboard",
    label: "Dashboard",
    separator: false,
  },
  {
    icon: "paid",
    label: "Transactions",
    separator: false,
  },
  {
    icon: "payment",
    label: "Accounts",
    separator: false,
  },
  {
    icon: "currency_exchange",
    label: "Transfers",
    separator: false,
  },
  {
    icon: "category",
    label: "Category",
    separator: false,
  },
];

function drawerClicked(events, params) {
  router.push({ name: params.label, replace: true });
}

function isActive(props) {
  return props === router.currentRoute.value.name;
}
</script>

<template>
  <q-drawer
    v-if="store.isLoggedIn"
    v-model="leftDrawerOpen"
    side="left"
    :width="250"
    :mini="miniState"
    @mouseover="miniState = false"
    @mouseout="miniState = true"
  >
    <q-scroll-area class="fit drawerStyle">
      <q-list>
        <template v-for="(menuItem, index) in menuList" :key="index">
          <q-item
            v-ripple
            clickable
            :active="isActive(menuItem.label)"
            active-class="drawerActive"
            @click="drawerClicked($event, menuItem)"
          >
            <q-item-section avatar>
              <q-icon :name="menuItem.icon" color="black" />
            </q-item-section>
            <q-item-section>
              {{ menuItem.label }}
            </q-item-section>
          </q-item>
          <q-separator v-if="menuItem.separator" :key="'sep' + index" />
        </template>
      </q-list>
    </q-scroll-area>
  </q-drawer>
</template>
<style scoped lang="scss">
.drawerStyle {
  background: $primary;
}

.drawerActive {
  background: $accent;
  color: #000000
}
</style>
