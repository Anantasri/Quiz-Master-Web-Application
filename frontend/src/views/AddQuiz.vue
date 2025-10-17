<template>
<AdminNavBar />
<br />
<div class="card container-fluid justify-content-center text-bg-light mb-3 p-4 shadow" style="width: 100%; max-width: 600px;">
<div class="text-center"><h3>Add New Quiz</h3></div>
<div class="container-fluid">
    <form @submit.prevent="Addquiz">
    
    <div class="mb-3">
    <label class="form-label"><b>Subject</b></label>
    <select v-model="selectedsubject" class="form-control" @change="fetchchapters" required>
    <option disabled value="">Select</option>
    <option v-for="sub in subjects" :key="sub.subject_id" :value="sub.subject_id">
    {{ sub.name }}
    </option>
    </select>
    </div>

    <div class="mb-3">
    <label class="form-label"><b>Chapter</b></label>
    <select v-model="quiz.chapter_id" class="form-control" required>
    <option disabled value = "">Select</option>
    <option v-for="chap in chapters" :key="chap.chapter_id" :value="chap.chapter_id">
    {{ chap.name }}
    </option>
    </select>
    </div>

    <div class="mb-3">
    <label class="form-label"><b>Date Of Quiz</b></label>
    <input type="date" v-model="quiz.date_of_quiz" class="form-control" @input = "validatedate" required/>
    <div v-if="dateError" class="form-text">{{ dateError }}</div>
    </div>

    <div class="mb-3">
    <label class="form-label"><b>Time Duration</b></label>
    <input type="time" v-model="quiz.time_duration" class="form-control" required/>
    </div>

    <div class="mb-3">
    <label class="form-label"><b>Remarks</b></label>
    <textarea v-model="quiz.remarks" rows="3" class="form-control" required></textarea>
    </div>

    <div class="text-center">
    <button type="reset" class = "btn btn-danger">Clear</button>  <button type="submit" class = "btn btn-success">Submit</button>
    </div>
    </form>
    </div>
</div>
</template>

<script setup>
import AdminNavBar from '@/components/AdminNavBar.vue';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const subjects = ref([]);
const chapters = ref([]);
const selectedsubject = ref('');

const quiz = ref({
    chapter_id: '',
    date_of_quiz: '',
    time_duration: '',
    remarks: ''
});

const dateError = ref('');

const validatedate = () => {
    const today = new DAte();
    selected.setHours(0,0,0,0);
    today.setHours(0,0,0,0);
    if (selected < today){
        dateError.value = "Please select today or a future date";
        return false;
    }
    else{
        emailerror.value = '';
        return true;
    }
};

onMounted(async () => {
    const response = await fetch('http://127.0.0.1:5000/api/subjects');
    const data = await response.json();
    subjects.value = data.subjects;
});

async function fetchchapters(){
    if(!selectedsubject.value) return;

    const response = await fetch(`http://127.0.0.1:5000/api/chapters/${selectedsubject.value}`);
    const data = await response.json();
    chapters.value = data.chapters;
}

async function Addquiz() {
    const q = quiz.value;
    if (!q.chapter_id || !q.date_of_quiz || !q.time_duration || !q.remarks.trim()){
        alert('Please enter all fields');
        return;
    }

    const response = await fetch('http://127.0.0.1:5000/api/admin/add-quiz', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(q)
    });

    const result = await response.json();

    if(!response.ok) {
        alert(result.message);
    }
    else{
        alert(result.message);
        router.push('/admin/quiz');
    }
}
</script>

