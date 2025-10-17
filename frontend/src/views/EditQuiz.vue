<template>
<AdminNavBar />
<br>
<div class="card container-fluid justify-content-center text-bg-light mb-3 p-4 shadow" style="width: 100%; max-width: 600px;">
<center><h3>Edit Quiz</h3></center>
<div class="container-fluid">
    <form @submit.prevent="Editquiz">
        <div class="mb-3">
            <br>
            <label class="form-label"><b>Chapter</b></label>
            <select class="form-control" v-model="chapterID" required>
            <option value="" disabled>Select a chapter</option>
            <option v-for="chapter in chapters" :key="chapter.chapter_id" :value="chapter.chapter_id">{{ chapter.name }}</option>
            </select>
        </div>

        <div class="mb-3">
            <label class="form-label"><b>Date of Quiz</b></label><br>
            <input type="date" class="form-control" v-model="date_of_quiz" required>
        </div>

        <div class="mb-3">
            <label class="form-label"><b>Time Duration</b></label><br>
            <input type="time" class="form-control" v-model="time_duration" required>
        </div>

        <div class="mb-3">
            <label class="form-label"><b>Remarks</b></label><br>
            <textarea class="form-control" rows="3" v-model="remarks" required></textarea>
        </div>
        
        <center>
        <button type="reset" class = "btn btn-danger">Clear</button> <button type="submit" class = "btn btn-success">Submit</button>
        </center>
        
    </form>
</div>
</div>
</template>

<script setup>
import AdminNavBar from '@/components/AdminNavBar.vue'
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const chapterID = ref('')
const date_of_quiz = ref('')
const time_duration = ref('')
const remarks = ref('')
const chapters = ref([])

const quizID = route.params.quiz_id

onMounted(async () => {
    try {
    const response = await fetch(`http://127.0.0.1:5000/api/admin/edit-quiz/${quizID}`)
    if (!response.ok) throw new Error('Failed to fetch quiz data')
    const data = await response.json()
    chapterID.value = data.chap_id
    date_of_quiz.value = data.date_of_quiz
    time_duration.value = data.time_duration
    remarks.value = data.remarks
    
    const chap = await fetch('http://127.0.0.1:5000/api/chapters')
    if (!chap.ok) throw new Error('Failed to fetch chapters')
    chapters.value = await chap.json()

    } catch(err) {
        alert('Error fetching quiz details.')
        console.error(err)
    }
})

async function Editquiz(){
    if (!chapterID.value || !date_of_quiz.value || !time_duration.value || !remarks.value){
        alert("Please fill in all the fields")
        return
    }
    const updatequiz = {
        chap_id: chapterID.value,
        date_of_quiz: date_of_quiz.value,
        time_duration: time_duration.value,
        remarks: remarks.value
    }
    
    const response = await fetch(`http://127.0.0.1:5000/api/admin/edit-quiz/${quizID}`,{
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(updatequiz)
    })
    
    if(!response.ok){
        const errorData = await response.json();
        alert(errorData.message);
        return;
    }
    else{
        const data = await response.json();
        alert(data.message);
        router.push('/admin/quiz');
    }
}
</script>