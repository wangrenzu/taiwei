<template>
  <div class="demo-date-picker">
    <div class="block">
      <el-date-picker
          v-model="home.search_date"
          type="daterange"
          range-separator="To"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          size="small"
      />
      <el-select v-model="home.order_status" clearable placeholder="Select" size="small"
                 @clear="home.order_status='请选择订单状态'">
        <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
        />
      </el-select>
      <el-button type="primary" :icon="Search" @click="search">Search</el-button>
      <el-button type="primary" @click="showSummary">显示条件汇总数据</el-button>
    </div>
  </div>


</template>

<script setup>
import {ref, reactive, h} from "vue";
import {Search} from "@element-plus/icons-vue";
import home from "../api/home.js";
import {ElMessage} from "element-plus";


// 搜索
const search = () => {
  home.size = 10
  // 根据用户选择搜索还是汇总展示对应的表格
  home.is_show_table = true
  home.is_show_search3_table = false
  home.is_show_search4_table = false
  home.is_show_search5_table = false
  home.is_show_search6_table = false
  home.is_show_report_table = false
  home.is_show_search7_table = false
  home.is_show_search8_table = false
  home.is_show_search9_table = false
  // 获取用户输入的内容进行搜索
  if (home.search_date !== null) {
    const dateArr = [new Date(home.search_date[0]), new Date(home.search_date[1])];
    const formattedArr = dateArr.map(date => {
      const year = date.getFullYear();
      const month = date.getMonth() + 1;
      const day = date.getDate();
      return `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
    });
    home.search_date = formattedArr
  }
  // 发送请求
  home.search().then(response => {
    console.log(response)
    home.data_list = response.data.results
    home.count = response.data.count
  }).catch(error => {
    console.log(error)
  })
}

const options = [
  // 搜索条件
  {
    value: '千川订单',
    label: '千川订单',
  },
  {
    value: '客户信息排名',
    label: '客户信息排名',
  },
    {
    value: '款号信息排名',
    label: '款号信息排名',
  },
    {
    value: '老款大于5,30天没播',
    label: '选款:库存大于5, 30天没销量',
  },
    {
    value: '热销款',
    label: '选款:档口热销款',
  },
    {
    value: '滞销款',
    label: '选款:档口滞销款',
  },
    {
    value: '最近几天热卖',
    label: '选款:最近几天热卖',
  },
    {
    value: '库存1-5',
    label: '选款:库存1-5',
  },
    {
    value: '选款:30天全量表汇总',
    label: '选款:30天全量表汇总',
  },
    {
    value: '选款:爆款',
    label: '选款:爆款',
  },
]


const showSummary = () => {
  home.loading = true
  home.size = 10
  if (home.order_status === "请选择订单状态") {
    ElMessage("请选择订单状态")
  } else {
    if (home.search_date !== null) {
      const dateArr = [new Date(home.search_date[0]), new Date(home.search_date[1])];
      const formattedArr = dateArr.map(date => {
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        return `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
      });
      home.search_date = formattedArr
    }
    if (home.order_status === "千川订单") {
      home.is_show_table = false
      home.is_show_search3_table = true
      home.is_show_search4_table = false
      home.is_show_search5_table = false
      home.is_show_search6_table = false
      home.is_show_search7_table = false
      home.is_show_search8_table = false
      home.is_show_search9_table = false
      home.is_show_search10_table = false
      home.is_show_search11_table = false
      home.is_show_search12_table = false
      home.is_show_report_table = false
    }
    if (home.order_status === "客户信息排名") {
      home.is_show_table = false
      home.is_show_search3_table = false
      home.is_show_search4_table = true
      home.is_show_search5_table = false
      home.is_show_search6_table = false
      home.is_show_search7_table = false
      home.is_show_search8_table = false
      home.is_show_search9_table = false
      home.is_show_search10_table = false
      home.is_show_search11_table = false
      home.is_show_search12_table = false
      home.is_show_report_table = false
    }
    if (home.order_status === "款号信息排名") {
      home.is_show_table = false
      home.is_show_search3_table = false
      home.is_show_search4_table = false
      home.is_show_search5_table = true
      home.is_show_search6_table = false
      home.is_show_search7_table = false
      home.is_show_search8_table = false
      home.is_show_search9_table = false
      home.is_show_search10_table = false
      home.is_show_search11_table = false
      home.is_show_search12_table = false
      home.is_show_summary = false
      home.is_show_report_table = false
    }
    if (home.order_status === "老款大于5,30天没播") {
      home.is_show_table = false
      home.is_show_search3_table = false
      home.is_show_search4_table = false
      home.is_show_search5_table = false
      home.is_show_search6_table = true
      home.is_show_search7_table = false
      home.is_show_search8_table = false
      home.is_show_search9_table = false
      home.is_show_search10_table = false
      home.is_show_search11_table = false
      home.is_show_search12_table = false
      home.is_show_report_table = false
    }
    if (home.order_status === "热销款") {
      home.is_show_table = false
      home.is_show_search3_table = false
      home.is_show_search4_table = false
      home.is_show_search5_table = false
      home.is_show_search6_table = false
      home.is_show_search7_table = true
      home.is_show_search8_table = false
      home.is_show_search9_table = false
      home.is_show_search10_table = false
      home.is_show_search11_table = false
      home.is_show_search12_table = false
      home.is_show_report_table = false
    }
    if (home.order_status === "滞销款") {
      home.is_show_table = false
      home.is_show_search3_table = false
      home.is_show_search4_table = false
      home.is_show_search5_table = false
      home.is_show_search6_table = false
      home.is_show_search7_table = false
      home.is_show_search8_table = true
      home.is_show_search9_table = false
      home.is_show_search10_table = false
      home.is_show_search11_table = false
      home.is_show_search12_table = false
      home.is_show_report_table = false
    }
    if (home.order_status === "最近几天热卖") {
      home.is_show_table = false
      home.is_show_search3_table = false
      home.is_show_search4_table = false
      home.is_show_search5_table = false
      home.is_show_search6_table = false
      home.is_show_search7_table = false
      home.is_show_search8_table = false
      home.is_show_search9_table = true
      home.is_show_search10_table = false
      home.is_show_search11_table = false
      home.is_show_search12_table = false
      home.is_show_report_table = false
    }
    if (home.order_status === "库存1-5") {
      home.is_show_table = false
      home.is_show_search3_table = false
      home.is_show_search4_table = false
      home.is_show_search5_table = false
      home.is_show_search6_table = false
      home.is_show_search7_table = false
      home.is_show_search8_table = false
      home.is_show_search9_table = false
      home.is_show_search10_table = true
      home.is_show_search11_table = false
      home.is_show_search12_table = false
      home.is_show_report_table = false
    }
    if (home.order_status === "选款:30天全量表汇总") {
      home.is_show_table = false
      home.is_show_search3_table = false
      home.is_show_search4_table = false
      home.is_show_search5_table = false
      home.is_show_search6_table = false
      home.is_show_search7_table = false
      home.is_show_search8_table = false
      home.is_show_search9_table = false
      home.is_show_search10_table = false
      home.is_show_search11_table = true
      home.is_show_search12_table = false
      home.is_show_report_table = false
    }
    if (home.order_status === "选款:爆款") {
      home.is_show_table = false
      home.is_show_search3_table = false
      home.is_show_search4_table = false
      home.is_show_search5_table = false
      home.is_show_search6_table = false
      home.is_show_search7_table = false
      home.is_show_search8_table = false
      home.is_show_search9_table = false
      home.is_show_search10_table = false
      home.is_show_search11_table = false
      home.is_show_search12_table = true
      home.is_show_report_table = false
    }
    home.summary().then(response => {
      home.count = response.data.count
      home.user_data_list = response.data.results
      home.nwe_user_data_list = response.data.results
      home.loading = false
    }).catch(err => {
      console.log(err)
    })


  }

}

</script>

<style scoped>


</style>