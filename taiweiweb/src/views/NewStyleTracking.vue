<template>
  <el-tag>款号重复的翻单不会移动，需要手动拖，颜色高亮的</el-tag>
  &nbsp;
  <el-button type="primary" @click="move">移动</el-button>
  <el-button type="primary" @click="compute_time">计算出货时间</el-button>
  <br/>
  <el-tag>下单时间，计划出货时间，可以改， 新款翻单后面的数字代表当前池子（后道，车间等）的实际数量，
    最后的括号里面代表实际交货日期，比如0711进后道，代表0711车间交货进后道， 深色的小块代表计算的出货日期（按照800件每天的出货量安排）
  </el-tag>
  <br>

  <div class="container" v-loading="loading">
    <div
        class="list"
        @drop="dropList($event, 0)"
        @dragover.prevent>
      <span style="color: #e1ba20">备料中&nbsp;&nbsp;{{ totalQuantity1 }}件</span>
      <div
          class="item-flex"
          v-for="(item, j) in list1"
          :key="j"
          draggable="true"
          @dragstart="dragStart(0, j)"
          @drop="dropItem($event, 0, j)"
          @dragover.prevent>
        <div :class="[ { 'item': item.is_d === 0 },{'item2': item.is_d === 1}]">
          {{ item.count }}-
          {{ item.order_date.slice(5).replace("-", '') }}-
          {{ item.code }}-
          {{ item.status }}-
          {{ item.total_quantity }}-
          {{ item.notes }}
        </div>
        <div :class="[ { 'auto-time': item.is_d === 0 },{'auto-time2': item.is_d === 1}]">
          {{ item.auto_time.slice(5).replace("-", '') }}
        </div>

      </div>
    </div>
    <div
        class="list"
        @drop="dropList($event, 1)"
        @dragover.prevent>
      <span style="color: #e1ba20">车间生产&nbsp;&nbsp;{{ totalQuantity2 }}件</span>
      <div
          class="item-flex"
          v-for="(item, j) in list2"
          :key="j"
          draggable="true"
          @dragstart="dragStart(1, j)"
          @drop="dropItem($event, 1, j)"
          @dragover.prevent>
        <div class="item">
          {{ item.count }}-
          {{ item.order_date.slice(5).replace("-", '') }}-
          {{ item.code }}-
          {{ item.status }}-
          {{ item.total_quantity }}-
          <el-input
              v-if="update_input===item.id"
              style="width: 100px"
              v-model="item.expected_date"
              @keydown.enter="updateNewStyleStatusTrackingView(item.id,'',item.expected_date,item.code,'',item.order_date)"
          >
          </el-input>
          <span v-else @click="update_input=item.id">
          {{ item.expected_date.slice(5).replace("-", '') }}-
        </span>
          ({{ item.notes }})
        </div>
        <div class="auto-time">
          {{ item.auto_time.slice(5).replace("-", '') }}
        </div>
      </div>
    </div>
    <div
        class="list"
        style="z-index: 1"
        @drop="dropList($event, 2)"
        @dragover.prevent>
      <span style="color: #e1ba20">后道&nbsp;&nbsp;{{ totalQuantity3 }}件</span>
      <div
          class="item-flex"
          v-for="(item, j) in list3"
          :key="j"
          draggable="true"
          @dragstart="dragStart(2, j)"
          @drop="dropItem($event, 2, j)"
          @dragover.prevent>
        <div class="item">
          {{ item.count }}-
          {{ item.order_date.slice(5).replace("-", '') }}-
          {{ item.code }}-
          {{ item.status }}-
          {{ item.total_quantity }}-
          <el-input
              v-if="update_input===item.id"
              style="width: 100px"
              v-model="item.expected_date"
              @keydown.enter="updateNewStyleStatusTrackingView(item.id,'',item.expected_date,item.code,'',item.order_date)"
          >
          </el-input>
          <span v-else @click="update_input=item.id">
          {{ item.expected_date.slice(5).replace("-", '') }}-
        </span>
          ({{ item.notes }})
        </div>
        <div class="auto-time">
          {{ item.auto_time.slice(5).replace("-", '') }}
        </div>
      </div>
    </div>
    <div
        class="list"
        @drop="dropList($event, 3)"
        @dragover.prevent>
      <span style="color: #e1ba20">入仓没上架&nbsp;&nbsp;{{ totalQuantity4 }}件</span>
      <div
          class="item-flex"
          v-for="(item, j) in list4"
          :key="j"
          draggable="true"
          @dragstart="dragStart(3, j)"
          @drop="dropItem($event, 3, j)"
          @dragover.prevent>
        <div class="item">
          {{ item.count }}-
          {{ item.order_date.slice(5).replace("-", '') }}-
          {{ item.code }}-
          {{ item.status }}-
          {{ item.total_quantity }}-
          ({{ item.notes }})
        </div>
      </div>
    </div>
    <div
        class="list"
        @drop="dropList($event, 4)"
        @dragover.prevent>
      <span style="color: #e1ba20">裁片完成(产前特殊工艺)&nbsp;&nbsp;{{ totalQuantity5 }}件</span>
      <div
          class="item-flex"
          v-for="(item, j) in list5"
          :key="j"
          draggable="true"
          @dragstart="dragStart(4, j)"
          @drop="dropItem($event, 4, j)"
          @dragover.prevent>
        <div class="item">
          {{ item.count }}-
          {{ item.order_date.slice(5).replace("-", '') }}-
          {{ item.code }}-
          {{ item.status }}-
          {{ item.total_quantity }}-
          <el-input
              v-if="update_input===item.id"
              style="width: 100px"
              v-model="item.expected_date"
              @keydown.enter="updateNewStyleStatusTrackingView(item.id,'',item.expected_date,item.code,'',item.order_date)"
          >
          </el-input>
          <span v-else @click="update_input=item.id">
          {{ item.expected_date.slice(5).replace("-", '') }}-
        </span>
          ({{ item.notes }})
        </div>
        <div class="auto-time">
          {{ item.auto_time.slice(5).replace("-", '') }}
        </div>
      </div>
    </div>
    <div
        class="list"
        @drop="dropList($event, 5)"
        @dragover.prevent>
      <span style="color: #e1ba20;">成衣水洗等工艺&nbsp;&nbsp;{{ totalQuantity6 }}件</span>
      <div
          class="item-flex"
          v-for="(item, j) in list6"
          :key="j"
          draggable="true"
          @dragstart="dragStart(5, j)"
          @drop="dropItem($event, 5, j)"
          @dragover.prevent>
        <div class="item">
          {{ item.count }}-
          {{ item.order_date.slice(5).replace("-", '') }}-
          {{ item.code }}-
          {{ item.status }}-
          {{ item.total_quantity }}-
          <el-input
              v-if="update_input===item.id"
              style="width: 100px"
              v-model="item.expected_date"
              @keydown.enter="updateNewStyleStatusTrackingView(item.id,'',item.expected_date,item.code,'',item.order_date)"
          >
          </el-input>
          <span v-else @click="update_input=item.id">
          {{ item.expected_date.slice(5).replace("-", '') }}-
        </span>
          ({{ item.notes }})
        </div>
        <div class="auto-time">
          {{ item.auto_time.slice(5).replace("-", '') }}
        </div>
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
          <p>回收站</p>
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


    <div
        style="height: 700px"
        class="list"
        @drop="dropList($event, 7)"
        @dragover.prevent>
      <span style="color: #e1ba20">加急,不会动,显示每个仓数量&nbsp;&nbsp;{{ totalQuantity8 }}件</span>
      <div
          class="item-flex"
          v-for="(item, j) in list8"
          :key="j"
          draggable="true"
          @dragstart="dragStart(7, j)"
          @drop="dropItem($event, 7, j)"
          @dragover.prevent>
        <div class="item">
          {{ item.count }}-
          {{ item.order_date.slice(5).replace("-", '') }}-
          {{ item.code }}-
          {{ item.status }}-
          {{ item.total_quantity }}-
          <el-input
              v-if="update_input===item.id"
              style="width: 100px"
              v-model="item.expected_date"
              @keydown.enter="updateNewStyleStatusTrackingView(item.id,'',item.expected_date,item.code,'',item.order_date)"
          >
          </el-input>
          <span v-else @click="update_input=item.id">
          {{ item.expected_date.slice(5).replace("-", '') }}-
        </span>
          ({{ item.notes }})-
          <el-input style="width: 200px"
                    type="textarea"
                    v-model="item.notes_info"
                    @blur="updateNotesInfo(item.id,item.notes_info)"
                    placeholder="备注">

          </el-input>
        </div>
        <div class="auto-time">
          {{ item.auto_time.slice(5).replace("-", '') }}
        </div>
      </div>
    </div>

  </div>
  <el-button type="primary" @click="exportExcel(list9Fields,list9)">导出</el-button>
  <el-table
      :data="list9"
      style="width: 30%;margin-bottom: 20px"
      border fit height="620">
    <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
    <el-table-column prop="label2" label="池子" show-overflow-tooltip/>
    <el-table-column prop="category" label="品类" show-overflow-tooltip/>
    <el-table-column prop="num" label="项目个数" show-overflow-tooltip/>
    <el-table-column prop="total_quantity" label="件数" show-overflow-tooltip/>

  </el-table>
  <div class="charts-container">
    <div ref="chartDom1" class="chart"></div>
    <div ref="chartDom2" class="chart"></div>
    <div ref="chartDom3" class="chart"></div>
    <div ref="chartDom6" class="chart"></div>
    <div ref="chartDom4" class="chart2"></div>
  </div>

</template>

<script setup>
import {computed, ref} from "vue";
import home from "../api/home";
import {ElMessage} from "element-plus";
import FileSaver from 'file-saver';
import * as XLSX from "xlsx";
import * as echarts from 'echarts/core';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components';
import {LineChart, ScatterChart, BarChart} from 'echarts/charts';
import {CanvasRenderer} from 'echarts/renderers';

echarts.use([
  BarChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  CanvasRenderer,
  ScatterChart
]);


const list1 = ref([])
const list2 = ref([])
const list3 = ref([])
const list4 = ref([])
const list5 = ref([])
const list6 = ref([])
const list7 = ref([])
const list8 = ref([])
const list9 = ref([])

const isBoxOpen = ref(false)

const lists = ref([list1, list2, list3, list4, list5, list6, list7, list8]);
const loading = ref(true);

const update_input = ref('')


const dragged = ref({list: null, item: null});


const list9Fields = [
  {key: 'label', label: '池子'},
  {key: 'category', label: '品类'},
  {key: 'num', label: '项目个数'},
  {key: 'total_quantity', label: '件数'},
]

const updateNotesInfo = (id, content) => {
  home.updateNotes(id, content).then(response => {
    ElMessage({
      message: '更新成功',
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error(err)
  })
}

const exportExcel = (exportFields, data_list) => {
  const sheet = XLSX.utils.json_to_sheet(data_list.map(item => {
    const row = {};
    exportFields.forEach(field => {
      row[field.label] = item[field.key];
    });
    return row;
  }));
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, sheet, 'Sheet1');
  const filename = 'table.xlsx';
  const wbout = XLSX.write(workbook, {bookType: 'xlsx', type: 'array'});
  const blob = new Blob([wbout], {type: 'application/octet-stream'});
  FileSaver.saveAs(blob, filename);
}

const dragStart = (listIndex, itemIndex) => {
  dragged.value = {
    list: listIndex,
    item: itemIndex,
    id: lists.value[listIndex].value[itemIndex].id, // assuming each item has an id field
    code: lists.value[listIndex].value[itemIndex].code,
    order_date: lists.value[listIndex].value[itemIndex].order_date,
  };
};


const dropItem = (event, listIndex, itemIndex) => {
  if (listIndex === 6) {
    return;
  }
  event.stopPropagation();
  const {list: draggedList, item: draggedItem, id, code, order_date} = dragged.value;

  // Remove item from the source list
  const item = lists.value[draggedList].value.splice(draggedItem, 1)[0];

  // Insert the item into the target list
  lists.value[listIndex].value.splice(itemIndex, 0, item);

  updateNewStyleStatusTrackingView(id, draggedList + 1, '', code, listIndex + 1, order_date)
};

const dropList = (event, listIndex) => {
  const {list: draggedList, item: draggedItem, id, code, order_date} = dragged.value;

  // Remove item from the source list
  const item = lists.value[draggedList].value.splice(draggedItem, 1)[0];

  // Add item to the end of the target list
  lists.value[listIndex].value.push(item);

  isBoxOpen.value = false;

  updateNewStyleStatusTrackingView(id, draggedList + 1, '', code, listIndex + 1, order_date)
};


const getNewStyleStatusTrackingView = () => {
  home.getNewStyleStatusTrackingView().then(response => {
    list1.value = response.data.data1
    list2.value = response.data.data2
    list3.value = response.data.data3
    list4.value = response.data.data4
    list5.value = response.data.data5
    list6.value = response.data.data6
    list8.value = response.data.data8
    list9.value = response.data.data9
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
const totalQuantity8 = computed(() => totalQuantity(list8));

const updateNewStyleStatusTrackingView = (id, start_label, expected_date, code, end_label, order_date) => {
  if (update_input.value) {
    update_input.value = ''
  }
  home.updateNewStyleStatusTrackingView(id, start_label, expected_date, code, end_label, order_date).then(response => {
    getNewStyleStatusTrackingView()
  }).catch(err => {
    console.log(err)
  })
}
// 移动池子
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
const compute_time = () => {
  loading.value = true
  home.compute_time().then(response => {
    getNewStyleStatusTrackingView()
    ElMessage({
      message: '计算成功',
      type: 'success',
    })
  }).catch(err => {
    getNewStyleStatusTrackingView()
    ElMessage.error('计算失败')
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
const chartDom1 = ref(null);
let chartInstance1 = null;
const chartDom2 = ref(null);
let chartInstance2 = null;
const chartDom3 = ref(null);
let chartInstance3 = null;
const chartDom4 = ref(null);
let chartInstance4 = null;
const chartDom5 = ref(null);
let chartInstance5 = null;
const chartDom6 = ref(null);
let chartInstance6 = null;
const getEcharts = (data, name, dom, instance) => {
  const categories = [];  // 用于 x 轴的数据
  const totals = [];      // 用于 y 轴的数据
  const tooltips = [];    // 用于保存鼠标悬停时的提示信息

  data.forEach(item => {
    for (let key in item) {
      if (key !== 'total') {
        categories.push(key);
        totals.push(item['total']);

        // 创建鼠标悬停提示信息
        let tooltipInfo = '';
        item[key].forEach(detail => {
          for (let subKey in detail) {
            tooltipInfo += `${subKey}: ${detail[subKey]}<br>`;
          }
        });
        tooltips.push(tooltipInfo);
      }
    }
  });

  instance = echarts.init(dom.value);
  const colors = ['#ff7f50', '#87cefa', '#da70d6', '#32cd32', '#6495ed', '#ff69b4', '#ba55d3', '#cd5c5c', '#ffa500', '#40e0d0'];
  const option = {
    title: {
      text: name,  // 修改为你想要的标题
      left: 'center',   // 标题居中
      top: 'top'       // 标题位于图表的顶部
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        interval: 0,  // 每隔一个刻度显示一个标签
        rotate: 45,   // 如果标签之间仍然重叠，你可以尝试旋转标签
      }
    },
    yAxis: {
      type: 'value'
    },

    tooltip: {
      trigger: 'axis',
      formatter: function (params) {
        // 将字符串拆分为各个部分
        const parts = tooltips[params[0].dataIndex].split('<br>');
        // 为每部分数据设置颜色
        const coloredParts = parts.map((part, index) => `<span style="color:${colors[index]}">${part}<br></span>`).join('    ');
        return `${params[0].name}<br/>${coloredParts}`;
      }
    },
    series: [{
      data: totals,
      type: 'bar',
      barWidth: '80%',  // 调整柱子的宽度
      barGap: '70%',    // 调整柱子之间的间距
      label: {
        show: true,           // 显示标签
        position: 'top',      // 标签位置
        color: '#000',        // 标签文字颜色
        formatter: '{c}'      // 标签内容，{c} 代表数据值
      }
    }]
  };

  instance.setOption(option);

}

const data = ref([])
const tracking_echarts = () => {
  home.tracking_echarts().then(response => {
    data.value = response.data.data
    getEcharts(data.value["车间生产"], "车间生产", chartDom1, chartInstance1)
    getEcharts(data.value["刚下单"], "刚下单", chartDom2, chartInstance2)
    getEcharts(data.value["后道"], "后道", chartDom3, chartInstance3)
    getEcharts(data.value["成品没上架"], "成品没上架", chartDom4, chartInstance4)
    getEcharts(data.value["加急"], "加急", chartDom6, chartInstance6)
  }).catch(err => {
    console.log(err)
  })
}
tracking_echarts()


</script>


<style scoped>
.container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 20px;
  width: 100%;
  height: 1100px;
  padding: 20px;
  text-align: center;
}

.list {
  width: 90%;
  height: auto;
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
  flex: 5;
}

.item2 {
  padding: 10px;
  margin: 15px 0;
  background-color: #63ffb4;
  border-radius: 5px;
  color: #e1ba20;
  font-size: 12px;
  flex: 5;
}

.item-flex {
  display: flex;

}
.charts-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}

.chart {
  width: 400px;
  height: 400px;
  margin-right: 10px;
  margin-bottom: 10px;
}

.chart2 {
  width: 1000px;
  height: 400px;
  margin-right: 10px;
  margin-bottom: 10px;
}

.auto-time {
  flex: 0.5;
  padding: 10px;
  margin: 15px 5px;
  background-color: #f1965a;
  border-radius: 5px;
  color: #172e54;
  font-size: 12px;
}

.auto-time2 {
  flex: 0.5;
  padding: 10px;
  margin: 15px 5px;
  border-radius: 5px;
  background-color: #63ffb4;
  color: #e1ba20;
  font-size: 12px;
}


.box {
  margin-top: -400px;
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

