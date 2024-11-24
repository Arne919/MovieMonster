<template>
  <div>
    <button @click="goBack">전체 리뷰로 돌아가기</button> <!-- 뒤로가기 버튼 추가 -->
    <div v-if="article">
      <h2>제목 : {{ article.title }}</h2>
      <!-- 작성자 정보 출력 -->
      <p>작성자: {{ article.user }}</p>

      <!-- 영화 정보 카드 -->
      <div class="movie-card" @click="navigateToMovieDetail(article.movie)">
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

      <p class="rating-container">
        <span>별점 : </span>
        <div class="stars">
          <div
            v-for="(star, index) in store.displayStars(article.rating)"
            :key="index"
            class="star"
            :class="{ filled: star.filled }"
          ></div>
        </div>
      </p>
      <p>게시글 번호 : {{ article.id }}</p>
      <p>내용 : {{ article.content }}</p>
      <p>작성일 : {{ store.formatDate(article.created_at) }}</p>
      <p>수정일 : {{ store.formatDate(article.updated_at) }}</p>
      <button v-if="isAuthor" @click="goToEdit">게시글 수정</button> <!-- 수정 버튼 -->
      <button v-if="isAuthor" @click="deleteArticle">게시글 삭제</button> <!-- 삭제 버튼 -->
      <p>좋아요 수: {{ article.like_count }}</p> <!-- 좋아요 수 표시 -->
      <button @click="toggleLike">좋아요</button> <!-- 좋아요 버튼 추가 -->

      <!-- 댓글 목록 표시 -->
      <div v-if="comments && comments.length > 0">
        <h3>댓글</h3>
        <div v-for="comment in comments" :key="comment.id">
          <p><strong>{{ comment.user }}</strong>: {{ comment.content }}</p>
          <!-- 댓글 수정 및 삭제 버튼 -->
          <button v-if="comment.user === store.Username" @click="editComment(comment)">수정</button>
          <button v-if="comment.user === store.Username" @click="removeComment(comment.id)">삭제</button>
        </div>
      </div>
      <!-- 댓글이 없으면 표시할 메시지 -->
      <div v-else>
        <p>댓글이 없습니다.</p>
      </div>

      <!-- 댓글 작성 폼 -->
      <div v-if="!editingComment">
        <textarea v-model="newComment" placeholder="댓글을 작성하세요"></textarea>
        <button @click="submitComment">댓글 작성</button> <!-- 댓글 작성 버튼 -->
      </div>

      <!-- 댓글 수정 폼 -->
      <div v-if="editingComment">
        <textarea v-model="updatedCommentContent"></textarea>
        <button @click="submitUpdatedComment">수정 완료</button>
        <button @click="cancelEdit">취소</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { useCounterStore } from "@/stores/counter";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";

const store = useCounterStore();
const route = useRoute();
const router = useRouter();
const article = ref(null);
const comments = ref([]); // 댓글 목록
const newComment = ref(""); // 새로운 댓글 내용
const isAuthor = ref(false); // 사용자가 작성자인지 여부

// 영화 디테일 페이지로 이동
const navigateToMovieDetail = (movieId) => {
  router.push({ name: "MovieDetail", params: { id: movieId } });
};

// 영화 포스터 URL 생성
const getFullPosterUrl = (posterUrl) => {
  const baseUrl = "https://image.tmdb.org/t/p/w500";
  return `${baseUrl}${posterUrl}`;
};

// DetailView가 마운트되기전에 DRF로 단일 게시글 조회를 요청 후 응답데이터를 저장
onMounted(() => {
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/communities/${route.params.id}/`,
    headers: {
      Authorization: `Token ${store.token}`, // 토큰 추가
    },
  })
    .then((res) => {
      console.log('aa',res.data)
      article.value = res.data;
      isAuthor.value = article.value.user === store.Username; // 작성자인지 확인
    })
    .catch((err) => {
      console.log(err);
    });

  // 댓글 목록 로드
  axios({
    method: "get",
    url: `${store.API_URL}/api/v1/communities/${route.params.id}/comments/list`, // 댓글 목록 URL
    headers: {
      Authorization: `Token ${store.token}`, // 토큰 추가
    },
  })
    .then((res) => {
      comments.value = res.data; // 댓글 목록 업데이트
    })
    .catch((err) => {
      console.log(err);
    });
});

// 뒤로가기
const goBack = () => {
  router.push({ name: "ArticleView" }); // 메인 페이지로 이동
};

const goToEdit = () => {
  router.push({ name: "EditView", params: { id: article.value.id } });
};

// 좋아요 토글
const toggleLike = () => {
  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/communities/${article.value.id}/like/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
  })
    .then((res) => {
      article.value.like_count = res.data.like_count;
    })
    .catch((err) => {
      console.log(err);
    });
};

// 댓글 작성 함수
const submitComment = () => {
  if (!newComment.value.trim() || editingComment.value) {
    return;
  }

  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/communities/${route.params.id}/comments/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
    data: { content: newComment.value },
  })
    .then((res) => {
      comments.value.push(res.data); // 새로운 댓글 추가
      newComment.value = ""; // 댓글 작성 후 입력 필드 초기화
    })
    .catch((err) => {
      console.log(err);
    });
};

// 댓글 수정 상태 관리
const editingComment = ref(null);
const updatedCommentContent = ref("");

// 댓글 수정 시작
const editComment = (comment) => {
  editingComment.value = comment;
  updatedCommentContent.value = comment.content;
};

// 댓글 수정 완료
const submitUpdatedComment = async () => {
  if (!updatedCommentContent.value.trim()) {
    return;
  }
  try {
    const response = await store.updateComment(
      route.params.id,
      editingComment.value.id,
      updatedCommentContent.value
    );
    const updatedCommentIndex = comments.value.findIndex(
      (c) => c.id === editingComment.value.id
    );
    if (updatedCommentIndex !== -1) {
      comments.value[updatedCommentIndex] = response.data;
    }
    editingComment.value = null;
    updatedCommentContent.value = "";
  } catch (error) {
    console.error("댓글 수정 실패:", error);
  }
};

// 댓글 수정 취소
const cancelEdit = () => {
  editingComment.value = null;
  updatedCommentContent.value = "";
};

// 댓글 삭제 API 호출
const removeComment = async (commentId) => {
  try {
    await store.deleteComment(route.params.id, commentId);
    comments.value = comments.value.filter((comment) => comment.id !== commentId);
  } catch (error) {
    console.error("댓글 삭제 실패:", error);
  }
};

// 게시글 삭제
const deleteArticle = async () => {
  try {
    await axios({
      method: "delete",
      url: `${store.API_URL}/api/v1/communities/${route.params.id}/delete/`,
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });
    alert("게시글이 삭제되었습니다.");
    await store.getArticles();
    router.push({ name: "ArticleView" });
  } catch (err) {
    console.log(err);
  }
};
</script>

<style scoped>
/* 영화 카드 스타일 */
.movie-card {
  display: flex;
  cursor: pointer;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
  margin-bottom: 20px;
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

/* 기존 스타일 */
.rating-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stars {
  display: flex;
  gap: 5px;
  pointer-events: none;
}

.star {
  width: 24px;
  height: 24px;
  background: url("/assets/images/gray-star.png") no-repeat center;
  background-size: contain;
}

.star.filled {
  background: url("/assets/images/yellow-star.png") no-repeat center;
  background-size: contain;
}
</style>
