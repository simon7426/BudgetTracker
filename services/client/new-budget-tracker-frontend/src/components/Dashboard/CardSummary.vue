<script setup>
import { ref } from "vue";
import summaryService from "../../services/summary.transaction.service";
import CardSummaryItem from "./CardSummaryItem.vue";
import DashboardChartBar from "./DashboardChartBar.vue";
import DashboardChartPie from "./DashboardChartPie.vue";

const items = ref([
  {
    title: "Income This Month",
    icon: "fas fa-caret-up",
    value: 0,
    color1: "#45D975",
  },
  {
    title: "Expense This Month",
    icon: "fas fa-caret-down",
    value: 0,
    color1: "#D93D3B",
  },
  {
    title: "Current Balance",
    icon: "fas fa-dollar-sign",
    value: 0,
    color1: "#666CD9",
  },
  {
    title: "Income All",
    icon: "fas fa-caret-up",
    value: 0,
    color1: "#45D975",
  },
  {
    title: "Expense All",
    icon: "fas fa-caret-down",
    value: 0,
    color1: "#D93D3B",
  },
  {
    title: "Monthly Balance",
    icon: "fas fa-caret-up",
    value: 0,
    color1: "#666CD9",
  },
]);

const dataLoaded = ref(false);

const previousMonths = ref([]);
const incomeLastYear = ref([]);
const expenseLastYear = ref([]);

const incomeChartTitle = ref("Historical income by category");
const incomeCategory = ref([]);
const incomeCategoryValues = ref([]);

const expenseChartTitle = ref("Historical expense by category");
const expenseCategory = ref([]);
const expenseCategoryValues = ref([]);

const incomeChartMonthTitle = ref("This month's income by category");
const incomeCategoryMonth = ref([]);
const incomeCategoryMonthValues = ref([]);

const expenseChartMonthTitle = ref("This month's expense by category");
const expenseCategoryMonth = ref([]);
const expenseCategoryMonthValues = ref([]);

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

      previousMonths.value = data["previousMonths"];
      incomeLastYear.value = data["incomeLastYear"];
      expenseLastYear.value = data["expenseLastYear"];

      incomeCategory.value = data["incomeCategory"];
      incomeCategoryValues.value = data["incomeCategoryValues"];

      expenseCategory.value = data["expenseCategory"];
      expenseCategoryValues.value = data["expenseCategoryValues"];

      incomeCategoryMonth.value = data["incomeCategoryMonth"];
      incomeCategoryMonthValues.value = data["incomeCategoryMonthValues"];

      expenseCategoryMonth.value = data["expenseCategoryMonth"];
      expenseCategoryMonthValues.value = data["expenseCategoryMonthValues"];

      dataLoaded.value = true;
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
      <div v-if="dataLoaded" class="row q-col-gutter-sm">
        <card-summary-item :key="items[3].title" :item="items[3]" />
        <card-summary-item :key="items[4].title" :item="items[4]" />
        <card-summary-item :key="items[2].title" :item="items[2]" />

        <card-summary-item :key="items[0].title" :item="items[0]" />
        <card-summary-item :key="items[1].title" :item="items[1]" />
        <card-summary-item :key="items[5].title" :item="items[5]" />

        <dashboard-chart-bar
          :income-last-year="incomeLastYear"
          :expense-last-year="expenseLastYear"
          :previous-months="previousMonths"
        />

        <dashboard-chart-pie
          :title="incomeChartTitle"
          :categories="incomeCategory"
          :amount="incomeCategoryValues"
        />
        <dashboard-chart-pie
          :title="expenseChartTitle"
          :categories="expenseCategory"
          :amount="expenseCategoryValues"
        />

        <dashboard-chart-pie
          :title="incomeChartMonthTitle"
          :categories="incomeCategoryMonth"
          :amount="incomeCategoryMonthValues"
        />
        <dashboard-chart-pie
          :title="expenseChartMonthTitle"
          :categories="expenseCategoryMonth"
          :amount="expenseCategoryMonthValues"
        />
      </div>
    </q-card-section>
  </q-card>
</template>

<style lang="sass" scoped>
.q-card
  width: 100%
</style>
