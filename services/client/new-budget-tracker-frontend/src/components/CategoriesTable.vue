<script setup>
import { useQuasar } from "quasar";
import { ref } from "vue";
import transactionServiceCategory from "../services/category.transaction.service";
import CategoriesFormCreate from "./CategoriesFormCreate.vue";
import CategoriesFormEdit from "./CategoriesFormEdit.vue";
import CategoriesFormDelete from "./CategoriesFormDelete.vue";

const pagination = { sortBy: "category_id", rowsPerPage: 0 };

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
    format: (val) => `${val.replace(/^./, val[0].toUpperCase())}`,
  },
  {
    name: "action",
    label: "",
    field: "action",
    sortable: false,
    align: "right",
  },
];

const categoryTable = ref(null);
const rows = ref([]);
const loading = ref(true);
const q = useQuasar();

function getTransactionCategories() {
  rows.value = [];
  transactionServiceCategory
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
    });
}

getTransactionCategories();

function addCategoryDialog() {
  q.dialog({
    component: CategoriesFormCreate,
  }).onOk((payload) => {
    rows.value.push(payload);
  });
}

function editCategory(category) {
  q.dialog({
    component: CategoriesFormEdit,
    componentProps: {
      row: category,
    },
  }).onOk((payload) => {
    rows.value[rows.value.findIndex((obj) => obj.id == category.id)] = payload;
  });
}

function deleteCategory(category) {
  q.dialog({
    component: CategoriesFormDelete,
    componentProps: {
      row: category,
    },
  }).onOk(() => {
    rows.value.splice(
      rows.value.findIndex((obj) => obj.id == category.id),
      1
    );
  });
}
</script>

<template>
  <div class="window-width column q-px-md">
    <div class="row justify-between text-h6 text-grey-8">
      <span class="table-header">Categories</span>
      <q-btn
        label="Add"
        class="float-right text-capitalize text-grey-9"
        icon="add"
        flat
        @click="addCategoryDialog"
      />
    </div>
    <div class="q-pa-none">
      <q-table
        ref="categoryTable"
        virtual-scroll
        flat
        separator="none"
        :pagination="pagination"
        :rows-per-page-options="[0]"
        :rows="rows"
        :columns="columns"
        row-key="category_id"
        :loading="loading"
        :visible-columns="['category_name', 'category_type', 'action']"
        binary-state-sort
        hide-pagination
        class="bg-cream-white"
      >
        <template #body-cell-action="props">
          <q-td :props="props">
            <div class="td-action">
              <q-btn
                icon="edit"
                size="sm"
                flat
                dense
                @click="editCategory(props.row)"
              />
              <q-btn
                icon="delete"
                size="sm"
                class="q-ml-sm"
                flat
                dense
                @click="deleteCategory(props.row)"
              />
            </div>
          </q-td>
        </template>
        <template #loading>
          <q-inner-loading showing>
            <q-spinner-gears size="10rem" color="primary" />
          </q-inner-loading>
        </template>
      </q-table>
    </div>
  </div>
</template>
<style scoped lang="sass">

.td-action
  display: flex
  justify-content: space-around

.bg-cream-white
  background: $primary
.table-header
  align-self: center
</style>
