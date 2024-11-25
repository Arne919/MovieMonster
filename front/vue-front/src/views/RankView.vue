<template>
  <div class="ranking-container">
    <h1>랭킹 페이지</h1>

    <!-- 랭크 시스템 안내 버튼 -->
    <div class="info-container">
      <button class="btn btn-primary" @click="showModal = true">랭크 시스템 안내</button>
    </div>

    <table class="ranking-table">
      <thead>
        <tr>
          <th>#</th>
          <th>프로필</th>
          <th>이름</th>
          <th>랭크</th>
          <th>게시물 수</th>
          <th>좋아요 수</th>
          <th>팔로워 수</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in rankings" :key="user.id">
          <td>
            <div v-if="index === 0">
              <img src="@/assets/gold.png" alt="Gold Medal" class="medal-icon" />
            </div>
            <div v-else-if="index === 1">
              <img src="@/assets/silver.png" alt="Silver Medal" class="medal-icon" />
            </div>
            <div v-else-if="index === 2">
              <img src="@/assets/bronze.png" alt="Bronze Medal" class="medal-icon" />
            </div>
            <div v-else>{{ index + 1 }}</div>
          </td>
          <td>
            <div class="profile-picture">
              <img :src="`http://127.0.0.1:8000${user.profile_picture}`" alt="프로필 사진" class="profile-img" />
            </div>
          </td>
          <td>
            <RouterLink :to="{ name: 'ProfileView', params: { username: user.username } }">
              {{ user.username }}
            </RouterLink>
          </td>
          <td>
            <div class="rank-display">
              <img :src="getRankImage(user.rank_title)" :alt="user.rank_title" class="rank-icon" />
              {{ user.points }}
            </div>
          </td>
          <td>{{ user.articles_count }}</td>
          <td>{{ user.likes_count }}</td>
          <td>{{ user.followers_count }}</td>
        </tr>
      </tbody>
    </table>

    <!-- RankInfoModal 컴포넌트 -->
    <RankInfoModal v-if="showModal" :isVisible="showModal" @close="showModal = false" />
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import RankInfoModal from "@/components/RankInfoModal.vue";

// Pinia 상태 관리
const store = useCounterStore();
const rankings = computed(() => store.rankings);
const showModal = ref(false);

// 랭크 이미지를 가져오는 함수
import bronzeRank from "@/assets/BronzeRank.png";
import silverRank from "@/assets/SilverRank.png";
import goldRank from "@/assets/GoldRank.png";
import platinumRank from "@/assets/PlatinumRank.png";
import diamondRank from "@/assets/DiamondRank.png";

const getRankImage = (rankTitle) => {
  switch (rankTitle) {
    case "Bronze": return bronzeRank;
    case "Silver": return silverRank;
    case "Gold": return goldRank;
    case "Platinum": return platinumRank;
    case "Diamond": return diamondRank;
    default: return bronzeRank;
  }
};

// 컴포넌트 로드 시 실행
onMounted(() => {
  if (!store.isLogin) {
    alert("로그인이 필요합니다.");
    store.router.push({ name: "LogInView" });
  } else {
    store.fetchRankings();
  }
});
</script>

<style scoped>
/* 스타일은 기존과 동일합니다. */
.ranking-container {
  max-width: 800px;
  margin: 20px auto;
  text-align: center;
}

.info-container {
  text-align: right;
  margin-bottom: 10px;
}

.ranking-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.ranking-table th,
.ranking-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.medal-icon {
  width: 32px;
  height: 32px;
}

.profile-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.rank-display {
  display: flex;
  align-items: center;
}

.rank-icon {
  width: 40px;
  height: 40px;
  margin-right: 8px;
}
</style>
