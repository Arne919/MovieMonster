<template>
  <div class="container">
    <h1 class="text-center my-4">한국영화 명대사</h1>

    <div v-if="gameOver" class="text-center">
      <h2>게임 종료!</h2>
      <p>모든 문제를 완료하였습니다.</p>
      <p>정답 수: {{ correctCount }} / {{ totalQuestions }}</p>
      <p>획득 가능한 포인트 : {{ 100 * correctCount }}</p>

      <!-- 포인트 획득하기 버튼 -->
      <button class="btn btn-success mt-3" @click="openConfirmModal('claim')">포인트 획득하기</button>

      <!-- 게임 재시작 버튼 -->
      <button class="btn btn-primary mt-3" @click="restartGame">다시 시작하기</button>

      <!-- 랭크 확인하기 버튼 -->
      <button class="btn btn-info mt-3" @click="openConfirmModal('rank')">랭크 확인하기</button>
    </div>

    <div v-else>
      <p class="text-center">문제 {{ currentQuestionIndex + 1 }} / {{ totalQuestions }}</p>

      <div v-if="!showResult" class="review-container text-center">
        <p class="review-text">{{ currentquote.movietext }}</p>
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

    <!-- 모달 -->
    <div v-if="isModalOpen" class="modal-overlay">
      <div class="modal">
        <p>{{ modalMessage }}</p>
        <button class="btn btn-success" @click="handleModalConfirm">Yes</button>
        <button class="btn btn-danger" @click="handleModalCancel">No</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
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
    const isModalOpen = ref(false);
    const modalMessage = ref("");
    const modalAction = ref("");

    const router = useRouter();
    const store = useCounterStore();

    const openConfirmModal = (action) => {
      modalAction.value = action;
      modalMessage.value = `${100 * correctCount.value}p를 획득 하시겠어요?`;
      isModalOpen.value = true;
    };

    const handleModalConfirm = async () => {
      isModalOpen.value = false;
      if (modalAction.value === "claim") {
        await claimPoints();
      } else if (modalAction.value === "rank") {
        await goToRank();
      }
    };

    const handleModalCancel = () => {
      isModalOpen.value = false;
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
        const response = await axios.post(
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
    };

    const fetchReviews = async () => {
      try {
        const response = await axios.get("/korea_movies_quotes.json");
        reviews.value = response.data;
        selectRandomReviews();
        currentquote.value = selectedQuotes.value[currentQuestionIndex.value];
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
      } else {
        gameOver.value = true;
      }
    };

    const getPosterUrl = (title) => `/korea_movie_poster/${title}.jpg`;

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
      isModalOpen,
      modalMessage,
    };
  },
};
</script>

<style scoped>
.container {
  margin-top: 40px;
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
  z-index: 1000;
}

.modal {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.modal button {
  margin: 10px;
}
</style>
