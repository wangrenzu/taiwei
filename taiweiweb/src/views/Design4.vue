<template>

  <div class='ab'>
    <div style="width: 170px;height: auto" v-for="(design,key) in design_list" :key="key">
      <img v-if="route.params.type==='1' && route.params.name==='yijia'" :src="'http://192.168.1.233/danpin-yijia/' + key" alt="" style="position: relative">
      <img v-else-if="route.params.type==='1' && route.params.name!=='yijia'" :src="'http://192.168.1.233/danpin/' + key" alt="" style="position: relative">
      <img v-else-if="route.params.type==='2' && route.params.name==='yijia'" :src="'http://192.168.1.233/zhengtao-dapei-yijia/' + key" alt="" style="position: relative">
      <img v-else :src="'http://192.168.1.233/zhengtao-dapei/' + key" alt="" style="position: relative">


      <span style="position: absolute;top:5px;right: 10px;cursor: pointer;z-index: 1" @click="delImg(key)">x</span>
      <span style="position: absolute;top:0;left: 10px;font-size: 10px">
            <div v-for="item in design.design_data">
             <span v-if="codeData[item.code]" class="square">
                <p>{{ item.code + "" + codeData[item.code].category }}</p>
                <p>{{ "库存" + codeData[item.code].inventory }}</p>
                <p>{{ "抖音销量" + codeData[item.code].live_deal_item_count }}</p>
                <p>{{ "档口销量" + codeData[item.code].sales_quantity }}</p>
             </span>
            </div>
      </span>
    </div>
  </div>

</template>

<script setup>


import {reactive, ref} from "vue";
import {design} from "../api/design.js";
import {useRoute} from "vue-router";
import {tags} from "../api/tags.js";
import {ElMessage} from "element-plus";

const route = useRoute();
const design_list = ref()
const getDesign = () => {
  design.getDesign4(route.params.type,route.params.name).then(response => {
    design_list.value = response.data.data
    const checkCode = async (code) => {
      try {
        const response = await design.checkCode(code);
        codeData[code] = response.data;
      } catch (err) {
        console.log(err);
      }
    };
    for (let code of response.data.code_list) {
      checkCode(code);
    }

  }).catch(err => {
    console.log(err)
  })
}
getDesign()


const moveImg = () => {
  design.moveImg(design_list.value).then(response => {
    ElMessage({
      message: response.data,
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error(err)
  })
}

const codeData = reactive({});

const delImg = (name) => {
  design.delImg(name, route.params.type,route.params.name).then(response => {
    ElMessage({
      message: response.data.message,
      type: 'success',
    })
    getDesign()
  }).catch(err => {
    ElMessage.error(err)
  })
}


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