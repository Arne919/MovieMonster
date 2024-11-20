<template>
  <header>
    <nav class="navbar">
      <div class="container">
        <!-- Navigation Links -->
        <RouterLink :to="{ name: 'SignUpView' }" class="nav-link">회원가입</RouterLink> |
        <!-- <RouterLink :to="{ name: 'LogInView' }" class="nav-link">LogIn</RouterLink> | -->
        <RouterLink :to="{ name: 'ArticleView' }" class="nav-link">리뷰</RouterLink> |
        <RouterLink :to="{ name: 'MovieList' }" class="nav-link">영화</RouterLink> |
        <RouterLink :to="{ name: 'GameView' }" class="nav-link">게임</RouterLink> |
        <RouterLink :to="{ name: 'RankView' }" class="nav-link">랭크</RouterLink> |
        <RouterLink v-if="isLogin" :to="{ name: 'ProfileView', params: { username: user.username } }" class="nav-link">내 프로필</RouterLink>
        <RouterLink v-else :to="{ name: 'LogInView' }" class="nav-link">로그인</RouterLink>


        <div class="user-info" v-if="user.username">
          {{ user.username }} | Points: {{ user.current_points }}
        </div>
        <form @submit.prevent="logOut" v-if="isLogin">
          <input type="submit" value="Logout">
        </form>
      </div>
    </nav>
  </header>

  <!-- Dynamic Route View -->
  <!-- <RouterView /> -->
  <RouterView :key="$route.fullPath" />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { RouterView, RouterLink } from 'vue-router';
import { useCounterStore } from '@/stores/counter'
import { computed } from 'vue';

const store = useCounterStore()
const isLogin = computed(() => store.isLogin);
const user = computed(() => store.user);

// const user = ref({ username: '', points: 0 }); // 유저 정보

// const fetchUserPoints = async () => {
//   try {
//     const response = await axios.get(`http://127.0.0.1:8000/accounts/user/points/`, {
//       headers: {
//         Authorization: `Token ${store.token}`, // JWT 토큰 추가
//       },
//     });
//     console.log(response.data)
//     user.value = response.data;
//   } catch (error) {
//     console.error('Error fetching user points:', error);
//   }
// };

// 로그아웃 함수
const logOut = () => {
  store.logOut();  // store에서 로그아웃 처리
  user.value = { username: '', points: 0 }; // 유저 정보 초기화
};
onMounted(() => {
  if (isLogin.value) {
    store.fetchUserPoints(); // 유저 포인트 가져오기
  }
});

// onMounted(() => {
//   store.fetchUserPoints(); // 컴포넌트가 마운트되면 유저 정보 가져오기
// });

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
