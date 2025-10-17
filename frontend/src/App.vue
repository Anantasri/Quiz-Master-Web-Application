<template>
<nav v-if="shouldshow" class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
          <div class="logo-container ps-4 pt-3 me-4">
            <img src="/static/Quiz Master.png" alt="Quiz Master" width="90" height="80" />
          </div>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav">
        <li class="nav-item">
          <RouterLink class="nav-link active" to="/login">Login</RouterLink>
        </li>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/register">Register</RouterLink>
        </li>
      </ul>
    </div>
  </div>
</nav>

<RouterView />

</template>

<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router';
import { computed } from 'vue';
import { useAuthStore } from '@/stores/auth.js';
const route = useRoute();
const authStore = useAuthStore();

const shouldshow = computed(() => {
  const r = ['/','/login','/register']
  return r.includes(route.path) 
});

</script>
