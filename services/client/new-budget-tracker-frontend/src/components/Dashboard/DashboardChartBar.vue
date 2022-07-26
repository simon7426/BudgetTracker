<script setup>
import { toRefs, ref } from "vue";

const props = defineProps({
  previousMonths: Array[String],
  incomeLastYear: Array[Number],
  expenseLastYear: Array[Number],
});

const { previousMonths, incomeLastYear, expenseLastYear } = toRefs(props);

const series = ref([
  {
    name: "Income",
    data: incomeLastYear.value,
  },
  {
    name: "Expense",
    data: expenseLastYear.value,
  },
]);

const chartOptions = ref({
  chart: {
    type: "bar",

    toolbar: {
      show: false,
    },
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: "55%",
      endingShape: "rounded",
    },
  },
  dataLabels: {
    enabled: false,
  },
  grid: {
    show: false,
  },
  legend: {
    show: true,
    position: "top",
    horizontalAlign: "right",
  },
  xaxis: {
    categories: previousMonths.value,
    axisTicks: {
      show: false,
    },
    axisBorder: {
      show: false,
    },
  },
  yaxis: {
    axisTicks: {
      show: false,
    },
    axisBorder: {
      show: false,
    },
  },
  fill: {
    opacity: 1,
  },
  title: {
    text: "Income/Expense of Last 12 Months",
    align: "center",
  },
  tooltip: {
    enabled: true,
    y: {
      formatter: (val) => {
        return `$${val}`;
      },
    },
  },
});
</script>

<template>
  <transition appear enter-active-class="animated bounceIn" :duration="500">
    <div class="col-md-12 col-sm-12 col-xs-12">
      <q-item class="q-pa-none">
        <q-item-section class="q-pa-md q-ml-none">
          <div id="barChart" class="chartPadding">
            <apexchart
              type="bar"
              :height="400"
              :options="chartOptions"
              :series="series"
            ></apexchart>
          </div>
        </q-item-section>
      </q-item>
    </div>
  </transition>
</template>
<style>
.apexcharts-tooltip-title {
  color: black;
}
.chartPadding {
  margin: 0.5rem;
}
</style>
