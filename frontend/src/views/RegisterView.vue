<template>
<br>
<div class="card container-fluid justify-content-center text-bg-light mb-3 p-4 shadow" style="width: 100%; max-width: 600px;">
  <div class="card-body p-3 justify-content-center">
<div class="text-center"><h3>Register</h3></div>
<form @submit.prevent="register">
    <div class="row-md-3">
      <br>
      <label for="user_email" class="form-label">Email ID</label>
      <input type="email" class="form-control" id="user_email" placeholder="example@gmail.com" name="user_email" v-model="email" @input = "validateemail" required>
      <div id="emailHelp" class="form-text">{{ emailerror }}</div>
    </div>
    <div class="row-md-3">
      <br>
      <label for="password" class="form-label">Password</label>
      <input type="password" id="inputPassword5" class="form-control" aria-describedby="passwordHelpBlock" name = 'password' v-model="password" @input = "validatePassword" required>
      <div id="passwordHelp" class="form-text">{{ passworderror }}</div>
    </div>
    <div class="row-md-3">
      <br>
      <label for="full_name" class="form-label">Full Name</label>
      <input type="text" class="form-control" id="full_name" name="full_name" v-model="name" required>
      <div class="valid-feedback">
        Please enter your full name
      </div>
    </div>
    <div class="row-md-3">
      <br>
      <label for="qualification" class="form-label">Qualification</label>
      <input type="text" class="form-control" id="Qualification" name="qualification" v-model="qualification" required>
      </div>
    <div class="col-md-4">
      <br>
      <label for="DOB" class="form-label">Date Of Birth</label>
      <input type="date" class="form-control" id="DOB" name="DOB" v-model="DOB" required>
    </div>
    <br>
    <div class="col-12">
      <button class="btn btn-primary" type="submit">Register</button>
    </div>
  </form>
</div>
</div>
</template>

<script setup>

import {ref} from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const email = ref('');
const emailerror = ref('');
const password = ref('');
const passworderror = ref('');
const name = ref('');
const qualification = ref('');
const DOB = ref('');
const checkEmailMessage = ref('');

const validateemail = () => {
    if (!email.value.includes('@gmail.com')){
        emailerror.value = "Enter only Gmail ID";
        return false;
    }
    else{
        emailerror.value = '';
        return true;
    }
}
const validatePassword = () => {
     if (password.value.length<8){
        passworderror.value = "Password must be at least 8 characters long.";
        return false;
     }
     else{
        passworderror.value = '';
        return true;
     }
}

async function register(){
    if (email.value === '' || password.value === '' || name.value === '' || qualification.value === '' || DOB.value === ''){
        alert("Please fill in all the fields");
        return;
    }
    if (!validatePassword()){
        alert("Please enter a valid password");
        return;
    }
    if (!validateemail()){
        alert("Please enter a valid Email ID");
        return;
    }

    const user = {
        email: email.value,
        name: name.value,
        password: password.value,
        qualification: qualification.value,
        DOB: DOB.value
    };

    const response = await fetch("http://127.0.0.1:5000/api/register",{
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(user)
    });
    
    if(!response.ok){
        const errorData = await response.json();
        alert(errorData.message);
        return;
    }
    else{
        const data = await response.json();
        alert(data.message);
        router.push('/login');
    }
}

function checkEmailAvailability(){
    fetch('http://127.0.0.1:5000/api/check-email',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email.value })
    }).then(response => {
        if(response.ok){
            return response.json();
        }
        else{
            console.error('Error checking email availability');
        }
    }).then(data=>{
        if (data.available) {
            checkEmailMessage.value = 'Email address is available'
        }
        else{
            checkEmailMessage.value = 'Email address already taken. Login to continue'
        }
    })  
}
</script>