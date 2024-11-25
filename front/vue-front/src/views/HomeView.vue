<template>
  <div class="main-page-container">
    <!-- Top Ranking Section -->
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

    <!-- Best Reviews Section -->
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
          <img :src="review.movie.poster_url" alt="포스터 이미지" class="poster" />
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

    <!-- Categories of Top Ranker -->
    <div class="top-ranker-categories-container" v-if="topRankerCategories">
      <h2>zㅣ존 Monster ★ {{ topThreeRankings[0]?.username }} ★님의 카테고리</h2>
      <div class="categories">
        <div
          v-for="category in topRankerCategories"
          :key="category.id"
          class="category-card"
          @click="navigateToCategoryDetail(category.id)"
        >
          <img
            :src="category.movies.length > 0 ? getFullPosterUrl(category.movies[0].poster_url) : '/default-category.png'"
            alt="카테고리 포스터"
            class="category-poster"
          />
          <h3>{{ category.name }}</h3>
          <p>영화 개수: {{ category.movies.length }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

// Pinia 상태 관리
const store = useCounterStore();
const router = useRouter();

// Top 3 랭킹 데이터 가져오기
const topThreeRankings = computed(() => store.rankings.slice(0, 3));

// 상태 관리
const topReviews = ref([]);
const isLoading = ref(true);
const topRankerCategories = ref(null);
const isLoadingCategories = ref(false);

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

// 포스터 URL 생성 함수
const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500";
  return `${baseUrl}${posterUrl}`;
};

// 프로필로 이동하는 함수
const navigateToProfile = (username) => {
  // 라우터를 사용하여 프로필 페이지로 이동
  window.location.href = `/profile/${username}`;
};

// API 호출: Top Reviews
const fetchTopReviews = async () => {
  try {
    const response = await axios.get(
      "http://127.0.0.1:8000/api/v1/communities/top-reviews/"
    );
    topReviews.value = response.data;
  } catch (error) {
    console.error("Error fetching top reviews:", error);
  } finally {
    isLoading.value = false;
  }
};

// API 호출: Top Ranker Categories
const fetchTopRankerCategories = async () => {
  if (!topThreeRankings.value[0]?.username) return;

  isLoadingCategories.value = true;
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/accounts/profile/${topThreeRankings.value[0].username}/categories/`,
      {
        headers: { Authorization: `Token ${store.token}` },
      }
    );
    topRankerCategories.value = response.data; // 성공적으로 데이터를 받음
  } catch (error) {
    console.error("Failed to fetch categories:", error);
  } finally {
    isLoadingCategories.value = false;
  }
};

// 상세 페이지로 이동
const navigateToDetail = (id) => {
  router.push({ name: "DetailView", params: { id } });
};

const navigateToCategoryDetail = (categoryId) => {
  window.location.href = `/categories/${categoryId}`;
};

// 데이터 로드
onMounted(async () => {
  if (!store.rankings.length) {
    await store.fetchRankings();
  }
  await fetchTopReviews();
  await fetchTopRankerCategories();
});

console.log('ppss',topReviews)
</script>


<style scoped>
/* 메인 페이지 컨테이너 스타일 */
.main-page-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 50px;
}

/* Top 랭킹 섹션 스타일 */
.top-ranking {
  position: relative;
  width: 400px;
  height: 300px;
}

.first {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
}

.second {
  position: absolute;
  top: 120px;
  left: 20%;
  transform: translateX(-50%);
  text-align: center;
}

.third {
  position: absolute;
  top: 120px;
  right: 20%;
  transform: translateX(50%);
  text-align: center;
}

.position-icon {
  width: 50px;
  height: 50px;
  cursor: pointer;
  transition: transform 0.2s;
}

.position-icon:hover {
  transform: scale(1.1);
}

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

/* 베스트 리뷰 섹션 */
.best-reviews-container {
  width: 100%;
  padding: 20px;
  border-top: 1px solid #ddd;
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
  align-items: center;
  gap: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  background-color: #f9f9f9; /* 조금 더 밝은 배경색 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.review-card:hover {
  transform: scale(1.03); /* 살짝 확대 효과 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* 호버 시 강조된 그림자 */
}

.poster {
  width: 100px;
  height: 150px;
  object-fit: cover;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 포스터 그림자 */
}

.review-details {
  display: flex;
  flex-direction: column;
  justify-content: center; /* 텍스트가 수직 중앙 정렬 */
  flex-grow: 1; /* 텍스트가 충분히 공간을 차지하도록 설정 */
}

.review-details h3 {
  margin: 0;
  font-size: 18px;
  font-weight: bold;
  color: #333; /* 다소 어두운 글씨 */
}

.review-details p {
  margin: 5px 0;
  font-size: 14px;
  color: #555; /* 중간 밝기의 글씨 */
}

.review-details p:first-of-type {
  font-weight: bold; /* 작성자 이름 강조 */
}

.review-details p:last-of-type {
  color: #777; /* 작성일자 다소 흐릿하게 표시 */
  font-size: 12px;
}


/* Top Ranker Categories Section */
.top-ranker-categories-container {
  border-top: 1px solid #ddd;
  padding-top: 20px;
}

.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.category-card {
  width: calc(25% - 20px);
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}

.category-card:hover {
  transform: scale(1.02);
}

.category-poster {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.category-card h3 {
  font-size: 18px;
  margin: 10px;
}

.category-card p {
  font-size: 14px;
  margin: 0 10px 10px;
}
</style>
