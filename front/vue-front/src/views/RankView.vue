<template>
  <div class="ranking-container">
    <h1>랭킹 페이지</h1>
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
          <!-- 순위 -->
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
          <!-- 프로필 -->
          <td>
            <div class="profile-picture">
              <img :src="`http://127.0.0.1:8000${user.profile_picture}`" alt="프로필 사진" class="profile-img" />
            </div>
          </td>
          <!-- 이름 -->
          <td>
            <RouterLink :to="{ name: 'ProfileView', params: { username: user.username } }">
              {{ user.username }}
            </RouterLink>
          </td>
          <!-- 랭크 -->
          <td>
            <div class="rank-display">
              <img :src="getRankImage(user.rank_title)" :alt="user.rank_title" class="rank-icon" />
              {{ user.points }}
            </div>
          </td>
          <!-- 게시물 수 -->
          <td>{{ user.articles_count }}</td>
          <!-- 좋아요 수 -->
          <td>{{ user.likes_count }}</td>
          <!-- 팔로워 수 -->
          <td>{{ user.followers_count }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 랭크 시스템 안내 버튼 -->
    <div class="info-container">
      <button class="btn btn-primary" @click="openModal">랭크 시스템 안내</button>
    </div>

    <!-- 모달 -->
    <div
      class="modal fade"
      id="rankInfoModal"
      tabindex="-1"
      aria-labelledby="rankInfoModalLabel"
      aria-hidden="true"
      ref="rankInfoModal"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="rankInfoModalLabel">랭크 시스템 안내</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <h4>Q) 포인트는 무엇인가요?</h4>
            <p>
              포인트는 리뷰 작성과 게임 플레이를 통해 얻을 수 있는 MovieMoster의 보상 시스템입니다.
              리뷰 작성 시 100점, 게임의 정답 1개당 100점씩 포인트가 부여됩니다.
            </p>
            <h4>Q) 포인트로 무엇을 할 수 있나요?</h4>
            <p>
              포인트는 누적되어 MovieMoster의 등급 시스템을 통해 등급이 부여됩니다.
              등급이 높을수록 RANK 페이지의 상단에 노출되며, 커뮤니티에서 더 높은 신뢰도를 가지게 됩니다.
            </p>
            <h4>Q) 등급의 종류는 몇 가지이고, 어떻게 등급을 상승시킬 수 있나요?</h4>
            <p>
              <strong>등급표</strong><br />
              <table>
  <thead>
    <tr>
      <th>등급</th>
      <th>누적 포인트</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Bronze</td>
      <td>0</td>
    </tr>
    <tr>
      <td>Silver</td>
      <td>1000</td>
    </tr>
    <tr>
      <td>Gold</td>
      <td>2000</td>
    </tr>
    <tr>
      <td>Platinum</td>
      <td>3000</td>
    </tr>
    <tr>
      <td>Diamond</td>
      <td>4000+</td>
    </tr>
  </tbody>
</table>
              등급 상승은 포인트를 꾸준히 누적함으로써 이루어집니다.
              리뷰 작성과 게임 정답을 통해 포인트를 얻어 등급을 올릴 수 있습니다.
            </p>
            <h4>Q) 게임 제한 시간은 어떻게 동작하나요?</h4>
            <p>
              각 게임은 플레이 후 일정 시간 동안 재시도가 제한됩니다.<br />
              제한 시간 동안 해당 게임은 비활성화 상태로 표시되며, 클릭 시 남은 시간 안내 모달창이 나타납니다.<br />
              예) "이 게임은 3시간 15분 후에 다시 이용할 수 있습니다."
            </p>
            <h4>Q) 높은 등급의 유저는 어떤 혜택을 받을 수 있나요?</h4>
            <p>
              높은 등급의 유저는 커뮤니티에서 더 두드러진 노출과 인정을 받을 수 있습니다.<br />
              - RANK 상단 노출: 높은 등급 유저가 우선적으로 노출됩니다.<br />
              - 카테고리 추천: 높은 등급 유저의 콘텐츠가 홈 페이지에 우선 표시됩니다.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">닫기</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import * as bootstrap from "bootstrap"; // Bootstrap 모듈 임포트

// Pinia 상태 관리
const store = useCounterStore();
const rankings = computed(() => store.rankings);

// 랭크 이미지를 가져오는 함수
import bronzeRank from "@/assets/BronzeRank.png";
import silverRank from "@/assets/SilverRank.png";
import goldRank from "@/assets/GoldRank.png";
import platinumRank from "@/assets/PlatinumRank.png";
import diamondRank from "@/assets/DiamondRank.png";

const getRankImage = (rankTitle) => {
  switch (rankTitle) {
    case "Bronze":
      return bronzeRank;
    case "Silver":
      return silverRank;
    case "Gold":
      return goldRank;
    case "Platinum":
      return platinumRank;
    case "Diamond":
      return diamondRank;
    default:
      return bronzeRank; // 기본값
  }
};

// 모달 핸들링
const openModal = () => {
  try {
    const modalElement = document.getElementById("rankInfoModal");
    if (modalElement) {
      const modalInstance = new bootstrap.Modal(modalElement);
      modalInstance.show();
    } else {
      console.error("Modal element not found");
    }
  } catch (error) {
    console.error("Error initializing modal:", error);
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

/* 특정 모달의 너비를 넓히기 (ID 기반) */
#rankInfoModal .modal-dialog {
  max-width: 800px; /* 원하는 너비 설정 */
  width: 90%;       /* 반응형을 위한 너비 설정 */
}
/* 컨테이너 스타일 */
.ranking-container {
  max-width: 800px;
  margin: 20px auto;
  text-align: center;
}

/* 테이블 스타일 */
.ranking-table {
  width: 100%;
  border-collapse: collapse;
}

.ranking-table th,
.ranking-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

/* 메달 스타일 */
.medal-icon {
  width: 40px;
  height: 40px;
}

/* 프로필 이미지 스타일 */
.profile-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.profile-picture {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 랭크 디스플레이 스타일 */
.rank-display {
  display: flex;
  align-items: center;
}

.rank-icon {
  width: 24px;
  height: 24px;
  margin-right: 8px;
}

/* 우측 안내 버튼 */
.info-container {
  margin-top: 20px;
  text-align: right;
}

#rankInfoModal .modal-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

#rankInfoModal .modal-body th,
#rankInfoModal .modal-body td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

#rankInfoModal .modal-body th {
  background-color: #f5f5f5;
  font-weight: bold;
}

#rankInfoModal .modal-body td {
  background-color: #fff;
}
</style>
