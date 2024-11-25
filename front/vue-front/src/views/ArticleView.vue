<template>
  <div class="review-page-container">
    <!-- 페이지 상단: 리뷰 작성 버튼과 제목 -->
    <div class="header">
      <h1>전체 영화 리뷰</h1>
      <RouterLink :to="{ name: 'CreateView' }" class="create-button">리뷰 작성하기</RouterLink>
    </div>
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue'
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'

const store = useCounterStore()

onMounted(() => {
  // mount 되기 전에 store에 있는 전체 게시글 요청 함수를 호출
  store.getArticles()
})
</script>

<style scoped>
.review-page-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px; /* 섹션 간격 */
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  font-size: 24px;
  margin: 0;
}

.create-button {
  padding: 8px 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.create-button:hover {
  background-color: #0056b3;
}
</style>
