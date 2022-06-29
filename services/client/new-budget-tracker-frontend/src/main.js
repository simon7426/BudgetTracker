import { createApp } from "vue";
import { Quasar, Notify, Dialog } from "quasar";
import router from "./router";

import { createPinia } from "pinia";
import setupIntercetor from "./services/setupInterceptors";
import "@quasar/extras/roboto-font/roboto-font.css";
import "@quasar/extras/material-icons/material-icons.css";

import "quasar/src/css/index.sass";

import App from "./App.vue";

const myApp = createApp(App);

const store = createPinia();

myApp.use(store);

myApp.use(router);

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
