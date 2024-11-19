<template>
  <div>
    <h1>게시글 생성</h1>
    <form @submit.prevent="createArticle">
      <div>
        <label for="title">제목</label>
        <input v-model="article.title" id="title" placeholder="게시글 제목" required />
      </div>
      <div>
        <label for="content">내용</label>
        <textarea v-model="article.content" id="content" placeholder="게시글 내용" required></textarea>
      </div>
      <button type="submit">등록</button>
    </form>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from "../axios";

export default {
  name: "CreateArticle",
  data() {
    return {
      article: {
        title: "",
        content: "",
      },
      message: "",
    };
  },
  methods: {
    async createArticle() {
      try {
        await axios.post("/communities/", this.article);
        this.message = "게시글이 성공적으로 생성되었습니다!";
        this.article.title = "";
        this.article.content = "";
      } catch (error) {
        console.error("게시글 생성 실패:", error);
        this.message = "게시글 생성에 실패했습니다.";
      }
    },
  },
};
</script>
