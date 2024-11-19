<template>
  <div class="container">
    <div class="row">
      <!-- 좌측: 포스터 섹션 -->
      <div class="col-md-4 text-center">
        <img
          :src="getFullPosterUrl(movie.poster_url)"
          class="img-fluid rounded shadow"
          :alt="movie.title"
        />
      </div>

      <!-- 우측: 상세 정보 섹션 -->
      <div class="col-md-8">
        <h1 class="mb-3">{{ movie.title }}</h1>
        <p><strong>개봉일:</strong> {{ movie.release_date }}</p>
        <p><strong>평점:</strong> {{ movie.vote_avg }}</p>
        <p><strong>줄거리:</strong> {{ movie.description }}</p>
        <p><strong>장르:</strong> {{ movie.genres.join(", ") }}</p>
        <p><strong>배우:</strong> {{ movie.actors.join(", ") }}</p>
        <p><strong>감독:</strong> {{ movie.director }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      movie: {}, // 영화 데이터를 저장할 객체
    };
  },
  methods: {
    // TMDB 이미지 URL 생성
    getFullPosterUrl(posterUrl) {
      const baseUrl = "https://image.tmdb.org/t/p/w500"; // TMDB 이미지 베이스 URL
      return `${baseUrl}${posterUrl}`;
    },
  },
  created() {
    const movieId = this.$route.params.id; // 라우터에서 영화 ID 가져오기
    axios
      .get(`http://127.0.0.1:8000/api/v1/movies/${movieId}/`) // API 요청
      .then((response) => {
        this.movie = response.data; // 응답 데이터 저장
        console.log("Movie Data Loaded:", this.movie); // 디버깅용 로그
      })
      .catch((error) => {
        console.error("Error loading movie:", error);
      });
  },
};
</script>

<style scoped>
.container {
  margin-top: 40px;
}

.row {
  align-items: center; /* 세로 정렬 */
}

.img-fluid {
  max-height: 500px; /* 포스터 최대 높이 */
  object-fit: cover; /* 이미지 비율 유지 */
  margin-bottom: 20px; /* 모바일에서 여백 */
}

.col-md-4 {
  margin-bottom: 20px; /* 작은 화면에서 좌측과 우측 간격 */
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 20px;
}

p {
  font-size: 1rem;
  margin-bottom: 10px;
}
</style>
