<template>
  <div class="container">
    <!-- 장르 선택 섹션 -->
    <GenreMovie @genre-selected="filterMovies" /> 
    <input v-model="searchQuery" type="text" placeholder="영화 제목 검색" />
    <button @click="searchMovie">검색</button>

    <!-- 인기영화 섹션 -->
    <div class="mt-5">
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
    </div>

    <!-- 최신영화 섹션 -->
    <div class="mt-5">
      <h2 class="text-center mb-4">최신영화</h2>
      <div class="grid-container">
        <div
          class="card"
          v-for="movie in recentMovies"
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
    </div>

    <!-- 개봉예정영화 섹션 -->
    <div class="mt-5">
      <h2 class="text-center mb-4">개봉예정영화</h2>
      <div class="grid-container">
        <div
          class="card"
          v-for="movie in upcomingMovies"
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
    </div>
  </div>
</template>

<script>
import axios from "axios";
import GenreMovie from "@/components/GenreMovie.vue"; // GenreMovie 컴포넌트 경로 확인

export default {
  components: { GenreMovie },
  data() {
    return {
      searchQuery: '',  // `searchQuery`를 `data`에 추가
      errorMessage: '', // `errorMessage`를 `data`에 추가
      popularMovies: [],
      recentMovies: [],
      upcomingMovies: [],
    };
  },
  methods: {
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
      } catch (error) {
        console.error("Error loading movies:", error);
      }
    },
    async searchMovie() {  // `searchMovie`를 `methods`에 추가
      if (!this.searchQuery.trim()) {
        this.errorMessage = "영화 제목을 입력해 주세요.";
        return;
      }

      try {
        // 서버에서 영화 검색 요청
        const response = await axios.get('http://127.0.0.1:8000/api/v1/movies/search/', {
          params: { title: this.searchQuery }
        });
        const movie = response.data;

        // 영화가 정확히 일치하면 디테일 페이지로 이동
        this.$router.push({ name: 'MovieDetail', params: { id: movie.id } });
        this.errorMessage = '';  // 오류 메시지 초기화
      } catch (error) {
        // 영화가 존재하지 않는 경우
        this.errorMessage = error.response.data.error || "영화 검색에 실패했습니다.";
      }
    },
    goToDetail(movieId) {
      this.$router.push({ name: "MovieDetail", params: { id: movieId } });
    },
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

.grid-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: start;
}

.card {
  width: 200px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  text-align: center;
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: scale(1.05);
}

.card-img-top {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.card-title {
  font-size: 0.9rem;
  font-weight: bold;
  margin-top: 10px;
}
</style>
