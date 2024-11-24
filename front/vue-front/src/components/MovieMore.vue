<template>
  <div class="container">
    <!-- 섹션 제목과 뒤로가기 버튼 -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="text-center">{{ sectionTitle }} 영화</h2>
      <button class="btn btn-secondary" @click="goBack">뒤로가기</button>
    </div>

    <!-- 영화 리스트 -->
    <div class="grid-container">
      <div
        class="card"
        v-for="movie in movies"
        :key="movie.movie_id"
        @click="goToDetail(movie.movie_id)"
      >
        <img
          :src="getFullPosterUrl(movie.poster_url)"
          class="card-img-top"
          :alt="movie.title"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();
    const section = ref(route.params.section);
    const movies = ref([]);

    // 영화 데이터 가져오기
    const fetchMovies = async () => {
      try {
        const apiEndpoint =
          section.value === "popular"
            ? "/popular.json"
            : section.value === "recent"
            ? "/recent.json"
            : "/upcoming.json";

        const response = await axios.get(apiEndpoint);
        movies.value = response.data.map((item) => ({
          movie_id: item.fields.movie_id,
          title: item.fields.title,
          poster_url: item.fields.poster_url,
        }));
      } catch (error) {
        console.error("Error fetching movies:", error);
      }
    };

    // 섹션 제목 계산
    const sectionTitle = computed(() => {
      return section.value === "popular"
        ? "인기"
        : section.value === "recent"
        ? "최신"
        : "개봉예정";
    });

    // 영화 디테일 페이지 이동
    const goToDetail = (movieId) => {
      router.push({ name: "MovieDetail", params: { id: movieId } });
    };

    // 영화 포스터 URL 생성
    const getFullPosterUrl = (posterUrl) =>
      `https://image.tmdb.org/t/p/w500${posterUrl}`;

    // 뒤로가기 기능
    const goBack = () => {
      router.go(-1); // 이전 페이지로 이동
    };

    onMounted(fetchMovies);

    return {
      sectionTitle,
      movies,
      goToDetail,
      getFullPosterUrl,
      goBack, // 뒤로가기 메서드 반환
    };
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
  row-gap: 2rem; /* 위아래 간격 */
  column-gap: 1.5rem; /* 좌우 간격 */
  justify-content: start;
}

.card {
  width: 240px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  text-align: center;
  transition: transform 0.2s ease-in-out;
  background-color: transparent; /* 카드 배경을 투명하게 설정 */
}

.card:hover {
  transform: scale(1.05);
}

.card-img-top {
  width: 100%;
  height: 360px;
  object-fit: cover;
}

.btn-secondary {
  padding: 5px 10px;
  font-size: 0.9rem;
}
</style>
