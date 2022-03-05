<script setup>
import { ref } from 'vue';
import transactionService from "../services/transaction.service"
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

const rows = ref([])
const loading = ref(true)

transactionService.getCategories().then(
  (data)=> {
    console.log(data.length)
    if (data.length) {
      for (var i in data) {
        rows.value.push(data[i])
      }
    }
    loading.value = false
    console.log(rows.value)
  }
).catch((err)=>{
  console.log("Error in get categories")
  console.log(err)
})
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
