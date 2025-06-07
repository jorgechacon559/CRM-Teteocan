<template>
  <div class="public-bg">
    <div class="public-container">
      <div class="wrapper">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {
  --primary-color: #2563eb;
  --primary-dark: #1e40af;
  --accent-color: #1abc9c;
  --light-gray: #f7f8fa;
  --medium-gray: #e0e7ff;
  --dark-gray: #718096;
  --white: #ffffff;
  --shadow-md: 0 20px 50px rgba(37, 99, 235, 0.15);
}

* {
  font-family: 'Poppins', sans-serif;
  box-sizing: border-box;
}

.public-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #f7f8fa 0%, #e0e7ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.public-container {
  width: 100%;
  max-width: 1100px;
  min-height: 80vh;
  background: #fff;
  border-radius: 24px;
  box-shadow: var(--shadow-md);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: center;
  min-height: 100%;
  padding: 0;
}

@media (max-width: 992px) {
  .public-container {
    max-width: 600px;
    min-height: unset;
    border-radius: 18px;
  }
}

@media (max-width: 576px) {
  .public-container {
    border-radius: 0;
    min-height: 100vh;
    max-width: 100vw;
  }
}
</style>