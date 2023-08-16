<template>
  <el-image style="width: 90px; height: 100px" :src="img"></el-image>
  <br>
  <span>款号：{{ code }}</span>
  <br>
  <span>商品序号：{{ id }}</span>
  <br>
  <span>已下单：{{ number }}</span>
  <div ref="chartDom2" style="width: 400px; height: 400px;"></div>
  <div ref="chartDom3" style="width: 400px; height: 400px;"></div>
  <div ref="chartDom4" style="width: 400px; height: 400px;"></div>
</template>

<script setup>
import {ref, onMounted, onUnmounted} from 'vue';
import * as echarts from 'echarts/core';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components';
import {LineChart, ScatterChart} from 'echarts/charts';
import {CanvasRenderer} from 'echarts/renderers';

import room from "../api/room.js";
import {useCounterStore} from "../stores/store.js";

echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  CanvasRenderer,
  ScatterChart
]);


// const chartDom = ref(null);
// let chartInstance = null;
// const list1 = ref([])
//
//
// const getEcharts1 = () => {
//   room.getEcharts1("S姐直播间", "2023-07-28").then(response => {
//     response.data.list1.forEach(item => {
//       list1.value.push(
//           {
//             "name": Object.keys(item)[0], // 设置第一条折线图的名称
//             "data": Object.values(item)[0],
//             "type": 'line',
//             "smooth": true,
//             "symbol": 'none',
//             // 给第一条折线图的每个数据点添加数值标签
//             "label": {
//               show: false,
//               position: 'top',
//               color: 'black'
//             }
//           },
//       )
//
//     })
//     chartInstance = echarts.init(chartDom.value);
//     chartInstance.setOption({
//       title: {
//         text: '进入直播间-广告流速'
//       },
//
//       xAxis: {
//         type: 'category',
//       },
//       yAxis: {
//         type: 'value'
//       },
//       series: list1.value,
//       tooltip: {
//         trigger: 'axis', // 设置 tooltip 的触发方式为 'axis'，即鼠标悬停在折线上时触发
//         axisPointer: {
//           type: 'line' // 设置 axisPointer 的类型为 'line'，即显示垂直于折线的线条
//         }
//       }
//     });
//
//   }).catch(err => {
//     console.log(err)
//   })
// }
// getEcharts1()
const code = ref()
const img = ref()
const id = ref()
const number = ref()
const getCode = () => {
  room.get_code().then(response => {
    code.value = response.data.data.code
    img.value = response.data.data.img
    id.value = response.data.data.id
    number.value = response.data.data.number
    getEcharts3()
    getEcharts4()
  }).catch(err => {
    console.log(err)
  })
}
getCode()

const chartDom2 = ref(null);
let chartInstance2 = null;
const list2 = ref([])


const getEcharts2 = () => {
  room.getEcharts2("S姐直播间",).then(response => {
    response.data.list1.forEach(item => {
      list2.value.push(
          {
            "name": Object.keys(item)[0], // 设置第一条折线图的名称
            "data": Object.values(item)[0],
            "type": 'line',
            "smooth": true,
            "symbol": 'none',
            "lineStyle": {
              "width": 1,  // 这里设置线条宽度，值越大线条越粗
              "color": Object.keys(item)[0].includes(code.value) ? 'red' : 'grey'
            },
            // 给第一条折线图的每个数据点添加数值标签
            "label": {
              show: false,
              position: 'top',
              color: 'black'
            }
          },
      )

    })
    chartInstance2 = echarts.init(chartDom2.value);
    chartInstance2.setOption({
      title: {
        text: '进入直播间-自然流速'
      },

      xAxis: {
        type: 'category',
      },
      yAxis: {
        type: 'value'
      },
      series: list2.value,
      tooltip: {
        trigger: 'axis', // 设置 tooltip 的触发方式为 'axis'，即鼠标悬停在折线上时触发
        axisPointer: {
          type: 'line' // 设置 axisPointer 的类型为 'line'，即显示垂直于折线的线条
        }
      }
    });

  }).catch(err => {
    console.log(err)
  })
}
getEcharts2()


const chartDom3 = ref(null);
let chartInstance3 = null;
const list3 = ref([])


const getEcharts3 = () => {
  room.getEcharts3("S姐直播间", code.value).then(response => {
    response.data.list1.forEach(item => {
      list3.value.push(
          {
            "name": Object.keys(item)[0], // 设置第一条折线图的名称
            "data": Object.values(item)[0],
            "type": 'line',
            "smooth": true,
            "symbol": 'none',
            // 给第一条折线图的每个数据点添加数值标签
            "label": {
              show: false,
              position: 'top',
              color: 'black'
            }
          },
      )

    })


    response.data.list2.forEach(item => {
      list3.value.push(
          {
            "name": Object.keys(item)[0],
            "data": Object.values(item)[0],
            "type": 'scatter', // Change line to scatter
            "symbolSize": function (data) {
              return data > 0 ? 5 : 0; // Show point if value is more than 0
            },
            "label": {
              show: false,
              position: 'top',
              color: 'red'
            },
            "tooltip": {
              "show": true
            },
            "itemStyle": { // Add this to customize the color
              "color": 'red' // Replace 'blue' with the desired color
            }
          },
      )
    })


    chartInstance3 = echarts.init(chartDom3.value);
    chartInstance3.setOption({
      title: {
        text: '曝光进入率'
      },

      xAxis: {
        type: 'category',
      },
      yAxis: {
        type: 'value'
      },
      series: list3.value,
      tooltip: {
        trigger: 'axis', // 设置 tooltip 的触发方式为 'axis'，即鼠标悬停在折线上时触发
        axisPointer: {
          type: 'line' // 设置 axisPointer 的类型为 'line'，即显示垂直于折线的线条
        }
      }
    });

  }).catch(err => {
    console.log(err)
  })
}


const chartDom4 = ref(null);
let chartInstance4 = null;
const list4 = ref([])

const length = ref()
const getEcharts4 = () => {
  room.getEcharts4("S姐直播间", code.value).then(response => {
    response.data.list1.forEach(item => {
      length.value = Object.values(item)[0].length
      list4.value.push(
          {
            "name": Object.keys(item)[0], // 设置第一条折线图的名称
            "data": Object.values(item)[0],
            "type": 'line',
            "smooth": true,
            "symbol": 'none',
            // 给第一条折线图的每个数据点添加数值标签
            "label": {
              show: false,
              position: 'top',
              color: 'black',
            }
          },
      )

    })
    response.data.list2.forEach(item => {
      list4.value.push(
          {
            "name": Object.keys(item)[0],
            "data": Object.values(item)[0],
            "type": 'scatter', // Change line to scatter
            "symbolSize": function (data) {
              return data > 0 ? 5 : 0; // Show point if value is more than 0
            },
            "label": {
              show: false,
              position: 'top',
              color: 'red'
            },
            "tooltip": {
              "show": true
            },
            "itemStyle": { // Add this to customize the color
              "color": 'red' // Replace 'blue' with the desired color
            }
          },
      )
    })


    list4.value.push({
          "name": '', // 设置第一条折线图的名称
          "data": Array.from({length: length.value}, () => 0.25),
          "type": 'line',
          "smooth": true,
          "symbol": 'none',
          // 给第一条折线图的每个数据点添加数值标签
          "lineStyle": {
            "type": "dashed",
            "color": "grey"
          },
          "tooltip": {
            "show": false
          }
        },
        {
          "name": '', // 设置第一条折线图的名称
          "data": Array.from({length: length.value}, () => 0.3),
          "type": 'line',
          "smooth": true,
          "symbol": 'none',
          // 给第一条折线图的每个数据点添加数值标签

          "lineStyle": {
            "type": "dashed",
            "color": "grey"
          },
          "tooltip": {
            "show": false
          }
        },
    )

    chartInstance4 = echarts.init(chartDom4.value);
    chartInstance4.setOption({
      title: {
        text: '曝光点击率'
      },
      xAxis: {
        type: 'category',
      },
      yAxis: {
        type: 'value',
      },
      series: list4.value,
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'line'
        }
      }
    });


  }).catch(err => {
    console.log(err)
  })
}

</script>

<style>
</style>
