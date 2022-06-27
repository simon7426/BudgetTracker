<script setup>
import { computed, ref } from "vue";
import transactionServiceTransfer from "../../services/transfers.transaction.service";
import { useDialogPluginComponent, useQuasar } from "quasar";

const props = defineProps({
  accountTable: {
    type: Array,
    default: () => [],
  },
  row: {
    type: Object,
    default: () => {},
  },
});

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();

console.log(props.row)

const accountOptions = ref(props.accountTable);
const options = ref(accountOptions.value);

const transferId = ref(props.row.id)
const fromAccount = ref(props.row.from_account);
const fromAccountRef = ref(null);
const toAccount = ref(props.row.to_account);
const toAccountRef = ref(null);
const transferAmount = ref(props.row.transfer_amount);
const transferAmountRef = ref(null);

const isLoading = ref(false);

const checkInput = [(val) => !!val || "Field is required"];
const checkAmount = [(val) => val > 0 || "Amount must be positive"];

const q = useQuasar();

function showNotif(msg, type) {
  q.notify({
    type: type,
    message: msg,
    position: "bottom-right",
  });
}

function onCancelClick() {
  onDialogCancel();
}

function filterFn(val, update) {
  if (val === "") {
    update(() => {
      options.value = accountOptions.value;
    });
    return;
  }
  update(() => {
    const needle = val.toLowerCase();
    options.value = accountOptions.value.filter(
      (v) => v.account_name.toLowerCase().indexOf(needle) > -1
    );
  });
}

const isError = computed(() => {
  return fromAccount.value === toAccount.value && fromAccount.value !== "";
});

const handleSubmit = () => {
    const transfer_id = transferId.value;
  const from_account_id = fromAccount.value.id;
  const to_account_id = toAccount.value.id;
  const transfer_amount = parseFloat(transferAmount.value);
  if (from_account_id && to_account_id && transferAmount) {
    isLoading.value = true;
    const transfer = {
        transfer_id,
      from_account_id,
      to_account_id,
      transfer_amount,
    };

    transactionServiceTransfer
      .editTranfer(transfer)
      .then((data) => {
        console.log(data);
        showNotif("Transfer edited successfully.", "positive");
        onDialogOK(data);
      })
      .catch((err) => {
        console.log("Unable to add account");
        console.log(err);
        showNotif("Unable to add account.", "negative");
      });
    isLoading.value = false;
  } else {
    fromAccountRef.value.validate();
    toAccountRef.value.validate();
    transferAmountRef.value.validate();
  }
};
</script>

<template>
  <q-dialog ref="dialogRef">
    <q-card flat class="bg-cream-white q-pa-lg shadow-1">
      <q-card-section class="card-header">
        <p class="card-header-text">Edit Transfer</p>
      </q-card-section>
      <q-card-section>
        <q-form class="q-gutter-md">
          <q-select
            ref="fromAccountRef"
            v-model="fromAccount"
            hint="From Account"
            filled
            use-input
            input-debounce="0"
            label="From"
            behavior="menu"
            options-selected-class="bg-light-green-3 text-grey-9"
            :options="options"
            option-value="id"
            option-label="account_name"
            :rules="checkInput"
            error-message="Cannot transfer between same accounts."
            :error="isError"
            @filter="filterFn"
          >
            <template #no-option>
              <q-item>
                <q-item-section class="text-grey"> No results </q-item-section>
              </q-item>
            </template>
          </q-select>

          <q-select
            ref="toAccountRef"
            v-model="toAccount"
            hint="To Account"
            filled
            use-input
            input-debounce="0"
            label="To"
            behavior="menu"
            options-selected-class="bg-light-green-3 text-grey-9"
            :options="options"
            option-value="id"
            option-label="account_name"
            :rules="checkInput"
            error-message="Cannot transfer between same accounts."
            :error="isError"
            @filter="filterFn"
          >
            <template #no-option>
              <q-item>
                <q-item-section class="text-grey"> No results </q-item-section>
              </q-item>
            </template>
          </q-select>

          <q-input
            ref="transferamountRef"
            v-model="transferAmount"
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
