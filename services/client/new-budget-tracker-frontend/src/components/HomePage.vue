<script setup>
import CategoriesTable from "./CategoriesTable.vue";
import AccountsTable from "./AccountsTable.vue";
</script>
<template>
<q-page-container class="bg-cream-white window-height window-width">
    <div class="categoriesTable">

    <AccountsTable />
    </div>
</q-page-container>
</template>

<style scoped lang="sass">
.categoriesTable
    padding: 1rem
</style>