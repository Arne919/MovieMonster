<template>
  <div class="container">
    <!-- 장르 선택 -->
    <GenreMovie @genre-selected="goToGenre" />

    <!-- 검색 -->
    <input v-model="searchQuery" type="text" placeholder="영화 제목 검색" />
    <button @click="searchMovie">검색</button>
    <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>

    <!-- 인기/최신/개봉예정 섹션 -->
    <div v-for="section in sections" :key="section.name" class="mt-5">
      <div class="d-flex justify-content-between align-items-center">
        <h2>{{ section.title }}</h2>
        <button class="btn btn-link" @click="goToMore(section.name)">더보기</button>
      </div>
      <div class="grid-container">
        <div
          class="card"
          v-for="movie in getRandomMovies(section.movies, 5)"
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

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import GenreMovie from "@/components/GenreMovie.vue";
import axios from "axios";

export default {
  components: { GenreMovie },
  setup() {
    const router = useRouter();
    const searchQuery = ref("");
    const errorMessage = ref(""); // 오류 메시지 상태 추가
    const sections = ref([
      { name: "popular", title: "인기영화", movies: [] },
      { name: "recent", title: "최신영화", movies: [] },
      { name: "upcoming", title: "개봉예정영화", movies: [] },
    ]);

    const fetchMovies = async () => {
      const endpoints = {
        popular: "/popular.json",
        recent: "/recent.json",
        upcoming: "/upcoming.json",
      };

      for (const section of sections.value) {
        try {
          const response = await axios.get(endpoints[section.name]);
          section.movies = response.data.map((item) => ({
            movie_id: item.fields.movie_id,
            title: item.fields.title,
            poster_url: item.fields.poster_url,
          }));
        } catch (error) {
          console.error(`Error fetching ${section.name}:`, error);
        }
      }
    };

    const getRandomMovies = (movies, count) => {
      const shuffled = [...movies].sort(() => 0.5 - Math.random());
      return shuffled.slice(0, count);
    };

    const goToDetail = (movieId) => {
      router.push({ name: "MovieDetail", params: { id: movieId } });
    };

    const goToMore = (section) => {
      router.push({ name: "MovieMore", params: { section } });
    };

    const goToGenre = (genre) => {
      if (genre === "home") {
        router.push({ name: "MovieView" });
      } else {
        router.push({ name: "GenreMovie", params: { genre } });
      }
    };

    const getFullPosterUrl = (posterUrl) =>
      `https://image.tmdb.org/t/p/w500${posterUrl}`;

    // 영화 검색
    const searchMovie = async () => {
      if (!searchQuery.value.trim()) {
        errorMessage.value = "영화 제목을 입력해 주세요.";
        return;
      }

      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/api/v1/movies/search/",
          {
            params: { title: searchQuery.value },
          }
        );
        const movie = response.data;

        // 영화가 정확히 일치하면 디테일 페이지로 이동
        router.push({ name: "MovieDetail", params: { id: movie.id } });
        errorMessage.value = ""; // 오류 메시지 초기화
      } catch (error) {
        errorMessage.value =
          error.response?.data?.error || "영화 검색에 실패했습니다.";
      }
    };

    onMounted(fetchMovies);

    return {
      sections,
      searchQuery,
      errorMessage,
      goToDetail,
      goToMore,
      goToGenre,
      getFullPosterUrl,
      getRandomMovies,
      searchMovie, // searchMovie 메서드 추가
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
