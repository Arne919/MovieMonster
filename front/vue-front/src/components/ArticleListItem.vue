<template>
  <div>
     <!-- 포스터 이미지 출력 -->
    <img v-if="article.poster_url" :src="article.poster_url" alt="포스터 이미지" class="poster-image" />
    <p>글 번호: {{ article.id }}</p>
    <p>제목 :{{ article.title }}</p>
    <p>내용 : {{ article.content }}</p>
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
    <p>작성자: {{ article.user }}</p>
    <p>좋아요 수: {{ article.like_count }}</p> <!-- 좋아요 수 표시 -->
    <p>댓글 수: {{ article.comment_count }}</p> <!-- 댓글 수 표시 -->
    <RouterLink 
      :to="{ name: 'DetailView', params: { id: article.id } }"  
    >
      Detail
    </RouterLink>
    <hr>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useCounterStore } from '@/stores/counter';

defineProps({
  article: Object
})

const store = useCounterStore()

const toggleLike = () => {
  // 서버로 좋아요 토글 요청
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/communities/${article.id}/like/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((res) => {
      // 성공적으로 좋아요를 추가/제거했을 때, like_count 값을 갱신
      article.like_count = res.data.like_count
    })
    .catch((err) => {
      console.log(err)
    })
}
</script>

<style scoped>
.poster-image {
  width: 150px;
  height: auto;
  margin-bottom: 10px;
}

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