<template>
  <div
    class="container movie-detail"
    :style="getBackdropStyle(movie.backdrop_url)"
  >
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
        <p><strong>장르:</strong> {{ movie.genres?.join(", ") }}</p>
        <p><strong>배우:</strong> {{ movie.actors?.join(", ") }}</p>
        <p><strong>감독:</strong> {{ movie.director }}</p>
        <!-- 카테고리 추가 버튼 -->
        <button class="btn btn-primary" @click="showCategoryModal = true">
          카테고리 추가
        </button>
      </div>

      <!-- 공식 예고편 섹션 -->
      <div class="movie-youtube mt-4 text-center">
      <h3>공식 예고편</h3>
      <button
        type="button"
        class="btn"
        data-bs-toggle="modal"
        data-bs-target="#youtubeTrailerModal"
      >
      <img :src="youtubeLogo" alt="YouTube" class="youtube-logo" />
        </button>
      </div>
    </div>
    <!-- 카테고리 추가 모달 -->
    <AddToCategoryModal
      v-if="showCategoryModal"
      :movie-id="movie.id"
      @close="showCategoryModal = false"
    />
    <YoutubeTrailerModal :movieTitle="movie.title" />
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import AddToCategoryModal from "@/components/AddToCategoryModal.vue";
import youtubeLogo from "@/assets/youtubeLogo.svg";
import YoutubeTrailerModal from "@/components/YoutubeTrailerModal.vue";


const route = useRoute();

const movie = ref({}); // 영화 데이터를 저장할 객체
const showCategoryModal = ref(false); // 카테고리 모달 상태

// TMDB 이미지 URL 생성
const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500";
  return `${baseUrl}${posterUrl}`;
};

// 배경 이미지 URL 생성
const getBackdropStyle = (backdropUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/original";
  return backdropUrl
    ? { backgroundImage: `url(${baseUrl}${backdropUrl})` }
    : {};
};

// 영화 데이터 가져오기
const fetchMovie = async () => {
  const movieId = route.params.id; // 라우터에서 영화 ID 가져오기
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/api/v1/movies/${movieId}/`
    );
    movie.value = response.data; // 응답 데이터 저장
  } catch (error) {
    console.error("Error loading movie:", error);
  }
};

// 컴포넌트 마운트 시 영화 데이터 로드
onMounted(fetchMovie);
</script>


<style scoped>
.container {
  margin-top: 40px;
  padding: 20px;
  border-radius: 8px;
}
.movie-detail {
  background-size: cover; /* 배경 이미지 크기를 전체 화면에 맞춤 */
  background-position: center; /* 배경 이미지 위치를 중앙에 맞춤 */
  background-repeat: no-repeat; /* 배경 이미지 반복 방지 */
  background-color: rgba(0, 0, 0, 0.5); /* 배경색 (이미지가 없을 경우 대비) */
  color: white; /* 텍스트 색상을 흰색으로 변경 */
  border-radius: 15px;
}
.row {
  align-items: center; /* 세로 정렬 */
}

.img-fluid {
  max-height: 500px; /* 포스터 최대 높이 */
  object-fit: cover; /* 이미지 비율 유지 */
  margin-bottom: 20px;
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

.youtube-logo {
  width: 36px;
  height: 36px;
}

.movie-youtube {
  margin-top: 20px;
  text-align: center;
}
</style>