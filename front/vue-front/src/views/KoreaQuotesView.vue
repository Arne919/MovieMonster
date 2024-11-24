<template>
  <div class="container">
    <h1 class="text-center-title my-4">한국영화 명대사</h1>

    <div v-if="gameOver" class="text-center">
      <h2>게임 종료!</h2>
      <p>모든 문제를 완료하였습니다.</p>
      <p>정답 수: {{ correctCount }} / {{ totalQuestions }}</p>
      <p>획득 가능한 포인트 : {{ 100 * correctCount }}</p>

      <!-- 포인트 획득하기 버튼 -->
      <a
        class="mt-3 add_point"
        href="#"
        @click.prevent="openConfirmModal('claim')"
        data-bs-toggle="modal"
        data-bs-target="#confirmModal"
      >
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        포인트 획득하기
      </a>


      <!-- 게임 재시작 버튼 -->
      <a
        class="mt-3 replay"
        href="#"
        @click.prevent="restartGame"
      >
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        다시 시작하기
      </a>

      <!-- 랭크 확인하기 버튼 -->
      <a
        class="mt-3 confirm_rank"
        href="#"
        @click.prevent="openConfirmModal('rank')"
        data-bs-toggle="modal"
        data-bs-target="#confirmModal"
      >
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        랭크 확인하기
      </a>
    </div>

    <div v-else>
      <p class="text-center">문제 {{ currentQuestionIndex + 1 }} / {{ totalQuestions }}</p>

      <div v-if="!showResult" class="review-container text-center">
        <!-- 타이핑 효과 -->
        <div id="typing-box">
          <span class="typing-text"></span><span class="blink">|</span>
        </div>

        <div class="input-container text-center">
          <input
            v-model="userAnswer"
            class="form-control w-50 mx-auto"
            type="text"
            placeholder="정답(영화 제목)을 입력하세요"
            @keyup.enter="checkAnswer"
          />
          <button class="btn btn-primary mt-3" @click="checkAnswer">제출</button>
        </div>
      </div>

      <div v-if="showResult" class="result-container text-center mt-4">
        <p v-if="isCorrect" class="text-success">정답입니다! 🎉</p>
        <p v-else class="text-danger">틀렸습니다. 정답은 "{{ currentquote.title[0] }}" 입니다. ❌</p>
        <img
          :src="getPosterUrl(currentquote.title[0])"
          class="img-fluid mt-3"
          alt="영화 포스터"
        />
        <button class="btn btn-secondary mt-4" @click="nextReview">다음</button>
      </div>
    </div>

    <!-- Bootstrap 모달 -->
    <div
      class="modal fade"
      id="confirmModal"
      tabindex="-1"
      aria-labelledby="confirmModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="confirmModalLabel">확인</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <p>{{ modalMessage }}</p>
          </div>
          <div class="modal-footer">
            <button
              class="btn btn-success"
              @click="handleModalConfirm"
              data-bs-dismiss="modal"
            >
              확인
            </button>
            <button
              class="btn btn-danger"
              @click="handleModalCancel"
              data-bs-dismiss="modal"
            >
              취소
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const COOLDOWN_KEY = "KoreaQuotesView"; // 고유 키 설정

import { ref, onMounted, nextTick } from "vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

export default {
  setup() {
    const reviews = ref([]);
    const selectedQuotes = ref([]);
    const currentquote = ref({});
    const currentQuestionIndex = ref(0);
    const totalQuestions = ref(5);
    const userAnswer = ref("");
    const isCorrect = ref(false);
    const showResult = ref(false);
    const gameOver = ref(false);
    const correctCount = ref(0);
    const modalMessage = ref("");
    const modalAction = ref("");

    const router = useRouter();
    const store = useCounterStore();

    const setCooldown = () => {
      localStorage.setItem(COOLDOWN_KEY, Date.now());
    };

    const openConfirmModal = (action) => {
      modalAction.value = action;
      modalMessage.value = `${100 * correctCount.value}p를 획득 하시겠어요?`;
    };

    const handleModalConfirm = async () => {
      if (modalAction.value === "claim") {
        await claimPoints();
        setCooldown();
      } else if (modalAction.value === "rank") {
        await goToRank();
        setCooldown();
      }
    };

    const handleModalCancel = () => {
      modalMessage.value = "";
    };

    const claimPoints = async () => {
      if (correctCount.value > 0) {
        await updatePoints(correctCount.value * 100);
      }
      await store.fetchUserPoints();
      router.push({ name: "GameView" });
    };

    const goToRank = async () => {
      if (correctCount.value > 0) {
        await updatePoints(correctCount.value * 100);
      }
      await store.fetchUserPoints();
      router.push({ name: "RankView" });
    };

    const updatePoints = async (points) => {
      try {
        await axios.post(
          `${store.API_URL}/accounts/user/points/`,
          { points },
          {
            headers: {
              Authorization: `Token ${store.token}`,
            },
          }
        );
        store.points += points;
      } catch (error) {
        console.error("Error updating points:", error);
      }
    };

    const restartGame = () => {
      currentQuestionIndex.value = 0;
      correctCount.value = 0;
      gameOver.value = false;
      userAnswer.value = "";
      showResult.value = false;
      isCorrect.value = false;
      selectRandomReviews();
      currentquote.value = selectedQuotes.value[currentQuestionIndex.value];

      // 타이핑 효과를 초기화하고 다시 실행
      nextTick(() => typingEffect(currentquote.value.movietext));
    };

    const fetchReviews = async () => {
      try {
        const response = await axios.get("/korea_movies_quotes.json");
        reviews.value = response.data;
        selectRandomReviews();
        currentquote.value = selectedQuotes.value[currentQuestionIndex.value];
        await nextTick();
        typingEffect(currentquote.value.movietext); // 타이핑 효과 시작
      } catch (error) {
        console.error("Error loading reviews:", error);
      }
    };

    const selectRandomReviews = () => {
      const shuffled = reviews.value.sort(() => 0.5 - Math.random());
      selectedQuotes.value = shuffled.slice(0, totalQuestions.value);
    };

    const checkAnswer = () => {
      if (userAnswer.value.trim() === "") return;
      isCorrect.value = currentquote.value.title.some(
        (correctTitle) =>
          userAnswer.value.trim().toLowerCase() === correctTitle.toLowerCase()
      );
      if (isCorrect.value) {
        correctCount.value += 1;
      }
      showResult.value = true;
    };

    const nextReview = () => {
      userAnswer.value = "";
      showResult.value = false;
      isCorrect.value = false;
      currentQuestionIndex.value += 1;
      if (currentQuestionIndex.value < totalQuestions.value) {
        currentquote.value = selectedQuotes.value[currentQuestionIndex.value];
        nextTick(() => typingEffect(currentquote.value.movietext)); // 다음 문제 타이핑 효과
      } else {
        gameOver.value = true;
      }
    };

    const getPosterUrl = (title) => `/korea_movie_poster/${title}.jpg`;

    const typingEffect = (text) => {
      const typingText = document.querySelector(".typing-text");
      typingText.textContent = "";
      let idx = 0;
      const type = () => {
        if (idx < text.length) {
          typingText.textContent += text[idx++];
          setTimeout(type, 100);
        }
      };
      type();
    };

    onMounted(() => {
      fetchReviews();
    });

    return {
      reviews,
      selectedQuotes,
      currentquote,
      currentQuestionIndex,
      totalQuestions,
      userAnswer,
      isCorrect,
      showResult,
      gameOver,
      correctCount,
      openConfirmModal,
      handleModalConfirm,
      handleModalCancel,
      claimPoints,
      goToRank,
      restartGame,
      fetchReviews,
      selectRandomReviews,
      checkAnswer,
      nextReview,
      getPosterUrl,
      modalMessage,
      setCooldown,
    };
  },
};
</script>

<style scoped>
.container {
  margin-top: 40px;
}

.text-center-title {
  color: #4caf50;
  text-align: center;
}

.modal-backdrop {
  background-color: rgba(0, 0, 0, 0.2) !important;
}

.modal {
  z-index: 1055;
  text-align: center;
}

.modal button {
  margin: 10px;
}

#typing-box {
  font-size: 1.5rem;
  color: #dddddd;
}

.blink {
  animation: blink 0.5s infinite;
}

@keyframes blink {
  to {
    opacity: 0;
  }
}

/* 포인트획득하기 버튼: 네온 스타일 */
.add_point {
  position: relative;
  display: inline-block;
  padding: 15px 20px;
  font-size: 14px; /* 텍스트 크기 조정 */
    margin: 50px 0; /* 여백 조정 */
  color: #4caf50;
  text-decoration: none;
  text-transform: uppercase;
  transition: 0.5s;
  letter-spacing: 1px;
  overflow: hidden;
  margin-right: 20px;
  margin-top: 40px;
}

.add_point:hover {
  background: #4caf50;
  color: #050801;
  box-shadow: 0 0 5px #4caf50, 0 0 25px #4caf50, 0 0 50px #4caf50,
    0 0 200px #4caf50;
  -webkit-box-reflect: below 1px linear-gradient(transparent, #0005);
}

.add_point span {
  position: absolute;
  display: block;
}

.add_point span:nth-child(1) {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #4caf50);
  animation: animate1 1s linear infinite;
}

@keyframes animate1 {
  0% {
    left: -100%;
  }
  50%,
  100% {
    left: 100%;
  }
}

.add_point span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #4caf50);
  animation: animate2 1s linear infinite;
  animation-delay: 0.25s;
}

@keyframes animate2 {
  0% {
    top: -100%;
  }
  50%,
  100% {
    top: 100%;
  }
}

.add_point span:nth-child(3) {
  bottom: 0;
  right: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #4caf50);
  animation: animate3 1s linear infinite;
  animation-delay: 0.5s;
}

@keyframes animate3 {
  0% {
    right: -100%;
  }
  50%,
  100% {
    right: 100%;
  }
}

.add_point span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #4caf50);
  animation: animate4 1s linear infinite;
  animation-delay: 0.75s;
}

@keyframes animate4 {
  0% {
    bottom: -100%;
  }
  50%,
  100% {
    bottom: 100%;
  }
}

/* 다시 시작하기 버튼: 네온 스타일 */
.replay {
  position: relative;
  display: inline-block;
  padding: 15px 20px;
  font-size: 14px; /* 텍스트 크기 조정 */
    margin: 50px 0; /* 여백 조정 */
  color: #f54a4a;
  text-decoration: none;
  text-transform: uppercase;
  transition: 0.5s;
  letter-spacing: 1px;
  overflow: hidden;
  margin-right: 20px;
  margin-top: 40px;
}

.replay:hover {
  background: #f54a4a;
  color: #050801;
  box-shadow: 0 0 5px #f54a4a, 0 0 25px #f54a4a, 0 0 50px #f54a4a,
    0 0 200px #f54a4a;
  -webkit-box-reflect: below 1px linear-gradient(transparent, #0005);
}

.replay span {
  position: absolute;
  display: block;
}

.replay span:nth-child(1) {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #f54a4a);
  animation: animate1 1s linear infinite;
}

@keyframes animate1 {
  0% {
    left: -100%;
  }
  50%,
  100% {
    left: 100%;
  }
}

.replay span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #f54a4a);
  animation: animate2 1s linear infinite;
  animation-delay: 0.25s;
}

@keyframes animate2 {
  0% {
    top: -100%;
  }
  50%,
  100% {
    top: 100%;
  }
}

.replay span:nth-child(3) {
  bottom: 0;
  right: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #f54a4a);
  animation: animate3 1s linear infinite;
  animation-delay: 0.5s;
}

@keyframes animate3 {
  0% {
    right: -100%;
  }
  50%,
  100% {
    right: 100%;
  }
}

.replay span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #f54a4a);
  animation: animate4 1s linear infinite;
  animation-delay: 0.75s;
}

@keyframes animate4 {
  0% {
    bottom: -100%;
  }
  50%,
  100% {
    bottom: 100%;
  }
}

/* 랭크 확인하기 버튼: 네온 버튼 스타일 */
.confirm_rank {
  position: relative;
  display: inline-block;
  padding: 15px 20px;
  font-size: 14px; /* 텍스트 크기 조정 */
    margin: 50px 0; /* 여백 조정 */
  color: #3358ff;
  text-decoration: none;
  text-transform: uppercase;
  transition: 0.5s;
  letter-spacing: 1px;
  overflow: hidden;
  margin-right: 20px;
  margin-top: 40px;
}

.confirm_rank:hover {
  background: #3358ff;
  color: #050801;
  box-shadow: 0 0 5px #3358ff, 0 0 25px #3358ff, 0 0 50px #3358ff,
    0 0 200px #3358ff;
  -webkit-box-reflect: below 1px linear-gradient(transparent, #0005);
}

.confirm_rank span {
  position: absolute;
  display: block;
}

.confirm_rank span:nth-child(1) {
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #3358ff);
  animation: animate1 1s linear infinite;
}

@keyframes animate1 {
  0% {
    left: -100%;
  }
  50%,
  100% {
    left: 100%;
  }
}

.confirm_rank span:nth-child(2) {
  top: -100%;
  right: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #3358ff);
  animation: animate2 1s linear infinite;
  animation-delay: 0.25s;
}

@keyframes animate2 {
  0% {
    top: -100%;
  }
  50%,
  100% {
    top: 100%;
  }
}

.confirm_rank span:nth-child(3) {
  bottom: 0;
  right: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #3358ff);
  animation: animate3 1s linear infinite;
  animation-delay: 0.5s;
}

@keyframes animate3 {
  0% {
    right: -100%;
  }
  50%,
  100% {
    right: 100%;
  }
}

.confirm_rank span:nth-child(4) {
  bottom: -100%;
  left: 0;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #3358ff);
  animation: animate4 1s linear infinite;
  animation-delay: 0.75s;
}

@keyframes animate4 {
  0% {
    bottom: -100%;
  }
  50%,
  100% {
    bottom: 100%;
  }
}
</style>
