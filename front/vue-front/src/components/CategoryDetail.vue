<template>
  <div>
    <h1>{{ category.name }} 카테고리</h1>
    <div v-if="movies.length === 0">
      <p>이 카테고리에 추가된 영화가 없습니다.</p>
    </div>

    <div v-else class="movie-list">
      <div
        v-for="movie in movies"
        :key="movie.id"
        class="movie-card"
        @click="goToMovieDetail(movie.id)"
      >
        <h3>{{ movie.title }}</h3> <!-- 영화 제목 표시 -->
        <p>개봉일: {{ movie.release_date }}</p> <!-- 영화 개봉일 표시 -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const category = ref({}); // 카테고리 데이터
const movies = ref([]); // 영화 데이터
const store = useCounterStore();

// 카테고리 상세 데이터 가져오기
const fetchCategoryDetails = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/accounts/categories/${route.params.categoryId}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );

    console.log("Category Details Response:", response.data); // 응답 데이터 로깅
    category.value = response.data;
    movies.value = response.data.movies; // 영화 데이터 설정
  } catch (error) {
    console.error("Error fetching category details:", error);
  }
};

// 영화 디테일 페이지로 이동
const goToMovieDetail = (movieId) => {
  router.push(`/movies/${movieId}`);
};

// 컴포넌트 마운트 시 데이터 로드
onMounted(fetchCategoryDetails);
</script>

<style scoped>
.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.movie-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background-color: #f9f9f9;
  width: calc(33.333% - 20px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  cursor: pointer;
}

.movie-card h3 {
  margin: 0;
  font-size: 1.2em;
}

.movie-card p {
  font-size: 0.9em;
  margin: 5px 0 0;
}
</style>
