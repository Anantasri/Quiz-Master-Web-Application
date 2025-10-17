<template>
<AdminNavBar />
<br />
<div class="card container-fluid justify-content-center text-bg-light mb-3 p-4 shadow" style="width: 100%; max-width: 600px;">
<div class="text-center"><h3>Add New Question</h3></div>
<div class="container-fluid">
    <form @submit.prevent="Addquestion">
    
    <div class="mb-3">
    <label class="form-label"><b>Question Title</b></label>
    <input type="text" class="form-control" v-model="question_title" required />
    </div>

    <div class="mb-3">
    <label class="form-label"><b>Question Statement</b></label>
    <textarea v-model="question_statement" rows="3" class="form-control" required></textarea>
    </div>
    
    <div class="mb-3">
    <label class="form-label"><b>Option A</b></label>
    <input type="text" class="form-control" v-model="option_a" required />
    </div>
    <div class="mb-3">
    <label class="form-label"><b>Option B</b></label>
    <input type="text" class="form-control" v-model="option_b" required />
    </div>
    <div class="mb-3">
    <label class="form-label"><b>Option C</b></label>
    <input type="text" class="form-control" v-model="option_c" required />
    </div>
    <div class="mb-3">
    <label class="form-label"><b>Option D</b></label>
    <input type="text" class="form-control" v-model="option_d" required />
    </div>

    <div class="mb-3">
    <label class="form-label"><b>Correcrt Answer</b></label>
    <select class="form-control" v-model="answer" required>
    <option disabled value="" selected>Select</option>
    <option value="option_a">Option A</option>
    <option value="option_b">Option B</option>
    <option value="option_c">Option C</option>
    <option value="option_d">Option D</option>
    </select>
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
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const quizID = route.params.quiz_id;

const question_title = ref('');
const question_statement = ref('');
const option_a = ref('');
const option_b = ref('');
const option_c = ref('');
const option_d = ref('');
const answer = ref('');

async function Addquestion() {
    if (
        !question_title.value || !question_statement.value || !option_a.value || !option_b.value || !option_c.value || !option_d.value || !answer.value ){
            alert('Please fill in all the fields');
            return;
        }
    const question = {
        question_title: question_title.value,
        question_statement: question_statement.value,
        option_a: option_a.value,
        option_b: option_b.value,
        option_c: option_c.value,
        option_d: option_d.value,
        answer: answer.value
    };

    const response = await fetch(`http://127.0.0.1:5000/api/admin/add-question/${quizID}`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(question),
    });
    const data = await response.json();
    if(!response.ok){
        alert(data.message);
    }
    else{
        alert(data.message);
        router.push('/admin/quiz');
    }
}
</script>

