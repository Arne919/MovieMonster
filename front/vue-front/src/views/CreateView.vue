<template>
  <div>
    <h1>리뷰 작성</h1>

    <button @click="goBack">리뷰 작성 취소</button>

    <!-- '리뷰 작성할 영화 선택하기' 버튼 -->
    <div>
      <button @click="openMovieSelectModal">리뷰 작성할 영화 선택하기</button>
    </div>

    <!-- 영화 추가 모달 -->
    <div v-if="showMovieModal" class="modal">
      <div class="modal-content">
        <h2>영화 검색</h2>
        <input v-model="searchQuery" @input="searchMovies" placeholder="영화 제목 입력" />
        <ul>
          <li v-for="movie in searchResults" :key="movie.id">
            {{ movie.title }}
            <button @click="selectMovie(movie)">추가</button>
          </li>
        </ul>
        <button @click="closeMovieModal" class="close-modal-btn">닫기</button>
      </div>
    </div>

    <!-- 선택한 영화 포스터 및 타이틀 표시 -->
    <div v-if="selectedMovie">
      <h3>선택한 영화: {{ selectedMovie.title }}</h3>
      <img :src="selectedMoviePoster" alt="선택된 영화 포스터" class="poster-image" />
    </div>

    <!-- 별점 매기기 -->
    <div class="stars">
      <div
        v-for="n in 10"
        :key="n"
        class="star"
        :class="{ filled: n <= hoverRating || n <= selectedRating }"
        @mouseover="hoverStar(n)"
        @mouseleave="clearHover"
        @click="selectRating(n)"
      ></div>
    </div>
    <p>선택한 별점: {{ selectedRating }} / 10</p>

    <!-- 게시글 작성 폼 -->
    <form @submit.prevent="createArticle">
      <div>
        <label for="title">제목 :</label>
        <input type="text" id="title" v-model.trim="title" />
      </div>
      <div>
        <label for="content">내용 :</label>
        <textarea id="content" v-model.trim="content"></textarea>
      </div>
      <input type="submit" value="작성" />
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

// 상태 정의
const title = ref("");
const content = ref("");
const searchQuery = ref("");
const searchResults = ref([]);
const selectedMovie = ref(null); // 선택된 영화 객체
const selectedMoviePoster = ref(null); // 선택된 영화의 포스터 URL
const errorMessage = ref("");
const showMovieModal = ref(false);
const hoverRating = ref(0);
const selectedRating = ref(0);

const store = useCounterStore();
const router = useRouter();

const goBack = () => {
  router.go(-1);
};

// 모달 열기/닫기
const openMovieSelectModal = () => (showMovieModal.value = true);
const closeMovieModal = () => {
  showMovieModal.value = false;
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
    const response = await store.searchMovies(searchQuery.value.trim());
    searchResults.value = response;
  } catch (error) {
    console.error("Error searching movies:", error);
    errorMessage.value = "영화를 검색하는데 실패했습니다.";
  }
};

// 영화 선택
const selectMovie = (movie) => {
  selectedMovie.value = movie; // 선택된 영화 객체 저장
  selectedMoviePoster.value = `https://image.tmdb.org/t/p/w500${movie.poster_url}`; // 포스터 URL 저장
  closeMovieModal();
};

// 별점 관련 함수
const hoverStar = (value) => (hoverRating.value = value);
const clearHover = () => (hoverRating.value = 0);
const selectRating = (rating) => (selectedRating.value = rating);

// 게시글 작성
const isSubmitting = ref(false);

const createArticle = async () => {
  if (isSubmitting.value) return; // 이미 요청 중이면 중지
  isSubmitting.value = true;

  if (!selectedMovie.value) {
    alert("리뷰 작성할 영화를 선택해주세요.");
    isSubmitting.value = false;
    return;
  }

  try {
    const newArticle = await store.createArticle({
      title: title.value,
      content: content.value,
      poster_url: selectedMoviePoster.value,
      rating: selectedRating.value,
      movie: selectedMovie.value.id,
    });

    // 작성된 리뷰를 프론트엔드의 상태에 추가
    store.articles.unshift(newArticle);  // 최신순으로 추가
    await store.fetchUserPoints(); // 사용자 정보를 다시 가져와 업데이트
    alert("리뷰가 성공적으로 작성되었습니다.");
    router.push({ name: "ArticleView" });
  } catch (error) {
    console.error("Error creating article:", error);
    alert("리뷰 작성에 실패했습니다.");
  } finally {
    isSubmitting.value = false; // 요청 완료 후 플래그 초기화
  }
};

</script>


<style scoped>
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

.poster-image {
  width: 200px;
  height: auto;
  margin-top: 10px;
}

.stars {
  display: flex;
  gap: 5px;
}

.star {
  width: 24px;
  height: 24px;
  background: url("/assets/images/gray-star.png") no-repeat center;
  background-size: contain;
  cursor: pointer;
}

.star.filled {
  background: url("/assets/images/yellow-star.png") no-repeat center;
  background-size: contain;
}
</style>
