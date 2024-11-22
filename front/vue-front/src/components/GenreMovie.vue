<template>
  <div class="container">
    <!-- 장르 선택 섹션 -->
    <div class="mb-4">
      <label for="genre-select" class="form-label">장르 선택</label> |
      <select id="genre-select" class="form-select" @change="handleGenreChange">
        <option value="home">영화 홈</option>
        <option v-for="genre in genres" :key="genre" :value="genre">
          {{ genre }}
        </option>
      </select>
    </div>

    <!-- 필터링된 영화 리스트 -->
    <div v-if="genre && filteredMovies.length" class="mt-4">
      <h2 class="text-center mb-4">
        {{ genre === "all" ? "전체 영화" : `${genreTitle} 영화` }}
      </h2>
      <div class="grid-container">
        <div
          class="card"
          v-for="movie in filteredMovies"
          :key="movie.movie_id"
          @click="goToDetail(movie.movie_id)"
        >
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

    <!-- 선택된 장르에 해당하는 영화가 없을 때 -->
    <div v-else-if="genre" class="mt-4 text-center">
      <h2>해당 장르에 맞는 영화가 없습니다.</h2>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();

    const genres = ref([]); // 장르 리스트
    const movies = ref([]); // 전체 영화 데이터
    const filteredMovies = ref([]); // 필터링된 영화 리스트
    const genre = ref(route.params.genre || null); // 현재 장르 (홈일 때 null)

    // 영화 데이터 가져오기
    const fetchMovies = async () => {
      try {
        const response = await axios.get("/movie_data.json");
        movies.value = response.data.map((item) => ({
          movie_id: item.fields.movie_id,
          title: item.fields.title,
          poster_url: item.fields.poster_url,
          genres: item.fields.genres,
        }));

        // 장르 목록 설정
        const genreSet = new Set();
        movies.value.forEach((movie) => {
          movie.genres.forEach((g) => genreSet.add(g));
        });
        genres.value = ["all", ...Array.from(genreSet)];

        filterMovies(); // 초기 필터링
      } catch (error) {
        console.error("Error fetching movies:", error);
      }
    };

    // 장르에 따라 영화 필터링
    const filterMovies = () => {
      if (!genre.value) {
        // 홈일 때 빈 배열
        filteredMovies.value = [];
      } else if (genre.value === "all") {
        filteredMovies.value = movies.value; // 전체 영화
      } else {
        filteredMovies.value = movies.value.filter((movie) =>
          movie.genres.includes(genre.value)
        );
      }
    };

    // 장르 변경 처리
    const handleGenreChange = (event) => {
      const selected = event.target.value;
      if (selected === "home") {
        genre.value = null; // 홈으로 이동 시 장르 null로 설정
        router.push({ name: "MovieView" });
      } else {
        router.push({ name: "GenreMovie", params: { genre: selected } });
      }
    };

    // 영화 상세 페이지로 이동
    const goToDetail = (movieId) => {
      router.push({ name: "MovieDetail", params: { id: movieId } });
    };

    // 포스터 URL 생성
    const getFullPosterUrl = (posterUrl) => {
      const baseUrl = "https://image.tmdb.org/t/p/w500";
      return `${baseUrl}${posterUrl}`;
    };

    // 장르 제목 표시
    const genreTitle = computed(() =>
      genre.value ? genre.value.charAt(0).toUpperCase() + genre.value.slice(1) : ""
    );

    // URL 변경 시 필터링 업데이트
    watch(route, (newRoute) => {
      genre.value = newRoute.params.genre || null;
      filterMovies();
    });

    onMounted(fetchMovies);

    return {
      genres,
      filteredMovies,
      genre,
      genreTitle,
      handleGenreChange,
      goToDetail,
      getFullPosterUrl,
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
