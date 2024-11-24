<template>
  <div class="container">
    <!-- 장르 선택 섹션 -->
    <div class="mb-4">
      <label for="genre-select" class="form-label">장르 선택</label> |
      <select
        id="genre-select"
        class="form-select"
        v-model="genre"
        @change="handleGenreChange"
      >
        <option value="home">영화 홈</option>
        <option v-for="genreItem in genres" :key="genreItem" :value="genreItem">
          {{ genreTranslations[genreItem] || genreItem }}
        </option>
      </select>
    </div>

    <!-- 필터링된 영화 리스트 -->
    <div v-if="genre && filteredMovies.length" class="mt-4">
      <h2 class="genre-title">
        {{ genre === "all" ? "전체 영화" : `${genreTranslations[genre] || genre} 영화` }}
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
        </div>
      </div>
    </div>

    <!-- 선택된 장르에 해당하는 영화가 없을 때 -->
    <!-- <div v-else-if="genre" class="mt-4 text-center">
      <h2>해당 장르에 맞는 영화가 없습니다.</h2>
    </div> -->
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

    const genreTranslations = {
      all: "전체 영화",
      Action: "액션",
      Thriller: " 스릴러",
      Crime: "범죄",
      Drama: "드라마",
      Fantasy: "판타지",
      Romance: "로맨스",
      Animation: "애니메이션",
      Adventure: "모험",
      Family: "가족",
      Comedy: "코미디",
      History: "역사",
      War: "전쟁",
      "Science Fiction": "SF", // 문자열 키로 설정
      Mystery: "미스테리",
      Music: "음악",
      Horror: "공포",
      Western: "서부",
      Documentary: "다큐멘터리"
      // 필요한 추가 장르를 여기에 추가
    };

    const genres = ref([]); // 장르 리스트
    const movies = ref([]); // 전체 영화 데이터
    const filteredMovies = ref([]); // 필터링된 영화 리스트
    const genre = ref(route.params.genre || "home"); // 현재 장르 (홈일 때 'home')

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
      if (!genre.value || genre.value === "home") {
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
    const handleGenreChange = () => {
      if (genre.value === "home") {
        router.push({ name: "MovieView" });
      } else {
        router.push({ name: "GenreMovie", params: { genre: genre.value } });
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

    // URL 변경 시 필터링 업데이트
    watch(route, (newRoute) => {
      genre.value = newRoute.params.genre || "home";
      filterMovies();
    });

    onMounted(fetchMovies);

    return {
      genres,
      filteredMovies,
      genre,
      genreTranslations,
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

.genre-title {
  text-align: left;
  /* margin-left: 10px; */
  margin-bottom: 20px;
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
</style>
