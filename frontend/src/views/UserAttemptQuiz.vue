<template>
<div class="container mt-4" v-if="quiz && questions.length">
<div class="text-center">Quiz - {{ quiz.Quiz_id }} ({{ chapter.name }})</div>

<div class="position-absolute top-0 end-0 m-3">
<p><b>Time Left: {{ time }}</b></p>
</div>

<div v-for="(question, index) in questions" :key="question.question_id" class="card p-3 mb-4">
<p><b>Q{{ index + 1 }}.</b> {{ question.Question_statement }}</p>
<div v-for="option in ['a','b','c','d']" :key="option">
<input type="radio" 
       :id="`q${question.question_id}_${option}`" 
       :name="'question_' + question.question_id" 
       :value="question['option_' + option]"
       v-model="answers[question.question_id]" />
<label :for="`q${question.question_id}_${option}`">{{ question['option_' + option] }}</label>
</div>
</div>

<div class="text-end">
<button class="btn btn-success" @click="submitquiz">Submit</button>
</div>
</div>

<div v-else-if="error" class="text-center"> {{ error }} </div>
</template>

<script>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
    setup() {
        const route = useRoute()
        const router = useRouter()

        const quiz = ref(null)
        const chapter = ref({})
        const questions = ref([])
        const answers = ref({})
        const currentindex = ref(0)
        const error = ref('')
        const timer = ref(0)
        const time = ref('')
        let interval = null
        const parseDuration = (timeStr) => {
        const [hours, minutes] = timeStr.split(':').map(Number)
        return (hours || 0) * 60 + (minutes || 0)
        }

        const formatTime = () => {
        const min = String(Math.floor(timer.value / 60)).padStart(2, '0')
        const sec = String(timer.value % 60).padStart(2, '0')
        time.value = `${min}:${sec}`
        }

        const startTimer = () => {
        interval = setInterval(() => {
            if (timer.value > 0) {
            timer.value--
            formatTime()
            } else {
            clearInterval(interval)
            submitquiz()
            }
        }, 1000)
        
        }
        const fetchQuiz = async() => {
            const quizID = route.params.quiz_id
            const token = localStorage.getItem('token')

            try{
                const response = await axios.get(`http://127.0.0.1:5000/api/attempt-quiz/${quizID}`,{
                    headers: {
                        'Authentication-Token':token
                    }
                })
                quiz.value = response.data.quiz
                chapter.value = response.data.chapter
                questions.value = response.data.questions
                 
                const durationMinutes = parseDuration(quiz.value.time_duration)
                timer.value = durationMinutes * 60

                formatTime()
                startTimer()

            } catch(err){
                if(err.response && err.response.status === 403){
                    alert("Quiz is not scheduled for today")
                    router.push('/user/home')
                } else {
                    error.value = "Could not load quiz."
                }
            }
        }
        
        const submitquiz = async () => {
            clearInterval(interval)
            const token = localStorage.getItem('token')
            const quizID = route.params.quiz_id

            const payload = {
                answers: answers.value,
                time_taken: (parseDuration(quiz.value.time_duration) * 60) - timer.value
            }
            try{
                await axios.post(`http://127.0.0.1:5000/api/submit-quiz/${quizID}`,
                payload, {
                    headers: {
                        'Content-Type':'application/json',
                        'Authentication-Token':token
                    }
                })
                router.push('/user/scores')
            } catch (err) {
                error.value = 'Failed to submit quiz.'
            }
        }

        onMounted(() => {
            fetchQuiz()
        })

        return {
            quiz,
            chapter,
            questions,
            answers,
            submitquiz,
            error,
            time
        }
    }
}
</script>

