<script setup>
import { useQuasar } from "quasar";
import { ref } from "vue";
import transactionServiceAccounts from "../services/accounts.transaction.service";
import AccountsFormCreate from "./AccountsFormCreate.vue";
import AccountsFormDelete from "./AccountsFormDelete.vue";
import AccountsFormEdit from "./AccountsFormEdit.vue";

const pagination = { sortBy: "account_id", rowsPerPage: 0 };

const columns = [
  {
    name: "account_id",
    label: "ID",
    align: "center",
    field: (row) => row.id,
    format: (val) => `${val}`,
  },
  {
    name: "account_name",
    required: true,
    label: "Name",
    align: "center",
    field: (row) => row.account_name,
    format: (val) => `${val}`,
  },
  {
    name: "account_type",
    required: true,
    label: "Type",
    align: "center",
    sortable: true,
    field: (row) => row.account_type,
    format: (val) => `${val.replace(/^./, val[0].toUpperCase())}`,
  },
  {
    name: "account_balance",
    required: true,
    label: "Balance",
    align: "center",
    sortable: true,
    field: (row) => row.account_balance,
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

const accountTable = ref(null);
const rows = ref([]);
const loading = ref(true);
const q = useQuasar();

function getTransactionAccounts() {
  rows.value = [];
  transactionServiceAccounts
    .getAccounts()
    .then((data) => {
      if (data.length) {
        for (var i in data) {
          rows.value.push(data[i]);
        }
      }
      loading.value = false;
    })
    .catch((err) => {
      console.log("Error in get accounts");
      console.log(err);
    });
}

getTransactionAccounts();

function addAccountDialog() {
  q.dialog({
    component: AccountsFormCreate,
  }).onOk((payload) => {
    rows.value.push(payload);
  });
}

function editAccountDialog(account) {
  q.dialog({
    component: AccountsFormEdit,
    componentProps: {
      row: account,
    },
  }).onOk((payload) => {
    rows.value[rows.value.findIndex((obj) => obj.id == account.id)] = payload;
  });
}

function deleteAccountDialog(account) {
  q.dialog({
    component: AccountsFormDelete,
    componentProps: {
      row: account,
    },
  }).onOk(() => {
    rows.value.splice(
      rows.value.findIndex((obj) => obj.id == account.id),
      1
    );
  });
}
</script>
<template>
  <div class="window-width column q-px-md">
    <div class="row justify-between text-h6 text-grey-8">
      <div class="">Accounts</div>
      <q-btn
        label="Add"
        class="float-right text-capitalize text-grey-9"
        icon="add"
        flat
        @click="addAccountDialog"
      />
    </div>
    <div class="q-pa-none">
      <q-table
        ref="accountTable"
        virtual-scroll
        flat
        separator="none"
        :pagination="pagination"
        :rows-per-page-options="[0]"
        :rows="rows"
        :columns="columns"
        row-key="account_id"
        :loading="loading"
        :visible-columns="[
          'account_name',
          'account_type',
          'account_balance',
          'action',
        ]"
        binary-state-sort
        hide-pagination
        class="bg-cream-white"
      >
        <template #body-cell-action="props">
          <q-td :props="props">
            <div class="td-action">
              <q-btn icon="info" size="sm" flat dense />
              <q-btn
                icon="edit"
                size="sm"
                class="q-ml-sm"
                flat
                dense
                @click="editAccountDialog(props.row)"
              />
              <q-btn
                icon="delete"
                size="sm"
                class="q-ml-sm"
                flat
                dense
                @click="deleteAccountDialog(props.row)"
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
</style>
