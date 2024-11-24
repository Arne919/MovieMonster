<template>
  <div>
    <h3>리뷰 목록</h3>

    <!-- 정렬 버튼 -->
    <div class="sort-buttons">
      <button @click="setSortOrder('popular')" :class="{ active: sortOrder === 'popular' }">인기순</button>
      <button @click="setSortOrder('recent')" :class="{ active: sortOrder === 'recent' }">최신순</button>
    </div>

    <div v-if="store.articles.length === 0">
      <p>등록된 리뷰가 없습니다.</p>
    </div>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-else>
      <ArticleListItem
        v-for="article in store.articles"
        :key="article.id"
        :article="article"
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

const sortOrder = ref('recent') // 기본 정렬 기준: 최신순

// 정렬 버튼 클릭 시 정렬 기준 변경
const setSortOrder = (order) => {
  sortOrder.value = order
  store.getSortedArticles(order) // 정렬된 데이터 가져오기
}

// 컴포넌트 마운트 시 초기 데이터 로드
onMounted(async () => {
  try {
    await store.getSortedArticles(sortOrder.value);
  } catch (err) {
    console.error("Error loading articles:", err);
    errorMessage.value = "게시글을 불러오는 중 오류가 발생했습니다.";
  }
});

</script>

<style scoped>
.sort-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.sort-buttons button {
  padding: 5px 10px;
  border: 1px solid #ccc;
  background-color: white;
  cursor: pointer;
}

.sort-buttons button.active {
  font-weight: bold;
  color: white;
  background-color: #007bff;
}
</style>