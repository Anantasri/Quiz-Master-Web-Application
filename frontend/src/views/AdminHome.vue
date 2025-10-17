<template>
  <div>
    <AdminNavBar />
    <br />
    <h3 class="text-center"><b>Subjects</b></h3> 
    <div class="text-center">
      <RouterLink to="/admin/add-subject">
        <img src="/static/add.jpeg" alt="Add Subject" width="80" height="80" />
      </RouterLink>
    </div>
    <div class="container mt-4">
      <div class="row justify-content-center">
        <div class="col-md-5 mb-3" v-for="subject in visibleSubjects" :key="subject.subject_id">
          <div class="card p-3 mb-3 container-fluid justify-content-center text-bg-light shadow" style="width: 100%; max-width: 600px;">
            <div class="d-flex justify-content-between align-items-center">
              <h4><b>{{ subject.name }}</b></h4>
              <div>
              <RouterLink :to="`/admin/edit-subject/${subject.subject_id}`" class="btn btn-primary me-2">Edit</RouterLink> <button @click="deletesub(subject.subject_id)" class="btn btn-warning" >Delete</button>
              </div>
            </div>
            <p>{{ subject.description }}</p>
              
              <br>

<table v-if="getChapters(subject.subject_id).length" class="table table-bordered">
              <thead>
                <tr>
                  <th>Chapter</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="chapter in getChapters(subject.subject_id)" :key="chapter.chapter_id">
                  <td>{{ chapter.name }}</td>
                  <td>
                    <RouterLink :to="`/admin/edit-chapter/${chapter.chapter_id}`" class="btn btn-primary me-2">Edit</RouterLink>
                    <button @click="deletechap(subject.subject_id, chapter.chapter_id)" class="btn btn-warning" >Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
            <div class="text-center"><div class="d-grid gap-2 d-md-block">
            <RouterLink :to="`/admin/add-chapter/${subject.subject_id}`" class="btn btn-success">+ Chapter</RouterLink>
            </div></div>
           </div> 
           
        </div>

      </div>
    </div>
  </div>
  
  <RouterView />
</template>

<script setup>
import AdminNavBar from '@/components/AdminNavBar.vue'
import { RouterLink, RouterView, useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const router = useRouter()

const subjects = ref([])
const chapters = ref({})
const visibleSubjects = ref([])

const getChapters = (subjectID) => {
    return chapters.value[subjectID] || []
}

onMounted(() => {
    fetchSubjectsandChapters()
})
onBeforeRouteUpdate((to, from, next) => {
  fetchSubjectsandChapters()
  next()
})

const fetchSubjectsandChapters = async () => {
    const sub = await axios.get('http://127.0.0.1:5000/api/subjects')
    subjects.value = sub.data.subjects
    
    visibleSubjects.value = []
    for (let i = 0; i< subjects.value.length; i++) {
        setTimeout(() =>{
            visibleSubjects.value.push(subjects.value[i])
        }, i*120)
    }
    await Promise.all(subjects.value.map(async (subject) => {
        const chap = await axios.get(`http://127.0.0.1:5000/api/chapters/${subject.subject_id}`)
        chapters.value[subject.subject_id] = chap.data.chapters;
    }))
}

async function deletesub(subjectID) {
    const dlt = confirm("Are you sure you want to delete this subject and all the related information?");
    if (!dlt) return;
    const response = await fetch(`http://127.0.0.1:5000/api/delete-subject/${subjectID}`,{
        method: 'DELETE'
    });
    const data = await response.json();
    if (!response.ok) {
        alert(data.message);
    }
    else{
        alert(data.message);
        visibleSubjects.value = visibleSubjects.value.filter(subject => subject.subject_id !== subjectID);
        delete chapters.value[subjectID];
    }
}

async function deletechap(subjectID, chapterID) {
    const dlt = confirm("Are you sure you want to delete this chapter and all the related information?");
    if (!dlt) return;
    const response = await fetch(`http://127.0.0.1:5000/api/delete-chapter/${chapterID}`,{
        method: 'DELETE'
    });
    const data = await response.json();
    if (!response.ok) {
        alert(data.message);
    }
    else{
        alert(data.message);
        chapters.value[subjectID] = chapters.value[subjectID].filter(
          chapter => chapter.chapter_id !== chapterID
        );
    }
}

</script>
