import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('authStore', () => {
    const auth_token = ref(localStorage.getItem('token') || null)
    const user = ref(JSON.parse(localStorage.getItem('user')) || null)
    const isAuthenticated = computed(() => auth_token.value !== null)

    function setUserCred(token, userData){
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(userData))
        auth_token.value = token
        user.value = userData
    }

    function clearAuthToken() {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        auth_token.value = null
        user.value = null
    }

    function getAuthToken() {
        return auth_token.value
    }

    function getUserEmail() {
        return user.value ? user.value.email : null
    }

    function getUserRoles() {
        return user.value ? user.value.roles : []
    }

    function getUserName() {
        return user.value ? user.value.name : null
    }

    return {isAuthenticated, getAuthToken, getUserEmail, getUserRoles, getUserName, setUserCred, clearAuthToken}
})