<template>
  <div>
    <input type="file" @change="handleFileChange" />
    <button @click="uploadFile">Upload</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    uploadFile() {
      if (this.selectedFile) {
        // 使用適當的 API 請求或其他方式將文件上傳到伺服器
        // 這裡可以使用 axios 或其他 HTTP 函式庫
        console.log('Uploading file:', this.selectedFile);
      } else {
        console.warn('No file selected for upload.');
      }
    },
  },
};
</script>

<style scoped>
/* 在這裡添加樣式，如果需要的話 */
</style>

