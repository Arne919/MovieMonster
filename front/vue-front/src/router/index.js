import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import CreateArticle from "../views/CreateArticle.vue"; // 게시글 생성 컴포넌트 추가


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/create-article",
      name: "create-article",
      component: CreateArticle,
    },
  ],
});

export default router;
