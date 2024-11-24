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

    <!-- 베스트 리뷰 섹션 -->
    <div class="best-reviews-container">
      <h2>베스트 리뷰</h2>
      <div v-if="isLoading" class="loading-message">리뷰 데이터를 불러오는 중입니다...</div>
      <div v-else class="best-reviews">
        <div
          v-for="review in topReviews"
          :key="review.id"
          class="review-card"
          @click="navigateToDetail(review.id)"
        >
          <img :src="review.poster_url" alt="포스터 이미지" class="poster" />
          <div class="review-details">
            <h3>{{ review.title }}</h3>
            <p>작성자: {{ review.user }}</p>
            <p>평점: {{ review.rating }} / 10</p>
            <p>{{ review.content }}...</p>
            <p>좋아요: {{ review.like_count }}</p>
            <p>작성일: {{ formatDate(review.created_at) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from 'vue-router';

// Pinia 상태 관리
const store = useCounterStore();

// Top 3 랭킹 데이터 가져오기
const topThreeRankings = computed(() => store.rankings.slice(0, 3));

// 상태 관리
const topReviews = ref([]);
const isLoading = ref(true);
const router = useRouter();

// 날짜 포맷 함수
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
};

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

// API 호출
const fetchTopReviews = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/v1/communities/top-reviews/');
    topReviews.value = response.data;
  } catch (error) {
    console.error('Error fetching top reviews:', error);
  } finally {
    isLoading.value = false;
  }
};

// 상세 페이지로 이동
const navigateToDetail = (id) => {
  router.push({ name: 'DetailView', params: { id } });
};

// 데이터 로드
onMounted(async () => {
  if (!store.rankings.length) {
    await store.fetchRankings();
  }
  fetchTopReviews()
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
  flex-direction: column; /* 랭킹과 베스트 리뷰 섹션을 세로로 배치 */
  align-items: center;
}

/* Top 랭킹 섹션 스타일 */
.top-ranking {
  position: relative;
  width: 400px;
  height: 300px;
  margin-bottom: 50px; /* 베스트 리뷰와의 간격 */
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

/* 베스트 리뷰 섹션 스타일 */
.best-reviews-container {
  width: 100%;
  padding: 20px;
  border-top: 1px solid #ddd; /* 구분선을 추가하여 랭킹과 시각적으로 분리 */
}

.loading-message {
  text-align: center;
  font-size: 16px;
  color: #888;
}

.best-reviews {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.review-card {
  display: flex;
  gap: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: transform 0.2s;
}

.review-card:hover {
  transform: scale(1.02);
}

.poster {
  width: 100px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
}

.review-details {
  display: flex;
  flex-direction: column;
}

.review-details h3 {
  margin: 0;
  font-size: 18px;
}

.review-details p {
  margin: 5px 0;
  font-size: 14px;
  color: #555;
}
</style>
