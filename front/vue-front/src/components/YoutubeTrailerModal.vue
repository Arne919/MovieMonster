<template>
  <div
    ref="modalRef"
    class="modal fade"
    id="youtubeTrailerModal"
    tabindex="-1"
    aria-labelledby="youtubeTrailerLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="youtubeTrailerLabel">
            {{ movieTitle }} 공식 예고편
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
            @click="stopVideo"
          ></button>
        </div>
        <div class="modal-body">
          <div v-if="isLoading" class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <iframe
            v-else-if="videoData"
            class="trailer-iframe"
            :src="videoData"
            frameborder="0"
            allowfullscreen
          ></iframe>
          <div v-else>
            <p>해당 영화의 예고편을 찾을 수 없습니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import axios from "axios";

const props = defineProps({
  movieTitle: String,
});

const videoData = ref("");
const isLoading = ref(false);
const modalRef = ref(null);
const youtubeKey = "AIzaSyAvDN5ECAKK-StTzlh97JIt_daHFyimQlY"; // API 키

const stopVideo = () => {
  videoData.value = ""; // 비디오 정지
};

// 트레일러 로드 함수
const fetchTrailer = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get("https://www.googleapis.com/youtube/v3/search", {
      params: {
        key: youtubeKey,
        part: "snippet",
        type: "video",
        q: `${props.movieTitle} 예고편 OR trailer`,
        maxResults: 1,
      },
    });

    const videoId = response.data.items[0]?.id?.videoId || null;
    if (videoId) {
      videoData.value = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1`;
    } else {
      videoData.value = null;
    }
  } catch (error) {
    console.error("YouTube API 호출 에러:", error);
    videoData.value = null;
  } finally {
    isLoading.value = false;
  }
};

// 포커스 관리
const disableBackground = () => {
  document.body.setAttribute("inert", "true");
};

const enableBackground = () => {
  document.body.removeAttribute("inert");
};

onMounted(() => {
  if (modalRef.value) {
    modalRef.value.addEventListener("show.bs.modal", fetchTrailer);
    modalRef.value.addEventListener("hidden.bs.modal", stopVideo);
  }
});

onBeforeUnmount(() => {
  if (modalRef.value) {
    modalRef.value.removeEventListener("show.bs.modal", fetchTrailer);
    modalRef.value.removeEventListener("hidden.bs.modal", stopVideo);
  }
});
</script>

<style scoped>
.modal-content {
  max-width: 820px;
}

.trailer-iframe {
  width: 100%;
  height: 450px;
  display: block;
  margin: 0 auto;
}
</style>
