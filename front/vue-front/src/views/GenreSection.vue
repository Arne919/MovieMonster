<template>
  <div class="container">
    <h2 class="text-center mb-4">{{ genreTitle }} 영화</h2>
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
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const genre = ref(route.params.genre);
const movies = ref([]);
const filteredMovies = ref([]);

const fetchMovies = async () => {
  try {
    const response = await axios.get("/movie_data.json");
    movies.value = response.data.map((item) => ({
      movie_id: item.fields.movie_id,
      title: item.fields.title,
      poster_url: item.fields.poster_url,
      genres: item.fields.genres,
    }));
    filterMovies();
  } catch (error) {
    console.error("Error loading movies:", error);
  }
};

const filterMovies = () => {
  filteredMovies.value = movies.value.filter((movie) =>
    movie.genres.includes(genre.value)
  );
};

const goToDetail = (movieId) => {
  router.push({ name: "MovieDetail", params: { id: movieId } });
};

const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500";
  return `${baseUrl}${posterUrl}`;
};

const genreTitle = computed(() => {
  if (genre.value === "all") {
    return "전체";
  }
  return genre.value.charAt(0).toUpperCase() + genre.value.slice(1);
});

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
