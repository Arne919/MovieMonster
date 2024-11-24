<template>
  <div class="review-card">
    <!-- 작성자 정보 -->
    <div class="author-section" @click="navigateToReviewDetail(article.id)">
      <img
        v-if="article.user_profile_image"
        :src="`${store.API_URL}${article.user_profile_image}`"
        alt="프로필 이미지"
        class="profile-image"
        @click.stop="navigateToProfile(article.user)"
      />
      <div>
        <p class="username">{{ article.user }}</p>
        <p class="created-at">작성일 : {{ store.formatDate(article.created_at) }}</p>
      </div>
    </div>

    <!-- 리뷰 내용 -->
    <div class="review-content">
      <p class="review-text">{{ article.content }}</p>
      <p class="rating">⭐ {{ article.rating.toFixed(1) }}</p>
    </div>

    <!-- 영화 정보 카드 -->
    <div class="movie-card" @click="navigateToMovieDetail(article.movie_id)">
      <img
        v-if="article.poster_url"
        :src="getFullPosterUrl(article.poster_url)"
        alt="영화 포스터"
        class="poster-image"
      />
      <div class="movie-info">
        <h4 class="movie-title">{{ article.movie_title }}</h4>
        <div class="movie-genres">
          <span v-for="genre in article.movie_genres" :key="genre" class="genre">
            {{ genre }}
          </span>
        </div>
        <p class="movie-overview">{{ article.movie_overview }}</p>
        <p class="movie-rating">⭐ {{ article.movie_rating.toFixed(1) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";

defineProps({
  article: Object,
});

const store = useCounterStore();
const router = useRouter();

// 리뷰 디테일 페이지로 이동
const navigateToReviewDetail = (articleId) => {
  router.push({ name: "DetailView", params: { id: articleId } });
};

// 작성자의 프로필 페이지로 이동
const navigateToProfile = (username) => {
  router.push({ name: "ProfileView", params: { username } });
};

// 영화 디테일 페이지로 이동
const navigateToMovieDetail = (movieId) => {
  router.push({ name: "MovieDetail", params: { id: movieId } });
};

// 영화 포스터 URL 생성
const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500";
  return `${baseUrl}${posterUrl}`;
};
</script>

<style scoped>
/* 동일한 스타일 유지 */
.review-card {
  display: flex;
  flex-direction: column;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.author-section {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  cursor: pointer; /* 클릭 가능 */
}

.profile-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
  cursor: pointer; /* 클릭 가능 */
}

.username {
  font-weight: bold;
}

.created-at {
  color: #888;
  font-size: 12px;
}

/* 기존 스타일 유지 */
.review-content {
  margin-bottom: 15px;
}

.review-text {
  font-size: 14px;
  margin-bottom: 10px;
}

.rating {
  font-weight: bold;
  color: #f39c12;
}

.movie-card {
  display: flex;
  cursor: pointer;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.movie-card:hover {
  transform: scale(1.02);
}

.poster-image {
  width: 100px;
  height: 150px;
  object-fit: cover;
}

.movie-info {
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.movie-title {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
}

.movie-genres {
  display: flex;
  gap: 5px;
}

.genre {
  background-color: #f1f1f1;
  padding: 2px 5px;
  font-size: 12px;
  border-radius: 4px;
}

.movie-overview {
  font-size: 12px;
  color: #666;
  margin-top: 10px;
  line-height: 1.4;
}

.movie-rating {
  font-weight: bold;
  color: #f39c12;
}
</style>
