<template>
  <div class="main-page-container">
    <div class="top-ranking">
      <!-- 2등 -->
      <div v-if="topThreeRankings[1]" class="second">
        <img
          src="@/assets/second.png"
          alt="2등"
          class="position-icon"
          @click="navigateToProfile(topThreeRankings[1].username)"
        />
        <div class="user-info">
          <img
            :src="getRankImage(topThreeRankings[1].rank_title)"
            :alt="topThreeRankings[1].rank_title"
            class="rank-icon"
          />
          <span class="username">{{ topThreeRankings[1].username }}</span>
        </div>
      </div>

      <!-- 1등 -->
      <div v-if="topThreeRankings[0]" class="first">
        <img
          src="@/assets/first.png"
          alt="1등"
          class="position-icon"
          @click="navigateToProfile(topThreeRankings[0].username)"
        />
        <div class="user-info">
          <img
            :src="getRankImage(topThreeRankings[0].rank_title)"
            :alt="topThreeRankings[0].rank_title"
            class="rank-icon"
          />
          <span class="username">{{ topThreeRankings[0].username }}</span>
        </div>
      </div>

      <!-- 3등 -->
      <div v-if="topThreeRankings[2]" class="third">
        <img
          src="@/assets/third.png"
          alt="3등"
          class="position-icon"
          @click="navigateToProfile(topThreeRankings[2].username)"
        />
        <div class="user-info">
          <img
            :src="getRankImage(topThreeRankings[2].rank_title)"
            :alt="topThreeRankings[2].rank_title"
            class="rank-icon"
          />
          <span class="username">{{ topThreeRankings[2].username }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";

// Pinia 상태 관리
const store = useCounterStore();

// Top 3 랭킹 데이터 가져오기
const topThreeRankings = computed(() => store.rankings.slice(0, 3));

// 랭크 이미지를 가져오는 함수
import bronzeRank from "@/assets/BronzeRank.png";
import silverRank from "@/assets/SilverRank.png";
import goldRank from "@/assets/GoldRank.png";
import platinumRank from "@/assets/PlatinumRank.png";
import diamondRank from "@/assets/DiamondRank.png";

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

// 프로필로 이동하는 함수
const navigateToProfile = (username) => {
  // 라우터를 사용하여 프로필 페이지로 이동
  window.location.href = `/profile/${username}`;
};

// 데이터 로드
onMounted(async () => {
  if (!store.rankings.length) {
    await store.fetchRankings();
  }
});
</script>

<style scoped>
/* 메인 페이지 컨테이너 스타일 */
.main-page-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Top 랭킹 섹션 스타일 */
.top-ranking {
  position: relative;
  width: 400px;
  height: 300px;
}

/* 1등 */
.first {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

/* 2등 */
.second {
  position: absolute;
  top: 120px;
  left: 20%;
  transform: translateX(-50%);
  text-align: center;
}

/* 3등 */
.third {
  position: absolute;
  top: 120px;
  right: 20%;
  transform: translateX(50%);
  text-align: center;
}

/* 순위 이미지 스타일 */
.position-icon {
  width: 50px;
  height: 50px;
  cursor: pointer;
  transition: transform 0.2s;
}

.position-icon:hover {
  transform: scale(1.1); /* 이미지 확대 효과 */
}

/* 유저 정보 스타일 */
.user-info {
  margin-top: 10px;
}

.rank-icon {
  width: 30px;
  height: 30px;
}

.username {
  font-size: 16px;
  font-weight: bold;
  margin-top: 5px;
  display: block;
}
</style>
