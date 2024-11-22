<template>
  <div class="container">
    <!-- 장르 선택 섹션 -->
    <GenreMovie @genre-selected="goToGenre" />
    <input v-model="searchQuery" type="text" placeholder="영화 제목 검색" />
    <button @click="searchMovie">검색</button>

    <!-- 인기영화 섹션 -->
    <div class="mt-5">
      <div class="d-flex justify-content-between align-items-center">
        <h2>인기영화</h2>
        <button class="btn btn-link" @click="goToMore('popular')">더보기</button>
      </div>
      <div class="grid-container">
        <div
          class="card"
          v-for="movie in randomPopularMovies"
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

    <!-- 최신영화 섹션 -->
    <div class="mt-5">
      <div class="d-flex justify-content-between align-items-center">
        <h2>최신영화</h2>
        <button class="btn btn-link" @click="goToMore('recent')">더보기</button>
      </div>
      <div class="grid-container">
        <div
          class="card"
          v-for="movie in randomRecentMovies"
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

    <!-- 개봉예정영화 섹션 -->
    <div class="mt-5">
      <div class="d-flex justify-content-between align-items-center">
        <h2>개봉예정영화</h2>
        <button class="btn btn-link" @click="goToMore('upcoming')">더보기</button>
      </div>
      <div class="grid-container">
        <div
          class="card"
          v-for="movie in randomUpcomingMovies"
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import GenreMovie from "@/components/GenreMovie.vue";

const searchQuery = ref("");
const popularMovies = ref([]);
const recentMovies = ref([]);
const upcomingMovies = ref([]);

const router = useRouter();

const fetchMovies = async () => {
  try {
    const popularResponse = await axios.get("/popular.json");
    popularMovies.value = popularResponse.data.map((item) => ({
      movie_id: item.fields.movie_id,
      title: item.fields.title,
      poster_url: item.fields.poster_url,
    }));

    const recentResponse = await axios.get("/recent.json");
    recentMovies.value = recentResponse.data.map((item) => ({
      movie_id: item.fields.movie_id,
      title: item.fields.title,
      poster_url: item.fields.poster_url,
    }));

    const upcomingResponse = await axios.get("/upcoming.json");
    upcomingMovies.value = upcomingResponse.data.map((item) => ({
      movie_id: item.fields.movie_id,
      title: item.fields.title,
      poster_url: item.fields.poster_url,
    }));
  } catch (error) {
    console.error("Error loading movies:", error);
  }
};

const getRandomMovies = (movies, count) => {
  const shuffled = [...movies].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
};

// 랜덤 5개 영화 가져오기
const randomPopularMovies = computed(() => getRandomMovies(popularMovies.value, 5));
const randomRecentMovies = computed(() => getRandomMovies(recentMovies.value, 5));
const randomUpcomingMovies = computed(() => getRandomMovies(upcomingMovies.value, 5));

// 영화 상세 페이지 이동
const goToDetail = (movieId) => {
  router.push({ name: "MovieDetail", params: { id: movieId } });
};

// 특정 섹션으로 이동
const goToMore = (section) => {
  router.push({ name: "MovieMore", params: { section } });
};

// 장르 선택 시 해당 장르 페이지로 이동
const goToGenre = (genre) => {
  router.push({ name: "GenreSection", params: { genre } });
};

// 영화 포스터 URL 생성
const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500";
  return `${baseUrl}${posterUrl}`;
};

onMounted(fetchMovies);
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
