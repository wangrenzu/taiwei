<template>
  <table>
    <tr>
      <th>季节标签仓</th>
      <th>生产和年份</th>
      <th>品类标签仓</th>
      <th>数量标签仓</th>
      <th>池子标签</th>
      <th>销售标签</th>
      <th>广告标签</th>
    </tr>
    <tr>
      <td
          @drop="dropList($event, 1,0)"
          @dragover.prevent>
        <div class="flex-container">
          <div
              v-for="(item, j) in list1"
              :key="j"
              draggable="true"
              @dragstart="dragStart(1, j,0)"
              @dragover.prevent>
            <el-tag
                class="mx-1"
                :disable-transitions="false"
                @click="updateseason(item)">
              {{ item }}
            </el-tag>
          </div>
        </div>
      </td>
      <td
          @drop="dropList($event, 2,0)"
          @dragover.prevent>
        <div class="flex-container">
          <div
              v-for="(item, j) in list2"
              :key="j"
              draggable="true"
              @dragstart="dragStart(2, j,0)"
              @dragover.prevent>
            <el-tag class="mx-1" :disable-transitions="false">
              {{ item }}
            </el-tag>
          </div>
        </div>
      </td>
      <td
          @drop="dropList($event, 3,0)"
          @dragover.prevent>
        <div class="flex-container">
          <div
              v-for="(item, j) in list3"
              :key="j"
              draggable="true"
              @dragstart="dragStart(3, j,0)"
              @dragover.prevent>
            <el-tag class="mx-1" :type="getType(item.code_describe)" :disable-transitions="false">
              {{ item.category }}
            </el-tag>
          </div>
        </div>
      </td>
      <td
          @drop="dropList($event, 4,0)"
          @dragover.prevent>
        <div class="flex-container">
          <div
              v-for="(item, j) in list4"
              :key="j"
              draggable="true"
              @dragstart="dragStart(4, j,0)"
              @dragover.prevent>
            <el-input
                v-if="showInput===j"
                style="width: 100px"
                v-model="list4[j]"
                @keydown.enter="showInput=''"
                @blur="showInput=''">
            </el-input>
            <el-tag v-else class="mx-1" :disable-transitions="false" @click="showInput=j">
              {{ item }}
            </el-tag>

          </div>
        </div>
      </td>
      <td
          @drop="dropList($event, 5,0)"
          @dragover.prevent>
        <div class="flex-container">
          <div
              v-for="(item, j) in list5"
              :key="j"
              draggable="true"
              @dragstart="dragStart(5, j,0)"
              @dragover.prevent>
            <el-tag class="mx-1" :disable-transitions="false">
              {{ item }}
            </el-tag>
          </div>
        </div>
      </td>
      <td
          @drop="dropList($event, 6,0)"
          @dragover.prevent>
        <div class="flex-container">
          <div
              v-for="(item, j) in list6"
              :key="j"
              draggable="true"
              @dragstart="dragStart(6, j,0)"
              @dragover.prevent>
            <el-tag class="mx-1" :disable-transitions="false">
              {{ item }}
            </el-tag>
          </div>
        </div>
      </td>
      <td
          @drop="dropList($event, 7,0)"
          @dragover.prevent>
        <div class="flex-container">
          <div
              v-for="(item, j) in list7"
              :key="j"
              draggable="true"
              @dragstart="dragStart(7, j,0)"
              @dragover.prevent>
            <el-tag class="mx-1" :disable-transitions="false">
              {{ item }}
            </el-tag>
          </div>
        </div>
      </td>
    </tr>
  </table>
  <div class="tags-content-div">
    <div class="tags-content" v-for="(i,key) in [list8,list9]" :key="key">
      <div class="tags-content-left">
        <template
            v-for="(item_list, index) in i"
            :key="index">
          <div
              class="tags-content-left-1"
              @drop="dropList($event, key+8,index)"
              @dragover.prevent>
            <div
                v-for="(item, j) in item_list"
                :key="j"
                v-if="item_list.length>0"
                draggable="true"
                @dragstart="dragStart(key+8, j,index)"
                @dragover.prevent>
              <el-tag
                  class="mx-1"
                  :disable-transitions="false"
                  closable
                  @close="handleClose(i,index,j)">
                {{ item }}
              </el-tag>
            </div>
            <div v-else></div>
            <div class="add-div" v-if="index === i.length - 1">
              <el-icon @click="addTagsDiv(i)"><a href="#">
                <Plus/>
              </a></el-icon>
            </div>
          </div>
          <p class="tags-content-left-p" v-if="index !== i.length - 1">并且</p>

        </template>
        <div class="tags-content-content">
          <el-button type="primary" @click="getGoodsInfo(i,key)">搜索</el-button>
        </div>
      </div>


      <div class="tags-content-right">
        <div class="slider-demo-block">
          <el-slider v-model="tags.nums[key]" :max="tags.goods_info[key].length" show-input/>
        </div>
        <el-table
            v-loading="tags.loadings[key]"
            :data="tags.new_goods_info[key]"
            style="width: 100%" border fit height="620"
        >
          <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
          <el-table-column prop="code" label="款号" show-overflow-tooltip></el-table-column>
          <el-table-column prop="category" label="品类" show-overflow-tooltip></el-table-column>
          <el-table-column label="图片" width="120" show-overflow-tooltip>
            <template #default="scope">
              <el-image style="width: 60px; height: 70px"
                        :src="'http://192.168.1.233/web_images/' + scope.row.code + '.jpg'">
              </el-image>

            </template>
          </el-table-column>
          <el-table-column prop="inventory" label="库存" sortable show-overflow-tooltip></el-table-column>
          <el-table-column fixed="right" label="购物车">
            <template #default="scope">
              <el-button
                  link
                  type="primary"
                  size="small"
                  @click.prevent="addCart(scope.row.code,'S姐购物车','标签库')"
              >
                加入购物车
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>

import {reactive, ref, watch} from "vue";
import {Plus} from '@element-plus/icons-vue'
import {tags} from "../api/tags.js";
import cart from "../api/cart.js";
import {ElMessage} from "element-plus";

const list1 = ref(["10-11月", "过年12月-1月", '6-7月', '8-9月', '4-5月', '四季', '早春2-3月', '日用品配饰', '全部']) //季节标签
const list2 = ref(['今年新款', '往年老款', '翻单款'])  //生产和年份标签
const list3 = ref([]);  //品类标签
const list4 = ref(["库存?-?件", "库存>?件", "库存<?件"])     //数量标签
const list5 = ref(['在车间', '在后道', '入仓没上架'])  //池子标签
const list6 = ref(['抖音没卖过', '30天没卖过', "7天没卖过", "有效款"])    //销售标签
const list7 = ref([])    //广告标签
const list8 = ref([[], [], []])
const list9 = ref([[], [], []])
const list10 = ref([[], [], []])
const showInput = ref("")


const lists = ref([[], list1, list2, list3, list4, list5, list6, list7, list8, list9, list10])

const dragged = ref({list: null, item: null});

const dragStart = (listIndex, itemIndex, index) => {
  //listIndex:所在的列表     index第几个2维数组 itemIndex:列表的第几个元素
  if (listIndex >= 8) {
    dragged.value = {
      list: listIndex,        //列表
      item: index,            //开始移动的二维列表索引
      itemIndex: itemIndex,
      tag: lists.value[listIndex].value[index][itemIndex]
    }
  } else if (listIndex === 3) {
    dragged.value = {
      list: listIndex,
      item: itemIndex,     //元素索引
      itemIndex: itemIndex,
      tag: lists.value[listIndex].value[itemIndex].category
    }
  } else {
    dragged.value = {
      list: listIndex,
      item: itemIndex,     //元素索引
      itemIndex: itemIndex,
      tag: lists.value[listIndex].value[itemIndex]
    }
  }
}
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


const updateseason = (item) => {
  tags.season = item
}

const addCart = (code, name, source) => {
  /**
   * 添加商品到购物车
   * @param {string} code - 款号
   * @param {string} name - 购物车名字
   * @param {string} source - 来源，从哪个地方加入的购物车
   */
  cart.addCart(code, name, source).then(response => {
    ElMessage({
      message: "添加成功",
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error("添加失败")
  })
}
//当一个元素被拖动到列表的某个区域并释放时
const dropList = (event, listIndex, index) => {
  //draggedList:哪里开始移动   listIndex：移动到哪里   draggedItem：移动的元素二维数组索引
  //itemIndex：移动元素的索引
  const {list: draggedList, itemIndex: itemIndex, item: draggedItem, tag} = dragged.value;
  if (listIndex >= 8) {
    lists.value[listIndex].value[index].push(tag)
  }
  // 如果不是从上面的标签列表移动出来移动出来的就进行下面的操作
  if (draggedList >= 8) {
    lists.value[draggedList].value[draggedItem].splice(itemIndex, 1)
  }
};

const getCategory = () => {
  tags.getCategory(tags.season).then(response => {
    list3.value = response.data.message
  }).catch(err => {
    console.log(err)
  })
}
getCategory()

const addTagsDiv = (list) => {
  list.push([])
}
const handleClose = (list, index1, index2) => {
  list[index1].splice(index2, 1)

}

const getGoodsInfo = (tag_list, key) => {
  tags.loadings[key] = true
  tags.getGoodsInfo(tag_list).then(response => {
    tags.goods_info[key] = response.data.data
    tags.new_goods_info[key] = tags.goods_info[key].slice(0, tags.nums[0]);
    tags.nums[key] = response.data.data.length
    tags.loadings[key] = false
  }).catch(err => {
    tags.loadings[key] = false
    console.log(err)
  })
}

watch(
    () => tags.season,
    () => {
      getCategory()
    }
)
watch(
    () => tags.nums[0],
    () => {
      tags.new_goods_info[0] = tags.goods_info[0].slice(0, tags.nums[0]);
    }
)
watch(
    () => tags.nums[1],
    () => {
      tags.new_goods_info[1] = tags.goods_info[1].slice(1, tags.nums[1]);
    }
)
watch(
    () => tags.nums[2],
    () => {
      tags.new_goods_info[2] = tags.goods_info[2].slice(2, tags.nums[2]);
    }
)


</script>

<style scoped>
table {
  border-collapse: collapse;
  width: 90%;
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

.tags-content-div {
  display: flex;
}

.tags-content {
  flex: 1;
  flex-direction: column;
  display: flex;

}

.tags-content-left {
  display: flex;
  flex: 1;
  width: 85%;
}

.tags-content-left-1 {
  flex: 1;
  display: flex;
  border: 1px solid black;
  flex-wrap: wrap;
  min-height: 100px;
}

.tags-content-left-p {
  display: flex;
  flex-direction: column;
  justify-content: center; /* 上下居中 */
  margin: 0 1vw;
}


.add-div {
  display: flex;
  width: 1.5vw;
  justify-content: center; /* 左右居中 */
  align-items: center; /* 上下居中 */
  border-left: 1px solid black;
  flex-wrap: wrap;
  margin: 0;
}

.slider-demo-block {
  display: flex;
  align-items: center;
}

.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}

.tags-content-content {
  display: flex;
  justify-content: center; /* 左右居中 */
  align-items: center; /* 上下居中 */
  margin-left: 1vw;
}

.tags-content-right {
  width: 90%;
}


</style>