<template>
<br>
<div class="card container-fluid justify-content-center text-bg-light mb-3 p-4 shadow" style="width: 100%; max-width: 600px;">
  <div class="card-body p-3 justify-content-center">
<div class="text-center"><h3>Login</h3></div>
    <form @submit.prevent="login">
        <div class="mb-2">
            <br>
            <label for="exampleFormControlInput1" class="form-label">Email ID</label>
            <input type="email" class="form-control" id="exampleFormControlInput1" name = 'email' v-model="email">
        </div>
        <div class="mb-3">
            <label for="inputPassword5" class="form-label">Password</label>
            <input type="password" id="inputPassword5" class="form-control" aria-describedby="passwordHelpBlock" name = 'password' v-model="password">
            <div id="passwordHelpBlock" class="form-text">
            </div>  
        </div>
        <div>
            <button type="submit" class = "btn btn-primary">Login</button>
        </div>
        <br>
        Click on<button type="button" class="btn btn-link" @click="gotoregister">Register</button>if you don't have an account
    </form>

</div>
</div>
</template>


<script setup>
import {ref} from 'vue';
import { useRouter } from 'vue-router';
import {useMessageStore } from '@/stores/counter.js';
import { useAuthStore } from '@/stores/auth.js';

const message_store = useMessageStore();
const auth_store = useAuthStore();

const router = useRouter();
const email = ref('');
const password = ref('');

async function login(){
    
    if (email.value === '' || password.value === ''){
        alert("Please fill in all the fields.");
        return;
    }

    const user = {
        email: email.value,
        password: password.value,
    };

    const response = await fetch("http://127.0.0.1:5000/api/login",{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            credentials: 'include'
        },
        body: JSON.stringify(user)
    });
    
    const data = await response.json();
    if(!response.ok){
        alert(`Login Failed: ${data.message}`);
        return;
    }
    else{
        message_store.updateErrorMessages(data.message);
        localStorage.setItem("token", data.user_details.auth_token);
        auth_store.setUserCred(data.user_details.auth_token, {
            email: data.user_details.email,
            roles: data.user_details.roles,
            name: data.user_details.name,
        });
        const roles = data.user_details?.roles || [];
        console.log("Login Success. Roles:", roles);
        if (roles.includes('admin')){
            router.push('/admin/home');
        }else{
            router.push('/user/home');
        }
    }
}

function gotoregister(){
    router.push('/register')
}
</script>