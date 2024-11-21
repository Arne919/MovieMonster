<template>
  <div>
    <h2>카테고리 생성</h2>
    <form @submit.prevent="createCategory">
      <input
        v-model="categoryName"
        placeholder="카테고리 이름을 입력하세요"
        class="form-control"
      />
      <button type="submit" class="btn btn-primary mt-2">카테고리 생성</button>
    </form>
    <p v-if="message" class="mt-2">{{ message }}</p>
  </div>
</template>

<script>
import axios from "@/axios"; // axios.js 파일에서 설정된 Axios 인스턴스 불러오기

export default {
  data() {
    return {
      categoryName: "", // 입력된 카테고리 이름
      message: "", // 사용자 메시지
    };
  },
  methods: {
    async createCategory() {
      try {
        const response = await axios.post("/accounts/categories/", {
          name: this.categoryName,
        });
        this.message = `카테고리 "${response.data.name}"가 생성되었습니다.`;
        this.categoryName = ""; // 입력 필드 초기화
      } catch (error) {
        if (error.response && error.response.data) {
          this.message = error.response.data.error || "카테고리 생성에 실패했습니다.";
        } else {
          this.message = "서버와의 연결에 문제가 발생했습니다.";
        }
      }
    },
  },
};
</script>

<style scoped>
form {
  max-width: 400px;
  margin: 0 auto;
}
</style>
