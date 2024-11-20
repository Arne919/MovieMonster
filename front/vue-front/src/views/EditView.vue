<template>
    <div>
      <h1>게시글 수정</h1>
      
      <!-- 포스터 이미지 -->
      <div v-if="posterUrl">
        <img :src="posterUrl" alt="영화 포스터" class="poster-image" />
      </div>
  
      <form @submit.prevent="submitEdit" class="edit-form">
        <div class="form-group">
          <label for="title">제목</label>
          <input v-model="title" id="title" type="text" required />
        </div>
  
        <div class="form-group">
          <label for="content">내용</label>
          <textarea v-model="content" id="content" required></textarea>
        </div>
  
        <button type="submit" class="submit-button">수정 저장</button>
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
  const posterUrl = ref('') // 포스터 URL
  
  onMounted(() => {
    // 기존 게시글 내용 로드
    axios.get(`${store.API_URL}/api/v1/communities/${route.params.id}/`, {
      headers: { Authorization: `Token ${store.token}` }
    })
      .then((res) => {
        title.value = res.data.title
        content.value = res.data.content
        posterUrl.value = res.data.poster_url // 포스터 URL 설정
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
  
  <style scoped>
  .edit-form {
    display: flex;
    flex-direction: column; /* 폼을 세로 배치 */
    gap: 15px; /* 각 입력 필드 간격 */
    max-width: 500px;
    margin: auto; /* 가운데 정렬 */
  }
  
  .form-group {
    display: flex;
    flex-direction: column; /* 라벨과 입력 필드를 세로로 배치 */
  }
  
  input, textarea {
    width: 100%;
    padding: 10px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  textarea {
    resize: none; /* 크기 조절 비활성화 */
    height: 150px;
  }
  
  .submit-button {
    padding: 10px;
    font-size: 1rem;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .submit-button:hover {
    background-color: #0056b3;
  }
  
  .poster-image {
    width: 100%; /* 포스터 이미지 너비 조정 */
    max-width: 500px; /* 최대 너비 제한 */
    margin-bottom: 20px;
    border-radius: 5px;
  }
  </style>
  