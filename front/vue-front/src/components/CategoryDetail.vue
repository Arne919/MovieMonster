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
      <button @click="deleteCategory" class="delete-category-btn">카테고리 삭제</button>
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
        <h3>{{ movie.title }}</h3> <!-- 영화 제목 표시 -->
        <p>개봉일: {{ movie.release_date }}</p> <!-- 영화 개봉일 표시 -->
        <button 
          v-if="isOwner" 
          @click="removeMovie(movie.id, $event)" 
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
const isEditingName = ref(false); // 이름 수정 상태
const newCategoryName = ref(""); // 새로운 카테고리 이름

// 현재 로그인한 유저와 카테고리 소유자 비교
const isOwner = computed(() => store.user?.id === category.value?.owner_id); // owner_id는 백엔드에서 반환

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

// 카테고리 이름 수정 시작
const startEditingName = () => {
  if (!isOwner.value) return;
  isEditingName.value = true;
};

// 카테고리 이름 저장
const saveCategoryName = async () => {
  if (!newCategoryName.value.trim()) {
    alert("새 카테고리 이름을 입력해주세요.");
    return;
  }
  try {
    const response = await axios.patch(
      `http://127.0.0.1:8000/accounts/categories/${route.params.categoryId}/update/`,
      { name: newCategoryName.value },
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    category.value.name = response.data.name; // 업데이트된 이름 설정
    isEditingName.value = false;
    alert("카테고리 이름이 수정되었습니다.");
  } catch (error) {
    console.error("Error updating category name:", error);
    alert("카테고리 이름 수정에 실패했습니다.");
  }
};

// 카테고리 이름 수정 취소
const cancelEditingName = () => {
  newCategoryName.value = category.value.name; // 기존 이름으로 복원
  isEditingName.value = false;
};

// 카테고리 삭제
const deleteCategory = async () => {
  if (!isOwner.value) return;
  if (!confirm("정말 이 카테고리를 삭제하시겠습니까?")) return;

  try {
    await axios.delete(
      `http://127.0.0.1:8000/accounts/categories/${route.params.categoryId}/delete/`,
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      }
    );
    alert("카테고리가 삭제되었습니다.");
    router.push("/profile/" + store.user.username); // 프로필 페이지로 이동
  } catch (error) {
    console.error("Error deleting category:", error);
    alert("카테고리를 삭제하는 데 실패했습니다.");
  }
};

// 카테고리에서 영화 삭제
const removeMovie = async (movieId, event) => {
  event.stopPropagation();
  // if (!isOwner.value) return;
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
    
    movies.value = movies.value.filter((movie) => movie.id !== movieId); // 삭제된 영화 로컬 상태에서 제거
    alert("영화가 삭제되었습니다.");
  } catch (error) {
    console.error("Error removing movie from category:", error);
    alert("영화를 삭제하는 데 실패했습니다.");
  }
};

// 영화 디테일 페이지로 이동
const goToMovieDetail = (movieId) => {
  router.push(`/movies/${movieId}`);
};

// 컴포넌트 마운트 시 데이터 로드
// onMounted(fetchCategoryDetails);
// 컴포넌트 마운트 시 데이터 로드
onMounted(async () => {
  try {
    console.log("Fetching user...");
    await store.fetchUser(); // 사용자 정보 먼저 가져오기
    console.log("Current User:", store.user); // 디버깅 로그

    await fetchCategoryDetails(); // 카테고리 정보 가져오기

    // 디버깅 로그
    console.log("isOwner:", isOwner.value);
    console.log("Current User ID:", store.user?.id);
    console.log("Category Owner ID:", category.value?.owner_id);
  } catch (error) {
    console.error("Error in onMounted:", error);
  }
});
</script>

<style scoped>
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
}

.movie-card h3 {
  margin: 0;
  font-size: 1.2em;
}

.movie-card p {
  font-size: 0.9em;
  margin: 5px 0 0;
}

.delete-category-btn {
  background-color: red;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  margin-bottom: 20px;
}

.edit-category-input {
  padding: 5px;
  font-size: 1em;
}

.edit-btn, .save-btn, .cancel-btn {
  margin-left: 10px;
  padding: 5px 10px;
  font-size: 0.9em;
  cursor: pointer;
}

</style>
