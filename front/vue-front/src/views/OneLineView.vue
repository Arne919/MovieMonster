<template>
  <div class="container">
    <h1 class="text-center my-4">이동진의 한줄평 게임</h1>

    <div v-if="gameOver" class="text-center">
      <h2>게임 종료!</h2>
      <p>모든 문제를 완료하였습니다.</p>
      <p>정답 수: {{ correctCount }} / {{ totalQuestions }}</p>
      <p>획득 가능한 포인트 : {{ 100 * correctCount }}</p>

      <!-- 포인트 획득하기 버튼 -->
      <button
        class="btn btn-success mt-3"
        @click="openConfirmModal('claim')"
        data-bs-toggle="modal"
        data-bs-target="#confirmModal"
      >
        포인트 획득하기
      </button>

      <!-- 재시작 버튼 -->
      <button class="btn btn-primary mt-3" @click="restartGame">다시 시작하기</button>

      <!-- 랭크 확인하기 버튼 -->
      <button
        class="btn btn-info mt-3"
        @click="openConfirmModal('rank')"
        data-bs-toggle="modal"
        data-bs-target="#confirmModal"
      >
        랭크 확인하기
      </button>
    </div>

    <div v-else>
      <!-- 문제 번호 표시 -->
      <p class="text-center">문제 {{ currentQuestionIndex + 1 }} / {{ totalQuestions }}</p>

      <!-- 랜덤 대사 출력 -->
      <div v-if="!showResult && currentReview" class="review-container text-center">
        <p class="review-text">{{ currentReview?.review }}</p>

        <!-- 정답 입력 -->
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

      <!-- 결과 출력 -->
      <div v-if="showResult && currentReview" class="result-container text-center mt-4">
        <p v-if="isCorrect" class="text-success">정답입니다! 🎉</p>
        <p v-else class="text-danger">
          틀렸습니다. 정답은 "{{ currentReview?.title[0] }}" 입니다. ❌
        </p>
        <img
          :src="getPosterUrl(currentReview?.id)"
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
import { ref, onMounted } from "vue";
import axios from "axios";
import { useCounterStore } from "@/stores/counter";
import { useRouter } from "vue-router";

export default {
  setup() {
    const reviews = ref([]);
    const selectedReviews = ref([]);
    const currentReview = ref({});
    const currentQuestionIndex = ref(0);
    const totalQuestions = ref(5);
    const userAnswer = ref("");
    const isCorrect = ref(false);
    const showResult = ref(false);
    const gameOver = ref(false);
    const correctCount = ref(0);
    const router = useRouter();
    const store = useCounterStore();

    // 모달 상태
    const modalMessage = ref("");
    const modalAction = ref("");

    const openConfirmModal = (action) => {
      modalAction.value = action;
      modalMessage.value = `${100 * correctCount.value}p를 획득 하시겠어요?`;
    };

    const handleModalConfirm = async () => {
      if (modalAction.value === "claim") {
        await claimPoints();
      } else if (modalAction.value === "rank") {
        await goToRank();
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
        const response = await axios.post(
          `${store.API_URL}/accounts/user/points/`,
          { points },
          {
            headers: {
              Authorization: `Token ${store.token}`,
            },
          }
        );
        console.log("Points updated successfully:", response.data);
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
      currentReview.value = selectedReviews.value[currentQuestionIndex.value];
    };

    const fetchReviews = async () => {
      try {
        const response = await axios.get("/one_line_review2.json");
        reviews.value = response.data;
        selectRandomReviews();
        currentReview.value = selectedReviews.value[currentQuestionIndex.value];
      } catch (error) {
        console.error("Error loading reviews:", error);
      }
    };

    const selectRandomReviews = () => {
      const shuffled = reviews.value.sort(() => 0.5 - Math.random());
      selectedReviews.value = shuffled.slice(0, totalQuestions.value);
    };

    const checkAnswer = () => {
      if (userAnswer.value.trim() === "") return;
      isCorrect.value = currentReview.value.title.some(
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
        currentReview.value = selectedReviews.value[currentQuestionIndex.value];
      } else {
        gameOver.value = true;
      }
    };

    const getPosterUrl = (id) => `/one_line_poster/${id}.jpg`;

    onMounted(() => {
      fetchReviews();
    });

    return {
      reviews,
      selectedReviews,
      currentReview,
      currentQuestionIndex,
      totalQuestions,
      userAnswer,
      isCorrect,
      showResult,
      gameOver,
      correctCount,
      claimPoints,
      restartGame,
      checkAnswer,
      nextReview,
      getPosterUrl,
      goToRank,
      modalMessage,
      openConfirmModal,
      handleModalConfirm,
      handleModalCancel,
    };
  },
};
</script>

<style scoped>
.container {
  margin-top: 40px;
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
</style>
