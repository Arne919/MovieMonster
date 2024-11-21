<template>
  <div>
    <h1>{{ user.username }}의 프로필 페이지</h1>
    <p>포인트: {{ user.points }}</p>
    <p>팔로잉: <span id="followings-count">{{ user.followingsCount }}</span></p>
    <p>팔로워: <span id="followers-count">{{ user.followersCount }}</span></p>
    <p>게시글 수: <span id="articles-count">{{ user.articlesCount }}</span></p>
    <p>받은 좋아요 수: <span id="like-count">{{ user.likesCount }}</span></p>
    <div v-if="!isOwnProfile">
      <button @click="toggleFollow" id="followBtn">
        {{ isFollowed ? '언팔로우' : '팔로우' }}
      </button>
    </div>

    <h2>내가 만든 카테고리</h2>
    <div v-if="categories.length === 0" class="empty-message">
      <p>아직 카테고리가 없습니다.</p>
    </div>

    <div v-else class="category-list">
      <div
        v-for="category in categories"
        :key="category.id"
        class="category-card"
        @click="goToCategoryDetail(category.id)"
      >
        <h3>{{ category.name }}</h3>
        <p>영화 개수: {{ category.movies.length }}</p>
        <ul>
          <li v-for="movie in category.movies" :key="movie.id">
            {{ movie.title }}
          </li>
        </ul>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useRoute, useRouter  } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

// Vue Router와 Pinia 스토어 사용
const route = useRoute();
const router = useRouter();
const store = useCounterStore();

// 유저 데이터 상태 관리
const user = ref({
  username: '',
  followingsCount: 0,
  followersCount: 0,
  articlesCount: 0, // 작성한 게시글 수
  likesCount: 0, // 받은 좋아요 수
});
const isFollowed = ref(false);
const categories = ref([]);

// 현재 프로필이 로그인된 사용자의 것인지 확인
const isOwnProfile = computed(() => store.user.username === route.params.username);

// API를 통해 프로필 데이터 가져오기
const fetchProfile = async () => {
  try {
    const { data } = await axios.get(
      `http://127.0.0.1:8000/accounts/profile/${route.params.username}/`, 
      {
        headers: {
          Authorization: `Token ${store.token}`,
        },
      });
    user.value = {
      id: data.id,
      username: data.username,
      points: data.points,
      followingsCount: data.followings_count,
      followersCount: data.followers_count,
      articlesCount: data.articles_count, // API 응답에서 게시글 수 추가
      likesCount: data.likes_count, // API 응답에서 받은 좋아요 수 추가
    };
    isFollowed.value = data.is_followed;
    categories.value = data.categories;
  } catch (error) {
    console.error('Error fetching profile:', error);
  }
};

// API를 통해 내가 만든 카테고리 데이터 가져오기
const fetchCategories = async () => {
  try {
    const { data } = await axios.get('http://127.0.0.1:8000/accounts/categories/', {
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });
    categories.value = data;
  } catch (error) {
    console.error('Error fetching categories:', error);
  }
};

// 팔로우/언팔로우 상태 변경
const toggleFollow = async () => {
  try {
    const { data } = await axios.post(`http://127.0.0.1:8000/accounts/${user.value.id}/follow/`, null, {
      headers: {
        Authorization: `Token ${store.token}`,
      },
    });
    isFollowed.value = data.is_followed;
    user.value.followersCount = data.followers_count;
    user.value.followingsCount = data.followings_count;
  } catch (error) {
    console.error('Error toggling follow:', error);
  }
};

// 카테고리 상세 페이지로 이동
const goToCategoryDetail = (categoryId) => {
  router.push(`/categories/${categoryId}`);
};
// 데이터 병렬로 가져오기
onMounted(async () => {
  await Promise.all([fetchProfile(), fetchCategories()]);
});
</script>

<style scoped>
button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.category-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.category-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background-color: #f9f9f9;
  width: calc(33.333% - 20px);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.category-card h3 {
  margin-top: 0;
  font-size: 1.2em;
}

.category-card ul {
  padding-left: 20px;
  margin: 10px 0 0;
}

.category-card li {
  font-size: 0.9em;
}
</style>
