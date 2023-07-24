<template>
<div class="parent">
  <div class="child">盒子 1</div>
  <div class="child">盒子 2</div>
  <div class="child">盒子 3</div>
  <!-- 添加更多子盒子... -->
</div>

</template>

<script setup>

</script>
<style>
.parent {
  width: 300px; /* 父盒子的宽度 */
  overflow-x: auto; /* 水平滚动条 */
  white-space: nowrap; /* 子盒子不换行 */
}

.child {
  display: inline-block; /* 子盒子水平排列 */
  width: 100px; /* 子盒子的宽度 */
  height: 100px; /* 子盒子的高度 */
  margin-right: 10px; /* 子盒子之间的间距 */
}

</style>
