<template>
  <div class="ranking-container">
    <h1>랭킹 페이지</h1>
    <table class="ranking-table">
      <thead>
        <tr>
          <th>#</th>
          <th>프로필</th>
          <th>이름</th>
          <th>포인트</th>
          <th>게시물 수</th>
          <th>좋아요 수</th>
          <th>팔로워 수</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in rankings" :key="user.id">
          <td>
            <div v-if="index === 0">
              <img src="@/assets/gold.png" alt="Gold Medal" class="medal-icon" />
            </div>
            <div v-else-if="index === 1">
              <img src="@/assets/silver.png" alt="Silver Medal" class="medal-icon" />
            </div>
            <div v-else-if="index === 2">
              <img src="@/assets/bronze.png" alt="Bronze Medal" class="medal-icon" />
            </div>
            <div v-else>{{ index + 1 }}</div>
          </td>
          <td>
            <div class="profile-picture">
              <img :src="user.profile_picture || placeholderImage" alt="Profile" class="profile-img" />
            </div>
          </td>
          <td>
            <RouterLink :to="{ name: 'ProfileView', params: { username: user.username } }">
              {{ user.username }}
            </RouterLink>
          </td>
          <td>{{ user.points }}</td>
          <td>{{ user.articles_count }}</td>
          <td>{{ user.likes_count }}</td>
          <td>{{ user.followers_count }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { ref } from 'vue';

const store = useCounterStore();
const rankings = computed(() => store.rankings);
const placeholderImage = '@/assets/profile-placeholder.png'; // 기본 이미지 경로

onMounted(() => {
  if (!store.isLogin) {
    alert('로그인이 필요합니다.');
    store.router.push({ name: 'LogInView' });
    return;
  }

  store.fetchRankings().then(() => {
    console.log('Rankings from Store (after fetch):', store.rankings);
  });
});

// onMounted(() => {
//     rankings.value = [
//     { id: 1, username: 'user1', points: 100, articles_count: 5, likes_count: 10, followers_count: 3 },
//     { id: 2, username: 'user2', points: 80, articles_count: 3, likes_count: 8, followers_count: 1 },
//   ];
//     console.log(rankings.value)
//   if (!store.isLogin) {
//     // 로그인 상태가 아니면 로그인 페이지로 리다이렉트
//     alert('로그인이 필요합니다.');
//     store.router.push({ name: 'LogInView' });
//     return;
//   }
//   store.fetchRankings();
//   console.log(store.rankings);
// });
</script>

<style scoped>
.ranking-container {
  max-width: 800px;
  margin: 20px auto;
  text-align: center;
}

.ranking-table {
  width: 100%;
  border-collapse: collapse;
}

.ranking-table th,
.ranking-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.medal-icon {
  width: 24px;
  height: 24px;
}

.profile-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.profile-picture {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
