<template>
  <div>
    <h1>Welcome to Home</h1>
    <p v-if="store.user.username">Hello, {{ store.user.username }}</p>
    <p v-else>로그인이 필요합니다.</p>
  </div>
</template>

<script setup>
import { useCounterStore } from "@/stores/counter";
const store = useCounterStore();
</script>
