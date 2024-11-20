<template>
  <div>
    <h1>게시글 작성</h1>

    <!-- 영화 검색 영역 추가 -->
    <div>
      <label for="movie-search">영화 제목 검색 : </label>
      <input type="text" id="movie-search" v-model.trim="searchQuery" placeholder="영화 제목을 입력하세요">
      <button @click="searchMovie">확인</button>
    </div>

    <!-- 오류 메시지 표시 -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <!-- 영화 포스터 미리보기 -->
    <div v-if="moviePoster">
      <h4>영화 포스터 미리보기</h4>
      <img :src="moviePoster" alt="영화 포스터" class="poster-image" />
    </div>

    <!-- 게시글 작성 폼 -->
    <form @submit.prevent="createArticle">
      <div>
        <label for="title">제목 : </label>
        <input type="text" id="title" v-model.trim="title">
      </div>
      <div>
        <label for="content">내용 : </label>
        <textarea id="content" v-model.trim="content"></textarea>
      </div>
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import { useRouter } from 'vue-router'

// 게시글 제목과 내용
const title = ref(null)
const content = ref(null)
const store = useCounterStore()
const router = useRouter()

// 영화 검색 관련 변수
const searchQuery = ref('')  // 영화 제목을 입력받는 변수
const moviePoster = ref(null)  // 영화 포스터 URL을 저장하는 변수
const errorMessage = ref('')  // 오류 메시지를 저장하는 변수

// 영화 검색 함수
const searchMovie = async () => {
  if (!searchQuery.value.trim()) {
    // 사용자가 영화 제목을 입력하지 않은 경우 오류 메시지 표시
    errorMessage.value = "영화 제목을 입력해 주세요."
    return
  }

  try {
    // 영화 검색 API 요청
    const response = await axios.get(`${store.API_URL}/api/v1/movies/search/`, {
      params: { title: searchQuery.value }
    })

    // 디버깅: API 응답 확인
    console.log("API 응답:", response.data)

    const movie = response.data
    console.log(movie.poster)
    // 검색된 영화의 포스터 URL 저장
    moviePoster.value = `https://image.tmdb.org/t/p/w500${movie.poster}`  // 포스터 URL 필드는 실제 API에 맞게 수정 필요
    errorMessage.value = ''  // 오류 메시지 초기화
  } catch (error) {
    // 오류가 발생한 경우 오류 메시지를 표시
    errorMessage.value = error.response?.data?.error || "영화 검색에 실패했습니다."
    moviePoster.value = null  // 포스터 이미지 초기화
  }
}

// 게시글 생성 함수 (DRF 요청)
const createArticle = function () {
  // 토큰 확인을 위해 콘솔에 출력
  console.log(store.token)
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/communities/`,
    data: {
      title: title.value,
      content: content.value,
      poster_url: moviePoster.value  // 영화 포스터 URL을 게시글에 추가
    },
    headers: {
      Authorization: `Token ${store.token}`  // 인증 헤더에 토큰 추가
    }
  })
    .then((res) => {
      // 게시글 작성 성공 시, ArticleView 페이지로 이동
      router.push({ name: 'ArticleView' })
    })
    .catch((err) => {
      // 오류 발생 시 콘솔에 오류 메시지 출력
      console.error('Error creating article:', err.response.data)
    })
}
</script>

<style>
.error-message {
  color: red;
  margin-top: 10px;
}
.poster-image {
  width: 200px;
  height: auto;
  margin-top: 10px;
}
</style>
