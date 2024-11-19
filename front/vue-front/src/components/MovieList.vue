<template>
  <div class="container">
    <!-- 인기영화 섹션 -->
    <h2 class="text-center mb-4">인기영화</h2>
    <div class="grid-container">
      <div 
        class="card" 
        v-for="movie in popularMovies" 
        :key="movie.movie_id"
        @click="goToDetail(movie.movie_id)"
      >
        <div class="card h-100">
          <img
            :src="getFullPosterUrl(movie.poster_url)"
            class="card-img-top"
            :alt="movie.title"
          />
          <div class="card-body text-center">
            <h5 class="card-title">{{ movie.title }}</h5>
          </div>
        </div>
      </div>
    </div>

    <!-- 최신영화 섹션 -->
    <h2 class="text-center mb-4 mt-5">최신영화</h2>
    <div class="grid-container">
      <div class="card" v-for="movie in recentMovies" :key="movie.movie_id"
        @click="goToDetail(movie.movie_id)">      
        <div class="card h-100">
          <img
            :src="getFullPosterUrl(movie.poster_url)"
            class="card-img-top"
            :alt="movie.title"
          />
          <div class="card-body text-center">
            <h5 class="card-title">{{ movie.title }}</h5>
          </div>
        </div>
      </div>
    </div>

    <!-- 개봉예정영화 섹션 -->
    <h2 class="text-center mb-4 mt-5">개봉예정영화</h2>
    <div class="grid-container">
      <div class="card" v-for="movie in upcomingMovies" :key="movie.movie_id"
        @click="goToDetail(movie.movie_id)">
        <div class="card h-100">
          <img
            :src="getFullPosterUrl(movie.poster_url)"
            class="card-img-top"
            :alt="movie.title"
          />
          <div class="card-body text-center">
            <h5 class="card-title">{{ movie.title }}</h5>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      popularMovies: [], // 인기영화 데이터
      recentMovies: [], // 최신영화 데이터
      upcomingMovies: [], // 개봉예정영화 데이터
    };
  },
  methods: {
    // JSON 파일에서 데이터를 가져오는 메서드
    async fetchMovies() {
      try {
        const popularResponse = await axios.get("/popular.json");
        this.popularMovies = popularResponse.data.map((item) => ({
          movie_id: item.fields.movie_id,
          title: item.fields.title,
          poster_url: item.fields.poster_url,
        }));

        const recentResponse = await axios.get("/recent.json");
        this.recentMovies = recentResponse.data.map((item) => ({
          movie_id: item.fields.movie_id,
          title: item.fields.title,
          poster_url: item.fields.poster_url,
        }));

        const upcomingResponse = await axios.get("/upcoming.json");
        this.upcomingMovies = upcomingResponse.data.map((item) => ({
          movie_id: item.fields.movie_id,
          title: item.fields.title,
          poster_url: item.fields.poster_url,
        }));

        console.log("Movies Loaded:", {
          popularMovies: this.popularMovies,
          recentMovies: this.recentMovies,
          upcomingMovies: this.upcomingMovies,
        });
      } catch (error) {
        console.error("Error loading movies:", error);
      }
    },
    goToDetail(movieId) {
      // 클릭된 영화의 상세페이지로 이동
      this.$router.push({ name: "MovieDetail", params: { id: movieId } });
    },
    // TMDB 포스터 URL 생성
    getFullPosterUrl(posterUrl) {
      const baseUrl = "https://image.tmdb.org/t/p/w500";
      return `${baseUrl}${posterUrl}`;
    },
  },
  
  created() {
    this.fetchMovies();
  },
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}

/* 카드 레이아웃 */
.grid-container {
  display: flex;
  flex-wrap: wrap; /* 줄바꿈 허용 */
  gap: 1.5rem; /* 카드 간 간격 */
  justify-content: start; /* 좌측 정렬 */
}

.card {
  width: 200px; /* 고정된 카드 너비 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  text-align: center;
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: scale(1.05); /* 호버 시 살짝 확대 효과 */
}

.card-img-top {
  width: 100%;
  height: 300px; /* 포스터 고정 높이 */
  object-fit: cover; /* 포스터 비율 유지 */
}

.card-title {
  font-size: 0.9rem;
  font-weight: bold;
  margin-top: 10px;
}
</style>
