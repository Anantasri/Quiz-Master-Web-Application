<template>
<UserNavBar />
  <div>
    
    <div class="container mt-4">
    <div v-if="scores.length" class="card m-4">
    <h5 class="card-header text-center" style="background-color:lightskyblue">Scores</h5>
    <div class="card-body">
    <table class="table text-center">
    <thead>
    <tr>
    <th>S.No</th>
    <th>Chapter</th>
    <th>No. of Questions</th>
    <th>Score</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(score, index) in scores" :key="score.quiz_id">
    <td>{{ index + 1 }}</td>
    <td>{{ getChapterName(score.quiz_id) }}</td>
    <td>{{ getQuestionCount(score.quiz_id) }}</td>
    <td>{{ score.total_scored }}/{{ getQuestionCount(score.quiz_id) }}</td>
    </tr>
    </tbody>
    </table>
    </div>
  </div>
  <div v-else class="text-center mt-5">
  <h3>No Quizzes attented till now</h3>
  </div>
  </div>
  </div>
</template>

<script>
import UserNavBar from '@/components/UserNavBar.vue';
import axios from 'axios';

export default {
    name: 'UserScores',
    components: {
        UserNavBar
    },
    data() {
        return {
            scores: [],
            quizzes: [],
            chapters: [],
            questions: []
        };
    },
    methods: {
        async fetchData(){
            const token = localStorage.getItem('token');
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/user/scores',{
                    headers: {
                        'Authentication-Token':token
                    }
                });
                this.scores = response.data.scores;
                this.quizzes = response.data.quizzes;
                this.chapters = response.data.chapters;
                this.questions = response.data.questions;
            } catch(err){
                console.error('Error fetching scores:',err);
            }
        },
        getChapterName(quizID){
            const quiz = this.quizzes.find(q => q.Quiz_id === quizID);
            if(!quiz) return '';
            const chapter = this.chapters.find(c => c.chapter_id === quiz.chap_id);
            return chapter ? chapter.name : '';
        },
        getQuestionCount(quizID) {
            return this.questions.filter(q => q.quiz_id === quizID).length;
        }
    },
    mounted() {
        this.fetchData();
    }
};
</script>