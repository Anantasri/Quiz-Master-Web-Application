import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login',
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path: '/admin/home',
      name: 'admin-home',
      component: () => import('../views/AdminHome.vue'),
    },
    {
      path: '/admin/add-subject',
      name: 'add subject',
      component: () => import('../views/AddSubject.vue'),
    },
    {
      path: '/admin/edit-subject/:subject_id',
      name: 'edit subject',
      component: () => import('../views/EditSubject.vue'),
    },
    {
      path: '/admin/add-chapter/:subject_id',
      name: 'add chapter',
      component: () => import('../views/AddChapter.vue'),
    },
    {
      path: '/admin/edit-chapter/:chapter_id',
      name: 'edit chapter',
      component: () => import('../views/EditChapter.vue'),
    },
    {
      path: '/admin/quiz',
      name: 'admin quiz',
      component: () => import('../views/AdminQuiz.vue'),
    },
    {
      path: '/admin/edit-quiz/:quiz_id',
      name: 'edit quiz',
      component: () => import('../views/EditQuiz.vue'),
    },
    {
      path: '/admin/add-quiz',
      name: 'add quiz',
      component: () => import('../views/AddQuiz.vue'),
    },
    {
      path: '/admin/add-question/:quiz_id',
      name: 'add question',
      component: () => import('../views/AddQuestion.vue'),
    },
    {
      path: '/admin/edit-question/:question_id',
      name: 'edit question',
      component: () => import('../views/EditQuestion.vue'),
    },
    {
      path: '/summary',
      name: 'summary page',
      component: () => import('../views/Summary.vue'),
    },
    {
      path: '/admin/search',
      name: 'search page',
      component: () => import('../views/AdminSearch.vue'),
    },
    {
      path: '/user/home',
      name: 'user home',
      component: () => import('../views/UserHome.vue'),
    },
    {
      path: '/user/quiz-view/:quiz_id',
      name: 'user quiz view',
      component: () => import('../views/UserViewQuiz.vue'),
    },
    {
      path: '/user/quiz-attempt/:quiz_id',
      name: 'user quiz attempt',
      component: () => import('../views/UserAttemptQuiz.vue'),
    },
    {
      path: '/user/scores',
      name: 'user scores',
      component: () => import('../views/UserScore.vue'),
    }
  ],
})

export default router
