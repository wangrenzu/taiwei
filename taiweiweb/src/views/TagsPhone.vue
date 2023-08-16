<template>
  <table>
    <tr>
      <th>季节标签仓</th>
      <th>生产和年份</th>
      <th>品类标签仓</th>
    </tr>
    <tr>
      <td>
        <div class="flex-container">
          <div
              v-for="(item, j) in list1"
              :key="j"
          >
            <el-tag
                class="mx-1"
                :disable-transitions="false"
                @click="updateseason(item)">
              {{ item }}
            </el-tag>
          </div>
        </div>
      </td>
      <td>
        <div class="flex-container">
          <div
              v-for="(item, j) in list2"
              :key="j">
            <el-tag class="mx-1" :disable-transitions="false" @click="pushStock(item)">
              {{ item }}
            </el-tag>
          </div>
        </div>
      </td>
      <td>
        <div class="flex-container">
          <div
              v-for="(item, j) in list3"
              :key="j">
            <el-tag class="mx-1" @click="list6.push(item.category)" :type="getType(item.code_describe)"
                    :disable-transitions="false">
              {{ item.category }}
            </el-tag>
          </div>
        </div>
      </td>
    </tr>
  </table>
  <div style="display: flex">
    <div
        style="flex:1;height:100px;border: 1px solid black">
      <el-tag
          v-for="(item,key) in list4"
          class="mx-1"
          :disable-transitions="false"
          closable
          @close="handleClose(list4,key)">
        {{ item }}
      </el-tag>
    </div>
    <div style="flex:1;height:100px;border: 1px solid black">
      <el-tag
          v-for="(item,key) in list5"
          class="mx-1"
          :disable-transitions="false"
          closable
          @close="handleClose(list5,key)">
        {{ item }}
      </el-tag>
    </div>
    <div style="flex:1;height:100px;border: 1px solid black">
      <el-tag
          v-for="(item,key) in list6"
          class="mx-1"
          :disable-transitions="false"
          closable
          @close="handleClose(list6,key)">
        {{ item }}
      </el-tag>
    </div>
    <div style="flex:1;height:100px;border: 1px solid black">
      <el-tag
          v-for="(item,key) in list7"
          class="mx-1"
          :disable-transitions="false"
          closable
          @close="handleClose(list7,key)">
        {{ item }}
      </el-tag>
    </div>


  </div>


  <el-button type="warning" @click="moveImg">入选</el-button>
  <el-button type="primary" @click="showDesign(1)">已选单品</el-button>
  <el-button type="primary" @click="showDesign(2)">已选搭配</el-button>
  <el-button type="warning" @click="getGoodsInfo([list4,list5,list6,list7])">筛选</el-button>
  <el-button v-if="route.params.name === 'yijia'" type="primary" @click="export_code(route.params.name,2)">
    易嘉组导出搭配
  </el-button>
  <el-button v-else-if="route.params.name === 'xj'" type="primary" @click="export_code(route.params.name,2)">
    小洁导出搭配
  </el-button>
  <el-button v-else-if="route.params.name === 'yy'" type="primary" @click="export_code(route.params.name,2)">
    小叶导出搭配
  </el-button>
  <el-button v-else type="primary" @click="export_code(route.params.name,2)">小何组导出导出搭配</el-button>

  <el-button v-if="route.params.name === 'yijia'" type="primary" @click="export_code(route.params.name,1)">
    易嘉组导出单品
  </el-button>
  <el-button v-else-if="route.params.name === 'xj'" type="primary" @click="export_code(route.params.name,1)">
    小洁导出单品
  </el-button>
  <el-button v-else-if="route.params.name === 'yy'" type="primary"
             @click="export_code(route.params.name,1)">小叶导出单品
  </el-button>
  <el-button v-else type="primary" @click="export_code(route.params.name,1)">小何组导出单品</el-button>

  <br>
  <el-input style="width: 180px;" v-model="search_code" placeholder="请输入要查询的款号"></el-input>
  <el-button style="margin-left: 10px" type="primary"
             @click="getGoodsInfo([list4,list5,list6,list7],search_code)">
    搜索
  </el-button>
  <span style="margin-left:10px;margin-top:10px;color: red">点图片看搭配</span>

  <div class='ab'>
    <div style="width: 170px;height: auto" v-for="(item,key) in data_list" :key="key">
      <img :src="'http://192.168.1.233/web_images/' + item.code +'.jpg'"
           alt="" style="position: relative"
           @click="openDesign(item.code)">
      <span style="position: absolute;top:0;left: 10px;font-size: 10px">
           <span v-if="codeData[item.code]" class="square">
              <p>{{ item.code + "" + codeData[item.code].category }}</p>
              <p>{{ "库存" + codeData[item.code].inventory }}</p>
              <p>{{ "抖音销量" + codeData[item.code].live_deal_item_count }}</p>
              <p>{{ "档口销量" + codeData[item.code].sales_quantity }}</p>
              <p v-if="codeData[item.code].price === '30天没卖过'||codeData[item.code].price==='null'">30天没卖过</p>
              <p v-else>{{ codeData[item.code].price }}</p>
           </span>
      </span>
      <el-checkbox v-model="item.checked" size="large"/>
    </div>

  </div>


</template>

<script setup>

import {reactive, ref, watch} from "vue";
import {tags} from "../api/tags.js";
import {design} from "../api/design.js";
import {ElMessage} from "element-plus";
import {useRoute} from "vue-router";
import Papa from 'papaparse';
import {saveAs} from 'file-saver';

const list1 = ref(["10-11月", "过年12月-1月", '6-7月', '8-9月', '4-5月', '四季', '早春2-3月', '日用品配饰', '全部']) //季节标签
const list2 = ref(['今年新款', '往年老款', '翻单款', '库存1-5件', '库存6-30件', '库存31-100件', '库存>100件'])  //生产和年份标签
const list3 = ref([]);  //品类标签
const list4 = ref([]);  //品类标签
const list5 = ref([]);  //品类标签
const list6 = ref([]);  //品类标签
const list7 = ref([]);  //品类标签

const data_list = ref([])
const route = useRoute();
const name = route.params.name
const search_code = ref()
const getType = (code_describe) => {
  if (code_describe === "上衣") {
    return "success"
  }
  if (code_describe === "配饰") {
    return ""
  }
  if (code_describe === "下衣") {
    return "info"
  }
  if (code_describe === "一身") {
    return "warning"
  }
  if (code_describe === "日用品") {
    return "danger"
  }
}

const handleClose = (list, index) => {
  list.splice(index, 1)
}


const pushStock = (item) => {
  if (item === '库存1-5件' || item === '库存6-30件' || item === '库存31-100件' || item === '库存>100件') {
    list7.value.push(item)
  } else {
    list5.value.push(item)
  }
}
const updateseason = (item) => {
  tags.season = item
  if (item !== "日用品配饰" && item !== "全部") {
    list4.value.push(item)
  }


}

const export_code = (name, type) => {
  design.exportCode(name, type).then(response => {
    const data = response.data.data; // 获取返回的文件名列表
    // 添加标题行，并将文件名列表转换为对象数组
    const csvData = [...data.map(item => ({款号: item}))];

    const csv = Papa.unparse(csvData); // 将数据转换为CSV格式
    const blob = new Blob([csv], {type: 'text/csv;charset=utf-8;'}); // 创建一个blob对象

    saveAs(blob, "table.csv"); // 使用FileSaver.js保存文件
  }).catch(err => {
    console.log(err);
  });
}
const getCategory = () => {
  tags.getCategory(tags.season).then(response => {
    list3.value = response.data.message
  }).catch(err => {
    console.log(err)
  })
}
getCategory()

const codeData = reactive({});
const getGoodsInfo = (tag_list, search_code) => {
  tags.getGoodsInfo(tag_list, search_code).then(response => {
    data_list.value = response.data.data
    let codes = response.data.data.map(item => item.code);
    const checkCode = async (code) => {
      try {
        const response = await design.checkCode(code);
        codeData[code] = response.data;
      } catch (err) {
        console.log(err);
      }
    };
    for (let code of codes) {
      checkCode(code);
    }
  }).catch(err => {
    console.log(err)
  })
}

const moveImg = () => {
  tags.moveImg(data_list.value, name).then(response => {
    ElMessage({
      message: response.data,
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error(err)
  })
}
const openDesign = (code) => {
  window.open('/design3/' + code + '/' + name, '_blank');
}

const showDesign = (type) => {
  window.open('/design4/' + type + '/' + name, '_blank');
}

watch(
    () => tags.season,
    () => {
      getCategory()
    }
)


</script>

<style scoped>
table {
  border-collapse: collapse;
  width: 100%;
  text-align: center;
  margin-bottom: 1vw;
}

table td {
  width: 100px;
}

table td:nth-child(3) {
  width: 300px;
}

table th {
  background-color: #e1ba20;
  font-size: 15px;
}

.flex-container {
  display: flex;
  flex-wrap: wrap;
}

.el-tag {
  margin: 5px;
}

* {
  margin: 0 auto;
}

table, th, td {
  border: 1px solid black;
}

.ab div {
  position: relative;
  float: left;
  /* border: 1px solid white; */
  padding: 10px 0 0 10px;
  overflow: hidden;
}

.ab div img {
  width: 170px;
  border-radius: 10px;
  vertical-align: middle;
}

.el-button {
  margin-top: 10px;
}

.el-input {
  margin-top: 10px;
}


</style>