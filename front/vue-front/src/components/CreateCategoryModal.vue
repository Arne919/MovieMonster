<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>새 카테고리 만들기</h3>
      <input
        v-model="categoryName"
        class="form-control"
        placeholder="카테고리 이름을 입력하세요"
      />
      <div class="modal-actions">
        <button class="btn btn-success" @click="createCategory">생성</button>
        <button class="btn btn-danger" @click="$emit('close')">취소</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useCounterStore } from "@/stores/counter";

export default {
  data() {
    return {
      categoryName: "",
    };
  },
  methods: {
    async createCategory() {
      if (!this.categoryName.trim()) {
        alert("카테고리 이름을 입력하세요.");
        return;
      }
      try {
        const store = useCounterStore();
        const { data } = await axios.post(
          `http://127.0.0.1:8000/accounts/categories/create/`,
          { name: this.categoryName },
          {
            headers: {
              Authorization: `Token ${store.token}`,
            },
          }
        );
        alert("카테고리가 생성되었습니다.");
        this.$emit("categoryCreated", data); // 생성된 카테고리를 부모 컴포넌트로 전달
        this.$emit("close"); // 모달 닫기
      } catch (error) {
        console.error("Error creating category:", error);
        alert("카테고리 생성에 실패했습니다.");
      }
    },
  },
};
</script>

<style scoped>
/* 모달 스타일 */
</style>
