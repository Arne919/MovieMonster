<template>
  <div class="profile">
    <h1>내 프로필</h1>
    <p>사용자 이름: {{ user.username }}</p>
    <p>포인트: {{ user.current_points }}</p>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import { computed, onMounted } from 'vue';

const store = useCounterStore();
const user = computed(() => store.user);

// 유저 정보를 마운트 시 업데이트
onMounted(() => {
  store.fetchUserPoints();
});
</script>

<style scoped>
.profile {
  padding: 20px;
}
</style>
