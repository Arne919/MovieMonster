<template>
  <div class="container">
    <h1 class="text-center tracking-in-expand-fwd my-4">MY PROFILE</h1>
    <div class="profile-page">
      <!-- 좌측: 프로필 정보 -->
      <div class="profile-info">
        <div class="profile-header">
          <img :src="`http://127.0.0.1:8000${user.profile_picture}`" class="profile-img" alt="프로필 사진">
          <div class="profile-basic">
            <h1 class="profile-title">{{ user.username }}</h1>
            <div class="profile-follow-stats">
              <p>팔로잉 {{ user.followingsCount }}</p><hr/><hr/>
              <p>팔로워 {{ user.followersCount }}</p>
            </div>
            <div class="follow-button-wrapper">
            <button v-if="!isOwnProfile" class="follow-button" @click="toggleFollow">
              {{ isFollowed ? '언팔로우' : '팔로우' }}
            </button>
          </div>
          </div>
        </div>
        <div class="profile-details">
          <div class="stats-row">
            <div class="stat-box">
              <img :src="getRankImage(user.rank_title)" alt="랭크 이미지" class="rank-icon-small" />
              <p>{{ user.points }}</p>
            </div>
            <div class="stat-box">
              <h6>📝</h6>
              <p>{{ user.articlesCount }}</p>
            </div>
            <div class="stat-box">
              <h6>❤️</h6>
              <p>{{ user.likesCount }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 우측: 추천 영화 -->
      <div class="recommended-movie-section">
        <h2>이거 안보면 진짜 후회해요!</h2>
        <div v-if="!recommendedMovie">
          <p  class="not_yet_recommend">아직 추천하는 영화가 없어요.</p>
          <a v-if="isOwnProfile" class="add-movie" @click="openRecommendationModal">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            영화 추천하기
          </a>
        </div>
        <div v-else>
          <img :src="recommendedMovie.posterUrl" alt="추천 영화 포스터" />
          <h3>{{ recommendedMovie.title }}</h3>
          <p class="recommendation-reason">추천 이유: {{ recommendedMovie.reason }}</p>
          <a v-if="isOwnProfile" class="add-movie-after" @click="editRecommendation" >
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            추천 수정
          </a>
        </div>
      </div>
    </div>

    <!-- 유저의 카테고리 섹션 -->
    <div class="category-section">
      <div class="category-header">
        <h2>{{ user.username }}의 카테고리</h2>
        <a v-if="isOwnProfile" class="add-category" @click.prevent="showCreateCategoryModal = true">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            새 카테고리
        </a>
      </div>
      <div v-if="categories.length === 0" class="empty-message">
        <p>아직 카테고리가 없습니다.</p>
      </div>

      <div v-else class="category-list">
      <div
        v-for="category in categories"
        :key="category.id"
        class="category-card"
        @click="goToCategoryDetail(category.id)"
      >
      <div class="image-container">
        <!-- 영화 포스터 또는 디폴트 이미지 -->
        <img :src="category.movies.length > 0 ? getFullPosterUrl(category.movies[0].poster_url) : 'http://127.0.0.1:8000/media/default_categories/default-category.png'" 
        alt="카테고리 이미지" 
        class="category-poster">
      </div>
      <h3>{{ category.name }}</h3>
      <p>영화 개수: {{ category.movies.length }}</p>
    </div>
  </div>
      
  <!-- 새 카테고리 추가 모달 -->
  <CreateCategoryModal
    v-if="showCreateCategoryModal"
    @close="closeCreateCategoryModal"
    @categoryCreated="addCategory"
  />
    </div>

    

    <!-- 추천 영화 모달 -->
    <div v-show="showRecommendationModal" class="modal">
  <div class="modal-content">
    <h2>추천 영화 선택</h2>
    <input v-model="searchQuery" @input="searchMovies" placeholder="영화 제목 입력" />

        <!-- 영화 검색 결과 -->
        <ul>
          <li v-for="movie in searchResults" :key="movie.id">
            {{ movie.title }}
            <button @click="selectRecommendedMovie(movie)">선택</button>
          </li>
        </ul>

        <!-- 선택된 영화 포스터 및 정보 -->
        <div v-if="selectedMovie" class="selected-movie-preview">
          <h3>선택된 영화:</h3>
          <img :src="selectedMovie.posterUrl" alt="선택된 영화 포스터" class="movie-poster-preview" />
          <p>{{ selectedMovie.title }}</p>
        </div>

        <!-- 추천 이유 작성 -->
        <textarea
          v-model="recommendationReason"
          placeholder="추천 이유를 작성해주세요"
          class="recommendation-reason"
        ></textarea>
        <button @click="saveRecommendation" class="save-btn">완료</button>
        <button @click="closeRecommendationModal" class="close-modal-btn">닫기</button>
      </div>
      <!-- 카테고리 추가 모달 -->
    <AddToCategoryModal
      v-if="showCategoryModal"
      :movie-id="movie.id"
      @close="showCategoryModal = false"
    />
  </div>
</div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import CreateCategoryModal from "@/components/CreateCategoryModal.vue";

// Vue Router와 Pinia 스토어 사용
const route = useRoute();
const router = useRouter();
const store = useCounterStore();

const toggleFollow = async () => {
  console.log("Toggle Follow clicked"); // 디버깅용
  try {
    const response = await axios.post(
      `http://127.0.0.1:8000/accounts/${user.value.id}/follow/`,
      null,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    // 응답 데이터를 사용하여 상태 업데이트
    isFollowed.value = response.data.is_followed;
    user.value.followersCount = response.data.followers_count;
    user.value.followingsCount = response.data.followings_count;

    console.log("Follow toggle success:", response.data); // 디버깅용
  } catch (error) {
    console.error("Error toggling follow:", error);
  }
};

const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500"; // TMDB 이미지 베이스 URL
  return `${baseUrl}${posterUrl}`;
};

// 랭크 이미지를 가져오는 함수
import bronzeRank from '@/assets/BronzeRank.png';
import silverRank from '@/assets/SilverRank.png';
import goldRank from '@/assets/GoldRank.png';
import platinumRank from '@/assets/PlatinumRank.png';
import diamondRank from '@/assets/DiamondRank.png';

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

// 유저 데이터 상태 관리
const user = ref({
  username: '',
  rank_title: '',
  followingsCount: 0,
  followersCount: 0,
  articlesCount: 0, // 작성한 게시글 수
  likesCount: 0, // 받은 좋아요 수
});
const isFollowed = ref(false);
const categories = ref([]);
const showCreateCategoryModal = ref(false); // 모달 표시 여부
const showRecommendationModal = ref(false);
const recommendedMovie = ref(null); // 추천 영화 상태
const recommendationReason = ref('');
const searchQuery = ref('');
const searchResults = ref([]);
const selectedMovie = ref(null); // 선택된 영화 상태 추가

// 현재 프로필이 로그인된 사용자의 것인지 확인
const isOwnProfile = computed(() => store.user.username === route.params.username);

// API를 통해 프로필 데이터 가져오기
const fetchProfile = async () => {
  try {
    const { data } = await axios.get(
      `http://127.0.0.1:8000/accounts/profile/${route.params.username}/`, 
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );

    // Use store.getRankTitle to calculate the rank_title if not provided
    const rankTitle = data.rank_title || store.getRankTitle(data.points);

    user.value = {
      id: data.id,
      username: data.username,
      points: data.points,
      rank_title: rankTitle, // Use calculated rank_title
      followingsCount: data.followings_count,
      followersCount: data.followers_count,
      articlesCount: data.articles_count,
      likesCount: data.likes_count,
      profile_picture: data.profile_image,
      // reason: data.recommended_movie.reason, // 추천 이유
    };

    // 추천 영화 데이터 처리
    if (data.recommended_movie) {
      recommendedMovie.value = {
        id: data.recommended_movie.movie.id,
        title: data.recommended_movie.movie.title,
        posterUrl: getFullPosterUrl(data.recommended_movie.movie.poster_url),
        reason: data.recommended_movie.reason,
      };
      console.log("추천 영화 로드 성공:", recommendedMovie.value);
    } else {
      recommendedMovie.value = null;
      console.log("추천 영화 데이터 없음");
    }
    console.log("프로필 데이터 로드 성공:", user.value);
    console.log("추천 영화 데이터:", recommendedMovie.value);

    console.log(user.value);
    isFollowed.value = data.is_followed;
    categories.value = data.categories;
    // recommendedMovie.value = data.recommended_movie || null; // 추천 영화 데이터
  } catch (error) {
    console.error('Error fetching profile:', error);
  }
};

// 카테고리 상세 페이지로 이동
const goToCategoryDetail = (categoryId) => {
  router.push(`/categories/${categoryId}`);
};

// 새 카테고리 모달 열기/닫기
const openCreateCategoryModal = () => {
  showCreateCategoryModal.value = true;
};
const closeCreateCategoryModal = () => {
  showCreateCategoryModal.value = false;
};

// 새 카테고리 목록에 추가
const addCategory = (category) => {
  categories.value.push(category);
};

// 추천 영화 모달 열기/닫기
// const openRecommendationModal = () => (showRecommendationModal.value = true);
const openRecommendationModal = () => {
  console.log("추천 수정 클릭됨");
  console.log("모달 상태 이전:", showRecommendationModal.value);
  showRecommendationModal.value = true; // 모달을 열기 위해 값 변경
  console.log("모달 상태 이후:", showRecommendationModal.value);
};
const closeRecommendationModal = () => {
  showRecommendationModal.value = false;
  searchQuery.value = '';
  searchResults.value = [];
  recommendationReason.value = '';
};

// 영화 검색
const searchMovies = async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = [];
    return;
  }
  try {
    const response = await axios.get(`${store.API_URL}/accounts/movies/search/`, {
      params: { title: searchQuery.value.trim() },
      headers: { Authorization: `Token ${store.token}` },
    });
    searchResults.value = response.data;
  } catch (error) {
    console.error('Error searching movies:', error);
  }
};

const selectRecommendedMovie = (movie) => {
  // 선택된 영화 데이터를 업데이트
  selectedMovie.value = {
    id: movie.id,
    title: movie.title,
    posterUrl: getFullPosterUrl(movie.poster_url), // 포스터 URL 생성
  };

  // 추천 영화 데이터에도 반영 (저장을 위해 필요)
  recommendedMovie.value = {
    id: movie.id,
    title: movie.title,
    posterUrl: getFullPosterUrl(movie.poster_url),
  };

  console.log("선택된 영화 데이터:", selectedMovie.value); // 디버깅용
};

// 추천 영화 저장
const saveRecommendation = async () => {
  if (!recommendedMovie.value || !recommendedMovie.value.id || !recommendationReason.value.trim()) {
    alert("영화와 추천 이유를 모두 입력해주세요.");
    console.error("추천 영화 저장 실패 - 데이터 확인:", {
      movie: recommendedMovie.value,
      reason: recommendationReason.value,
    });
    return;
  }
  try {
    const response = await axios.post(
      `${store.API_URL}/accounts/recommend-movie/`,
      {
        movie_id: recommendedMovie.value.id,
        reason: recommendationReason.value.trim(),
      },
      { headers: { Authorization: `Token ${store.token}` } }
    );

    // 서버 응답을 추천 영화 데이터로 반영
    recommendedMovie.value = {
      id: response.data.movie.id,
      title: response.data.movie.title,
      posterUrl: getFullPosterUrl(response.data.movie.poster_url),
      reason: response.data.reason,
    };

    console.log("추천 영화 저장 성공:", response.data);

    closeRecommendationModal();
    alert("추천 영화가 저장되었습니다!");
  } catch (error) {
    console.error("추천 영화 저장 중 오류 발생:", error.response?.data || error);
  }
};

// 추천 영화 수정
const editRecommendation = () => {
  console.log("추천 수정 버튼 클릭됨"); // 디버깅용 로그
  openRecommendationModal();
  recommendationReason.value = recommendedMovie.value.reason || '';
};

onMounted(() => {
  fetchProfile();
});

// 라우트 변경을 감지하고 새 데이터를 로드
watch(() => route.params.username, (newUsername, oldUsername) => {
  console.log(`Route username changed: ${oldUsername} -> ${newUsername}`);
  fetchProfile();
});
</script>




<style scoped>



.container {
  margin-top: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.text-center {
  color: #e02ff0;
  font-size: 2rem;
  font-weight: bold;
  animation: tracking-in-expand-fwd 0.8s cubic-bezier(0.215, 0.610, 0.355, 1.000) both; /* 애니메이션 추가 */
}

@keyframes tracking-in-expand-fwd {
  0% {
    letter-spacing: -0.5em;
    transform: translateZ(-700px);
    opacity: 0;
  }
  40% {
    opacity: 0.6;
  }
  100% {
    transform: translateZ(0);
    opacity: 1;
  }
}


/* 전체 페이지 스타일 */
.profile-page {
  width: 80%; /* 전체 컨테이너 너비를 80%로 설정 */
  max-width: 1200px; /* 최대 고정 너비 설정 */
  margin: 0 auto; /* 중앙 정렬 */
  display: grid;
  grid-template-columns: 1fr 1fr; /* 좌측 1, 우측 2 비율 */
  gap: 20px;
  padding: 20px;
  /* background-color: #e02ff017; */
  color: #f5f5f5;
  border-radius: 10px;
}


/* 프로필 정보 (좌측 섹션) */
.profile-info {
  background-color: #e02ff01c;
  border-radius: 10px;
  margin: 20px;
  padding: 30px;
  display: flex;
  flex-direction: column;
  /* position: relative; */
  gap: 20px;
  height: 425px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
}

.profile-header img {
  display: flex;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 1.5px solid #f5f5f5;
}


.profile-basic {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
}

.profile-title {
  align-items: center;
  font-size: 2.5rem;
  /* font-weight: bold; */
}

.profile-follow-stats {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.follow-button {
  margin-top: 10px;
  padding: 10px;
  width: 100%; /* 버튼 길이를 프로필 스탯에 맞춤 */
  background-color: #3897f0;
  color: white;
  font-weight: bold;
  font-size: 1rem;
  border-radius: 10px;
  border: none;
  cursor: pointer;
}

.follow-button:hover {
  background-color: #217ac0;
}

.profile-details {
  margin-top: auto; /* 프로필 헤더와 버튼 사이 고정된 거리 확보 */
}

/* 랭크 이미지 */
.rank-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* 랭크 이미지 및 유저 이름 */
.username-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rank-icon-small {
  width: 25px;
  height: 25px;
}

.rank-stats {
  font-size: 0.9rem;
}


/* 포인트, 게시글, 좋아요 수 */
.stats-row {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
  /* background-color: #e02ff02c; */
  padding: 10px 20px;
  /* border-radius: 10px; */
  text-align: center;
  /* border: 1px solid #e02ff06b; */
  border-top: 1px solid #e02ff06b;
  color: white;
  font-size: 1rem;
}

.stat-box {
  /* background-color: #282b3b; */
  padding: 10px 20px;
  border-radius: 10px;
  text-align: center;
  color: white;
  font-size: 0.9rem;
}
/* 추천 영화 섹션 */
.not_yet_recommend {
  padding-top: 15%;
}

.recommended-movie-section {
  text-align: center;
  padding: 30px;
  background-color: #e02ff01c;
  border-radius: 10px;
  height: 425px;
  margin: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.recommendation-reason {
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 최대 3줄까지만 보이게 설정 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
  font-size: 0.9rem; /* 글자 크기 조정 */
  line-height: 1.4; /* 줄 간격 조정 */
  color: #aaa; /* 텍스트 색상 */
  margin: 5px 0;
}



.recommended-movie-section h2 {
  font-size: 1.2rem;
  margin-bottom: 15px;
  color: #f5f5f5;
}

.recommended-movie-section img {
  width: 150px; /* 포스터 크기 조정 */
  height: 225px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 10px;
}

.recommended-movie-section h3 {
  font-size: 1rem;
  color: #fff;
}

.recommended-movie-section p {
  font-size: 0.9rem;
  color: #aaa;
  margin: 5px 0;
}

/* 카테고리 섹션 */
.category-section {
  margin-top: 30px;
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); /* 카테고리 이미지의 그리드 레이아웃 */
  gap: 15px;
  /* margin-top: 15px; */
}

.category-card {
  text-align: center;
  /* font-size: 0.9rem; */
}

.category-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 10px;
  border: 1px solid #ddd;
  margin: 0 auto 10px auto;
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  z-index: 9999;
  width: 80%;
  max-width: 450px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: block; /* 강제로 표시 */
}

.modal-content {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.hidden {
  display: none; /* 숨김 */
}

/* 네온 버튼 스타일 */
a {
  position: relative;
  display: inline-block;
  padding: 15px 20px;
  font-size: 14px; /* 텍스트 크기 조정 */
    margin: 50px 0; /* 여백 조정 */
  color: #e02ff0;
  text-decoration: none;
  text-transform: uppercase;
  transition: 0.5s;
  letter-spacing: 1px;
  overflow: hidden;
  margin-right: 20px;
  margin-top: 40px;
}

a:hover {
  background: #e02ff0;
  color: #050801;
  box-shadow: 0 0 5px #e02ff0, 0 0 25px #e02ff0, 0 0 50px #e02ff0,
    0 0 200px #e02ff0;
  -webkit-box-reflect: below 1px linear-gradient(transparent, #0005);
}

a span {
  position: absolute;
  display: block;
}

a span:nth-child(1) {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #e02ff0);
  animation: animate1 1s linear infinite;
}

@keyframes animate1 {
  0% {
    left: -100%;
  }
  50%,
  100% {
    left: 100%;
  }
}

a span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #e02ff0);
  animation: animate2 1s linear infinite;
  animation-delay: 0.25s;
}

@keyframes animate2 {
  0% {
    top: -100%;
  }
  50%,
  100% {
    top: 100%;
  }
}

a span:nth-child(3) {
  bottom: 0;
  right: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #e02ff0);
  animation: animate3 1s linear infinite;
  animation-delay: 0.5s;
}

@keyframes animate3 {
  0% {
    right: -100%;
  }
  50%,
  100% {
    right: 100%;
  }
}

a span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #e02ff0);
  animation: animate4 1s linear infinite;
  animation-delay: 0.75s;
}

@keyframes animate4 {
  0% {
    bottom: -100%;
  }
  50%,
  100% {
    bottom: 100%;
  }
}
</style>
