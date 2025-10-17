<template>

<nav class="navbar navbar-expand-lg bg-body-tertiary px-3 bg-dark border-bottom border-body w-100">
        <div class="container-fluid">
          <div class="logo-container ps-4 pt-3 me-4">
            <img src="/static/Quiz Master.png" alt="Quiz Master" width="90" height="80" />
          </div>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item" mx-2>
                <RouterLink class="nav-link" to="/admin/home">Home</RouterLink>
              </li>
              <li class="nav-item" mx-2>
                <RouterLink class="nav-link" to="/admin/quiz">Quiz</RouterLink>
              </li>
              <li class="nav-item" mx-2>
                <RouterLink class="nav-link" to="/summary">Summary</RouterLink>
              </li>
              
            <form class="d-flex" role="search" @submit.prevent="search" mx-4>
              <input v-model="searchQuery" class="form-control me-2 w-auto" type="search" placeholder="Search" aria-label="Search" name="search">
              <select v-model="searchKey" class="form-select me-2" aria-label="Default select example" name="key">
              <option disabled value="" selected>Select</option>
              <option value="user">User</option>
              <option value="subject">Subject</option>
              <option value="quiz">Quiz</option>
              </select>
              <button class="btn btn-outline-success">Search</button>
            </form>
            
            </ul>
            <ul class="nav justify-content-end">
              <li class="nav-item">
                <a class="nav-link">Welcome {{ userName }}</a>
              </li>
              <li class="nav-item" mx-2>
                <a class="nav-link" href="/" @click="logout">Logout</a>
              </li>
            </ul>
          </div>
        </div>
</nav>
<RouterView />
</template>

<script setup>
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth.js'
import { ref, computed } from 'vue'

const router = useRouter()

const authStore = useAuthStore()
const route = useRoute()

const userName = computed(() => {
  return authStore.getUserName() || 'Quiz Master'
})

const searchQuery = ref('')
const searchKey = ref('')
const results = ref([])
const errormsg = ref('')

function logout() {
  authStore.clearAuthToken()
  route.push('/')
}

const search = () => {
  if (!searchQuery.value || !searchKey.value) return
  router.push({ 
    path: '/admin/search', 
    query: { 
      search: searchQuery.value, 
      key: searchKey.value 
      }
    })
}
</script>