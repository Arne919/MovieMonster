<template>
    <div>
      <h1>게시글 수정</h1>
      <form @submit.prevent="submitEdit">
        <label for="title">제목</label>
        <input v-model="title" id="title" type="text" required />
  
        <label for="content">내용</label>
        <textarea v-model="content" id="content" required></textarea>
  
        <button type="submit">수정 저장</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useCounterStore } from '@/stores/counter'
  import axios from 'axios'
  
  const store = useCounterStore()
  const route = useRoute()
  const router = useRouter()
  
  const title = ref('')
  const content = ref('')
  
  onMounted(() => {
    // 기존 게시글 내용 로드
    axios.get(`${store.API_URL}/api/v1/communities/${route.params.id}/`, {
      headers: { Authorization: `Token ${store.token}` }
    })
      .then((res) => {
        title.value = res.data.title
        content.value = res.data.content
      })
      .catch((err) => console.log(err))
  })
  
  // 수정 데이터 제출
  const submitEdit = () => {
    axios.put(`${store.API_URL}/api/v1/communities/${route.params.id}/`, {
      title: title.value,
      content: content.value
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })
      .then(() => {
        alert('수정이 완료되었습니다.')
        router.push({ name: 'DetailView', params: { id: route.params.id } }) // 수정 후 상세 페이지로 이동
      })
      .catch((err) => console.log(err))
  }
  </script>
  