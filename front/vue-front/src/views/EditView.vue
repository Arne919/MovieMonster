<template>
    <div>
      <h1>게시글 수정</h1>
      
      <!-- 포스터 이미지 -->
      <div v-if="posterUrl">
        <img :src="posterUrl" alt="영화 포스터" class="poster-image" />
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
      content: content.value,
      rating: selectedRating.value
    }, {
      headers: { Authorization: `Token ${store.token}` }
    })
      .then(() => {
        alert('수정이 완료되었습니다.')

          // store에 있는 articles 배열 업데이트
        store.getSortedArticles('recent');
        router.push({ name: 'DetailView', params: { id: route.params.id } }) // 수정 후 상세 페이지로 이동
      })
      .catch((err) => console.log(err))
  }
  // 별점 관련 함수 ---------------

const hoverRating = ref(0); // 마우스 위치에 따라 표시되는 별점

// 마우스 오버 함수
const hoverStar = (value) => {
  hoverRating.value = value; // 마우스 위치에 따라 별점 변경
};

// 마우스 아웃 함수
const clearHover = () => {
  hoverRating.value = 0; // 마우스가 별에서 떠나면 초기화
};
const selectedRating = ref(0);

const selectRating = (rating) => {
  selectedRating.value = rating; // 선택한 별점 업데이트
};
  </script>
  
  <style scoped>
  .star-rating {
  display: flex;
  direction: row;
  gap: 4px;
}

.stars {
  display: flex;
  gap: 5px;
}

.star {
  width: 24px;
  height: 24px;
  background: url('/assets/images/gray-star.png') no-repeat center;
  background-size: contain;
  cursor: pointer;
}

.star.filled {
  background: url('/assets/images/yellow-star.png') no-repeat center;
  background-size: contain;
}
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
  