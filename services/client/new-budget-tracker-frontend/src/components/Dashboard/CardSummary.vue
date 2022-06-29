<script setup>
import { ref } from "vue";

const items = ref([
  {
    title: "Income This Month",
    icon: "fas fa-caret-up",
    value: "$20k",
    color1: "#7cb342",
  },
  {
    title: "Expense This Month",
    icon: "fas fa-caret-down",
    value: "20",
    color1: "#ff160c",
  },
  {
    title: "Current Balance",
    icon: "fas fa-dollar-sign",
    value: "321",
    color1: "#546bfa",
  },
]);
</script>

<template>
  <q-card class="bg-transparent no-shadow no-border">
    <q-card-section class="q-pa-none">
      <div class="row q-col-gutter-sm">
        <div
          v-for="(item, index) in items"
          :key="index"
          class="col-md-4 col-sm-12 col-xs-12"
        >
          <q-item :style="`background-color: ${item.color1}`" class="q-pa-none">
            <q-item-section class="q-pa-md q-ml-none text-white">
              <q-item-label class="text-white text-h6 text-weight-bolder">{{
                item.value
              }}</q-item-label>
              <q-item-label>{{ item.title }}</q-item-label>
            </q-item-section>
            <q-item-section side class="q-mr-md text-white">
              <q-icon :name="item.icon" color="white" size="2.5rem"></q-icon>
            </q-item-section>
          </q-item>
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<style lang="sass" scoped>
.q-card
  width: 100%
</style>
