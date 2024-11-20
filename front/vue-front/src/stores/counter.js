import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const Username = ref(null)  // 사용자 이름 저장 변수 추가
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()

  // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/communities/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        // console.log(res.data)
        articles.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 회원가입 요청 액션
  const signUp = function (payload) {
    // const username = payload.username
    // const password1 = payload.password1
    // const password2 = payload.password2
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then((res) => {
        // console.log(res)
        // console.log('회원가입 성공')
        const password = password1
        logIn({ username, password })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 로그인 요청 액션
  const logIn = function (payload) {
    // const username = payload.username
    // const password1 = payload.password
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        token.value = res.data.key
        // 사용자 정보를 가져오는 추가 요청
        axios({
          method: 'get',
          url: `${API_URL}/accounts/user/`,  // 사용자 정보를 가져오는 엔드포인트
          headers: {
            Authorization: `Token ${token.value}`
          }
        })
          .then((userRes) => {
            console.log(userRes.data)
            Username.value = userRes.data.username  // 사용자 이름 저장
            router.push({ name: 'ArticleView' })
          })
          .catch((err) => {
            console.log('Error fetching user information:', err)
          })
      })
      .catch((err) => {
        console.log(err)
      })
  }
  
  // [추가기능] 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log(res.data)
        token.value = null
        username.value = null  // 로그아웃 시 사용자 이름 초기화
        router.push({ name: 'ArticleView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 댓글 작성 및 댓글 목록 요청을 위한 함수 추가
  const getComments = (articleId) => {
    return axios({
      method: 'get',
      url: `${API_URL}/api/v1/communities/${articleId}/comments/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
  }

  const addComment = (articleId, commentContent) => {
    return axios({
      method: 'post',
      url: `${API_URL}/api/v1/communities/${articleId}/comments/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: { content: commentContent }
    })
  }
  return { articles, API_URL, addComment, getComments, getArticles, signUp, logIn, token, isLogin, logOut, Username }
}, { persist: true })
