<template>
<AdminNavBar />
<br />
<h2><center><b>Quizes</b></center></h2>
<div class="text-center">
    <RouterLink to="/admin/add-quiz">
        <img src="/static/add.jpeg" alt="Add Subject" width="80" height="80" />
    </RouterLink>
</div>
<div class="container">
  <div class = "row justify-content-center">
    <div class="col-md-5 mb-3" v-for="chapter in Object.values(chapters).flat()" :key="chapter.chapter_id">
          <div class = "card p-4 mb-4 container-fluid justify-content-center text-bg-light shadow" style="width: 100%; max-width: 600px;" v-for="quiz in visiblequiz.filter(q => q.chap_id === chapter.chapter_id)" :key="quiz.Quiz_id">
            <table>
            <tbody>
              <tr>
                <td><h4><b>Quiz-{{ quiz.Quiz_id }} ({{ chapter.name }})</b></h4></td>
                <td>
                <RouterLink :to="`/admin/edit-quiz/${quiz.Quiz_id}`" class="btn btn-primary">Edit</RouterLink> <button @click="deletequiz(quiz.Quiz_id)" class="btn btn-warning">Delete</button>
                </td>
              </tr> 
              </tbody>
            </table>
        
            <p>Date of quiz : {{ quiz.date_of_quiz }} <br>
            Duration (hh:mm) : {{ quiz.time_duration }}</p>
        
              <table v-if="getquestions(quiz.Quiz_id).length" class="table table-bordered">
              <thead>
                <tr>
                  <th><b>Question ID</b></th>
                  <th><b>Question Title</b></th>
                  <th><b>Action</b></th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(question, index) in getquestions(quiz.Quiz_id)" :key="question.question_id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ question.Question_title }}</td>
                  <td><RouterLink :to="`/admin/edit-question/${question.question_id}`" class="btn btn-primary">Edit</RouterLink> <button @click="deletequestion(question.question_id)" class="btn btn-warning">Delete</button></td>
                </tr>
                </tbody>
              </table>
              <div class="text-center"><div class="d-grid gap-2 d-md-block">
            <RouterLink :to="`/admin/add-question/${quiz.Quiz_id}`" class="btn btn-success">+ Question</RouterLink>
            </div></div>
           </div> 
          </div>
        </div>
  </div>

</template>

<script setup>
import AdminNavBar from '@/components/AdminNavBar.vue'
import { RouterLink, RouterView, useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const router = useRouter()

const subjects = ref([])
const chapters = ref({})
const quizzes = ref([])
const questions = ref([])
const visiblequiz = ref([])

onMounted(async () => {
    await fetchData()
})

const fetchData = async () => {
    const sub = await axios.get('http://127.0.0.1:5000/api/subjects')
    subjects.value = sub.data.subjects
    
    for (const subject of subjects.value){
        const chap = await axios.get(`http://127.0.0.1:5000/api/chapters/${subject.subject_id}`)
        chapters.value[subject.subject_id] = chap.data.chapters
    }

    const quizresponse = await axios.get('http://127.0.0.1:5000/api/quizzes')
    quizzes.value = quizresponse.data.quizzes
    
    visiblequiz.value = []
    for (let i = 0; i< quizzes.value.length; i++) {
        setTimeout(() =>{
            visiblequiz.value = quizzes.value;
        }, i*120)
    }

    const quest = await axios.get('http://127.0.0.1:5000/api/questions')
    questions.value = quest.data.questions
}
const getquestions = (quizID) => {
    return questions.value.filter(q => q.quiz_id === quizID)
}
async function deletequiz(quizID) {
    const dlt = confirm("Are you sure you want to delete this quiz and all the related information?");
    if (!dlt) return;
    const response = await fetch(`http://127.0.0.1:5000/api/delete-quiz/${quizID}`,{
        method: 'DELETE'
    });
    const data = await response.json();
    if (!response.ok) {
        alert(data.message);
    }
    else{
        alert(data.message);
        visiblequiz.value = visiblequiz.value.filter(quiz => quiz.Quiz_id !== quizID);
        await fetchData();
    }
}

async function deletequestion(questionID) {
    const dlt = confirm("Are you sure you want to delete this question?");
    if (!dlt) return;
    const response = await fetch(`http://127.0.0.1:5000/api/delete-question/${questionID}`,{
        method: 'DELETE'
    });
    const data = await response.json();
    alert(data.message)
    await fetchData()
}

</script>
