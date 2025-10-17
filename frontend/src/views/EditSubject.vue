<template>
<AdminNavBar />
<br>
<div class="card container-fluid justify-content-center text-bg-light mb-3 p-4 shadow" style="width: 100%; max-width: 600px;">
<center><h3>Edit Subject</h3></center>
<div class="container-fluid">
    <form @submit.prevent="Editsub">
        <div class="mb-3">
            <br>
            <label class="form-label"><b>Subject</b></label>
            <input type="text" class="form-control" name = 'subject' v-model="name" required>
        </div>
        <div class="mb-3">
            <label class="form-label"><b>Description</b></label><br>
            <textarea name="description" rows="6" cols="70" class="form-control" v-model="description" required></textarea>
        </div>
        <button type="reset" class = "btn btn-danger">Clear</button> <button type="submit" class = "btn btn-success">Submit</button>
        
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

const name = ref('')
const description = ref('')

const subjID = route.params.subject_id

onMounted(async () => {
    try {
    const response = await fetch(`http://127.0.0.1:5000/api/subjects/${subjID}`)
    if (!response.ok) throw new Error('Failed to fetch subject data')
    const data = await response.json()
    name.value = data.name
    description.value = data.description
    } catch(err) {
        alert('Error fetching subject details.')
        console.error(err)
    }
})

async function Editsub(){
    if (!name.value || !description.value){
        alert("Please fill in all the fields")
        return
    }
    const sub = {
        name: name.value,
        description: description.value
    }

    const response = await fetch(`http://127.0.0.1:5000/api/edit-subject/${subjID}`,{
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(sub)
    })
    
    if(!response.ok){
        const errorData = await response.json();
        alert(errorData.message);
        return;
    }
    else{
        const data = await response.json();
        alert(data.message);
        router.push('/admin/home');
    }
}
</script>