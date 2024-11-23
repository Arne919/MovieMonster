<template>
  <div class="container">
    <h1 class="text-center my-4">게임하고 포인트 받자!</h1>

    <div class="game-list">
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
        <div class="game-info">
          <h2>이동진의 한줄평</h2>
          <p>이동진의 한줄평 보고 영화 맞추기!</p>
        </div>
      </div>

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
        <div class="game-info">
          <h2>해외영화 명대사</h2>
          <p>해외영화 명대사 보고 영화 맞추기! (어려움)</p>
        </div>
      </div>
    </div>

    <!-- 모달 -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <p>{{ modalMessage }}</p>
        <button class="btn btn-primary" @click="closeModal">닫기</button>
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

.game-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
  width: 100%;
}

.game-card {
  display: flex;
  align-items: center;
  width: 90%;
  max-width: 1400px;
  height: 150px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.game-card.disabled {
  background-color: #ccc;
  cursor: not-allowed;
  opacity: 0.7;
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
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.game-card:hover {
  transform: scale(1.03);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.thumbnail {
  flex: 1;
  height: 100%;
  max-width: 200px;
  margin-right: 20px;
  border-radius: 5px;
  object-fit: contain;
  background-color: #f9f9f9;
}

.game-info {
  flex: 3;
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
