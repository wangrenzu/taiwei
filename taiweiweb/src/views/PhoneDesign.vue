<template>
  <el-select style="width:150px;" v-model="name" class="m-2" placeholder="Select" size="large">
    <el-option
        v-for="(item,key) in designer_list"
        :key="key"
        :label="item"
        :value="item"
    />
  </el-select>

  <el-select v-model="time_count" style="width:100px;" class="m-2" placeholder="Select" size="large">
    <el-option
        v-for="(item,key) in month_list"
        :key="key"
        :label="item.key"
        :value="item.value"
    />
  </el-select>
  <br>
  <el-input style="width: 150px;margin-top: 5px;margin-left: 150px" v-model="search_code" clearable placeholder="请输入款号"></el-input>
  <el-button style="margin-left: 10px;margin-top: 5px" type="primary" @click="get_search_code">搜索</el-button>


  <div class='ab'>
    <div style="width: 170px;height: auto" v-for="(code,key) in code_list" :key="key">
      <img
          v-if="codeData[code] && codeData[code].category === undefined"
          :src="'http://192.168.1.233/web_images/2.png'"
          @click="getCodeInfo(code)"
          style="position: relative">
      <img
          v-else
          :src="'http://192.168.1.233/web_images/' + code+ '.jpg'"
          @click="getCodeInfo(code)"
          @error="setDefaultImage"
          style="position: relative">


      <span style="position: absolute;top:0;left: 10px;font-size: 10px">
             <span v-if="codeData[code]" class="square">
                <p>{{ code + "" + codeData[code].category }}</p>
                <p>{{ "库存" + codeData[code].inventory }}</p>
                <p>{{ "抖音销量" + codeData[code].live_deal_item_count }}</p>
                <p>{{ "档口销量" + codeData[code].sales_quantity }}</p>
             </span>
      </span>
    </div>
  </div>

</template>

<script setup>


import {reactive, ref, watch} from "vue";
import {design} from "../api/design.js";
import {useRoute} from "vue-router";

const route = useRoute();
const setDefaultImage = (event) => {
  event.target.src = 'http://192.168.1.233/web_images/1.png';
}

const codeData = reactive({});

const name = ref(route.params.name)
const search_code = ref('')
const designer_list = ref([])
const get_designer = () => {
  design.getDesigner().then(response => {
    designer_list.value = response.data.message
  }).catch(err => {
    console.log(err)
  })
}
get_designer()
const code_list = ref([])
const time_count = ref(7)
const getDesignerCode = () => {
  design.getDesignerCode(name.value, time_count.value).then(response => {
    code_list.value = response.data.message

    const checkCode = async (code) => {
      try {
        const response = await design.checkCode(code);
        codeData[code] = response.data;
      } catch (err) {
        console.log(err);
      }
    };
    for (let code of code_list.value) {
      checkCode(code);
    }
  }).catch(err => {
    console.log(err)
  })
}
const postDesignerCode = () => {
  design.postDesignerCode(name.value, time_count.value).then(response => {
  }).catch(err => {
    console.log(err)
  })
}
postDesignerCode()
getDesignerCode()

const month_list = [
  {key: "加急", value: "加急"},
  {key: "1月", value: 1},
  {key: "2月", value: 2},
  {key: "3月", value: 3},
  {key: "4月", value: 4},
  {key: "5月", value: 5},
  {key: "6月", value: 6},
  {key: "7月", value: 7},
  {key: "8月", value: 8},
  {key: "9月", value: 9},
  {key: "10月", value: 10},
  {key: "11月", value: 11},
  {key: "12月", value: 12},
]

const getCodeInfo = (code) => {
  window.open('/phonedesign/info/' + code, '_blank');
}

const get_search_code = () => {
  design.getSearchCode(search_code.value).then(response => {
    code_list.value = response.data.message
    const checkCode = async (code) => {
      try {
        const response = await design.checkCode(code);
        codeData[code] = response.data;
      } catch (err) {
        console.log(err);
      }
    };
    for (let code of code_list.value) {
      checkCode(code);
    }
  }).catch(err => {
    console.log(err)
  })
}

watch(
    () => [name.value, time_count.value],
    () => {
      postDesignerCode()
      getDesignerCode()
    }
)


</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: content-box;
}

.content {
  display: flex;
  margin: 0 auto;
  width: 99vw;
  height: 99vh;
  overflow: hidden;
}

.left {
  flex: 5;
  height: 100vh;
  margin-right: 1vh;
  overflow: auto;
}


/*  */
.ab {
  width: 100%;
  height: auto;
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


</style>