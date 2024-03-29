import { createApp } from "vue";
import { Quasar, Notify, Dialog } from "quasar";
import router from "./router";
import ApexCharts from "apexcharts";
import VueApexCharts from "vue3-apexcharts";

import VueNumber from "vue-number-animation";
import { createPinia } from "pinia";
import setupIntercetor from "./services/setupInterceptors";
import { VueReCaptcha } from "vue-recaptcha-v3";
import "@quasar/extras/roboto-font/roboto-font.css";
import "@quasar/extras/material-icons/material-icons.css";
import "@quasar/extras/fontawesome-v5/fontawesome-v5.css";
import "@quasar/extras/animate/bounceIn.css";

import "quasar/src/css/index.sass";

import App from "./App.vue";

const myApp = createApp(App);

const store = createPinia();

myApp.use(store);

myApp.use(router);

myApp.use(VueNumber);

myApp.use(VueApexCharts);

myApp.use(VueReCaptcha, {
  siteKey: "6Lft2R4hAAAAABOqIEoYJHXo1xZL9O60pf9o2NVW",
});

// myApp.use(Quasar, {
//     plugins: {},
// })

myApp.use(Quasar, {
  plugins: {
    Notify,
    Dialog,
  },
  config: {
    notify: {
      /* look at QuasarConfOptions from the API card */
    },
  },
});

myApp.mount("#app");
