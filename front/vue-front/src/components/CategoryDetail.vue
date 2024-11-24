<template>
  <div>
    <h1>{{ category.name }} 카테고리</h1>
    <div v-if="isOwner">
      <button @click="startEditingName" v-if="!isEditingName" class="edit-btn">이름 수정</button>
      <input
        v-if="isEditingName"
        v-model="newCategoryName"
        type="text"
        class="edit-category-input"
        placeholder="새 카테고리 이름 입력"
      />
      <button v-if="isEditingName" @click="saveCategoryName" class="save-btn">저장</button>
      <button v-if="isEditingName" @click="cancelEditingName" class="cancel-btn">취소</button>
      <button @click="openAddMovieModal" class="add-movie-btn">이 카테고리에 영화 추가</button>
      <button @click="deleteCategory" class="delete-category-btn">카테고리 삭제</button>
    </div>

    <!-- 영화 추가 모달 -->
    <div v-if="showAddMovieModal" class="modal">
      <div class="modal-content">
        <h2>영화 검색</h2>
        <input v-model="searchQuery" @input="searchMovies" placeholder="영화 제목 입력" />
        <ul>
          <li v-for="movie in searchResults" :key="movie.id">
            {{ movie.title }}
            <button @click="confirmAddMovie(movie)">추가</button>
          </li>
        </ul>
        <button @click="closeAddMovieModal" class="close-modal-btn">닫기</button>
      </div>
    </div>

    <div v-if="movies.length === 0">
      <p>이 카테고리에 추가된 영화가 없습니다.</p>
    </div>

    <div v-else class="movie-list">
      <div
        v-for="movie in movies"
        :key="movie.id"
        class="movie-card"
        @click="goToMovieDetail(movie.id)"
      >
        <!-- 영화 포스터 -->
        <div class="image-container">
          <img 
            :src="movie.poster_url ? getFullPosterUrl(movie.poster_url) : 'http://127.0.0.1:8000/media/default_movies/default-movie.png'" 
            alt="영화 포스터" 
            class="movie-poster" 
          />
        </div>
        <!-- 영화 정보 -->
        <h3>{{ movie.title }}</h3>
        <p>개봉일: {{ movie.release_date }}</p>
        <button 
          v-if="isOwner" 
          @click.stop="removeMovie(movie.id)" 
          class="remove-movie-btn"
        >삭제</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useCounterStore } from "@/stores/counter";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const category = ref({}); // 카테고리 데이터
const movies = ref([]); // 영화 데이터
const store = useCounterStore();
const showAddMovieModal = ref(false);
const searchQuery = ref(""); // 영화 검색어
const searchResults = ref([]); // 검색 결과
const isEditingName = ref(false); // 이름 수정 상태
const newCategoryName = ref(""); // 새로운 카테고리 이름

const startEditingName = () => {
  isEditingName.value = true;
};

const saveCategoryName = async () => {
  if (!newCategoryName.value.trim()) {
    alert("새 카테고리 이름을 입력해주세요.");
    return;
  }
  try {
    const response = await axios.patch(
      `${store.API_URL}/accounts/categories/${category.value.id}/update/`,
      { name: newCategoryName.value.trim() },
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    category.value.name = response.data.name;
    isEditingName.value = false; // 저장 후 수정 모드 종료
    alert("카테고리 이름이 수정되었습니다.");
  } catch (error) {
    console.error("Error saving category name:", error);
    alert("카테고리 이름 저장에 실패했습니다.");
  }
};

const cancelEditingName = () => {
  newCategoryName.value = category.value.name; // 기존 이름 복원
  isEditingName.value = false; // 수정 모드 종료
};


// 현재 로그인한 유저와 카테고리 소유자 비교
const isOwner = computed(() => store.user?.id === category.value?.owner_id); // owner_id는 백엔드에서 반환

// 포스터 URL을 처리하는 함수
const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500"; // TMDB 이미지 베이스 URL
  return `${baseUrl}${posterUrl}`;
};

// 카테고리 상세 데이터 가져오기
const fetchCategoryDetails = async () => {
  try {
    const response = await axios.get(
      `http://127.0.0.1:8000/accounts/categories/${route.params.categoryId}/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );

    console.log("Category Details Response:", response.data); // 응답 데이터 로깅
    category.value = response.data;
    movies.value = response.data.movies; // 영화 데이터 설정
    newCategoryName.value = response.data.name; // 기존 이름 설정
  } catch (error) {
    console.error("Error fetching category details:", error);
  }
};

// 영화 삭제 함수
const removeMovie = async (movieId) => {
  try {
    await axios.post(
      `http://127.0.0.1:8000/accounts/categories/remove-movie/`,
      {
        category_id: route.params.categoryId,
        movie_id: movieId,
      },
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    movies.value = movies.value.filter((movie) => movie.id !== movieId);
    alert("영화가 삭제되었습니다.");
  } catch (error) {
    console.error("Error removing movie:", error);
  }
};

// 영화 디테일 페이지로 이동
const goToMovieDetail = (movieId) => {
  router.push({ name: "MovieDetail", params: { id: movieId } });
};

// 영화 추가 모달 열기/닫기
const openAddMovieModal = () => (showAddMovieModal.value = true);
const closeAddMovieModal = () => {
  showAddMovieModal.value = false;
  searchQuery.value = "";
  searchResults.value = [];
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
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });
    searchResults.value = response.data;
  } catch (error) {
    console.error("Error searching movies:", error);
  }
};

// 영화 추가 확인 및 추가
const confirmAddMovie = async (movie) => {
  const confirmed = confirm(`영화 "${movie.title}"를 카테고리에 추가하시겠습니까?`);
  if (confirmed) {
    await addMovieToCategory(movie);
  }
};

// 영화 추가
const addMovieToCategory = async (movie) => {
  try {
    await store.addMovieToCategory(route.params.categoryId, movie.id);
    await fetchCategoryDetails(); // 카테고리 데이터 갱신
    closeAddMovieModal();
  } catch (error) {
    console.error("Error adding movie to category:", error);
  }
};

// **카테고리 삭제 함수**
const deleteCategory = async () => {
  const confirmed = confirm("진짜 삭제하시겠습니까?");
  if (confirmed) {
    try {
      await axios.delete(
        `${store.API_URL}/accounts/categories/${category.value.id}/delete/`,
        {
          headers: {
            Authorization: `Token ${store.token}`,
          },
        }
      );
      alert("카테고리가 삭제되었습니다.");
      router.push(`/profile/${store.user.username}`);
    } catch (error) {
      console.error("Error deleting category:", error);
      alert("카테고리 삭제에 실패했습니다.");
    }
  }
};

// 컴포넌트 마운트 시 데이터 로드
onMounted(async () => {
  try {
    await fetchCategoryDetails();
    await store.fetchUser()
    await store.fetchUserPoints(); // 사용자 포인트 정보 가져오기
    console.log("isOwner:", isOwner.value);
    console.log("store.user:", store.user);
    console.log("category.value:", category.value);


  } catch (error) {
    console.error("Error in onMounted:", error);
  }
});
</script>

<style scoped>
/* 모달 스타일 */
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
  border-radius: 8px;
  width: 400px;
}

.close-modal-btn {
  margin-top: 10px;
}

.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.movie-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background-color: #f9f9f9;
  width: calc(33.333% - 20px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  object-fit: contain;
}

.movie-card h3 {
  margin: 0;
  font-size: 1.2em;
}

.movie-card p {
  font-size: 0.9em;
  margin: 5px 0 0;
}

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

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>
