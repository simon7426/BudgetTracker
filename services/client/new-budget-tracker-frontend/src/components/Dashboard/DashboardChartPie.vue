<script setup>
import { toRefs, ref } from "vue";

const props = defineProps({
  categories: Array[String],
  amount: Array[Number],
  title: {
    type: String,
    default: "",
  },
});

const { categories, amount, title } = toRefs(props);

console.log(props);
const series = ref(amount.value);

const chartOptions = ref({
  chart: {
    type: "pie",
  },
  dataLabels: {
    enabled: true,
    formatter: (val, opts) => {
      console.log(opts.seriesIndex);
      return categories.value[opts.seriesIndex];
    },
  },
  labels: categories.value,
  title: {
    text: title.value,
    align: "center",
    margin: 10,
  },
  legend: {
    show: false,
  },
  plotOptions: {
    pie: {
      dataLabels: {
        offset: -20,
        minAngleToShowLabel: 10,
      },
    },
  },
  responsive: [
    {
      // breakpoint: 480,
      // options: {
      //   chart: {
      //     width: 200,
      //   },
      //   legend: {
      //     position: "bottom",
      //   },
      // },
    },
  ],
});
</script>

<template>
  <transition appear enter-active-class="animated bounceIn" :duration="500">
    <div class="col-md-6 col-sm-12 col-xs-12">
      <q-item class="q-pa-none">
        <q-item-section class="q-pa-md q-ml-none">
          <div class="chartPadding">
            <apexchart
              type="pie"
              :height="300"
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
