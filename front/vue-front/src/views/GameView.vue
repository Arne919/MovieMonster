<template>
  <div class="container">
    <h1 class="text-center my-4">게임하고 포인트 받자!</h1>

    <div class="link-container">
      <!-- OneLineView 링크 -->
      <div class="link-box" @click="goTo('OneLineView')">
        <h2>이동진의 한줄평</h2>
        <p>이동진의 한줄평 보고 영화 맞추기!</p>
      </div>

      <!-- KoreaQuotesView 링크 -->
      <div class="link-box" @click="goTo('KoreaQuotesView')">
        <h2>한국영화 명대사</h2>
        <p>한국영화 명대사 보고 영화 맞추기!</p>
      </div>

      <!-- ForeignQuotesView 링크 -->
      <div class="link-box" @click="goTo('ForeignQuotesView')">
        <h2>해외영화 명대사</h2>
        <p>해외영화 명대사 보고 영화 맞추기! (어려움)</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "GameView",
  methods: {
    goTo(routeName) {
      this.$router.push({ name: routeName }); // 라우터를 통한 이동
    },
  },
};
</script>

<style scoped>
.container {
  margin-top: 40px;
}

.text-center {
  text-align: center;
}

.link-container {
  display: flex;
  flex-direction: column; /* 세로 정렬 */
  gap: 20px; /* 박스 간 간격 */
  align-items: center; /* 박스 중앙 정렬 */
}

.link-box {
  width: 80%; /* 박스 너비를 화면의 80%로 설정 */
  max-width: 600px; /* 최대 너비 제한 */
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  text-align: center;
  cursor: pointer;
  background-color: #f9f9f9;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.link-box:hover {
  transform: scale(1.05); /* 호버 시 크기 확대 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* 호버 시 그림자 추가 */
}

.link-box h2 {
  font-size: 1.5rem; /* 제목 크기 */
  margin-bottom: 10px;
}

.link-box p {
  font-size: 1rem; /* 설명 크기 */
  color: #555;
}
</style>
