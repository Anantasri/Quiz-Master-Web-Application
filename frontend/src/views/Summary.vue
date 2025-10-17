<template>
<div>
<AdminNavBar v-if="role === 'admin'" />
<UserNavBar v-else-if="role === 'user'" />

<div class="container mt-4">
<h2 class="text-center mb-4"><b>Summary</b></h2>

<div v-if="role === 'admin'">
<h4 class="text-center">Subject-wise User Attempts</h4>
<div class="d-flex justify-content-center">
<canvas id="adminPie" style="max-width: 300px; max-height: 300px;"></canvas>
</div>
<br>
<h4 class="text-center">Subject-wise Top Scores</h4>
<div class="d-flex justify-content-center">
<canvas id="adminBar" style="max-width: 300px; max-height: 300px;"></canvas>
</div>
</div>

<div v-if="role === 'user'" >
<h4 class="text-center">Quizzes Per Subject</h4>
<div class="d-flex justify-content-center">
<canvas id="userBar" style="max-width: 300px; max-height: 300px;"></canvas>
</div>
<br>
<h4 class="text-center">Quizzes Per Month</h4>
<div class="d-flex justify-content-center">
<canvas id="userPie" style="max-width: 300px; max-height: 300px;"></canvas>
</div>
</div>
</div>
</div>
</template>

<script setup>
import { onMounted, ref, nextTick } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'
import AdminNavBar from '@/components/AdminNavBar.vue'
import UserNavBar from '@/components/UserNavBar.vue'

const role = ref('')

function generatedColors(n) {
    const colors = ['red','blue','green','orange','yellow','purple']
    return Array.from({length: n }, (_, i) => colors[i % colors.length])
}

onMounted(async() => {
    try {
        const token = localStorage.getItem("token");
        const response = await fetch('http://127.0.0.1:5000/api/summary', {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authentication-Token": token
            }
        })
        const data = await response.json()
        role.value = data.role
        await nextTick()
        if (data.role === 'admin'){
        new Chart(document.getElementById('adminPie'), {
            type: 'pie',
            data: {
                labels: data.subject_attempt.subjects,
                datasets: [{
                    data: data.subject_attempt.attempts,
                    backgroundColor: generatedColors(data.subject_attempt.attempts.length),
                }]
            },
            options: {
                plugins: {
                    title:{
                        display: true,
                        text: 'User Attempts'
                    }
                }
            }
        })

        new Chart(document.getElementById('adminBar'),{
            type: 'bar',
            data: {
                labels: data.topScores.subjects,
                datasets: [{
                    label: 'Top Scores',
                    data: data.topScores.scores,
                    backgroundColor: generatedColors(data.topScores.scores.length),
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true }
                }
            }
        })
    } else if (data.role === 'user'){
        new Chart(document.getElementById('userBar'), {
            type: 'bar',
            data: {
                labels: data.quiz_counts.subjects,
                datasets: [{
                    label: 'Quiz Count',
                    data: data.quiz_counts.quizcount,
                    backgroundColor: generatedColors(data.quiz_counts.quizcount.length),
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true }
                }
            }
        })
        new Chart(document.getElementById('userPie'), {
            type: 'pie',
            data: {
                labels: data.monthlyQuiz.month,
                datasets: [{
                    data: data.monthlyQuiz.quizcount,
                    backgroundColor: generatedColors(data.monthlyQuiz.quizcount.length),
                }]
                }
            })
        }

    } catch (err) {
        console.error('Summary fetch error:', err)
    } 
})
</script>