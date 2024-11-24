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
          <button class="btn-more" @click="goToMore(section.name)">
            더보기 <span class="arrow">&gt;</span>
          </button>
        </div>

        <!-- 캐러셀 -->
        <div class="carousel-wrapper">
          <button class="carousel-btn prev" @click="prevSlide(section.name)">
            &lt;
          </button>
          <div class="carousel-track-container">
            <div
              class="carousel-track"
              :style="{
                transform: `translateX(-${currentIndex[section.name] * 100}%)`,
              }"
            >
              <div
                class="carousel-slide"
                v-for="(chunk, index) in getChunks(section.movies, 5)"
                :key="index"
              >
                <div class="card" v-for="movie in chunk" :key="movie.movie_id"
                @click.stop="goToDetail(movie.movie_id)">
                  <img
                    :src="getFullPosterUrl(movie.poster_url)"
                    class="card-img-top"
                    :alt="movie.title"
                  />
                </div>
              </div>
            </div>
          </div>
          <button class="carousel-btn next" @click="nextSlide(section.name)">
            &gt;
          </button>
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

    const currentIndex = ref({
      popular: 0,
      recent: 0,
      upcoming: 0,
    });

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

    const getChunks = (movies, size) => {
      const chunks = [];
      for (let i = 0; i < movies.length; i += size) {
        chunks.push(movies.slice(i, i + size));
      }
      return chunks;
    };

    const nextSlide = (sectionName) => {
      const totalSlides = Math.ceil(
        sections.value.find((s) => s.name === sectionName).movies.length / 5
      );
      if (currentIndex.value[sectionName] < totalSlides - 1) {
        currentIndex.value[sectionName]++;
      }
    };

    const prevSlide = (sectionName) => {
      if (currentIndex.value[sectionName] > 0) {
        currentIndex.value[sectionName]--;
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
      currentIndex,
      getChunks,
      nextSlide,
      prevSlide,
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
  overflow: hidden; /* 넘치는 콘텐츠 숨김 */
  width: 100%; /* 컨테이너 너비를 화면에 맞춤 */
  padding: 0; /* 기본 패딩 제거 */
}

.grid-container {
  display: flex; /* Flexbox로 가로 배치 */
  gap: 1rem; /* 카드 간의 간격 */
  width: calc(240px * 5 + 1rem * 4); /* 카드 5개 크기 + 간격 4개 */
  overflow: hidden; /* 넘치는 부분 숨김 */
}

.card {
  flex: 0 0 auto; /* 크기 고정 */
  width: 240px; /* 카드 너비 */
  height: 360px; /* 카드 높이 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s ease-in-out;
  background-color: transparent; /* 카드 배경을 투명하게 설정 */
}

.card img {
  width: 100%; /* 카드 크기에 맞춰 이미지 크기 */
  height: 100%; /* 고정된 높이 맞춤 */
  object-fit: cover; /* 이미지 비율 유지 */
} 

.card:hover {
  transform: scale(1.05); /* 호버 시 살짝 확대 */
}


.btn-more {
  display: inline-flex;
  align-items: center; /* 텍스트와 아이콘 정렬 */
  color: #d9d9d9; /* 평소 텍스트 색상 */
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

.carousel-wrapper {
  display: flex;
  align-items: center;
  position: relative;
}

.carousel-track-container {
  overflow: hidden;
  width: 100%;
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease-in-out; /* 부드러운 이동 효과 */
  gap: 0; /* 각 슬라이드 사이의 간격 제거 */
}

.carousel-slide {
  display: flex;
  flex-shrink: 0; /* 크기 축소 방지 */
  width: 100%; /* 슬라이드 하나의 너비를 컨테이너의 100%로 설정 */
  justify-content: space-between; /* 내부 카드 간격 유지 */
}

.card {
  width: 240px;
  height: 360px;
}

.carousel-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  cursor: pointer;
  padding: 10px 15px;
  z-index: 10;
}

.carousel-btn.prev {
  left: 0;
}

.carousel-btn.next {
  right: 0;
}

</style>
