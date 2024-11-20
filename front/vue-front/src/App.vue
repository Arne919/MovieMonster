<template>
  <header>
    <nav class="navbar">
      <div class="container">
        <!-- Navigation Links -->
        <RouterLink :to="{ name: 'SignUpView' }" class="nav-link">SignUp</RouterLink> |
        <RouterLink :to="{ name: 'LogInView' }" class="nav-link">LogIn</RouterLink> |
        <RouterLink :to="{ name: 'ArticleView' }" class="nav-link">Reviews</RouterLink> |
        <RouterLink :to="{ name: 'MovieList' }" class="nav-link">Movies</RouterLink> |
        <RouterLink :to="{ name: 'GameView' }" class="nav-link">Game</RouterLink> |
        <RouterLink :to="{ name: 'RankView' }" class="nav-link">Rank</RouterLink>

        <div class="user-info" v-if="user.username">
          {{ user.username }} | Points: {{ user.points }}
        </div>
        <form @submit.prevent="logOut">
          <input type="submit" value="Logout">
        </form>
      </div>
    </nav>
  </header>

  <!-- Dynamic Route View -->
  <RouterView />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { RouterView, RouterLink } from 'vue-router';

const user = ref({ username: '', points: 0 }); // 유저 정보

const fetchUserPoints = async () => {
  try {
    const response = await axios.get('/api/user/points/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`, // JWT 토큰 추가
      },
    });
    user.value = response.data;
  } catch (error) {
    console.error('Error fetching user points:', error);
  }
};

// 로그아웃 함수
const logOut = () => {
  localStorage.removeItem('token'); // JWT 토큰 제거
  // user.value = { username: '', points: 0 }; // 사용자 정보 초기화
};

onMounted(() => {
  fetchUserPoints(); // 컴포넌트가 마운트되면 유저 정보 가져오기
});
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

.user-info {
  display: inline-block;
  margin-left: 20px;
  font-weight: bold;
}
</style>
