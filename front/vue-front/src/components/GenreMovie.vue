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
    <div v-if="filteredMovies.length" class="mt-4">
      <h2 class="text-center mb-4">
        {{ selectedGenre === "all" ? "전체 영화" : `장르: ${selectedGenre}` }}
      </h2>
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
    <div v-else-if="selectedGenre && selectedGenre !== 'all'" class="mt-4 text-center">
      <h2>해당 장르에 맞는 영화가 없습니다.</h2>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

export default {
  setup() {
    const genres = ref([]); // 장르 리스트
    const movies = ref([]); // 모든 영화 데이터
    const filteredMovies = ref([]); // 필터링된 영화 리스트
    const selectedGenre = ref(""); // 선택된 장르
    const router = useRouter();

    // JSON 파일에서 영화 데이터 가져오기
    const fetchMovies = async () => {
      try {
        const response = await axios.get("/movie_data.json");
        movies.value = response.data.map((item) => ({
          movie_id: item.fields.movie_id,
          title: item.fields.title,
          poster_url: item.fields.poster_url,
          genres: item.fields.genres,
        }));

        // 고유한 장르 추출
        const genreSet = new Set();
        movies.value.forEach((movie) => {
          movie.genres.forEach((genre) => genreSet.add(genre));
        });
        genres.value = ["all", ...Array.from(genreSet)]; // "전체" 추가
        filterMovies(); // 초기 필터링
        console.log("Genres Loaded:", genres.value); // 디버깅 로그
      } catch (error) {
        console.error("Error loading movies:", error);
      }
    };

    // 선택된 장르에 따른 영화 필터링
    const filterMovies = () => {
      if (selectedGenre.value === "all") {
        filteredMovies.value = movies.value; // 전체 영화 출력
      } else if (selectedGenre.value) {
        filteredMovies.value = movies.value.filter((movie) =>
          movie.genres.includes(selectedGenre.value)
        );
      } else {
        filteredMovies.value = []; // 선택 해제 시 필터링 초기화
      }
    };

    // 장르 선택 시 처리
    const handleGenreChange = (event) => {
      const selected = event.target.value;
      console.log(selected)

      if (selected === "home") {
        // 영화 홈으로 이동
        console.log(selected)
        router.push({ name: "MovieView" });
      } else {
        console.log(selected)
        selectedGenre.value = selected;
        filterMovies(); // 장르에 따른 필터링
      }
    };

    // 영화 상세 페이지 이동
    const goToDetail = (movieId) => {
      router.push({ name: "MovieDetail", params: { id: movieId } });
    };

    // TMDB 포스터 URL 생성
    const getFullPosterUrl = (posterUrl) => {
      const baseUrl = "https://image.tmdb.org/t/p/w500";
      return `${baseUrl}${posterUrl}`;
    };

    onMounted(fetchMovies);

    return {
      genres,
      movies,
      filteredMovies,
      selectedGenre,
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

.genre-label {
  font-size: 2rem;
  font-weight: bold;
  display: block;
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
