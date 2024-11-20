<template>
  <div>
    <div v-if="article">
      <h2>제목 : {{ article.title }}</h2>
      <!-- 작성자 정보 출력 -->
      <p>작성자: {{ article.user }}</p>
       <!-- 포스터 이미지 출력 -->
       <div v-if="article.poster_url">
        <h4>영화 포스터</h4>
        <img :src="article.poster_url" alt="영화 포스터" class="poster-image" />
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
      <p>작성일 : {{ article.created_at }}</p>
      <p>수정일 : {{ article.updated_at }}</p>
      <button v-if="isAuthor" @click="goToEdit">게시글 수정</button> <!-- 수정 버튼 -->
      <button v-if="isAuthor" @click="deleteArticle">게시글 삭제</button> <!-- 삭제 버튼 -->
      <p>좋아요 수: {{ article.like_count }}</p> <!-- 좋아요 수 표시 -->
      <button @click="toggleLike">좋아요</button> <!-- 좋아요 버튼 추가 -->
      <!-- 댓글 목록 표시 -->
      <div v-if="comments && comments.length > 0">
        <h3>댓글</h3>
        <div v-for="comment in comments" :key="comment.id">
          <p><strong>{{ comment.user }}</strong>: {{ comment.content }}</p>
        </div>
      </div>
      <!-- 댓글이 없으면 표시할 메시지 -->
      <div v-else>
        <p>댓글이 없습니다.</p>
      </div>

      <!-- 댓글 작성 폼 -->
      <div>
        <textarea v-model="newComment" placeholder="댓글을 작성하세요"></textarea>
        <button @click="submitComment">댓글 작성</button> <!-- 댓글 작성 버튼 -->
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const route = useRoute()
const router = useRouter() 
const article = ref(null)
const comments = ref([])  // 댓글 목록 (이 부분을 ref()로 정의)
const newComment = ref('')  // 새로운 댓글 내용
const isAuthor = ref(false)  // 사용자가 작성자인지 여부


// DetailView가 마운트되기전에 DRF로 단일 게시글 조회를 요청 후 응답데이터를 저장
onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/communities/${route.params.id}/`,
    headers: {
      Authorization: `Token ${store.token}`  // 토큰 추가
    }
  })
    .then((res) => {
      // console.log(res.data)
      article.value = res.data
      isAuthor.value = article.value.user === store.Username  // 작성자인지 확인
      console.log(article.value)
    })
    .catch((err) => {
      console.log(err)
    })
})
const goToEdit = () => {
  router.push({ name: 'EditView', params: { id: article.value.id } })
}


  // 댓글 목록 로드
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/communities/${route.params.id}/comments/list`,  // 댓글 목록 URL
    headers: {
      Authorization: `Token ${store.token}`  // 토큰 추가
    }
  })
    .then((res) => {
      comments.value = res.data  // 댓글 목록 업데이트
    })
    .catch((err) => {
      console.log(err)
    })

// 댓글 작성 함수
const submitComment = () => {
  if (!newComment.value.trim()) {
    return
  }

  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/communities/${route.params.id}/comments/`,
    headers: {
      Authorization: `Token ${store.token}`  // 토큰 추가
    },
    data: { content: newComment.value }
  })
    .then((res) => {
      comments.value.push(res.data)  // 새로운 댓글 추가
      newComment.value = ''  // 댓글 작성 후 입력 필드 초기화

      // 댓글 작성 후, 전체 게시글 목록을 갱신
      store.getArticles();  // 댓글 추가 후 전체 게시글 리스트를 새로고침
    })
    .catch((err) => {
      console.log(err)
    })
}

const toggleLike = () => {
  // 좋아요 토글 요청
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/communities/${article.value.id}/like/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((res) => {
      article.value.like_count = res.data.like_count
    })
    .catch((err) => {
      console.log(err)
    })
}

const deleteArticle = async () => {
  try {
    await axios({
      method: 'delete',
      url: `${store.API_URL}/api/v1/communities/${route.params.id}/delete/`,
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    alert('게시글이 삭제되었습니다.')

    // 게시글 목록을 새로 고친 후에 페이지 이동
    await store.getArticles()  // 전체 게시글 목록을 새로고침하고 기다림
    router.push({ name: 'ArticleView' })  // 게시글 목록 페이지로 이동
  } catch (err) {
    console.log(err)
  }
}
</script>

<style scoped>
.rating-container {
  display: flex;
  align-items: center; /* 텍스트와 별점을 세로로 정렬 */
  gap: 8px; /* 텍스트와 별점 사이의 간격 조절 */
}

.stars {
  display: flex;
  gap: 5px;
  pointer-events: none; /* 마우스 이벤트를 비활성화 */
}

.star {
  width: 24px;
  height: 24px;
  background: url('/assets/images/gray-star.png') no-repeat center;
  background-size: contain;
}

.star.filled {
  background: url('/assets/images/yellow-star.png') no-repeat center;
  background-size: contain;
}
</style>
