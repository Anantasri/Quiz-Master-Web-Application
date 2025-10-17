<template>
<AdminNavBar />
<br>
<div class="card container-fluid justify-content-center text-bg-light mb-3 p-4 shadow" style="width: 100%; max-width: 600px;">
<center><h3>Edit Question</h3></center>
<div class="container-fluid">
    <form @submit.prevent="Editquestion">
        <div class="mb-3">
            <br>
            <label class="form-label"><b>Question Title</b></label>
            <input type="text" class="form-control" name = 'Question_title' v-model="Question_title" required>
        </div>
        <div class="mb-3">
            <label class="form-label"><b>Question Stetement</b></label><br>
            <textarea name="question_statement" rows="6" cols="70" class="form-control" v-model="Question_statement" required></textarea>
        </div>
        <div class="mb-3">
            <br>
            <label class="form-label"><b>Option A</b></label>
            <input type="text" class="form-control" name = 'option_a' v-model="option_a" required>
        </div>
        <div class="mb-3">
            <br>
            <label class="form-label"><b>Option B</b></label>
            <input type="text" class="form-control" name = 'option_b' v-model="option_b" required>
        </div>
        <div class="mb-3">
            <br>
            <label class="form-label"><b>Option C</b></label>
            <input type="text" class="form-control" name = 'option_c' v-model="option_c" required>
        </div>
        <div class="mb-3">
            <br>
            <label class="form-label"><b>Option D</b></label>
            <input type="text" class="form-control" name = 'option_d' v-model="option_d" required>
        </div>
        <div class="mb-3">
            <br>
            <label class="form-label"><b>Correct Answer</b></label>
            <select class="form-control" v-model="answer" required>
            <option value="" disabled>Select a chapter</option>
            <option value="option_a">Option A</option>
            <option value="option_b">Option B</option>
            <option value="option_c">Option C</option>
            <option value="option_d">Option D</option>
            </select>
        </div>
        <div class="text-center">
        <button type="reset" class = "btn btn-danger">Clear</button> <button type="submit" class = "btn btn-success">Submit</button>
        </div>
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

const Question_title = ref('')
const Question_statement = ref('')
const option_a = ref('')
const option_b = ref('')
const option_c = ref('')
const option_d = ref('')
const answer = ref('')

const questionID = route.params.question_id

onMounted(async () => {
    try {
    const response = await fetch(`http://127.0.0.1:5000/api/admin/edit-question/${questionID}`)
    if (!response.ok) throw new Error('Failed to fetch question data')
    const data = await response.json()
    Question_title.value = data.Question_title
    Question_statement.value = data.Question_statement
    option_a.value = data.option_a
    option_b.value = data.option_b
    option_c.value = data.option_c
    option_d.value = data.option_d
    answer.value = getanswerkey(data)
    } catch(err) {
        alert('Error fetching question details.')
    }
})

function getanswerkey(data){
    if (data.answer === data.option_a) return 'option_a'
    if (data.answer === data.option_b) return 'option_b'
    if (data.answer === data.option_c) return 'option_c'
    if (data.answer === data.option_d) return 'option_d'
    return ''
}
async function Editquestion(){
    if (!Question_title.value || !Question_statement.value || !option_a.value || !option_b.value || !option_c.value || !option_d.value || !answer.value){
        alert("Please fill in all the fields")
        return
    }
    const ques = {
        Question_title: Question_title.value,
        Question_statement: Question_statement.value,
        option_a: option_a.value,
        option_b: option_b.value,
        option_c: option_c.value,
        option_d: option_d.value,
        answer: answer.value
    }

    const response = await fetch(`http://127.0.0.1:5000/api/admin/edit-question/${questionID}`,{
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(ques)
        })
    
    
    if(!response.ok){
        const errorData = await response.json();
        alert(errorData.message);
    }
    else{
        const data = await response.json();
        alert(data.message);
        router.push('/admin/quiz');
    }
}
</script>