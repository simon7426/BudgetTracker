<script setup>
import { ref } from 'vue';
const columns = [
  {
    name: "category_name",
    required: true,
    label: "Category",
    align: "left",
    field: (row) => row.category_name,
    format: (val) => `${val}`,
  },
  {
    name: "category_type",
    required: true,
    label: "Type",
    field: "category_type",
  },
];

const rows = [
  {
    category_name: "Salary",
    category_type: "Income",
  },
];

const loading = ref(false)

</script>
<template>
  <div class="q-pa-md">
    <q-table
      title="Categories"
      :rows="rows"
      :columns="columns"
      row-key="category_name"
      :loading="loading"
    >
    <template #loading>
        <q-inner-loading showing />
    </template>
    </q-table>
  </div>
</template>
