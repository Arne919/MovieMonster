<template>
  <div id="app">
    <nav>
      <router-link to="/">홈</router-link>
      <router-link to="/create-article">게시글 생성</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* 추가 스타일 */
</style>
