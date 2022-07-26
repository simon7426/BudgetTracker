<script setup>
import { useQuasar } from "quasar";
import { computed, ref } from "vue";
import transactionServiceCategories from "../../services/category.transaction.service";
import transactionServiceAccounts from "../../services/accounts.transaction.service";
import transactionService from "../../services/transactions.transaction.service";
import TransactionsFormCreate from "./TransactionsFormCreate.vue";
import TransactionsFormEdit from "./TransactionsFormEdit.vue";
import TransactionsFormDelete from "./TransactionsFormDelete.vue";

const dateOption = {
  year: "numeric",
  month: "long",
  day: "numeric",
};

const columns = [
  {
    name: "transaction_id",
    label: "ID",
    align: "center",
    field: (row) => row.id,
    format: (val) => `${val}`,
  },
  {
    name: "transaction_date",
    label: "Date",
    align: "center",
    sortable: true,
    sort: (a, b, rowA, rowB) => new Date(a) < new Date(b),
    field: (row) => row.transaction_date,
    format: (val) => `${val.toLocaleDateString("en-US", dateOption)}`,
  },
  {
    name: "transaction_type",
    required: true,
    label: "Type",
    align: "center",
    field: (row) => row.transaction_type,
    format: (val) => `${val.replace(/^./, val[0].toUpperCase())}`,
  },
  {
    name: "transaction_description",
    required: true,
    label: "Description",
    align: "center",
    sortable: false,
    field: (row) => row.transaction_description,
    format: (val) => `${val}`,
  },
  {
    name: "transaction_amount",
    required: true,
    label: "Amount",
    align: "center",
    sortable: true,
    field: (row) => row.transaction_amount,
    format: (val) => `${parseFloat(val).toFixed(2)}`,
  },
  {
    name: "transaction_category",
    required: true,
    label: "Category",
    align: "center",
    sortable: false,
    field: (row) => row.transaction_category.category_name,
    format: (val) => `${val}`,
  },
  {
    name: "transaction_account",
    required: true,
    label: "Account",
    align: "center",
    sortable: false,
    field: (row) => row.transaction_account.account_name,
    format: (val) => `${val}`,
  },
  {
    name: "action",
    label: "",
    field: "action",
    sortable: false,
    align: "right",
  },
];

const accountDict = ref(null);
const categoryDict = ref(null);
const transactionsTable = ref(null);
const rows = ref([]);
const loading = ref(true);
const q = useQuasar();
const firstPageId = ref(Math.pow(10, 9));
const previousPageIds = ref([]);
const limit = ref(100);
const nextPageDisabled = ref(false);
const previousPageDisabled = computed(() => previousPageIds.value.length === 0);

async function getTransactions() {
  rows.value = [];
  accountDict.value = {};
  categoryDict.value = {};

  await transactionServiceAccounts
    .getAccounts()
    .then((data) => {
      if (data.length) {
        for (var i in data) {
          accountDict.value[data[i]["id"]] = data[i];
        }
      }
    })
    .catch((err) => {
      console.log("Error in get accounts.");
      console.log(err);
    });

  await transactionServiceCategories
    .getCategories()
    .then((data) => {
      if (data.length) {
        for (var i in data) {
          categoryDict.value[data[i]["id"]] = data[i];
        }
      }
    })
    .catch((err) => {
      console.log("Error in get categories.");
      console.log(err);
    });

  await transactionService
    .getTransactions(firstPageId.value, limit.value + 1)
    .then((data) => {
      if (data.length > limit.value) {
        nextPageDisabled.value = false;
      } else {
        nextPageDisabled.value = true;
      }
      if (data.length) {
        for (var i in data.slice(0, limit.value)) {
          rows.value.push({
            id: data[i]["id"],
            transaction_date: new Date(data[i]["transaction_date"]),
            transaction_type: data[i]["transaction_type"],
            transaction_description: data[i]["transaction_description"],
            transaction_amount: data[i]["transaction_amount"],
            transaction_category:
              categoryDict.value[data[i]["transaction_category_id"]],
            transaction_account:
              accountDict.value[data[i]["transaction_account_id"]],
          });
        }
      }
      loading.value = false;
    })
    .catch((err) => {
      console.log("Error in get transactions");
      console.log(err);
    });
}

getTransactions();

async function getNextPage() {
  var nextPageId = rows.value[rows.value.length - 1].id - 1;
  previousPageIds.value.push(rows.value[0].id);
  await transactionService
    .getTransactions(nextPageId, limit.value + 1)
    .then((data) => {
      rows.value = [];
      if (data.length > limit.value) {
        nextPageDisabled.value = false;
      } else {
        nextPageDisabled.value = true;
      }
      if (data.length) {
        for (var i in data.slice(0, limit.value)) {
          rows.value.push({
            id: data[i]["id"],
            transaction_date: new Date(data[i]["transaction_date"]),
            transaction_type: data[i]["transaction_type"],
            transaction_description: data[i]["transaction_description"],
            transaction_amount: data[i]["transaction_amount"],
            transaction_category:
              categoryDict.value[data[i]["transaction_category_id"]],
            transaction_account:
              accountDict.value[data[i]["transaction_account_id"]],
          });
        }
      }

      loading.value = false;
    })
    .catch((err) => {
      console.log("Error in get transactions");
      console.log(err);
    });
}

async function getPreviousPage() {
  await transactionService
    .getTransactions(
      previousPageIds.value[previousPageIds.value.length - 1],
      limit.value + 1
    )
    .then((data) => {
      previousPageIds.value.pop();
      rows.value = [];
      if (data.length > limit.value) {
        nextPageDisabled.value = false;
      } else {
        nextPageDisabled.value = true;
      }
      if (data.length) {
        for (var i in data.slice(0, limit.value)) {
          rows.value.push({
            id: data[i]["id"],
            transaction_date: new Date(data[i]["transaction_date"]),
            transaction_type: data[i]["transaction_type"],
            transaction_description: data[i]["transaction_description"],
            transaction_amount: data[i]["transaction_amount"],
            transaction_category:
              categoryDict.value[data[i]["transaction_category_id"]],
            transaction_account:
              accountDict.value[data[i]["transaction_account_id"]],
          });
        }
      }

      loading.value = false;
    })
    .catch((err) => {
      console.log("Error in get transactions");
      console.log(err);
    });
}

function getAccountTable() {
  let accountTable = [];
  for (var i in accountDict.value) {
    accountTable.push(accountDict.value[i]);
  }
  return accountTable;
}

function getCategoryTable() {
  let categoryTable = [];
  for (var i in categoryDict.value) {
    categoryTable.push(categoryDict.value[i]);
  }
  return categoryTable;
}

function addTransactionDialog() {
  q.dialog({
    component: TransactionsFormCreate,
    componentProps: {
      accountTable: getAccountTable(),
      categoryTable: getCategoryTable(),
    },
  }).onOk((payload) => {
    rows.value.push({
      id: payload["id"],
      transaction_date: new Date(payload["transaction_date"]),
      transaction_type: payload["transaction_type"],
      transaction_description: payload["transaction_description"],
      transaction_amount: payload["transaction_amount"],
      transaction_category:
        categoryDict.value[payload["transaction_category_id"]],
      transaction_account: accountDict.value[payload["transaction_account_id"]],
    });
  });
}

function editTransaction(transaction) {
  q.dialog({
    component: TransactionsFormEdit,
    componentProps: {
      accountTable: getAccountTable(),
      categoryTable: getCategoryTable(),
      row: transaction,
    },
  }).onOk((payload) => {
    rows.value[rows.value.findIndex((obj) => obj.id == transaction.id)] = {
      id: payload["id"],
      transaction_date: new Date(payload["transaction_date"]),
      transaction_type: payload["transaction_type"],
      transaction_description: payload["transaction_description"],
      transaction_amount: payload["transaction_amount"],
      transaction_category:
        categoryDict.value[payload["transaction_category_id"]],
      transaction_account: accountDict.value[payload["transaction_account_id"]],
    };
  });
}

function deleteTransaction(transaction) {
  q.dialog({
    component: TransactionsFormDelete,
    componentProps: {
      row: transaction,
    },
  }).onOk(() => {
    rows.value.splice(
      rows.value.findIndex((obj) => obj.id == transaction.id),
      1
    );
  });
}
</script>

<template>
  <div class="window-width column q-px-md">
    <div class="row justify-between text-h6 text-grey-8">
      <span class="table-header">Transactions</span>
      <q-btn
        label="Add"
        class="float-right text-capitalize text-grey-9"
        icon="add"
        flat
        @click="addTransactionDialog"
      />
    </div>
    <div class="q-pa-none">
      <q-table
        ref="transactionTable"
        virtual-scroll
        grid
        flat
        separator="none"
        :rows-per-page-options="[0]"
        :rows="rows"
        :columns="columns"
        row-key="transaction_id"
        :loading="loading"
        :visible-columns="[
          'transaction_date',
          'transaction_type',
          'transaction_description',
          'transaction_amount',
          'transaction_category',
          'transaction_account',
          'action',
        ]"
        hide-pagination
        hide-header
        class="bg-cream-white"
      >
        <!-- <template #body-cell-action="props">
          <q-td :props="props">
            <div class="td-action">
              <q-btn
                icon="edit"
                size="sm"
                flat
                dense
                @click="editTransaction(props.row)"
              />
              <q-btn
                icon="delete"
                size="sm"
                class="q-ml-sm"
                flat
                dense
                @click="deleteTransaction(props.row)"
              />
            </div>
          </q-td>
        </template> -->
        <template #item="props">
          <div class="col-md-12 col-sm-12 col-xs-12">
            <q-item class="q-pa-none bg-cream-white text-center">
              <q-item-section class="q-pa-md q-ml-none">
                <q-item-label class="text-grey-9">{{
                  props.row.transaction_date.toLocaleDateString(
                    "en-US",
                    dateOption
                  )
                }}</q-item-label>
              </q-item-section>
              <q-item-section class="q-pa-md q-ml-none">
                <q-item-label class="text-grey-9">{{
                  props.row.transaction_description
                }}</q-item-label>
                <q-item-label class="text-grey-9"
                  >Category:
                  {{
                    props.row.transaction_category.category_name
                  }}</q-item-label
                >
              </q-item-section>
              <q-item-section class="q-pa-md q-ml-none">
                <q-item-label class="text-grey-9 text-weight-bolder"
                  >${{ props.row.transaction_amount }}</q-item-label
                >
              </q-item-section>
              <q-item-section>
                <div class="row justify-around full-width">
                  <q-btn
                    icon="edit"
                    size="sm"
                    flat
                    dense
                    @click="editTransaction(props.row)"
                  />
                  <q-btn
                    icon="delete"
                    size="sm"
                    class="q-ml-sm"
                    flat
                    dense
                    @click="deleteTransaction(props.row)"
                  />
                </div>
              </q-item-section>
            </q-item>
          </div>
        </template>
        <template #loading>
          <q-inner-loading showing>
            <q-spinner-gears size="10rem" color="primary" />
          </q-inner-loading>
        </template>
        <template #bottom>
          <div class="row justify-between full-width">
            <q-btn
              flat
              rounded
              :disabled="previousPageDisabled"
              color="secondary"
              label="<< Previous"
              @click="getPreviousPage"
            />
            <q-btn
              flat
              rounded
              :disabled="nextPageDisabled"
              color="secondary"
              label="Next >>"
              @click="getNextPage"
            />
          </div>
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
.full-width
  width: 100%
</style>
