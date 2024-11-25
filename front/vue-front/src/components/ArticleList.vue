<template>
  <div>
    <!-- <h3>리뷰 목록</h3> -->

    <!-- 정렬 버튼 -->
    <div class="sort-buttons">
      <button @click="setSortOrder('popular')" :class="{ active: sortOrder === 'popular' }">인기순</button>
      <button @click="setSortOrder('recent')" :class="{ active: sortOrder === 'recent' }">최신순</button>
    </div>

    <div v-if="store.articles.length === 0">
      <p>등록된 리뷰가 없습니다.</p>
    </div>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="articles.length > 0">
      <ArticleListItem
        v-for="article in articles"
        :key="article.id"
        :article="article"
        @update-article="updateArticle"
      />
    </div>
  </div>
</template>

<script setup>
import ArticleListItem from '@/components/ArticleListItem.vue'
import { useCounterStore } from '@/stores/counter'
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const searchQuery = ref('')
const errorMessage = ref('')
const router = useRouter()

const store = useCounterStore()

const articles = computed(() => store.articles);
console.log('vvv',articles)

const sortOrder = ref('recent') // 기본 정렬 기준: 최신순

// 정렬 버튼 클릭 시 정렬 기준 변경
const setSortOrder = (order) => {
  sortOrder.value = order
  store.getSortedArticles(order) // 정렬된 데이터 가져오기
}

const updateArticle = (updatedArticle) => {
  const index = store.articles.findIndex((article) => article.id === updatedArticle.id);
  if (index !== -1) {
    store.articles[index] = { ...updatedArticle };
    console.log("Updated article in parent component:", store.articles[index]);
  }
};



// 컴포넌트 마운트 시 초기 데이터 로드
onMounted(async () => {
  try {
    // // 데이터가 없거나 강제로 새로 고침이 필요한 경우만 호출
    // if (!store.articles.length) {
      await store.getSortedArticles(sortOrder.value);
    
    console.log('dfdf', articles.value)
  } catch (err) {
    console.error("Error loading articles:", err);
    errorMessage.value = "게시글을 불러오는 중 오류가 발생했습니다.";
  }
});

</script>


<style scoped>
/* 정렬 버튼 스타일링 */
.sort-buttons {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.sort-buttons button {
  padding: 10px 20px;
  border: 1px solid #ccc;
  background-color: white;
  cursor: pointer;
  font-size: 16px;
  color: #333;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s;
}

.sort-buttons button.active {
  font-weight: bold;
  color: white;
  background-color: #007bff;
}

/* 에러 메시지 스타일 */
.error-message {
  color: red;
  margin-top: 10px;
}
</style>