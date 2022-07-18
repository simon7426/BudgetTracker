<script setup>
import { defineProps } from "vue";

const props = defineProps({
  item: {
    type: Object,
    default: () => {},
  },
});
</script>

<template>
  <transition appear enter-active-class="animated bounceIn" :duration="500">
    <div class="col-md-4 col-sm-12 col-xs-12">
      <q-item :style="`background-color: ${item.color1}`" class="q-pa-none">
        <q-item-section class="q-pa-md q-ml-none text-white">
          <q-item-label class="text-white text-h6 text-weight-bolder"
            >$<number
              ref="item.title"
              :from="0"
              :to="item.value"
              :duration="1"
              easing="Power0.easeNone"
          /></q-item-label>
          <q-item-label>{{ item.title }}</q-item-label>
        </q-item-section>
        <q-item-section side class="q-mr-md text-white">
          <q-icon :name="item.icon" color="white" size="2.5rem"></q-icon>
        </q-item-section>
      </q-item>
    </div>
  </transition>
</template>
