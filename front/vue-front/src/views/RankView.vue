<template>
  <div class="ranking-container">
    <h1>랭킹 페이지</h1>
    <table class="ranking-table">
      <thead>
        <tr>
          <th>#</th>
          <th>프로필</th>
          <th>이름</th>
          <th>랭크</th>
          <th>게시물 수</th>
          <th>좋아요 수</th>
          <th>팔로워 수</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in rankings" :key="user.id">
          <!-- 순위 -->
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
          <!-- 프로필 -->
          <td>
            <div class="profile-picture">
              <img :src="user.profile_picture || placeholderImage" alt="Profile" class="profile-img" />
            </div>
          </td>
          <!-- 이름 -->
          <td>
            <RouterLink :to="{ name: 'ProfileView', params: { username: user.username } }">
              {{ user.username }}
            </RouterLink>
          </td>
          <!-- 랭크 -->
          <td>
            <div class="rank-display">
              <img :src="getRankImage(user.rank_title)" :alt="user.rank_title" class="rank-icon" />
              {{ user.points }}
            </div>
          </td>
          <!-- 게시물 수 -->
          <td>{{ user.articles_count }}</td>
          <!-- 좋아요 수 -->
          <td>{{ user.likes_count }}</td>
          <!-- 팔로워 수 -->
          <td>{{ user.followers_count }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';

// Pinia 상태 관리
const store = useCounterStore();
const rankings = computed(() => store.rankings);
const placeholderImage = '@/assets/profile-placeholder.png';

import bronzeRank from '@/assets/BronzeRank.png';
import silverRank from '@/assets/SilverRank.png';
import goldRank from '@/assets/GoldRank.png';
import platinumRank from '@/assets/PlatinumRank.png';
import diamondRank from '@/assets/DiamondRank.png';

// 랭크 이미지를 가져오는 함수
const getRankImage = (rankTitle) => {
  switch (rankTitle) {
    case "Bronze":
      return bronzeRank;
    case "Silver":
      return silverRank;
    case "Gold":
      return goldRank;
    case "Platinum":
      return platinumRank;
    case "Diamond":
      return diamondRank;
    default:
      return bronzeRank; // 기본값
  }
};

// 컴포넌트가 로드될 때 실행
onMounted(() => {
  if (!store.isLogin) {
    alert('로그인이 필요합니다.');
    store.router.push({ name: 'LogInView' });
    return;
  }

  store.fetchRankings();
});
</script>

<style scoped>
/* 컨테이너 스타일 */
.ranking-container {
  max-width: 800px;
  margin: 20px auto;
  text-align: center;
}

/* 테이블 스타일 */
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

/* 메달 스타일 */
.medal-icon {
  width: 40px;
  height: 40px;
}

/* 프로필 이미지 스타일 */
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

/* 랭크 디스플레이 스타일 */
.rank-display {
  display: flex;
  align-items: center;
}

.rank-icon {
  width: 24px;
  height: 24px;
  margin-right: 8px;
}
</style>
