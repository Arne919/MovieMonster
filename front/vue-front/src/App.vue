<template>
  <header>
    <nav class="navbar">
      <div class="container">
        <!-- 네비게이션 링크 -->
        <RouterLink :to="{ name: 'SignUpView' }" class="nav-link">회원가입</RouterLink> |
        <RouterLink :to="{ name: 'ArticleView' }" class="nav-link">리뷰</RouterLink> |
        <RouterLink :to="{ name: 'MovieView' }" class="nav-link">영화</RouterLink> |
        <RouterLink :to="{ name: 'GameView' }" class="nav-link">게임</RouterLink> |
        <RouterLink :to="{ name: 'RankView' }" class="nav-link">랭크</RouterLink> |

        <RouterLink
          v-if="isLogin"
          :to="{ name: 'ProfileView', params: { username: user.username } }"
          class="nav-link"
        >
          내 프로필
        </RouterLink>
        <RouterLink v-else :to="{ name: 'LogInView' }" class="nav-link">로그인</RouterLink>

        <!-- 사용자 정보 -->
        <div class="user-info" v-if="user.username">
          <div v-if="user.rank_title" class="rank-display">
            <img :src="getRankImage(user.rank_title)" :alt="user.rank_title" class="rank-icon" />
          </div> |
          {{ user.username }} | 포인트: {{ user.current_points }}

        </div>

        <form @submit.prevent="logOut" v-if="isLogin">
          <input type="submit" value="로그아웃">
        </form>
      </div>
    </nav>
  </header>

  <!-- 동적 라우터 뷰 -->
  <RouterView />
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const isLogin = computed(() => store.isLogin);
const user = computed(() => store.user);

// 랭크 이미지 불러오기
import bronzeRank from '@/assets/BronzeRank.png';
import silverRank from '@/assets/SilverRank.png';
import goldRank from '@/assets/GoldRank.png';
import platinumRank from '@/assets/PlatinumRank.png';
import diamondRank from '@/assets/DiamondRank.png';

// 랭크 이미지를 반환하는 함수
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

// 로그아웃 기능
const logOut = () => {
  store.logOut();
};

// 마운트 시 사용자 정보 가져오기
onMounted(() => {
  if (isLogin.value) {
    store.fetchUserPoints(); // 사용자 포인트 정보 가져오기
  }
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

/* 랭크 표시 스타일 */
.rank-display {
  display: inline-flex;
  align-items: center;
  margin-left: 10px;
}

.rank-icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}
</style>
