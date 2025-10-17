<template>
<AdminNavBar />
<br>
<div class="card container-fluid justify-content-center text-bg-light mb-3 p-4 shadow" style="width: 100%; max-width: 600px;">
<center><h3>Add New Subject</h3></center>
<div class="container-fluid">
    <form @submit.prevent="Addsub">
        <div class="mb-3">
            <br>
            <label class="form-label"><b>Subject</b></label>
            <input type="text" class="form-control" name = 'subject' v-model='name' required>
        </div>
        <div class="mb-3">
            <label class="form-label"><b>Description</b></label><br>
            <textarea name="description" rows="6" cols="70" class="form-control" v-model='description' required></textarea>
        </div>
        <center><button type="reset" class = "btn btn-danger">Clear</button> <button type="submit" class = "btn btn-success">Submit</button></center>
    </form>
</div>
</div>
</template>

<script setup>
import AdminNavBar from '@/components/AdminNavBar.vue';
import {ref} from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const name = ref('');
const description = ref('');

async function Addsub(){
    if (name.value === '' || description.value === ''){
        alert("Please fill in all the fields");
        return;
    }

    const sub = {
        name: name.value,
        description: description.value
    };

    const response = await fetch("http://127.0.0.1:5000/api/add-subject",{
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(sub)
    });
    
    if(!response.ok){
        const errorData = await response.json();
        alert(errorData.message);
        name.value = ''
        description.value = ''
    }
    else{
        const data = await response.json();
        alert(data.message);
        router.push('/admin/home');
    }
}
</script>