<template>

<nav class="navbar navbar-expand-lg bg-body-tertiary px-3 bg-dark border-bottom border-body w-100">
        <div class="container-fluid">
          <div class="logo-container ps-4 pt-3 me-4">
            <center><img src="/static/Quiz Master.png" alt="Quiz Master" width="90" height="80" /></center>
          </div>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item" mx-2>
                <RouterLink class="nav-link" to="/user/home">Home</RouterLink>
              </li>
              <li class="nav-item" mx-2>
                <RouterLink class="nav-link" to="/user/scores">Scores</RouterLink>
              </li>
              <li class="nav-item" mx-2>
                <RouterLink class="nav-link" to="/summary">Summary</RouterLink>
              </li>
              <li class="nav-item" mx-2>
                <a class="nav-link" href="/" @click="logout">Logout</a>
              </li>
            </ul>
                <h5 class="text-center">Welcome to the Quiz Master App</h5>
            
          </div>
        </div>
</nav>
<RouterView />
</template>

<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth.js'
import { ref, computed } from 'vue'

const authStore = useAuthStore()
const route = useRoute()

const userName = computed(() => {
  return authStore.getUserName() 
})

const searchQuery = ref('')
const searchKey = ref('')

function logout() {
  authStore.clearAuthToken()
  route.push('/')
}

function search() {
  alert(`Searching for ${searchKey.value}: ${searchQuery.value}`)
}
</script>