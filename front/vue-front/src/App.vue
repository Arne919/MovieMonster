<template>
  <div class="app-wrapper">
  <header>
    <nav class="navbar">
      <div class="container">
        <!-- 네비게이션 링크 -->
        <RouterLink :to="{ name: 'SignUpView' }" class="nav-link">회원가입</RouterLink> |
        <RouterLink :to="{ name: 'HomeView' }" class="nav-link">홈</RouterLink> |
        <RouterLink :to="{ name: 'ArticleView' }" class="nav-link">리뷰</RouterLink> |
        <RouterLink :to="{ name: 'MovieView' }" class="nav-link">영화</RouterLink> |
        <RouterLink :to="{ name: 'GameView' }" class="nav-link">게임</RouterLink> |
        <RouterLink :to="{ name: 'RankView' }" class="nav-link">랭크</RouterLink> |

        <RouterLink
        v-if="isLogin && user.username"
        :to="{ name: 'ProfileView', params: { username: user.username || '' } }"
        class="nav-link"
        >
        내 프로필
      </RouterLink>

        <RouterLink v-else :to="{ name: 'LogInView' }" class="nav-link">로그인</RouterLink>

        <!-- 사용자 정보 -->
        <div class="user-info" v-if="!isLoading && user.username">
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
  <main class="content">
      <!-- 로딩 상태 -->
      <div v-if="isLoading" class="loading">
        <p>Loading...</p>
      </div>
      <!-- 동적 라우터 뷰 -->
      <RouterView v-else />
    </main>
  


  

  <footer class="footer">
    <div class="footer-container">
      <!-- 왼쪽 섹션 -->
      <div class="footer-left">
        <p><strong>MovieMoster</strong> | 팀장 하건수 | <a href="mailto:rjs4013@naver.com">rjs4013@naver.com</a></p>
        <p>팀원 강혜경 | <a href="mailto:ghgghg96@naver.com">ghgghg96@naver.com</a> | 대표전화 010-1234-5678</p>
      </div>

      <!-- 오른쪽 섹션 -->
      <div class="footer-right">
        <p>Copyright &copy; 2024 by MovieMoster, Inc. All Rights Reserved.</p>
      </div>
    </div>
  </footer>
</div>
</template>

<script setup>
import { computed, ref, watchEffect } from "vue";
import { useCounterStore } from "@/stores/counter";

const store = useCounterStore();
const isLogin = computed(() => store.isLogin);
const user = computed(() => store.user);

const isLoading = ref(true); // 로딩 상태 관리

// 랭크 이미지 불러오기
import bronzeRank from "@/assets/BronzeRank.png";
import silverRank from "@/assets/SilverRank.png";
import goldRank from "@/assets/GoldRank.png";
import platinumRank from "@/assets/PlatinumRank.png";
import diamondRank from "@/assets/DiamondRank.png";

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

// 상태값이 로드되었는지 감지
watchEffect(async () => {
  if (store.token) {
    await store.fetchUser(); // 사용자 정보 로드
    await store.fetchUserPoints(); // 사용자 포인트 로드
    isLoading.value = false; // 로드 완료
  } else {
    isLoading.value = false; // 토큰이 없는 경우도 로드 완료로 처리
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
