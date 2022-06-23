<script setup>
import { useQuasar } from "quasar";
import { ref } from "vue";
import transactionService from "../services/transaction.service";
import CategoriesFormCreate from "./CategoriesFormCreate.vue";
import CategoriesFormEdit from "./CategoriesFormEdit.vue";
import CategoriesFormDelete from "./CategoriesFormDelete.vue";

const pagination = { sortBy: 'category_id', rowsPerPage: 0 }

const columns = [
  {
    name: "category_id",
    label: "ID",
    align: "center",
    field: (row) => row.id,
    format: (val) => `${val}`,
  },
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
    align: "center",
    sortable: true,
    field: (row) => row.category_type,
    format: (val) => `${val.replace(/^./, val[0].toUpperCase())}`
  },
  {
    name: "action",
    label: "",
    field: "action",
    sortable: false,
    align: "right",
  },
];

const categoryTable = ref(null)
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
      // categoryTable.value.sort("category_id")
      loading.value = false;
    })
    .catch((err) => {
      console.log("Error in get categories");
      console.log(err);
    });}

getTransactionCategories()

function addCategoryDialog() {
  q.dialog({
    component: CategoriesFormCreate,
  }).onOk(()=> {
    getTransactionCategories()
  })
}

function editCategory(category) {
  q.dialog({
    component: CategoriesFormEdit,
    componentProps: {
      row: category
    }
  }).onOk(() => {
    getTransactionCategories()
  })
}

function deleteCategory(category) {
  q.dialog({
    component: CategoriesFormDelete,
    componentProps: {
      row: category
    }
  }).onOk(() => {
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
          class="float-right text-capitalize text-indigo-8 "
          icon="add"
          flat
          rounded
          @click="addCategoryDialog"
        />
      </div>
    </q-card-section>
    <q-card-section class="q-pa-none">
      <q-table
        ref="categoryTable"
        virtual-scroll
        :pagination="pagination"
        :rows-per-page-options="[0]"
        :rows="rows"
        :columns="columns"
        row-key="category_id"
        :loading="loading"
        :visible-columns="['category_name','category_type', 'action']"
        binary-state-sort
        hide-pagination
      >
        <template #body-cell-action="props">
          <q-td :props="props">
            <div class="td-action">
              <q-btn icon="edit" size="sm" flat dense @click="editCategory(props.row)" />
              <q-btn icon="delete" size="sm" class="q-ml-sm" flat dense @click="deleteCategory(props.row)" />
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
