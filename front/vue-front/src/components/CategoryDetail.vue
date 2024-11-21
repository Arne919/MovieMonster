<template>
  <div>
    <h2>{{ category.name }}</h2>
    <ul>
      <li v-for="movie in category.movies" :key="movie.id">
        <h3>{{ movie.title }}</h3>
        <img :src="movie.poster_url" alt="Movie Poster" />
      </li>
    </ul>
  </div>
</template>

<script>
import { useCounterStore } from '@/stores/counter';

export default {
  data() {
    return {
      category: {},
    };
  },
  async mounted() {
    const store = useCounterStore();
    this.category = store.categories.find((cat) => cat.id === parseInt(this.$route.params.id, 10));
  },
};
</script>
