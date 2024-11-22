<template>
  <div class="container">
    <h1 class="text-center my-4">게임하고 포인트 받자!</h1>

    <div class="game-list">
      <!-- 이동진의 한줄평 -->
      <div class="game-card" @click="goTo('OneLineView')">
        <img
          src="@/assets/leedongjin.jpg"
          alt="이동진의 한줄평"
          class="thumbnail"
        />
        <div class="game-info">
          <h2>이동진의 한줄평</h2>
          <p>이동진의 한줄평 보고 영화 맞추기!</p>
        </div>
      </div>

      <!-- 한국영화 명대사 -->
      <div class="game-card" @click="goTo('KoreaQuotesView')">
        <img
          src="@/assets/koreansumnail.jpg"
          alt="한국영화 명대사"
          class="thumbnail"
        />
        <div class="game-info">
          <h2>한국영화 명대사</h2>
          <p>한국영화 명대사 보고 영화 맞추기!</p>
        </div>
      </div>

      <!-- 해외영화 명대사 -->
      <div class="game-card" @click="goTo('ForeignQuotesView')">
        <img
          src="@/assets/foreignsumbnail.jpg"
          alt="해외영화 명대사"
          class="thumbnail"
        />
        <div class="game-info">
          <h2>해외영화 명대사</h2>
          <p>해외영화 명대사 보고 영화 맞추기! (어려움)</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "GameView",
  methods: {
    goTo(routeName) {
      this.$router.push({ name: routeName });
    },
  },
};
</script>

<style scoped>
.container {
  margin-top: 20px; /* 상단 여백 줄이기 */
  width: 100%; /* 컨테이너를 화면 너비에 맞춤 */
  display: flex;
  flex-direction: column;
  align-items: center; /* 중앙 정렬 */
}

.game-list {
  display: flex;
  flex-direction: column;
  gap: 20px; /* 카드 간 간격 */
  align-items: center;
  width: 100%; /* 게임 리스트도 전체 너비에 맞춤 */
}

/* 개별 게임 카드 */
.game-card {
  display: flex; /* 가로 정렬 */
  align-items: center;
  width: 90%; /* 화면의 90%를 차지 */
  max-width: 1400px; /* 지나치게 길어지지 않도록 최대 너비 제한 */
  height: 150px; /* 카드 높이 고정 */
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  justify-content: flex-start; /* 내용 정렬 */
}

.game-card:hover {
  transform: scale(1.03);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

/* 썸네일 이미지 */

.thumbnail {
  flex: 1; /* 썸네일 크기 비율 */
  width: auto;
  height: 100%; /* 카드 높이에 맞춤 */
  max-width: 200px; /* 최대 너비 제한 */
  margin-right: 20px; /* 썸네일과 텍스트 간격 */
  border-radius: 5px;
  object-fit: contain; /* 원본 비율 유지 */
  object-position: center; /* 이미지 중앙 정렬 */
  background-color: #f9f9f9; /* 이미지 없는 경우 배경 */
}

/* 게임 정보 */
.game-info {
  flex: 3; /* 텍스트 크기 비율 */
}

.game-info h2 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.game-info p {
  font-size: 1rem;
  color: #555;
}

</style>
