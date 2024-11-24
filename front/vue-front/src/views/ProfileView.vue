<template>
  <div>
    <div>
      <img :src="`http://127.0.0.1:8000${user.profile_picture}`" alt="프로필 사진">

      <h1>{{ user.username }}의 프로필 페이지</h1>
    </div>
    <!-- 사용자 랭크 -->
    <p>
      랭크: 
      <span class="rank-display">
        <img :src="getRankImage(user.rank_title)" :alt="user.rank_title" class="rank-icon" />
        {{ user.rank_title }}
      </span>
    </p>
    <p>포인트: {{ user.points }}</p>
    <p>팔로잉: <span id="followings-count">{{ user.followingsCount }}</span></p>
    <p>팔로워: <span id="followers-count">{{ user.followersCount }}</span></p>
    <p>게시글 수: <span id="articles-count">{{ user.articlesCount }}</span></p>
    <p>받은 좋아요 수: <span id="like-count">{{ user.likesCount }}</span></p>
    <div v-if="!isOwnProfile">
      <button @click="toggleFollow" id="followBtn">
        {{ isFollowed ? '언팔로우' : '팔로우' }}
      </button>
    </div>

    <h2>{{ user.username }}의 카테고리</h2>
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
      <!-- 새 카테고리 추가 버튼 -->
      <div v-if="isOwnProfile" class="add-category">
        <button class="btn btn-primary" @click="showCreateCategoryModal = true">
          새 카테고리 만들기
        </button>
      </div>
      <!-- 새 카테고리 추가 모달 -->
      <CreateCategoryModal
        v-if="showCreateCategoryModal"
        @close="closeCreateCategoryModal"
        @categoryCreated="addCategory"
      />
    </div>

    <!-- 추천 영화 섹션 -->
    <div class="recommended-movie-section">
      <h2>이거 안보면 진짜 후회해요!</h2>
      <div v-if="!recommendedMovie" class="empty-recommendation">
        <p>아직 추천하는 영화가 없어요.</p>
        <button v-if="isOwnProfile" @click="openRecommendationModal">영화 추천하기</button>
      </div>
      <div v-if="recommendedMovie">
        <div class="recommendation-display">
          <div class="movie-details">
            <img :src="recommendedMovie.posterUrl" alt="추천 영화 포스터" class="movie-poster" />
            <div>
              <h3>{{ recommendedMovie.title }}</h3>
              <p>추천 이유: {{ recommendedMovie.reason }}</p>
            </div>
          </div>
          <button v-if="isOwnProfile" @click="editRecommendation">추천 수정</button>
        </div>
      </div>
    </div>

    <!-- 추천 영화 모달 -->
    <div v-if="showRecommendationModal" class="modal">
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
const openRecommendationModal = () => (showRecommendationModal.value = true);
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
.recommended-movie-section {
  margin-top: 30px;
}

.movie-details {
  display: flex;
  align-items: center;
}

.movie-poster {
  width: 100px;
  height: 150px;
  margin-right: 20px;
}

/* 선택된 영화 미리보기 스타일 */
.selected-movie-preview {
  margin-top: 20px;
  text-align: center;
}

.movie-poster-preview {
  width: 150px;
  height: auto;
  margin-bottom: 10px;
}

.recommendation-reason {
  width: 100%;
  margin-top: 10px;
  height: 80px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
}

.close-modal-btn {
  margin-top: 10px;
}

/* 카드 내용 */
.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 10px;
}
/* 이미지 컨테이너 */
.image-container {
  width: 300px;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  border-radius: 8px;
  margin: 0 auto 10px auto;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.category-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.category-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: calc(33.333% - 20px);
  margin: 10px;
  background-color: #fff;
}

.category-card h3 {
  margin-top: 0;
  font-size: 1.2em;
}

.category-poster {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

/* 랭크 표시 스타일 */
.rank-display {
  display: inline-flex;
  align-items: center;
}

.rank-icon {
  width: 20px;
  height: 20px;
  margin-right: 5px;
}
</style>
