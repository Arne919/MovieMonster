<template>
  <div class="container">
    <h1 class="text-center my-4">게임하고 포인트 받자!</h1>

    <div class="game-list">
      <!-- 한국영화 명대사 -->
      <div
        class="game-card"
        :class="{ disabled: isDisabled('KoreaQuotesView') }"
        @click="handleGameClick('KoreaQuotesView', '한국영화 명대사')"
      >
        <img
          src="@/assets/koreansumnail.jpg"
          alt="한국영화 명대사"
          class="thumbnail"
        />
        <div class="badge difficulty-badge">쉬움</div>
        <div class="game-info">
          <h2>한국영화 명대사</h2>
          <p>한국영화 명대사 보고 영화 맞추기!</p>
        </div>
      </div>

      <!-- 해외영화 명대사 -->
      <div
        class="game-card"
        :class="{ disabled: isDisabled('ForeignQuotesView') }"
        @click="handleGameClick('ForeignQuotesView', '해외영화 명대사')"
      >
        <img
          src="@/assets/foreignsumbnail.jpg"
          alt="해외영화 명대사"
          class="thumbnail"
        />
        <div class="badge difficulty-badge medium">중간</div>
        <div class="game-info">
          <h2>해외영화 명대사</h2>
          <p>해외영화 명대사 보고 영화 맞추기!</p>
        </div>
      </div>

      <!-- 이동진의 한줄평 -->
      <div
        class="game-card"
        :class="{ disabled: isDisabled('OneLineView') }"
        @click="handleGameClick('OneLineView', '이동진의 한줄평')"
      >
        <img
          src="@/assets/leedongjin.jpg"
          alt="이동진의 한줄평"
          class="thumbnail"
        />
        <div class="badge difficulty-badge hard">어려움</div>
        <div class="game-info">
          <h2>이동진의 한줄평</h2>
          <p>이동진의 한줄평 보고 영화 맞추기!</p>
        </div>
      </div>
    </div>

    <!-- 모달 -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <p>{{ modalMessage }}</p>
        <button class="btn" @click="closeModal">닫기</button>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "GameView",
  data() {
    return {
      // cooldownTime: 8 * 60 * 60 * 1000, // 8시간 제한 시간
      cooldownTime: 2 * 60 * 1000, // 테스트용 시간조절(2분)
      showModal: false,
      modalMessage: "",
    };
  },
  methods: {
    handleGameClick(gameKey, gameName) {
      const lastPlayed = localStorage.getItem(gameKey);
      const now = Date.now();

      if (lastPlayed && now - lastPlayed < this.cooldownTime) {
        const remainingTime = this.cooldownTime - (now - lastPlayed);
        const hours = Math.floor(remainingTime / (1000 * 60 * 60));
        const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
        this.modalMessage = `${gameName}은(는) ${hours}시간 ${minutes}분 후에 다시 이용할 수 있습니다.`;
        this.showModal = true; // 모달 열기
      } else {
        this.$router.push({ name: gameKey }); // 게임 페이지로 이동
      }
    },
    isDisabled(gameKey) {
      const lastPlayed = localStorage.getItem(gameKey);
      const now = Date.now();
      return lastPlayed && now - lastPlayed < this.cooldownTime;
    },
    closeModal() {
      this.showModal = false;
    },
  },
};
</script>

<style scoped>
.container {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.text-center {
  color: #4caf50;
  font-size: 2rem;
  font-weight: bold;
}

.game-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); /* 그리드 레이아웃 */
  gap: 20px;
  width: 100%;
  padding: 20px;
}

.game-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative; /* 레이블 배치를 위해 */
  text-align: center;
  padding: 15px;
  border-radius: 15px;
  background: linear-gradient(145deg, #ffffff, #e6e6e6);
  box-shadow: 6px 6px 12px #c8c8c8, -6px -6px 12px #ffffff;
  transition: all 0.3s ease-in-out;
  animation: fadeIn 0.5s ease-in-out; /* 등장 애니메이션 */
  height: 500px; /* 세로 길이를 기존보다 늘림 */
}

.game-card:hover {
  transform: translateY(-5px);
  box-shadow: 10px 10px 20px #c8c8c8, -10px -10px 20px #ffffff;
  border-color: #4caf50;
}

.game-card.disabled {
  background-color: #ccc;
  cursor: not-allowed;
  opacity: 0.5;
}

.thumbnail {
  width: 100%;
  max-height: 210px;
  margin-top: 50px;
  border-radius: 15px;
  object-fit: cover;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
}

.thumbnail:hover {
  transform: scale(1.05);
}

.difficulty-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background: #4caf50;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 0.9rem;
  font-weight: bold;
}

.difficulty-badge.medium {
  background: #ff9800; /* 중간 레이블 색상 */
}

.difficulty-badge.hard {
  background: #f44336; /* 어려움 레이블 색상 */
}

.game-info {
  color: #555;
}

.game-info h2 {
  font-size: 1.5rem;
  margin-top: 10px;
}

.game-info p {
  font-size: 1rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(4px); /* 배경 흐림 효과 */
}

.modal-content {
  background: linear-gradient(145deg, #ffffff, #e6e6e6);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 6px 6px 12px rgba(0, 0, 0, 0.1), -6px -6px 12px rgba(255, 255, 255, 0.6);
  text-align: center;
}

.modal-content p {
  font-size: 1.2rem;
  margin-bottom: 20px;
  color: #333;
}

.modal-content .btn {
  padding: 10px 20px;
  background: #4caf50;
  color: #fff;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: background 0.3s ease;
}

.modal-content .btn:hover {
  background: #45a049;
}

/* 등장 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>
