<template>
  <header>
    <nav class="navbar">
      <div class="container">
        <!-- Navigation Links -->
        <RouterLink :to="{ name: 'ArticleView' }" class="nav-link">Articles</RouterLink> |
        <RouterLink to="/movies" class="nav-link">Movies</RouterLink>
      </div>
    </nav>
  </header>

  <!-- Dynamic Route View -->
  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router';
</script>

<style scoped>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

.navbar {
  padding: 10px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
}

.nav-link {
  text-decoration: none;
  margin-right: 10px;
  color: #007bff;
}

.nav-link:hover {
  text-decoration: underline;
}
</style>
