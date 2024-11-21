import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const rankings = ref([]); // 랭킹 데이터를 저장
  const Username = ref(null)  // 사용자 이름 저장 변수 추가
  const user = ref({ username: '', points: 0 }); // 유저 정보
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()

  // 랭킹 데이터를 가져오는 함수
  const fetchRankings = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/communities/ranking/`, {
        headers: { Authorization: `Token ${token.value}` },
      });
      rankings.value = response.data;
      console.log('Fetching rankings...');
      console.log('Rankings fetched:', response.data);
    } catch (error) {
      console.error('Error fetching rankings:', error);
    }
  };

  // 별점 표시 함수
  const displayStars = (rating) => {
    const stars = []
    for (let i = 1; i <= 10; i++) {
      stars.push({
        filled: i <= rating, // rating 이하의 별은 노란색으로 채워짐
      })
    }
    return stars
  }


  
  const fetchUserPoints = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/accounts/user/points/`, {
        headers: {
          Authorization: `Token ${token.value}`, // JWT 토큰 추가
        },
      });
      console.log(response.data)
      user.value = response.data;
      // fetchRankings 함수에서 데이터를 로깅합니다.
      console.log('Rankings fetched:', response.data);

    } catch (error) {
      console.error('Error fetching user points:', error);
    }
  };
  // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
      const getArticles = async function () {
        console.log("getArticles function called");
        try {
          const response = await axios({
            method: 'get',
            url: `${API_URL}/api/v1/communities/`,
            headers: {
              Authorization: `Token ${token.value}`
            }
          })
          articles.value = response.data
          console.log(articles.value)
          console.log("Updated articles:", articles.value)
        } catch (err) {
          console.log(err)
        }
      }
  
  // const getArticles = function () {
  //   axios({
  //     method: 'get',
  //     url: `${API_URL}/api/v1/communities/`,
  //     headers: {
  //       Authorization: `Token ${token.value}`
  //     }
  //   })
  //     .then((res) => {
  //       // console.log(res.data)
  //       articles.value = res.data
  //     })
  //     .catch((err) => {
  //       console.log(err)
  //     })
  // }


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
        // console.log("로그인됐나요?:", isLogin)
      })
      .then(() => {
        fetchUserPoints(); // 로그인 이후 즉시 사용자 포인트 정보를 가져옴
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
        token.value = res.data.key;
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
        return fetchUserPoints()
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
        Username.value = null  // 로그아웃 시 사용자 이름 초기화
        localStorage.removeItem('token')  // 로컬 스토리지에서 토큰 제거
        user.value = { username: '', points: 0 } // 유저 정보 초기화
        router.push({ name: 'ArticleView' }) // 로그아웃 후 리다이렉트
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
  return { articles, API_URL, addComment, getComments, getArticles, signUp, logIn, token, isLogin, logOut, Username, fetchUserPoints, user, displayStars, fetchRankings, rankings}
}, { persist: true })