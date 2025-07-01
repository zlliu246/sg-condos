<script setup>
defineProps(["tableData"])
</script>

<template>
    <table
        style="z-index:10; position:relative"
        class="result-table table table-light table-striped" 
        v-if="tableData.length > 0"
    >
        <!-- TABLE HEADERS -->
        <thead>
            <tr>
                <th v-for="col in Object.keys(tableData[0])">
                    {{ col }}
                </th>
            </tr>
        </thead>
        <!-- TABLE ROWS -->
        <tbody>
            <tr v-for="row in tableData">
                <td v-for="col in row">{{ col }}</td>
            </tr>
        </tbody>
    </table>
</template>