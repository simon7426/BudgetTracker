<script setup>
import { ref } from "vue";
import transactionServiceAccounts from "../../services/accounts.transaction.service";
import { useDialogPluginComponent, useQuasar } from "quasar";

const props = defineProps({
  row: {
    type: Object,
    default: () => {},
  },
})

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();

const accountID = ref(props.row.id)
const accountName = ref(props.row.account_name);
const accountNameRef = ref(null);
const accountType = ref(props.row.account_type);
const accountTypeRef = ref(null);
const accountBalance = ref(props.row.account_balance);
const accountBalanceRef = ref(null);

const isLoading = ref(false);

const checkInput = [(val) => !!val || "Field is required"];
const checkAmount = [(val) => val >= 0 || "Amount must be positive"]

const q = useQuasar();

function showNotif(msg, type) {
  q.notify({
    type: type,
    message: msg,
    position: "bottom-right",
  });
}

function onCancelClick() {
    onDialogCancel()
}

const handleSubmit = () => {
  const inp_name = accountName.value;
  const inp_type = accountType.value.toLowerCase();
  const inp_balance = parseFloat(accountBalance.value);
  if (
    inp_name.length !== 0 &&
    inp_type.length !== 0
  ) {
    isLoading.value = true;
    const account = {
        account_id: accountID.value,
      account_name: inp_name,
      account_type: inp_type,
      account_balance: inp_balance,
    };
    transactionServiceAccounts
      .editAccount(account)
      .then((data) => {
        showNotif("Account edited successfully.", "positive");
        onDialogOK(data)
      })
      .catch((err) => {
        console.log("Unable to edit account");
        console.log(err);
        showNotif("Unable to edit account.", "negative");
      });
    isLoading.value = false;
  } else {
    accountNameRef.value.validate();
    accountTypeRef.value.validate();
    accountBalanceRef.value.validate();
  }
};
</script>

<template>
  <q-dialog ref="dialogRef">
    <q-card flat class="bg-cream-white q-pa-lg shadow-1">
      <q-card-section class="card-header">
        <p class="card-header-text">Edit Account</p>
      </q-card-section>
      <q-card-section>
        <q-form class="q-gutter-md">
          <q-input
            ref="accountNameRef"
            v-model="accountName"
            outlined
            standout="bg-white text-black"
            type="text"
            label="Name"
            :rules="checkInput"
          />
          
          <q-input
            ref="accountTypeRef"
            v-model="accountType"
            outlined
            standout="bg-white text-black"
            type="text"
            label="Type"
            :rules="checkInput"
          />
          <q-input
            ref="accountBalanceRef"
            v-model="accountBalance"
            outlined
            standout="bg-white text-black"
            type="number"
            label="Balance"
            prefix="$"
            :rules="checkAmount"
          />
          
        </q-form>
      </q-card-section>
      <q-card-actions class="q-px-md card-buttons">
        <q-btn
          unelevated
          flat
          size="md"
          label="Edit"
          :loading="isLoading"
          @click="handleSubmit"
        />
        <q-btn
          unelevated
          flat
          size="md"
          label="Cancel"
          @click="onCancelClick"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped lang="sass">
.card-header-text 
  font-size: 2rem

.card-buttons 
  justify-content: space-between

.bg-cream-white
  background: $primary
</style>
