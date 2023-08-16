<template>
  <img style="width: 350px;height: 400px" :src="'http://192.168.1.233/web_images/' + code+ '.jpg'">
  <el-input
      type="textarea" v-model="notes"
      placeholder="讲讲你的灵感来源////
讲讲你觉得可能的卖点，有可能是细节，有可能是颜色，总之是能打动客户的点////
版型方面，是不是可以讲讲////
面料和辅料，如果有特别之处，一定记得说一下"
      @blur="updateTagNotes()">
  </el-input>
</template>

<script setup>


import {design} from "../api/design.js";
import {useRoute} from "vue-router";
import {ref} from "vue";
import {ElMessage} from "element-plus";


const route = useRoute();
const code = route.params.code
const tag_id = ref()
const notes = ref('')
const getCodeInfo = () => {
  design.getCodeInfo(code).then(response => {
    notes.value = response.data.message.notes
    tag_id.value = response.data.message.tag_id


  }).catch(err => {
    console.log(err)
  })
}
getCodeInfo()




const updateTagNotes = () => {
  design.updateNotes(tag_id.value, notes.value).then(response => {
    ElMessage({
      message: response.data.message,
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error(err)
  })
}


</script>

<style>
* {
  margin: 0 auto;
}

.el-textarea__inner {
  width: 350px;
  height: 200px;
}

</style>