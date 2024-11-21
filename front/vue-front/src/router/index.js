import { createRouter, createWebHistory } from 'vue-router'
import ArticleList from '@/components/ArticleList.vue'
import ArticleView from '@/views/ArticleView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import MovieList from '@/components/MovieList.vue'; // MovieList 컴포넌트 추가
import MovieDetail from '@/components/MovieDetail.vue'; // MovieDetail 컴포넌트 추가
import GameView from '@/views/GameView.vue'
import OneLineView from "@/views/OneLineView.vue"
import KoreaQuotesView from "@/views/KoreaQuotesView.vue"
import ForeignQuotesView from "@/views/ForeignQuotesView.vue"
import RankView from '@/views/RankView.vue'
import { useCounterStore } from '@/stores/counter'
import EditView from '@/views/EditView.vue'
import ProfileView from '@/views/ProfileView.vue';
import CategoryDetail from '@/components/CategoryDetail.vue';
import CategoryList from '@/components/CategoryList.vue';
import CreateCategory from "@/components/CreateCategory.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'ArticleView',
      component: ArticleView
    },
    {
      path: '/articles/:id/edit',
      name: 'EditView',
      component: EditView
    },
    {
      path: '/articles/:id',
      name: 'DetailView',
      component: DetailView
    },
    {
      path: '/create',
      name: 'CreateView',
      component: CreateView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    // 영화 리스트 페이지 추가
    {
      path: '/movies',
      name: 'MovieList',
      component: MovieList,
    },
    // 영화 상세 페이지 추가
    {
      path: '/movies/:id',
      name: 'MovieDetail',
      component: MovieDetail,
    },
    {
      path: '/game',
      name: 'GameView',
      component: GameView,
    },
    {
      path: "/game/one-line",
      name: "OneLineView",
      component: OneLineView,
    },
    {
      path: "/game/korea-quotes",
      name: "KoreaQuotesView",
      component: KoreaQuotesView,
    },
    {
      path: "/game/foreign-quotes",
      name: "ForeignQuotesView",
      component: ForeignQuotesView,
    },
    {
      path: '/rank',
      name: 'RankView',
      component: RankView,
    },
    {
      path: '/profile/:username',
      name: 'ProfileView',
      component: ProfileView,
    },
    {
      path: '/profile/:username/categories',
      name: 'CategoryList',
      component: CategoryList,
    },
    {
      path: '/categories/:id',
      name: 'CategoryDetail',
      component: CategoryDetail,
    },{
      path: '/categories/create',
      name: 'CreateCategory',
      component: CreateCategory,
    },
  ]
})

router.beforeEach((to, from) => {
  const store = useCounterStore();

  // 로그인 상태 확인이 필요한 경로들
  const protectedRoutes = ['ArticleView', 'MovieList', 'GameView', 'RankView'];

  if (protectedRoutes.includes(to.name) && !store.isLogin) {
    window.alert('로그인이 필요합니다.');
    return { name: 'LogInView' };
  }

  // 로그인 사용자가 회원가입 또는 로그인 페이지로 이동하려고 하면 메인 페이지로 리다이렉트
  if ((to.name === 'SignUpView' || to.name === 'LogInView') && store.isLogin) {
    window.alert('이미 로그인 되어있습니다.');
    return { name: 'ArticleView' };
  }
});

export default router
