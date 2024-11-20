<template>
  <div class="container">
    <h1 class="text-center my-4">이동진의 한줄평 게임</h1>

    <div v-if="gameOver" class="text-center">
      <h2>게임 종료!</h2>
      <p>모든 문제를 완료하였습니다.</p>
      <p>정답 수: {{ correctCount }} / {{ totalQuestions }}</p>
      <!-- 필요에 따라 다시 시작하거나 다른 동작을 추가할 수 있습니다 -->
      <button class="btn btn-primary mt-3" @click="restartGame">다시 시작하기</button>
    </div>

    <div v-else>
      <!-- 문제 번호 표시 -->
      <p class="text-center">문제 {{ currentQuestionIndex + 1 }} / {{ totalQuestions }}</p>

      <!-- 랜덤 대사 출력 -->
      <div v-if="!showResult" class="review-container text-center">
        <p class="review-text">{{ currentReview.review }}</p>

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
      <div v-if="showResult" class="result-container text-center mt-4">
        <p v-if="isCorrect" class="text-success">정답입니다! 🎉</p>
        <p v-else class="text-danger">틀렸습니다. 정답은 "{{ currentReview.title[0] }}" 입니다. ❌</p>
        <img
          :src="getPosterUrl(currentReview.id)"
          class="img-fluid mt-3"
          alt="영화 포스터"
        />
        <button class="btn btn-secondary mt-4" @click="nextReview">다음</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      reviews: [], // 모든 대사 데이터
      selectedReviews: [], // 랜덤으로 선택된 20개의 대사
      currentReview: {}, // 현재 대사
      currentQuestionIndex: 0, // 현재 문제 번호
      totalQuestions: 20, // 총 문제 수
      userAnswer: "", // 사용자 입력
      isCorrect: false, // 정답 여부
      showResult: false, // 결과 화면 표시 여부
      gameOver: false, // 게임 종료 여부
      correctCount: 0, // 정답 개수
    };
  },
  methods: {
    // 게임 재시작
    restartGame() {
      this.currentQuestionIndex = 0;
      this.correctCount = 0;
      this.gameOver = false;
      this.userAnswer = "";
      this.showResult = false;
      this.isCorrect = false;
      this.selectRandomReviews(); // 새로운 랜덤 리뷰 선택
      this.currentReview = this.selectedReviews[this.currentQuestionIndex];
    },
    // JSON 파일에서 대사 데이터 가져오기
    async fetchReviews() {
      try {
        const response = await axios.get("/one_line_review2.json");
        this.reviews = response.data; // JSON 데이터를 reviews 배열에 저장
        this.selectRandomReviews(); // 랜덤으로 20개 선택
        this.currentReview = this.selectedReviews[this.currentQuestionIndex];
      } catch (error) {
        console.error("Error loading reviews:", error);
      }
    },
    // 랜덤으로 20개의 리뷰 선택 (중복 없이)
    selectRandomReviews() {
      const shuffled = this.reviews.sort(() => 0.5 - Math.random());
      this.selectedReviews = shuffled.slice(0, this.totalQuestions);
    },
    // 정답 확인
    checkAnswer() {
      if (this.userAnswer.trim() === "") return; // 빈 입력은 무시
      this.isCorrect = this.currentReview.title.some(
        (correctTitle) =>
          this.userAnswer.trim().toLowerCase() === correctTitle.toLowerCase()
      );
      if (this.isCorrect) {
        this.correctCount += 1;
      }
      this.showResult = true; // 결과 화면 표시
    },
    // 다음 대사로 이동
    nextReview() {
      this.userAnswer = "";
      this.showResult = false;
      this.isCorrect = false;
      this.currentQuestionIndex += 1;
      if (this.currentQuestionIndex < this.totalQuestions) {
        this.currentReview = this.selectedReviews[this.currentQuestionIndex];
      } else {
        this.gameOver = true; // 게임 종료
      }
    },
    handleKeyPress(event) {
      if (event.key === "Enter") {
        if (this.showResult) {
          this.nextReview(); // 결과 화면에서는 다음으로 이동
        } else {
          this.checkAnswer(); // 입력 화면에서는 제출 동작
        }
      }
    },
    
    // 영화 포스터 URL 생성 (id 기반)
    getPosterUrl(id) {
      return `/one_line_poster/${id}.jpg`; // 포스터 파일 경로
    },
  },
  created() {
    this.fetchReviews(); // 컴포넌트 생성 시 대사 데이터 가져오기
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