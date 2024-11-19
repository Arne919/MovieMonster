<template>
  <div class="container">
    <div class="card mb-4">
      <img 
        :src="movie.poster_url" 
        class="card-img-top" 
        :alt="movie.title"
      />
      <div class="card-body">
        <h5 class="card-title">{{ movie.title }}</h5>
        <p class="card-text"><strong>Director:</strong> {{ movie.director }}</p>
        <p class="card-text"><strong>Genres:</strong> {{ movie.genres.join(', ') }}</p>
        <p class="card-text"><strong>Actors:</strong> {{ movie.actors.join(', ') }}</p>
        <p class="card-text"><strong>Description:</strong> {{ movie.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      movie: {}
    };
  },
  created() {
    const movieId = this.$route.params.id;
    axios.get(`http://127.0.0.1:8000/api/v1/movies/${movieId}/`)
      .then(response => {
        this.movie = response.data;
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
  height: 400px;
  object-fit: cover;
}
</style>
