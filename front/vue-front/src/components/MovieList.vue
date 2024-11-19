<template>
  <div class="container">
    <h1 class="text-center my-4">Movie List</h1>
    <div class="grid-container">
      <!-- Movie Cards -->
      <div class="card" v-for="movie in movies" :key="movie.id">
        <img 
          :src="getFullPosterUrl(movie.poster_url)" 
          class="card-img" 
          :alt="movie.title"
        />
        <div class="card-body">
          <h5 class="card-title">{{ movie.title }}</h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      movies: [] // 영화 데이터 리스트
    };
  },
  methods: {
    // 상대 URL을 절대 URL로 변환
    getFullPosterUrl(posterUrl) {
      const baseUrl = 'https://image.tmdb.org/t/p/w500';
      return `${baseUrl}${posterUrl}`;
    }
  },
  created() {
    // API 호출로 영화 데이터 가져오기
    axios.get('http://127.0.0.1:8000/api/v1/movies/')
      .then(response => {
        this.movies = response.data; // API에서 받은 영화 데이터 저장
      })
      .catch(error => {
        console.error('Error fetching movies:', error);
      });
  }
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem; /* 카드 간 간격 */
}

.card {
  border: 1px solid #ddd;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  text-align: center;
}

.card-img {
  width: 100%;
  height: 300px;
  object-fit: cover; /* 이미지 비율 유지 */
}

.card-body {
  padding: 10px;
}

.card-title {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
  text-align: center;
}
</style>
