<script setup>
import { useQuasar } from "quasar";
import { ref } from "vue";
import transactionServiceTransfers from "../../services/transfers.transaction.service";
import transactionServiceAccounts from "../../services/accounts.transaction.service";
import TransfersFormCreate from "./TransfersFormCreate.vue";
import TransfersFormEdit from "./TransfersFormEdit.vue";
import TransfersFormDelete from "./TransfersFormDelete.vue";

const pagination = { sortBy: "transfer_id", descending: true, rowsPerPage: 0 };

const columns = [
  {
    name: "transfer_id",
    label: "ID",
    align: "center",
    field: (row) => row.id,
    format: (val) => `${val}`,
  },
  {
    name: "from_account",
    required: true,
    label: "From",
    align: "center",
    field: (row) => row.from_account.account_name,
    format: (val) => `${val}`,
  },
  {
    name: "to_account",
    required: true,
    label: "To",
    align: "center",
    sortable: true,
    field: (row) => row.to_account.account_name,
    format: (val) => `${val}`,
  },
  {
    name: "transfer_description",
    required: true,
    label: "Description",
    align: "center",
    sortable: true,
    field: (row) => row.transfer_description,
    format: (val) => `${!val ? "" : val}`,
  },
  {
    name: "transfer_amount",
    required: true,
    label: "Amount",
    align: "center",
    sortable: true,
    field: (row) => row.transfer_amount,
    format: (val) => `${parseFloat(val).toFixed(2)}`,
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
const transferTable = ref(null);
const rows = ref([]);
const loading = ref(true);
const q = useQuasar();

async function getTransactionAccountsTransfers() {
  rows.value = [];
  accountDict.value = {};

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

  await transactionServiceTransfers
    .getTransfers()
    .then((data) => {
      if (data.length) {
        for (var i in data) {
          rows.value.push({
            id: data[i]["id"],
            from_account: accountDict.value[data[i]["from_account_id"]],
            to_account: accountDict.value[data[i]["to_account_id"]],
            transfer_amount: data[i]["transfer_amount"],
            transfer_description: data[i]["transfer_description"],
          });
        }
      }
      loading.value = false;
    })
    .catch((err) => {
      console.log("Error in get transfers");
      console.log(err);
    });
}

getTransactionAccountsTransfers();

function getAccountTable() {
  let accountTable = [];
  for (var i in accountDict.value) {
    accountTable.push(accountDict.value[i]);
  }
  return accountTable;
}

function addTransferDialog() {
  q.dialog({
    component: TransfersFormCreate,
    componentProps: {
      accountTable: getAccountTable(),
    },
  }).onOk((payload) => {
    rows.value.unshift({
      id: payload["id"],
      from_account: accountDict.value[payload["from_account_id"]],
      to_account: accountDict.value[payload["to_account_id"]],
      transfer_amount: payload["transfer_amount"],
      transfer_description: payload["transfer_description"],
    });
  });
}

function editTransfer(transfer) {
  q.dialog({
    component: TransfersFormEdit,
    componentProps: {
      accountTable: getAccountTable(),
      row: transfer,
    },
  }).onOk((payload) => {
    rows.value[rows.value.findIndex((obj) => obj.id == transfer.id)] = {
      id: payload["id"],
      from_account: accountDict.value[payload["from_account_id"]],
      to_account: accountDict.value[payload["to_account_id"]],
      transfer_amount: payload["transfer_amount"],
      transfer_description: payload["transfer_description"],
    };
  });
}

function deleteTransfer(transfer) {
  q.dialog({
    component: TransfersFormDelete,
    componentProps: {
      row: transfer,
    },
  }).onOk(() => {
    rows.value.splice(
      rows.value.findIndex((obj) => obj.id == transfer.id),
      1
    );
  });
}
</script>

<template>
  <div class="window-width column q-px-md">
    <div class="row justify-between text-h6 text-grey-8">
      <span class="table-header">Transfers</span>
      <q-btn
        label="Add"
        class="float-right text-capitalize text-grey-9"
        icon="add"
        flat
        @click="addTransferDialog(accountTable)"
      />
    </div>
    <div class="q-pa-none">
      <q-table
        ref="transferTable"
        virtual-scroll
        flat
        separator="none"
        :pagination="pagination"
        :rows-per-page-options="[0]"
        :rows="rows"
        :columns="columns"
        row-key="transfer_id"
        :loading="loading"
        :visible-columns="[
          'from_account',
          'to_account',
          'transfer_amount',
          'transfer_description',
          'action',
        ]"
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
                @click="editTransfer(props.row)"
              />
              <q-btn
                icon="delete"
                size="sm"
                class="q-ml-sm"
                flat
                dense
                @click="deleteTransfer(props.row)"
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
