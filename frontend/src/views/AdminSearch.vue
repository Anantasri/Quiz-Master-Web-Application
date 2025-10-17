<template>
<AdminNavBar />
<div class="container mt-4">
<h3>Search Result</h3>
<div class="card container-fluid justify-content-center text-bg-light mb-3 p-4 shadow" style="width: 100%; max-width: 600px;">
<p v-if="searchQuesry && searchKey">
Showing results for "<strong>{{ searchQuery }}</strong>" in <strong>{{ searchKey }}</strong>
</p>

<div v-if="results.length > 0">
<ul v-if="searchKey =='user'">
<li v-for="(item, index) in results" :key="index">
    Name: {{ item.name }}<br />
    Email:{{ item.email }}<br />
    Qualification: {{ item.qualification }}<br />
    Date of Birth: {{ item.DOB }}
</li>
</ul>

<ul v-if="searchKey === 'quiz'">
<li v-for="(item, index) in results" :key="index">
    Quiz ID: {{ item.quiz_id }}<br />
    Chapter: {{ item.chapter }}<br />
    Date: {{ item.date }}<br />
    Reamrks: {{ item.remarks }}
</li>
</ul>
</div>
<p v-else>No Results found.</p>
</div>
</div>
</template>

<script setup>
import AdminNavBar from '@/components/AdminNavBar.vue'
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const route = useRoute()

const searchQuery = route.query.search || ''
const searchKey = route.query.key || ''
const results = ref([])

onMounted(async () => {
    if(!searchQuery || !searchKey) return

    try{
        const response = await axios.get('/api/search', {
            params: {
                search: searchQuery,
                key: searchKey
            }
        })
        results.value = response.data.results
    } catch(error){
        console.error('Error fetching search results:', error)
    }
})
</script>