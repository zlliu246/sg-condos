<script setup>
defineProps(["schemaMetadata"])
</script>

<template>
    <div class="meta-table" style="position:relative; z-index:1">

        <table class="table table-light table-striped table-sm">
            <thead>
                <tr>
                    <th>{{ schemaMetadata.name }}</th>
                    <th>{{ schemaMetadata.desc }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="col in schemaMetadata.columns">
                <td>{{ col.name }}</td>
                <td>{{ col.desc }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style>
.meta-table {
    font-size: 80%!important
}
</style>