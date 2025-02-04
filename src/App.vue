<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'

const headerLinks = [
  {name:'Home', path:'/'},
  {name:'About', path:'/about'},
];

</script>

<template>
  <header class="p-2">
    <span v-for="row of headerLinks" :key="row.name">
      <RouterLink :to="row.path" class="topbar-name">{{row.name}}</RouterLink>
    </span>
  </header>

  <RouterView />

  <footer>
    <br>
    <br>
  </footer>
</template>

<style>

header {
  box-shadow: 0 0 1px 1px #ccc!important;
  text-align: right; 
  margin-bottom:3px;
}

header span {
  margin: 0.5em;
}

.topbar-name {
  text-decoration: none !important;
}

.topbar-name:hover {
  font-weight: 500;
}

</style>
