<template>
  <div>
     <!-- 포스터 이미지 출력 -->
    <img v-if="article.poster_url" :src="article.poster_url" alt="포스터 이미지" class="poster-image" />
    <h5>{{ article.id }}</h5>
    <p>{{ article.title }}</p>
    <p>{{ article.content }}</p>
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
</style>