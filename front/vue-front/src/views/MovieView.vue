<template>
  <div class="container">
    <!-- 장르 선택 -->
    <GenreMovie @genre-selected="goToGenre" />

    <!-- 검색 -->
    <div class="search-container">
      <input v-model="searchQuery" type="text" placeholder="영화 제목 검색" />
      <button @click="searchMovie">검색</button>
    </div>
    <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>

    <!-- 검색 결과 -->
    <div v-if="searchResults.length > 0" class="search-results">
      <h2>검색 결과</h2>
      <div class="grid-container">
        <div
          class="card"
          v-for="movie in searchResults"
          :key="movie.id"
          @click="goToDetail(movie.id)"
        >
          <img
            :src="getFullPosterUrl(movie.poster_url)"
            class="card-img-top"
            :alt="movie.title"
          />
        </div>
      </div>
    </div>

    <!-- 검색 결과가 없을 때만 기존 섹션 표시 -->
    <div v-else>
      <p v-if="searchQuery" class="text-center text-muted">검색 결과가 없습니다.</p>

      <!-- 인기/최신/개봉예정 섹션 -->
      <div v-for="section in sections" :key="section.name" class="mt-5">
        <div class="d-flex justify-content-between align-items-center">
          <h2>{{ section.title }}</h2>
          <!-- <button class="btn btn-link" @click="goToMore(section.name)">더보기 ></button> -->
          <button class="btn-more" @click="goToMore(section.name)">
            더보기 <span class="arrow">&gt;</span>
          </button>

        </div>
        <div class="grid-container">
          <div
            class="card"
            v-for="movie in getMoviesInOrder(section.movies, 5)"
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
    const errorMessage = ref("");
    const searchResults = ref([]);
    const defaultPoster = "http://127.0.0.1:8000/media/default_movies/default-movie.png";
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

    const getMoviesInOrder = (movies, count) => {
      return movies.slice(0, count);
    };

    const goToDetail = (movieId) => {
      router.push({ name: "MovieDetail", params: { id: movieId } });
    };

    const goToMore = (section) => {
      router.push({ name: "MovieMore", params: { section } });
    };

    const goToGenre = (genre) => {
      if (genre === "home") {
        router.push({ name: "MovieView" }).then(() => {
          window.location.reload();
        });
      } else {
        router.push({ name: "GenreMovie", params: { genre } });
      }
    };

    const getFullPosterUrl = (posterUrl) =>
      `https://image.tmdb.org/t/p/w500${posterUrl}`;

    const searchMovie = async () => {
      if (!searchQuery.value.trim()) {
        searchResults.value = [];
        errorMessage.value = "영화 제목을 입력해 주세요.";
        return;
      }

      try {
        const processedQuery = searchQuery.value.replace(/\s+/g, "");
        const response = await axios.get(
          "http://127.0.0.1:8000/api/v1/movies/search/",
          {
            params: { title: processedQuery },
          }
        );

        searchResults.value = response.data.map((movie) => ({
          id: movie.id,
          title: movie.title,
          poster_url: movie.poster_url,
          description: movie.description,
        }));
        errorMessage.value = "";
      } catch (error) {
        errorMessage.value =
          error.response?.data?.error || "영화 검색에 실패했습니다.";
        searchResults.value = [];
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
      getMoviesInOrder,
      searchMovie,
      defaultPoster,
      searchResults,
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
  gap: 1rem;
  justify-content: start;
}

.card {
  width: 240px;
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
  height: 360px;
  object-fit: cover;
}

.btn-more {
  display: inline-flex;
  align-items: center; /* 텍스트와 아이콘 정렬 */
  color: #e5e5e5; /* 평소 텍스트 색상 (연한 흰색) */
  font-size: 16px; /* 글자 크기 */
  font-weight: 500; /* 적당한 두께 */
  background: none; /* 배경 제거 */
  border: none; /* 버튼 테두리 제거 */
  cursor: pointer; /* 커서를 포인터로 변경 */
  padding: 5px 10px; /* 버튼 안쪽 여백 */
  text-decoration: none; /* 텍스트 장식 제거 */
  transition: color 0.3s ease-in-out;
}

.btn-more .arrow {
  margin-left: 5px; /* 텍스트와 화살표 간격 */
  font-size: 18px; /* 화살표 크기 */
  color: inherit; /* 부모의 텍스트 색상 상속 */
}
</style>
