<template>
  <div class="container">
    <h1 class="text-center my-4">해외영화 명언</h1>

    <div v-if="gameOver" class="text-center">
      <h2>게임 종료!</h2>
      <p>모든 문제를 완료하였습니다.</p>
      <p>정답 수: {{ correctCount }} / {{ totalQuestions }}</p>
      <button class="btn btn-primary mt-3" @click="restartGame">다시 시작하기</button>
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
import axios from "axios";

export default {
  data() {
    return {
      reviews: [],
      selectedQuotes: [],
      currentquote: {},
      currentQuestionIndex: 0,
      totalQuestions: 5,
      userAnswer: "",
      isCorrect: false,
      showResult: false,
      gameOver: false,
      correctCount: 0,
    };
  },
  methods: {
    async updatePoints(points) {
      try {
        const response = await axios.post(
          "/api/user/points/",
          { points },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );
        console.log("Points updated successfully:", response.data);
      } catch (error) {
        console.error("Error updating points:", error);
      }
    },
    restartGame() {
      if (this.correctCount > 0) {
        this.updatePoints(this.correctCount * 100);
      }
      this.currentQuestionIndex = 0;
      this.correctCount = 0;
      this.gameOver = false;
      this.userAnswer = "";
      this.showResult = false;
      this.isCorrect = false;
      this.selectRandomReviews();
      this.currentquote = this.selectedQuotes[this.currentQuestionIndex];
    },
    async fetchReviews() {
      try {
        const response = await axios.get("/foreign_movies_quotes.json");
        this.reviews = response.data;
        this.selectRandomReviews();
        this.currentquote = this.selectedQuotes[this.currentQuestionIndex];
      } catch (error) {
        console.error("Error loading reviews:", error);
      }
    },
    selectRandomReviews() {
      const shuffled = this.reviews.sort(() => 0.5 - Math.random());
      this.selectedQuotes = shuffled.slice(0, this.totalQuestions);
    },
    checkAnswer() {
      if (this.userAnswer.trim() === "") return;
      this.isCorrect = this.currentquote.title.some(
        (correctTitle) =>
          this.userAnswer.trim().toLowerCase() ===
          correctTitle.toLowerCase()
      );
      if (this.isCorrect) {
        this.correctCount += 1;
      }
      this.showResult = true;
    },
    nextReview() {
      this.userAnswer = "";
      this.showResult = false;
      this.isCorrect = false;
      this.currentQuestionIndex += 1;
      if (this.currentQuestionIndex < this.totalQuestions) {
        this.currentquote = this.selectedQuotes[this.currentQuestionIndex];
      } else {
        this.gameOver = true;
      }
    },
    handleKeyPress(event) {
      if (event.key === "Enter") {
        if (this.showResult) {
          this.nextReview();
        } else {
          this.checkAnswer();
        }
      }
    },
    getPosterUrl(title) {
      return `/foreign_movie_poster/${title}.jpg`;
    },
  },
  created() {
    this.fetchReviews();
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
