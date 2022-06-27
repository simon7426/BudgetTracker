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
})

const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } =
  useDialogPluginComponent();
const options = ["Income", "Expense"];
const categoryID = ref(props.row.id)
const categoryName = ref(props.row.category_name);
const categoryNameRef = ref(null);
const categoryType = ref(props.row.category_type.replace(/^./, props.row.category_type[0].toUpperCase()));
const categoryTypeRef = ref(null);
const isLoading = ref(false);

const checkInput = [(val) => !!val || "Field is required"];
const checkCategoryType = [
  (val) =>
    val.toLowerCase() == "income" ||
    val.toLowerCase() === "expense" ||
    "Please select a value from the dropdown.",
];

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
  const inp_name = categoryName.value;
  const inp_type = categoryType.value.toLowerCase();
  console.log(inp_name, inp_type)
  if (
    inp_name.length !== 0 &&
    (inp_type === "income" || inp_type === "expense")
  ) {
    isLoading.value = true;
    const category = {
      category_id: categoryID.value,
      category_name: inp_name,
      category_type: inp_type,
    };
    transactionServiceCategory
      .editCategory(category)
      .then((data) => {
        showNotif("Category edited successfully.", "positive");
        onDialogOK(data)
      })
      .catch((err) => {
        console.log("Unable to edit category");
        console.log(err);
        showNotif("Unable to edit category.", "negative");
      });
    isLoading.value = false;
  } else {
    categoryNameRef.value.validate();
    categoryTypeRef.value.validate();
  }
};
</script>

<template>
  <q-dialog ref="dialogRef">
    <q-card flat class="bg-cream-white q-pa-lg shadow-1">
      <q-card-section class="card-header">
        <p class="card-header-text">Edit Category</p>
      </q-card-section>
      <q-card-section>
        <q-form class="q-gutter-md">
          <q-input
            ref="categoryNameRef"
            v-model="categoryName"
            outlined
            standout="bg-white text-black"
            type="text"
            label="Name"
            :rules="checkInput"
          >
          </q-input>
          <q-select
            ref="categoryTypeRef"
            v-model="categoryType"
            standout="bg-white text-black"
            outlined
            :options="options"
            label="Type"
            :rules="checkCategoryType"
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
