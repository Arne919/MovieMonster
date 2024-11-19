<template>
  <div class="container">
    <h1>Movie List</h1>
    <div class="row">
      <div class="col-md-4" v-for="movie in movies" :key="movie.id">
        <div class="card mb-4">
          <!-- Convert relative URL to absolute URL -->
          <img 
            :src="getFullPosterUrl(movie.poster_url)" 
            class="card-img-top" 
            :alt="movie.title"
          />
          <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      movies: []
    };
  },
  methods: {
    // Function to convert relative URL to absolute URL
    getFullPosterUrl(posterUrl) {
      const baseUrl = 'https://image.tmdb.org/t/p/w500';
      return `${baseUrl}${posterUrl}`;
    }
  },
  created() {
    axios.get('http://127.0.0.1:8000/api/v1/movies/')
      .then(response => {
        this.movies = response.data;
      })
      .catch(error => {
        console.error(error);
      });
  }
};
</script>

<style>
.container {
  margin-top: 20px;
}
.card-img-top {
  height: 300px;
  object-fit: cover;
}
</style>
