<template>
  <div class="container">
    <h1 class="text-center my-4">해외영화 명대사</h1>

    <div v-if="gameOver" class="text-center">
      <h2>게임 종료!</h2>
      <p>모든 문제를 완료하였습니다.</p>
      <p>정답 수: {{ correctCount }} / {{ totalQuestions }}</p>

      <!-- 포인트 획득하기 버튼 -->
      <button class="btn btn-success mt-3" @click="claimPoints">포인트 획득하기</button>

      <button class="btn btn-primary mt-3" @click="restartGame">다시 시작하기</button>

      <!-- <랭크 확인하기> 버튼 -->
      <button class="btn btn-info mt-3" @click="goToRank">랭크 확인하기</button>

      
    </div>

    <div v-else>
      <p class="text-center">문제 {{ currentQuestionIndex + 1 }} / {{ totalQuestions }}</p>

      <div v-if="!showResult" class="review-container text-center">
        <p class="review-text">{{ currentquote.movietext }}</p>
        <p class="review-text">{{ currentquote.translatedMovietext }}</p>
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
        <p v-else class="text-danger">틀렸습니다. 정답은 "{{ currentquote.title[1] }}" 입니다. ❌</p>
        <img
          :src="getPosterUrl(currentquote.title[0])"
          class="img-fluid mt-3"
          alt="영화 포스터"
        />
        <button class="btn btn-secondary mt-4" @click="nextReview">다음</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';

export default {
  setup() {
    // 상태 정의
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
    const router = useRouter();
    const store = useCounterStore();

    const goToRank = () => {
      router.push({ name: "RankView" }); // RankView 페이지로 이동
    };
    // 포인트 업데이트 함수
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
        store.points += points; // Pinia 스토어의 포인트 업데이트
      } catch (error) {
        console.error("Error updating points:", error);
      }
    };

    // 포인트 획득하기
    const claimPoints = async () => {
      if (correctCount.value > 0) {
        await updatePoints(correctCount.value * 100);
      }
      await store.fetchUserPoints(); // 사용자 포인트 최신화
      router.push({ name: "GameView" }); // 게임 뷰로 이동
    };

    // 게임 재시작
    const restartGame = () => {
      if (correctCount.value > 0) {
        updatePoints(correctCount.value * 100);
      }
      currentQuestionIndex.value = 0;
      correctCount.value = 0;
      gameOver.value = false;
      userAnswer.value = "";
      showResult.value = false;
      isCorrect.value = false;
      selectRandomReviews();
      currentquote.value = selectedQuotes.value[currentQuestionIndex.value];
    };

    // 리뷰 데이터 가져오기
    const fetchReviews = async () => {
      try {
        const response = await axios.get("/foreign_movies_quotes.json");
        reviews.value = response.data;
        selectRandomReviews();
        currentquote.value = selectedQuotes.value[currentQuestionIndex.value];
      } catch (error) {
        console.error("Error loading reviews:", error);
      }
    };

    // 랜덤 리뷰 선택
    const selectRandomReviews = () => {
      const shuffled = reviews.value.sort(() => 0.5 - Math.random());
      selectedQuotes.value = shuffled.slice(0, totalQuestions.value);
    };

    // 정답 확인
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

    // 다음 리뷰로 이동
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

    // 포스터 URL 가져오기
    const getPosterUrl = (title) => `/foreign_movie_poster/${title}.jpg`;

    // 키보드 입력 처리
    const handleKeyPress = (event) => {
      if (event.key === "Enter") {
        if (showResult.value) {
          nextReview();
        } else {
          checkAnswer();
        }
      }
    };

    // 컴포넌트가 마운트될 때 리뷰 데이터 로드
    onMounted(() => {
      fetchReviews();
    });

    // 반환
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
      updatePoints,
      restartGame,
      fetchReviews,
      selectRandomReviews,
      checkAnswer,
      nextReview,
      getPosterUrl,
      handleKeyPress,
      claimPoints,
      goToRank,
    };
  },
};
</script>


<style scoped>
.container {
  margin-top: 40px;
}
.review-container {
  font-size: 1.2rem;
  font-style: italic;
  margin-bottom: 20px;
}
.input-container {
  margin-top: 20px;
}
.result-container img {
  max-width: 300px;
  margin-top: 20px;
}
.result-container p {
  font-size: 1.2rem;
}
</style>
