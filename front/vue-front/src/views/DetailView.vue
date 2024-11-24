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
      <!-- 좋아요 -->
      <div class="like-container">
        <button class="like-button" @click="toggleLike">
          <span v-if="article.is_liked" class="liked-icon">❤️</span>
          <span v-else class="like-icon">🤍</span>
        </button>
        <span class="like-count">{{ article.like_count }}</span>
      </div>

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
const isAuthor = ref(true); // 사용자가 작성자인지 여부

const isLiked = ref(false); // 좋아요 상태
const likeCount = ref(0); // 좋아요 수

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
  const articleId = route.params.id;
  fetchArticle(articleId);
});

const fetchArticle = async (articleId) => {
  try {
    // store에서 캐싱된 데이터 우선 사용
    const cachedArticle = store.articles.find((a) => a.id === articleId);
    if (cachedArticle) {
      article.value = { ...cachedArticle };
    }

    const response = await store.getArticleDetail(articleId); // 개별 게시글 요청
    console.log('aaaaaaaaaaaa', response)
    article.value = response;
    const index = store.articles.findIndex((a) => a.id === article.value.id);
    if (index !== -1) {
      store.articles[index] = { ...article.value };
    }
    // API 응답 데이터 출력 (디버깅)
    console.log("Fetched article data:", response);

    // 작성자 확인
    isAuthor.value = article.value.user === store.Username;
    console.log("isAuthor 상태:", isAuthor.value);
  }
   catch (error) {
    console.error("Error fetching article:", error);
  }}


// 좋아요 토글
const toggleLike = async () => {
  try {
    const updatedArticle = await store.updateLikeStatus(article.value.id);

    // Local state 업데이트
    article.value.is_liked = updatedArticle.action === "added";
    article.value.like_count = updatedArticle.like_count;

    // store의 articles 상태도 업데이트
    const index = store.articles.findIndex((a) => a.id === article.value.id);
    if (index !== -1) {
      store.articles[index] = { ...article.value };
    }
  } catch (err) {
    console.error("좋아요 상태 업데이트 실패:", err);
  }
};


// const toggleLike = async () => {
//   try {
//     const response = await axios.post(
//       `${store.API_URL}/api/v1/communities/${article.value.id}/like/`,
//       {},
//       {
//         headers: { Authorization: `Token ${store.token}` },
//       }
//     );
//     isLiked.value = response.data.action === "added";
//     likeCount.value = response.data.like_count;

//     // Vue reactivity를 보장하기 위해 article.value도 업데이트
//     article.value.is_liked = isLiked.value;
//     article.value.like_count = likeCount.value;
//   } catch (error) {
//     console.error("Error toggling like:", error);
//   }
// };

// 뒤로가기
const goBack = () => {
  router.push({ name: "ArticleView" }); // 메인 페이지로 이동
};

// 게시글 수정 페이지 이동
const goToEdit = () => {
  router.push({ name: "EditView", params: { id: article.value.id } });
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
    await axios.delete(`${store.API_URL}/api/v1/communities/${article.value.id}/delete/`, {
      headers: { Authorization: `Token ${store.token}` },
    });
    alert("게시글이 삭제되었습니다.");
    router.push({ name: "ArticleView" }); // 전체 리뷰로 이동
  } catch (error) {
    console.error("게시글 삭제 실패:", error);
    alert("게시글 삭제 중 오류가 발생했습니다.");
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

/* 좋아요 버튼 스타일 */
.like-container {
  display: flex;
  align-items: center;
  gap: 10px;
}
.like-button {
  border: none;
  background: transparent;
  cursor: pointer;
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
