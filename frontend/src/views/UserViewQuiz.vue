<template>
<UserNavBar />
<br />
<div class="card container-fluid justify-content-center text-bg-light mb-3 p-4 shadow" style="width: 100%; max-width: 350px;">
  <div class="card-body p-3 justify-content-center">
  <div class="text-center"><h4>Quiz - {{ quiz.Quiz_id }}</h4></div>
  <p>
  Subject: {{ subject.name }}<br>
  Description: {{ subject.description }}
  </p>
  <p>
  Chapter: {{ chapter.name }}<br>
  Description: {{ chapter.description }}
  </p>
  <p>
  Quiz Date: {{ quiz.date_of_quiz }}<br>
  Duration (hh:mm): {{ quiz.time_duration }}<br>
  Number of Questions: {{ question_count }}<br>
  Remarks: {{ quiz.remarks }}
  </p>
  </div>
<center><RouterLink to="/user/home" class="btn btn-danger">Close</RouterLink></center>
</div>
</template>

<script setup>
import UserNavBar from '@/components/UserNavBar.vue'
import axios from 'axios'
import { RouterLink, useRoute } from 'vue-router'
import { onMounted, ref } from 'vue'

const route = useRoute()
const quizID = route.params.quiz_id

const quiz = ref({})
const subject = ref({})
const chapter = ref({})
const question_count = ref(0)

onMounted(async () => {
    const response = await axios.get(`http://127.0.0.1:5000/api/quiz-details/${quizID}`)
    quiz.value = response.data.quiz
    subject.value = response.data.subject
    chapter.value = response.data.chapter
    question_count.value = response.data.question_count
})
</script>