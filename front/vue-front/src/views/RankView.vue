<template>
  <div class="ranking-container">
    <h1>랭킹 페이지</h1>

    <!-- 랭크 시스템 안내 버튼 -->
    <div class="info-container">
      <button class="btn btn-secondary" @click="showModal = true">랭크 시스템 안내</button>
    </div>

    <table class="ranking-table">
      <thead>
        <tr>
          <th>순위</th>
          <th class="with-border">프로필</th>
          <th>이름</th>
          <th>랭크</th>
          <th>게시물 수</th>
          <th>좋아요 수</th>
          <th>팔로워 수</th>
          <th>추천 영화</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(user, index) in rankings"
          :key="user.id"
          :class="{ 'text-focus-in': animatedIndexes.includes(index), hidden: !animatedIndexes.includes(index) }"
        >
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
          <td class="with-border">
            <div class="profile-picture">
              <img :src="`http://127.0.0.1:8000${user.profile_picture}`" alt="프로필 사진" class="profile-img" />
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
          <!-- 추천 영화 -->
          <td>
            <div v-if="user.recommended_movie">
              <RouterLink :to="{ name: 'MovieDetail', params: { id: user.recommended_movie.movie.id } }">
                {{ user.recommended_movie.movie.title }}
              </RouterLink>
            </div>
            <div v-else>
              <span>추천 없음</span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- RankInfoModal 컴포넌트 -->
    <RankInfoModal v-if="showModal" :isVisible="showModal" @close="showModal = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import RankInfoModal from "@/components/RankInfoModal.vue";

// Pinia 상태 관리
const store = useCounterStore();
const rankings = computed(() => store.rankings); // 순위를 고정시키기 위한 데이터
const showModal = ref(false);

// 애니메이션 상태
const animatedIndexes = ref([]); // 애니메이션이 적용된 인덱스를 저장

const applySequentialAnimation = () => {
  rankings.value.forEach((_, index) => {
    setTimeout(() => {
      animatedIndexes.value.push(index);
    }, index * 300); // 각 행마다 300ms의 지연 추가
  });
};

// 랭크 이미지를 가져오는 함수
import bronzeRank from "@/assets/BronzeRank.png";
import silverRank from "@/assets/SilverRank.png";
import goldRank from "@/assets/GoldRank.png";
import platinumRank from "@/assets/PlatinumRank.png";
import diamondRank from "@/assets/DiamondRank.png";

const getRankImage = (rankTitle) => {
  switch (rankTitle) {
    case "Bronze": return bronzeRank;
    case "Silver": return silverRank;
    case "Gold": return goldRank;
    case "Platinum": return platinumRank;
    case "Diamond": return diamondRank;
    default: return bronzeRank;
  }
};

// 컴포넌트 로드 시 실행
onMounted(() => {
  if (!store.isLogin) {
    alert("로그인이 필요합니다.");
    store.router.push({ name: "LogInView" });
  } else {
    store.fetchRankings().then(() => {
      applySequentialAnimation(); // 순차적으로 애니메이션 적용
    });
  }
});
</script>

<style scoped>
/* 테이블 스타일 */
.ranking-container {
  max-width: 800px;
  width: 90%;
  margin: 20px auto;
  text-align: center;
}

.info-container {
  text-align: right;
  margin-bottom: 10px;
}

.ranking-table {
  width: 100%;
  border-collapse: separate; /* 셀 간격을 분리 */
  border-spacing: 0; /* 셀 간격 없음 */
  margin-bottom: 20px;
  background-color: #222; /* 테이블 배경색 */
  border: 1px solid #444; /* 테이블 전체 외곽선 */
}

.ranking-table th,
.ranking-table td {
  padding: 10px;
  text-align: center;
  background-color: #2c2c2c; /* 셀 배경색 */
  color: #fff; /* 글자색 */
}

/* 세로 구분선 스타일 */
.ranking-table th.with-border,
.ranking-table td.with-border {
  border-right: 1px solid #555; /* 프로필 옆 회색 선 */
}

/* 행 구분선 스타일 */
.ranking-table tbody tr {
  border-bottom: 1px solid #555; /* 행 간 회색 구분선 */
}

.ranking-table thead th {
  border-bottom: 2px solid #777; /* 헤더 구분선 */
}

.medal-icon {
  width: 32px;
  height: 32px;
}

/* 프로필 이미지를 둥글게 */
.profile-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

/* 애니메이션 */
.text-focus-in {
  animation: text-focus-in 1s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
}

@keyframes text-focus-in {
  0% {
    filter: blur(12px);
    opacity: 0;
  }
  100% {
    filter: blur(0px);
    opacity: 1;
  }
}

/* 처음에 숨김 */
.hidden {
  opacity: 0;
}
</style>
