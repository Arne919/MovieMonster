<template>
  <div>
    <h1>전체 영화 리뷰</h1>
    <RouterLink :to="{ name: 'CreateView' }">리뷰 작성하기</RouterLink>
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/ArticleList.vue'
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'

const store = useCounterStore()

onMounted(() => {
  // mount 되기전에 store에 있는 전체 게시글 요청 함수를 호출
  store.getArticles()
})
</script>

<style>

</style>
