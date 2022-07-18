<script setup>
import { ref } from "vue";
import summaryService from "../../services/summary.transaction.service";
import CardSummaryItem from "./CardSummaryItem.vue";

const items = ref([
  {
    title: "Income This Month",
    icon: "fas fa-caret-up",
    value: 0,
    color1: "#7cb342",
  },
  {
    title: "Expense This Month",
    icon: "fas fa-caret-down",
    value: 0,
    color1: "#ff160c",
  },
  {
    title: "Current Balance",
    icon: "fas fa-dollar-sign",
    value: 0,
    color1: "#546bfa",
  },
  {
    title: "Income All",
    icon: "fas fa-caret-up",
    value: 0,
    color1: "#7cb342",
  },
  {
    title: "Expense All",
    icon: "fas fa-caret-down",
    value: 0,
    color1: "#ff160c",
  },
  {
    title: "Monthly Balance",
    icon: "fas fa-caret-up",
    value: 0,
    color1: "#546bfa",
  },
]);

async function getBasicSummary() {
  await summaryService
    .basicSummary()
    .then((data) => {
      items.value[0]["value"] = data["incomeMonth"];
      items.value[1]["value"] = data["expenseMonth"];
      items.value[2]["value"] = data["balance"];
      items.value[3]["value"] = data["incomeAll"];
      items.value[4]["value"] = data["expenseAll"];
      items.value[5]["value"] = data["incomeMonth"] - data["expenseMonth"];
      if (items.value[5]["value"] < 0) {
        items.value[5]["icon"] = "fas fa-caret-down";
        items.value[5]["value"] = -items.value[5]["value"];
      } else {
        items.value[5]["icon"] = "fas fa-caret-up";
      }
    })
    .catch((err) => {
      console.log(err);
    });
}

getBasicSummary();
</script>

<template>
  <q-card class="bg-transparent no-shadow no-border">
    <q-card-section class="q-pa-none">
      <div class="row q-col-gutter-sm">
        <card-summary-item :key="items[3].title" :item="items[3]" />
        <card-summary-item :key="items[4].title" :item="items[4]" />
        <card-summary-item :key="items[2].title" :item="items[2]" />

        <card-summary-item :key="items[0].title" :item="items[0]" />
        <card-summary-item :key="items[1].title" :item="items[1]" />
        <card-summary-item :key="items[5].title" :item="items[5]" />
      </div>
    </q-card-section>
  </q-card>
</template>

<style lang="sass" scoped>
.q-card
  width: 100%
</style>
