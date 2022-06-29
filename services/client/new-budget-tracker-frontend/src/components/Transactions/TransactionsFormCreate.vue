<script setup>
import { computed, ref } from "vue";
import transactionService from "../../services/transactions.transaction.service";
import { useDialogPluginComponent, useQuasar } from "quasar";

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();

const options = ["Income", "Expense"];
const dateOption = {
  year: "numeric",
  month: "long",
  day: "numeric",
};
const today = new Date();
const transactionDate = ref(today.toISOString().substring(0, 10));
const transactionDateRef = ref(null);
const transactionDateFormatted = ref(
  today.toLocaleDateString("en-US", dateOption)
);
const transactionDateFormattedRef = ref(null);
const transactionType = ref("");
const transactionTypeRef = ref(null);
const transactionDescription = ref("");
const transactionDescriptionRef = ref(null);
const transactionAmount = ref(0);
const transactionAmountRef = ref(null);
const transactionCategory = ref("");
const transactionCategoryRef = ref(null);
const transactionAccount = ref("");
const transactionAccountRef = ref(null);
const isLoading = ref(false);

const props = defineProps({
  accountTable: {
    type: Array,
    default: () => [],
  },
  categoryTable: {
    type: Array,
    default: () => [],
  },
});

const accountOptions = ref(props.accountTable);
const optionsAccount = ref(accountOptions.value);

const categoryOptions = ref(props.categoryTable);
const optionsCategory = ref(categoryOptions.value);

const checkInput = [(val) => !!val || "Field is required"];
const checkAmount = [(val) => val > 0 || "Amount must be positive"];

const checkTransactionType = [
  (val) =>
    val.toLowerCase() === "income" ||
    val.toLowerCase() === "expense" ||
    "Please select a value from dropdown",
];

function filterAccount(val, update) {
  if (val === "") {
    update(() => {
      optionsAccount.value = accountOptions.value;
    });
    return;
  }
  update(() => {
    const needle = val.toLowerCase();
    optionsAccount.value = accountOptions.value.filter(
      (v) => v.account_name.toLowerCase().indexOf(needle) > -1
    );
  });
}

function filterCategory(val, update) {
  if (transactionType.value === "") {
    if (val === "") {
      update(() => {
        optionsCategory.value = categoryOptions.value;
      });
      return;
    }
    update(() => {
      const needle = val.toLowerCase();
      optionsCategory.value = categoryOptions.value.filter(
        (v) => v.category_name.toLowerCase().indexOf(needle) > -1
      );
    });
  } else {
    if (val === "") {
      update(() => {
        optionsCategory.value = categoryOptions.value.filter(
          (v) =>
            v.category_type.toLowerCase() ===
            transactionType.value.toLowerCase()
        );
      });
    } else {
      update(() => {
        optionsCategory.value = categoryOptions.value.filter(
          (v) =>
            v.category_type.toLowerCase() ===
              transactionType.value.toLowerCase() &&
            v.category_name.toLowerCase().indexOf(needle) > -1
        );
      });
    }
  }
}

function updateType() {
  transactionType.value = transactionCategory.value.category_type.replace(
    /^./,
    transactionCategory.value.category_type[0].toUpperCase()
  );
}

function updateCategory() {
  if (
    transactionCategory.value !== "" &&
    transactionCategory.value.category_type.toLowerCase() !==
      transactionType.value.toLowerCase()
  ) {
    transactionCategory.value = "";
  }
}

function updateDate() {
  transactionDateFormatted.value = new Date(transactionDate.value).toLocaleDateString('en-US', dateOption)
}

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

const handleSubmit = () => {
  const inp_date = transactionDate.value;
  const inp_type = transactionType.value.toLowerCase();
  const inp_description = transactionDescription.value;
  const inp_amount = parseFloat(transactionAmount.value);
  const inp_category = transactionCategory.value;
  const inp_account = transactionAccount.value;
  if (
    (inp_type === "income" || inp_type == "expense") &&
    inp_type === transactionCategory.value.category_type &&
    inp_description.length !== 0 &&
    inp_amount > 0 &&
    inp_category !== "" &&
    inp_account !== "" &&
    inp_date !== ""
  ) {
    const inp_category_id = inp_category.id;
    const inp_account_id = inp_account.id;
    isLoading.value = true;
    const transaction = {
      transaction_type: inp_type,
      transaction_date: inp_date,
      transaction_amount: inp_amount,
      transaction_description: inp_description,
      transaction_category_id: inp_category_id,
      transaction_account_id: inp_account_id,
    };
    transactionService
      .addTransaction(transaction)
      .then((data) => {
        showNotif("Transaction added successfully.", "positive");
        onDialogOK(data);
      })
      .catch((err) => {
        console.log("Unable to add transaction.");
        console.log(err);
        showNotif("Unable to add transaction.", "negative");
      });
    isLoading.value = false;
  } else {
    transactionDateFormattedRef.value.validate();
    transactionTypeRef.value.validate();
    transactionAmountRef.value.validate();
    transactionDescriptionRef.value.validate();
    transactionCategoryRef.value.validate();
    transactionAccountRef.value.validate();
  }
};
</script>

<template>
  <q-dialog ref="dialogRef">
    <q-card flat class="bg-cream-white q-pa-lg shadow-1">
      <q-card-section class="card-header">
        <p class="card-header-text">Add Transaction</p>
      </q-card-section>
      <q-card-section>
        <q-form class="q-gutter-md">
          <q-input
            ref="transactionDateFormattedRef"
            v-model="transactionDateFormatted"
            outlined
            readonly
            :rules="['checkInput']"
          >
            <template #append>
              <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy
                  cover
                  transition-show="scale"
                  transition-hide="scale"
                >
                  <q-date
                    ref="transactionDateRef"
                    v-model="transactionDate"
                    mask="YYYY-MM-DD"
                    color="light-green-5"
                    @update:model-value="updateDate"
                  >
                    <div class="row items-center justify-end">
                      <q-btn v-close-popup label="Close" flat />
                    </div>
                  </q-date>
                </q-popup-proxy>
              </q-icon>
            </template>
          </q-input>

          <q-select
            ref="transactionTypeRef"
            v-model="transactionType"
            standout="bg-white text-black"
            outlined
            options-selected-class="bg-light-green-3 text-grey-9"
            :options="options"
            label="Type"
            :rules="checkTransactionType"
            @update:model-value="updateCategory"
          />
          <q-input
            ref="transactionDescriptionRef"
            v-model="transactionDescription"
            outlined
            standout="bg-white text-black"
            type="text"
            label="Description"
            :rules="checkInput"
          />
          <q-input
            ref="transactionAmountRef"
            v-model="transactionAmount"
            outlined
            standout="bg-white text-black"
            type="number"
            label="Amount"
            prefix="$"
            :rules="checkAmount"
          />
          <q-select
            ref="transactionCategoryRef"
            v-model="transactionCategory"
            hint="Category"
            filled
            use-input
            input-debounce="0"
            label="Category"
            behavior="menu"
            options-selected-class="bg-light-green-3 text-grey-9"
            :options="optionsCategory"
            option-value="id"
            option-label="category_name"
            :rules="checkInput"
            @filter="filterCategory"
            @update:model-value="updateType"
          >
            <template #no-option>
              <q-item>
                <q-item-section class="text-grey"> No results </q-item-section>
              </q-item>
            </template>
          </q-select>
          <q-select
            ref="transactionAccountRef"
            v-model="transactionAccount"
            hint="Account"
            filled
            use-input
            input-debounce="0"
            label="Account"
            behavior="menu"
            options-selected-class="bg-light-green-3 text-grey-9"
            :options="optionsAccount"
            option-value="id"
            option-label="account_name"
            :rules="checkInput"
            @filter="filterAccount"
          >
            <template #no-option>
              <q-item>
                <q-item-section class="text-grey"> No results </q-item-section>
              </q-item>
            </template>
          </q-select>
        </q-form>
      </q-card-section>
      <q-card-actions class="q-px-md card-buttons">
        <q-btn
          unelevated
          flat
          size="md"
          label="Add"
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
