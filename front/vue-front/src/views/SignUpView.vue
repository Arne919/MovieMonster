<template>
  <div>
    <h1>Sign Up Page</h1>
    <form @submit.prevent="signUp">
      <!-- 프로필 사진 업로드 -->
      <div>
        <label for="profilePicture">Profile Picture:</label>
        <input type="file" id="profilePicture" @change="onFileChange">
        <div v-if="profilePreview">
          <img :src="profilePreview" alt="Profile Preview" class="profile-preview" />
        </div>
      </div>

      <!-- 기존 회원가입 필드 -->
      <label for="username">username :</label>
      <input type="text" id="username" v-model.trim="username"><br>

      <label for="password1">password :</label>
      <input type="password" id="password1" v-model.trim="password1"><br>

      <label for="password2">password confirmation :</label>
      <input type="password" id="password2" v-model.trim="password2">
      
      <input type="submit" value="SignUp">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

const username = ref('');
const password1 = ref('');
const password2 = ref('');
const profilePicture = ref(null);
const profilePreview = ref(null);

const store = useCounterStore();

const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    profilePicture.value = file;
    profilePreview.value = URL.createObjectURL(file); // 미리보기 URL 생성
  }
  console.log(profilePicture)
};

const signUp = async () => {
  const formData = new FormData();
  formData.append('username', username.value);
  formData.append('password1', password1.value);
  formData.append('password2', password2.value);
  if (profilePicture.value) {
    formData.append('profile_picture', profilePicture.value);
  }

  console.log("DEBUG: FormData content:");
  for (let [key, value] of formData.entries()) {
    console.log(`${key}:`, value);
  }

  try {
    await store.signUp(formData); // 스토어에서 FormData 처리
    alert('회원가입 성공!');
  } catch (error) {
    console.error('회원가입 실패:', error);
    alert('회원가입 실패!');
  }
};
</script>

<style scoped>
.profile-preview {
  margin-top: 10px;
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 50%;
}
</style>
