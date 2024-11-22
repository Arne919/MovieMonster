<template>
  <div class="container">
    <h2 class="text-center mb-4">{{ sectionTitle }} 영화</h2>
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
        <div class="card-body text-center">
          <h5 class="card-title">{{ movie.title }}</h5>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      section: this.$route.params.section,
      movies: [],
    };
  },
  computed: {
    sectionTitle() {
      return this.section === "popular"
        ? "인기"
        : this.section === "recent"
        ? "최신"
        : "개봉예정";
    },
  },
  methods: {
    fetchMovies() {
      const movieData =
        this.section === "popular"
          ? this.$root.$data.popularMovies
          : this.section === "recent"
          ? this.$root.$data.recentMovies
          : this.$root.$data.upcomingMovies;

      this.movies = movieData;
    },
    getFullPosterUrl(posterUrl) {
      const baseUrl = "https://image.tmdb.org/t/p/w500";
      return `${baseUrl}${posterUrl}`;
    },
    goToDetail(movieId) {
      this.$router.push({ name: "MovieDetail", params: { id: movieId } });
    },
  },
  created() {
    this.fetchMovies();
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