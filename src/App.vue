<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'

const headerLinks = [
  {name:'Home', path:'/'},
  {name:'About', path:'/about'},
];

function redirectGithub() {
  window.open("https://github.com/zlliu246/sg-condos", "_blank");
}

</script>

<template>
  <header class="p-2">
    <!-- <span v-for="row of headerLinks" :key="row.name">
      <RouterLink :to="row.path" class="topbar-name">{{row.name}}</RouterLink>
    </span> -->

    <span>
      <RouterLink :to="'/'" class="topbar-name">Home</RouterLink>
    </span>

    <span>
      <span class="topbar-name" @click="redirectGithub">About</span>
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
  text-align: left; 
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
