<script setup>
import { useQuasar } from "quasar";
import { ref } from "vue";
import transactionService from "../services/transaction.service";
import CreateCategoriesForm from "./CreateCategoriesForm.vue";

const columns = [
  {
    name: "category_name",
    required: true,
    label: "Category",
    align: "center",
    field: (row) => row.category_name,
    format: (val) => `${val}`,
  },
  {
    name: "category_type",
    required: true,
    label: "Type",
    field: "category_type",
    align: "center",
  },
  {
    name: "Action",
    label: "",
    field: "Action",
    sortable: false,
    align: "right",
  },
];

const rows = ref([]);
const loading = ref(true);
const q = useQuasar();


function getTransactionCategories() {
  rows.value = []
  transactionService
    .getCategories()
    .then((data) => {
      if (data.length) {
        for (var i in data) {
          rows.value.push(data[i]);
        }
      }
      loading.value = false;
    })
    .catch((err) => {
      console.log("Error in get categories");
      console.log(err);
    });}

getTransactionCategories()

function addCategoryDialog() {
  q.dialog({
    component: CreateCategoriesForm,
  }).onOk(()=> {
    getTransactionCategories()
  })
}



</script>
<template>
  <q-card class="my-card">
    <q-card-section>
      <div class="text-h6 text-grey-8">
        Categories
        <q-btn
          label="Add"
          class="float-right text-capitalize text-indigo-8 shadow-3"
          icon="add"
          @click="addCategoryDialog"
        />
      </div>
    </q-card-section>
    <q-card-section class="q-pa-none">
      <q-table
        :rows="rows"
        :columns="columns"
        row-key="category_name"
        :loading="loading"
        
      >
        <template #body-cell-Action="props">
          <q-td :props="props">
            <div class="td-action">
              <q-btn icon="edit" size="sm" flat dense />
              <q-btn icon="delete" size="sm" class="q-ml-sm" flat dense />
            </div>
          </q-td>
        </template>
        <template #loading>
          <q-inner-loading showing />
        </template>
      </q-table>
    </q-card-section>
  </q-card>
</template>
<style scoped lang="sass">
.my-card
  width: 100%
  max-width: 25rem
.td-action
  display: flex
  justify-content: space-around
</style>
