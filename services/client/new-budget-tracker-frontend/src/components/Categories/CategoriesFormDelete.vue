/* eslint-disable vue/require-default-prop */
<script setup>
import { ref, toRefs } from "vue";
import transactionServiceCategory from "../../services/category.transaction.service";
import { useDialogPluginComponent, useQuasar } from "quasar";

const props = defineProps({
  row: {
    type: Object,
    default: () => {},
  },
});

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();
const options = ["Income", "Expense"];
const categoryID = ref(props.row.id);
const isLoading = ref(false);

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
  console.log(`Delete Category ${categoryID.value}`);
  transactionServiceCategory
    .deleteCategory(categoryID.value)
    .then((data) => {
      console.log(data);
      showNotif("Category deleted successfully.", "positive");
      onDialogOK();
    })
    .catch((err) => {
      console.log("Unable to add category");
      console.log(err);
      showNotif("Unable to delete category.", "negative");
    });
  isLoading.value = false;
};
</script>

<template>
  <q-dialog ref="dialogRef">
    <q-card flat class="bg-cream-white q-pa-lg shadow-1">
      <q-card-section class="card-header">
        <p class="card-header-text">Are you sure you want to delete?</p>
      </q-card-section>
      <q-card-actions class="q-px-md card-buttons">
        <q-btn
          unelevated
          flat
          size="md"
          label="Delete"
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
  font-size: 1.5rem
  text-align: center

.card-buttons
  justify-content: space-between

.bg-cream-white
  background: $primary
</style>
