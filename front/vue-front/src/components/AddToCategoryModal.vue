<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h5>카테고리 선택</h5>
        <button class="btn-close" @click="$emit('close')"></button>
      </div>
      <div class="modal-body">
        <!-- 카테고리 리스트 -->
        <ul class="list-group">
          <li
            v-for="category in categories"
            :key="category.id"
            class="list-group-item"
          >
            {{ category.name }}
            <button
              class="btn btn-success btn-sm"
              @click="addMovieToCategory(category.id)"
            >
              추가
            </button>
          </li>
        </ul>

        <!-- 새 카테고리 생성 -->
        <div class="mt-3">
          <input
            v-model="newCategoryName"
            placeholder="새 카테고리 이름"
            class="form-control"
          />
          <button class="btn btn-primary mt-2" @click="createCategory">
            카테고리 생성
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from "@/axios";
const ACCOUNTS_BASE_URL = "http://127.0.0.1:8000/accounts";


export default {
  props: {
    movieId: Number, // 영화 ID
  },
  data() {
    return {
      categories: [], // 카테고리 목록
      newCategoryName: "", // 새 카테고리 이름
    };
  },
  methods: {
    // 카테고리 목록 가져오기
    fetchCategories() {
      axiosInstance
      .get("http://127.0.0.1:8000/accounts/categories/") // baseURL + "/categories/"
      .then((response) => {
        this.categories = response.data;
      })
      .catch((error) => {
        console.error("Error fetching categories:", error);
        alert("카테고리를 불러오는 데 실패했습니다.");
      });
    },



    // 새 카테고리 생성
    createCategory() {
      if (!this.newCategoryName.trim()) {
        alert("카테고리 이름을 입력해주세요.");
        return;
      }

      axiosInstance
        .post("http://127.0.0.1:8000/accounts/categories/create/", { name: this.newCategoryName })
        .then((response) => {
          this.categories.push(response.data); // 새 카테고리를 목록에 추가
          this.newCategoryName = ""; // 입력 필드 초기화
          alert("카테고리가 생성되었습니다.");
        })
        .catch((error) => {
          console.error("Error creating category:", error.response || error.message);
          alert(
            "카테고리를 생성하는 데 실패했습니다: " +
              (error.response?.data?.detail || "알 수 없는 오류")
          );
        });
    },
    // 영화를 카테고리에 추가
    addMovieToCategory(categoryId) {
      axiosInstance
        .post("http://127.0.0.1:8000/accounts/categories/add-movie/", {
          category_id: categoryId,
          movie_id: this.movieId,
        })
        .then(() => {
          alert("영화가 카테고리에 추가되었습니다.");
        })
        .catch((error) => {
          console.error("Error adding movie to category:", error);
          alert("영화를 추가하는 데 실패했습니다.");
        });
    },
  },
  mounted() {
    this.fetchCategories();
  },
};
</script>

<style>
/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
