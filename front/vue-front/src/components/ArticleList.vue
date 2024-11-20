<template>
  <div>
    <h3>Article List</h3>
    <input v-model="searchQuery" type="text" placeholder="영화 제목 검색" />
    <button @click="searchMovie">리뷰 쓰러가기</button>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <ArticleListItem 
      v-for="article in store.articles"
      :key="article.id"
      :article="article"
    />
  </div>
</template>

<script setup>
import ArticleListItem from '@/components/ArticleListItem.vue'
import { useCounterStore } from '@/stores/counter'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const searchQuery = ref('')
const errorMessage = ref('')
const router = useRouter()

// 영화 검색 함수
const searchMovie = async () => {
  if (!searchQuery.value.trim()) {
    errorMessage.value = "영화 제목을 입력해 주세요."
    return
  }

  try {
    // 서버에서 영화 검색 요청
    const response = await axios.get('http://127.0.0.1:8000/api/v1/movies/search/', {
      params: { title: searchQuery.value }
    })
    const movie = response.data

    // 영화가 정확히 일치하면 디테일 페이지로 이동
    router.push({ name: 'MovieDetail', params: { id: movie.id } })
    errorMessage.value = ''  // 오류 메시지 초기화
  } catch (error) {
    // 영화가 존재하지 않는 경우
    errorMessage.value = error.response.data.error || "영화 검색에 실패했습니다."
  }
}
const store = useCounterStore()
</script>
