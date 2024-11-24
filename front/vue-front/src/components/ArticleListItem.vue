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

     <!-- 좋아요 기능 -->
     <div class="like-container">
      <button class="like-button" @click="toggleLike">
        <!-- props.article.is_liked 대신 로컬 상태 isLiked 사용 -->
        <span v-if="isLiked" class="liked-icon">❤️</span>
        <span v-else class="like-icon">🤍</span>
      </button>
      <span class="like-count">{{ likeCount }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import axios from "axios"; // axios 임포트

const props = defineProps({ article: { type: Object, required: true } });
const emit = defineEmits(["update:article"]); // 부모에게 상태 전달 이벤트 정의


const store = useCounterStore();
const router = useRouter();

// 반응형 데이터
const article = ref({ ...props.article }); // props.article을 반응형으로 관리

// 초기화: props.article.is_liked를 기반으로 isLiked를 설정
const isLiked = ref(props.article.is_liked ?? false); // nullish coalescing: 없으면 false
const likeCount = ref(props.article.like_count ?? 0);

// 좋아요 토글
const toggleLike = async () => {
  try {
    const updatedArticle = await store.updateLikeStatus(article.value.id);

    // Local state 업데이트
    article.value.is_liked = updatedArticle.action === "added";
    article.value.like_count = updatedArticle.like_count;

    // 부모 컴포넌트에 업데이트 알림
    emit("update-article", article.value);
  } catch (err) {
    console.error("좋아요 상태 업데이트 실패:", err);
  }
};


// Props 변경 감지
watch(
  () => props.article,
  (newArticle) => {
    if (newArticle) {
      console.log("Updated props.article:", newArticle);
      isLiked.value = newArticle.is_liked ?? false; // is_liked 반영
      likeCount.value = newArticle.like_count ?? 0; // like_count 반영
      console.log("Local state isLiked:", isLiked.value);
    }
  },
  { immediate: true } // 초기에도 실행
);

// 디테일 페이지 이동
const navigateToReviewDetail = (articleId) => {
  router.push({ name: "DetailView", params: { id: articleId } });
};

// 프로필 페이지 이동
const navigateToProfile = (username) => {
  router.push({ name: "ProfileView", params: { username } });
};

// 영화 디테일 페이지 이동
const navigateToMovieDetail = (movieId) => {
  router.push({ name: "MovieDetail", params: { id: movieId } });
};

// 포스터 URL 생성
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

/* 좋아요 기능 스타일 */
.like-container {
  display: flex;
  align-items: center;
  margin-top: 15px;
  gap: 8px;
}

.like-button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 20px;
  display: flex;
  align-items: center;
}

.like-icon,
.liked-icon {
  color: #ff6b6b;
}

.like-count {
  font-size: 16px;
  color: #333;
}
</style>
