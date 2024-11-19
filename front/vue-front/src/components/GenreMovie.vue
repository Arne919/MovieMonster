<template>
  <div class="container">
    <!-- 장르 선택 섹션 -->
    <div class="mb-4">
      <label for="genre-select" class="form-label">장르 선택</label> |
      <select
        id="genre-select"
        class="form-select"
        v-model="selectedGenre"
        @change="filterMovies"
      >
        <option value="" disabled selected>장르를 선택하시오</option>
        <option v-for="genre in genres" :key="genre" :value="genre">
          {{ genre }}
        </option>
      </select>
    </div>

    <!-- 필터링된 영화 리스트 -->
    <div v-if="filteredMovies.length" class="mt-4">
      <h2 class="text-center mb-4">장르: {{ selectedGenre }}</h2>
      <div class="grid-container">
        <div
          class="card"
          v-for="movie in filteredMovies"
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

    <!-- 선택된 장르에 해당하는 영화가 없을 때 -->
    <div v-else-if="selectedGenre" class="mt-4 text-center">
      <h2>해당 장르에 맞는 영화가 없습니다.</h2>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      movies: [], // 모든 영화 데이터
      genres: [], // 고유한 장르 리스트
      selectedGenre: "", // 선택된 장르
      filteredMovies: [], // 선택된 장르에 따른 필터링된 영화 리스트
    };
  },
  methods: {
    // JSON 파일에서 영화 데이터 가져오기
    async fetchMovies() {
      try {
        const response = await axios.get("/movie_data.json"); // JSON 파일 경로
        this.movies = response.data.map((item) => ({
          movie_id: item.fields.movie_id,
          title: item.fields.title,
          poster_url: item.fields.poster_url,
          genres: item.fields.genres,
        }));

        // 고유한 장르 추출
        const genreSet = new Set();
        this.movies.forEach((movie) => {
          movie.genres.forEach((genre) => genreSet.add(genre));
        });
        this.genres = Array.from(genreSet); // 고유한 장르 배열로 변환
        console.log("Genres Loaded:", this.genres); // 디버깅용 로그
      } catch (error) {
        console.error("Error loading movies:", error);
      }
    },
    // 선택된 장르에 따른 영화 필터링
    filterMovies() {
      if (this.selectedGenre) {
        this.filteredMovies = this.movies.filter((movie) =>
          movie.genres.includes(this.selectedGenre)
        );
      } else {
        this.filteredMovies = []; // 선택 해제 시 필터링된 리스트 초기화
      }
    },
    // 영화 상세 페이지 이동
    goToDetail(movieId) {
      this.$router.push({ name: "MovieDetail", params: { id: movieId } });
    },
    // TMDB 포스터 URL 생성
    getFullPosterUrl(posterUrl) {
      const baseUrl = "https://image.tmdb.org/t/p/w500";
      return `${baseUrl}${posterUrl}`;
    },
  },
  created() {
    this.fetchMovies(); // 영화 데이터 가져오기
  },
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}

.genre-label {
  font-size: 2rem; /* h2와 동일한 폰트 크기 */
  font-weight: bold; /* h2의 기본 굵기 */
  display: block; /* label을 블록 요소로 표시 */
  margin-bottom: 15px;
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
