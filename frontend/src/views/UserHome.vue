<template>
  <div>
    <UserNavBar />
    <div class="container mt-4 d-flex flex-column align-items-center">
    <div v-if="quizzes.length > 0">
    <h3 class="mb-4"><b>Upcoming Quizzes</b></h3>
    <div v-for="quiz in quizzes" :key="quiz.Quiz_id" class="card text-bg-light p-3 mb-3 container-fluid justify-content-center shadow" style="width: 100%; max-width: 600px;">
    
    <h5 class="card-title">Quiz {{ quiz.Quiz_id }}</h5>
    <p class="card-text"><b>Chapter:</b> {{ getchaptername(quiz.chap_id) }}<br>
    <b>Date:</b> {{ quiz.date_of_quiz }}</p>
    <div>
    <RouterLink :to="`/user/quiz-view/${quiz.Quiz_id}`" class="btn btn-warning">View</RouterLink> <RouterLink :to="`/user/quiz-attempt/${quiz.Quiz_id}`" class="btn btn-success">Start</RouterLink>
    </div>
    </div>
    </div>

    <div v-else>
    <h3><b>No Upcoming Quizzes.</b></h3>
    </div>
    </div>
  </div>
</template>

<script setup>
import UserNavBar from '@/components/UserNavBar.vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { onMounted, ref } from 'vue'

const quizzes = ref([])
const chapters = ref([])

onMounted(async () => {
    try {
        const [quizresponse, chapresponse] = await Promise.all([
            axios.get('http://127.0.0.1:5000/api/upcoming-quizzes'),
            axios.get('http://127.0.0.1:5000/api/chapters')
        ])
        quizzes.value = quizresponse.data
        chapters.value = chapresponse.data
    } catch (err) {
        console.error('Error fetching the data',err)
    }
})

function getchaptername(chapID) {
    const chapter = chapters.value.find(c => c.chapter_id === chapID)
    return chapter ? chapter.name : 'Unknown'
}
</script>