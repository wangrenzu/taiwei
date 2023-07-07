<template>
  <el-tag>款号重复的翻单不会移动，需要手动拖，颜色高亮的</el-tag>
  <el-button type="primary" @click="move">刷新</el-button>
  <div class="container" v-loading="loading">
    <div
        class="list"
        @drop="dropList($event, 0)"
        @dragover.prevent>
      <span style="color: #e1ba20">备料中&nbsp;&nbsp;{{ totalQuantity1 }}件</span>
      <div
          :class="[ { 'item': item.is_d === 0 },{'item2': item.is_d === 1}]"
          v-for="(item, j) in list1"
          :key="j"
          draggable="true"
          @dragstart="dragStart(0, j)"
          @drop="dropItem($event, 0, j)"
          @dragover.prevent>
        {{ item.order_date.slice(5).replace("-", '') }}-
        {{ item.code }}-
        {{ item.status }}-
        {{ item.total_quantity }}-
        <el-input
            v-if="update_input===item.id"
            style="width: 100px"
            v-model="item.expected_date"
            @keydown.enter="updateNewStyleStatusTrackingView(item.id,'',item.expected_date)"
        >
        </el-input>
        <span v-else @click="update_input=item.id">
          {{ item.expected_date.slice(5).replace("-", '') }}
        </span>
      </div>
    </div>
    <div
        class="list"
        @drop="dropList($event, 1)"
        @dragover.prevent>
      <span style="color: #e1ba20">车间生产&nbsp;&nbsp;{{ totalQuantity2 }}件</span>
      <div
          class="item"
          v-for="(item, j) in list2"
          :key="j"
          draggable="true"
          @dragstart="dragStart(1, j)"
          @drop="dropItem($event, 1, j)"
          @dragover.prevent>
        {{ item.order_date.slice(5).replace("-", '') }}-
        {{ item.code }}-
        {{ item.status }}-
        {{ item.total_quantity }}-
        ({{ item.notes }})-
        <el-input
            v-if="update_input===item.id"
            style="width: 100px"
            v-model="item.expected_date"
            @keydown.enter="updateNewStyleStatusTrackingView(item.id,'',item.expected_date)"
        >
        </el-input>
        <span v-else @click="update_input=item.id">
          {{ item.expected_date.slice(5).replace("-", '') }}
        </span>
      </div>
    </div>
    <div
        class="list"
        @drop="dropList($event, 2)"
        @dragover.prevent>
      <span style="color: #e1ba20">后道&nbsp;&nbsp;{{ totalQuantity3 }}件</span>
      <div
          class="item"
          v-for="(item, j) in list3"
          :key="j"
          draggable="true"
          @dragstart="dragStart(2, j)"
          @drop="dropItem($event, 2, j)"
          @dragover.prevent>
        {{ item.order_date.slice(5).replace("-", '') }}-
        {{ item.code }}-
        {{ item.status }}-
        {{ item.total_quantity }}-
        ({{ item.notes }})-
        <el-input
            v-if="update_input===item.id"
            style="width: 100px"
            v-model="item.expected_date"
            @keydown.enter="updateNewStyleStatusTrackingView(item.id,'',item.expected_date)"
        >
        </el-input>
        <span v-else @click="update_input=item.id">
          {{ item.expected_date.slice(5).replace("-", '') }}
        </span>
      </div>
    </div>
    <div
        class="list"
        @drop="dropList($event, 3)"
        @dragover.prevent>
      <span style="color: #e1ba20">入仓没上架&nbsp;&nbsp;{{ totalQuantity4 }}件</span>
      <div
          class="item"
          v-for="(item, j) in list4"
          :key="j"
          draggable="true"
          @dragstart="dragStart(3, j)"
          @drop="dropItem($event, 3, j)"
          @dragover.prevent>
        {{ item.order_date.slice(5).replace("-", '') }}-
        {{ item.code }}-
        {{ item.status }}-
        {{ item.total_quantity }}-
        ({{ item.notes }})-
        <el-input
            v-if="update_input===item.id"
            style="width: 100px"
            v-model="item.expected_date"
            @keydown.enter="updateNewStyleStatusTrackingView(item.id,'',item.expected_date)"
        >
        </el-input>
        <span v-else @click="update_input=item.id">
          {{ item.expected_date.slice(5).replace("-", '') }}
        </span>
      </div>
    </div>
    <div
        class="list"
        @drop="dropList($event, 4)"
        @dragover.prevent>
      <span style="color: #e1ba20">裁片完成(产前特殊工艺)&nbsp;&nbsp;{{ totalQuantity5 }}件</span>
      <div
          class="item"
          v-for="(item, j) in list5"
          :key="j"
          draggable="true"
          @dragstart="dragStart(4, j)"
          @drop="dropItem($event, 4, j)"
          @dragover.prevent>
        {{ item.order_date.slice(5).replace("-", '') }}-{{ item.code }}-{{
          item.status
        }}-
        {{ item.notes }}-
        {{ item.expected_date.slice(5).replace("-", '') }}
      </div>
    </div>
    <div
        class="list"
        @drop="dropList($event, 5)"
        @dragover.prevent>
      <span style="color: #e1ba20;">成衣水洗等工艺&nbsp;&nbsp;{{ totalQuantity6 }}件</span>
      <div
          class="item"
          v-for="(item, j) in list6"
          :key="j"
          draggable="true"
          @dragstart="dragStart(5, j)"
          @drop="dropItem($event, 5, j)"
          @dragover.prevent>
        {{ item.order_date.slice(5).replace("-", '') }}-
        {{ item.code }}-
        {{ item.status }}-
        {{ item.total_quantity }}-
        ({{ item.notes }})-
        <el-input
            v-if="update_input===item.id"
            style="width: 100px"
            v-model="item.expected_date"
            @keydown.enter="updateNewStyleStatusTrackingView(item.id,'',item.expected_date)"
        >
        </el-input>
        <span v-else @click="update_input=item.id">
          {{ item.expected_date.slice(5).replace("-", '') }}
        </span>
      </div>
    </div>


    <div class="box">
      <div class="side front"
           @drop="dropList($event, 6);isBoxOpen=false"
           @dragover.prevent="isBoxOpen=true"
           @dragleave="isBoxOpen=false">
        <div
            class="side front"
            draggable="true"
            @dragstart="dragStart(6, 7)"
            @drop="dropItem($event, 6, 7)"
            @dragover.prevent>

        </div>
      </div>
      <div class="side back"></div>
      <div class="side left"></div>
      <div class="side right"></div>
      <div class="side top">
        <div class="tl" :class="{ 'open': isBoxOpen }"></div>
        <div class="tr" :class="{ 'open': isBoxOpen }"></div>
      </div>
      <div class="side bottom"></div>
    </div>


  </div>
</template>

<script setup>
import {computed, ref, watchEffect} from "vue";
import home from "../api/home";
import {ElMessage} from "element-plus";

const list1 = ref([])
const list2 = ref([])
const list3 = ref([])
const list4 = ref([])
const list5 = ref([])
const list6 = ref([])
const list7 = ref([])

const isBoxOpen = ref(false)

const lists = ref([list1, list2, list3, list4, list5, list6, list7]);
const loading = ref(true);

const update_input = ref('')


const dragged = ref({list: null, item: null});

const dragStart = (listIndex, itemIndex) => {
  dragged.value = {
    list: listIndex,
    item: itemIndex,
    id: lists.value[listIndex].value[itemIndex].id, // assuming each item has an id field
  };
};


const dropItem = (event, listIndex, itemIndex) => {
  if (listIndex === 6) {
    return
  }
  event.stopPropagation();
  const {list: draggedList, item: draggedItem, id} = dragged.value;
  [lists.value[draggedList].value[draggedItem], lists.value[listIndex].value[itemIndex]] =
      [lists.value[listIndex].value[itemIndex], lists.value[draggedList].value[draggedItem]];
  updateNewStyleStatusTrackingView(id, listIndex + 1, '')

};

const dropList = (event, listIndex) => {
  const {list: draggedList, item: draggedItem, id} = dragged.value;
  lists.value[listIndex].value.push(lists.value[draggedList].value[draggedItem]);
  lists.value[draggedList].value.splice(draggedItem, 1);
  isBoxOpen.value = false
  updateNewStyleStatusTrackingView(id, listIndex + 1, '')

};


const getNewStyleStatusTrackingView = () => {
  home.getNewStyleStatusTrackingView().then(response => {
    list1.value = response.data.data1
    list2.value = response.data.data2
    list3.value = response.data.data3
    list4.value = response.data.data4
    list5.value = response.data.data5
    list6.value = response.data.data6
    isd()
  }).catch(err => {
    console.log(err)
  })
  loading.value = false
}
getNewStyleStatusTrackingView()


const totalQuantity = (list) => {
  if (!list.value) {
    return 0;
  }
  return list.value.reduce((total, item) => {
    return total + (typeof item.total_quantity === 'number' ? item.total_quantity : 0);
  }, 0);
};
const totalQuantity1 = computed(() => totalQuantity(list1));
const totalQuantity2 = computed(() => totalQuantity(list2));
const totalQuantity3 = computed(() => totalQuantity(list3));
const totalQuantity4 = computed(() => totalQuantity(list4));
const totalQuantity5 = computed(() => totalQuantity(list5));
const totalQuantity6 = computed(() => totalQuantity(list6));

const updateNewStyleStatusTrackingView = (id, label, expected_date) => {
  if (update_input.value) {
    update_input.value = ''
  }
  home.updateNewStyleStatusTrackingView(id, label, expected_date).then(response => {
  }).catch(err => {
    console.log(err)
  })
}
const move = () => {
  loading.value = true
  home.move().then(response => {
    getNewStyleStatusTrackingView()
    ElMessage({
      message: '移动成功',
      type: 'success',
    })
  }).catch(err => {
    getNewStyleStatusTrackingView()
    ElMessage.error('移动失败')
  })
}

// 获取那些款号重复了
const isd = () => {
  const codeCount = {}

  list1.value.forEach(item => {
    const {code} = item

    // 更新 codeCount 中对应 code 的计数
    codeCount[code] = (codeCount[code] || 0) + 1
  })

  list1.value.forEach(item => {
    const {code} = item

    // 根据 code 在 codeCount 中的计数，设置 is_d 字段
    item.is_d = codeCount[code] > 1 ? 1 : 0
  })
}


</script>


<style scoped>
.container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 20px;
  width: 100%;
  height: 100vh;
  padding: 20px;
  text-align: center;
}

.list {
  width: 90%;
  height: 90%;
  border: 1px solid #ccc;
  padding: 10px;
  overflow-y: auto;
}

.item {
  padding: 10px;
  margin: 15px 0;
  background-color: #fff4de;
  border-radius: 5px;
  color: #e1ba20;
  font-size: 12px;
}

.item2 {
  padding: 10px;
  margin: 15px 0;
  background-color: #63ffb4;
  border-radius: 5px;
  color: #e1ba20;
  font-size: 12px;
}


.box {
  display: flex;
  justify-content: center;
  align-items: center;
  /* 相对定位 */
  position: relative;
  /* 开启3D效果 */
  transform-style: preserve-3d;
  /* 设置视距 */
  perspective: 1000px;
  /* 默认沿X轴旋转-20度 */
  transform: rotateX(-20deg);
}

/* 箱子各个面的统一样式 */
.side {
  /* 绝对定位 */
  position: absolute;
  width: 200px;
  height: 200px;
  background-color: #c09551;
  border: 1px solid #e4c084;
}

/* 前 */
.front {
  transform: translateZ(100px);
}

/* 后 */
.back {
  transform: translateZ(-100px) rotateY(180deg);
}

/* 左 */
.left {
  transform: translateX(-100px) rotateY(-90deg);
}

/* 右 */
.right {
  transform: translateX(100px) rotateY(90deg);
}

/* 上 */
.top {
  transform: translateY(-100px) rotateX(90deg);
  background-color: transparent;
  transform-style: preserve-3d;
}

.top div {
  background-color: #c09551;
  position: absolute;
  top: 0;
  width: 50%;
  height: 100%;
  border: 1px solid #e4c084;
  /* 设置过渡 */
  transition: 0.5s;
}

.top .tl {
  left: 0;
  /* 设置旋转的基点位置为左边 */
  transform-origin: left;
}

.top .tr {
  right: 0;
  /* 设置旋转的基点位置为右边 */
  transform-origin: right;
}

/* 下 */
.bottom {
  transform: translateY(100px) rotateX(-90deg);
  /* 阴影 */
  box-shadow: 5px -5px 15px rgba(0, 0, 0, 0.4);
}

.box:hover .top .tl {
  transform: rotateY(-135deg);
}

.box:hover .top .tr {
  transform: rotateY(135deg);
}

.box .top .tl.open {
  transform: rotateY(-135deg);
}

.box .top .tr.open {
  transform: rotateY(135deg);
}


</style>

