<template>
  <div class='content'>
    <div class='left'>
      <div class='left-head'>
        <span>序号</span>
        <span>款号</span>
        <span>货品名</span>
        <span>设计师</span>
        <span>季节</span>
        <span>规格数量</span>
      </div>
      <div v-if="commodities" class='commodity' v-for="(commodity,key) in commodities" :key=key>
        <div class="goodsIntro" @click="getTags(key,commodity.id);design_code=commodity.code"
             :class='{goodsIntroActive:showTags === key}'>
          <span>{{ key + 1 }}</span>
          <span>{{ commodity.code }}</span>
          <span>{{ commodity.name }}</span>
          <span>{{ commodity.designer }}</span>
          <span>{{ commodity.material }}</span>
          <span>
            <p v-for="i in commodity.specification_quantity.split(' ')">
              {{ i }}
            </p></span>
        </div>
        <div class="goodsLabels" v-if="showTags===key">
          <span class="tags" v-for="(item,tagKey) in tagList" :key="tagKey">
            <span class="tag-text" @click="delTag(item.id,tagKey)">-</span>
            <span class="del-tag" @click='tagContent(item.tags,item.id)'>{{ item.tags }}</span>
          </span>


          <span class="add-tag" @click="addTagInput=key">
            <el-input
                v-if="addTagInput===key"
                style="width: 100px"
                v-model="addTagName"
                @blur="addTags(addTagName,commodity.id)"
                @keydown.enter="addTags(addTagName,commodity.id)">
            </el-input>
            <span v-else>+</span>
          </span>

        </div>
      </div>

    </div>
    <!-- 这是描述 -->
    <div class='middle'>
      <div :style="{display: contentChangeStyle}">
        <div class='conts' v-for='(item,key) in contents' :key='key'>
						<span class='conts-left'>
							<button class='remove' @click="delScript(item.id)">-</button>
							<textarea
                  v-model="item.original"
                  @blur="updateScript(item.id,item.original,item.gpt_original)">
              </textarea>
						</span>
          <el-icon>
            <Tools/>
          </el-icon>
          <span class='conts-middle'>
            <el-icon size="30" @click="reply(item.original,key)"><Setting/></el-icon>
          </span>
          <span class='conts-right'>
							<textarea
                  v-model="item.gpt_original"
                  @blur="updateScript(item.id,item.original,item.gpt_original)">
              </textarea>
						</span>
        </div>
        <button class='push' @click="addScript()">+</button>
      </div>
      <!-- 这是搭配 -->
      <div class='ab' :style="{display: mixChangeStyle}">
        <div class='pairing'>
          <div class='pairingHead'>搭配信息</div>
          <div class="pairingList" v-for="(item,key) in pairingList" :key="key">
            <div class="pairing-item" v-for="(code, j) in item.codes.split(',')">
                <span class="tips_success">
                    {{ codeStatus[item.id] && codeStatus[item.id][j] }}
                </span>
              <span class="inp-del">
                  <input
                      class="inp"
                      type="text"
                      :value="code.trim()"
                      @input="updateCode($event, item, j)"
                      @blur="updateCollocation(item.id,item.codes,item.notes)"/>
                  <span class="button-del" @click="removeCode(item, j)">x</span>
                </span>
              <span>
                  <img class="img" :src="'http://192.168.1.233/web_images/' + code + '.jpg'"/>
              </span>


            </div>
            <div class="ac">
              <div class="add-item">
                <el-icon color="green" size="2vw" @click="addCollocationCode(item)">
                  <CirclePlusFilled/>
                </el-icon>
              </div>
            </div>
            <textarea
                id="textarea"
                oninput="this.style.height = '';
                      this.style.height = this.scrollHeight + 'px'"
                v-model="item.notes"
                @blur="updateCollocation(item.id,item.codes,item.notes)"
                placeholder="此处输入搭配建议话术。"
                class="collocation_notes">
					</textarea>
          </div>


          <div class="addpairing" @click="addCollocation()">添加</div>
        </div>
      </div>
      <!-- 这是规格选择 -->
      <div class='cd' :style="{display: detailChangeStyle}">
        <div class="box">
          <div class="sizeTable">
            <span>尺码</span>
            <span>体重</span>
            <span>身高</span>
            <span>管理</span>
          </div>
          <div class='sizeCode' v-for="item in sizeCodeList" :key="item.id">
            <select v-model="item.size" @change="updateSize(item.id,'size',item.size)" class="size">
              <!-- 假设这些是可能的尺寸，您可以根据需要更改 -->
              <option>S</option>
              <option>M</option>
              <option>L</option>
              <option>XL</option>
            </select>
            <input type="text" v-model="item.weight" class="mass"
                   @blur="updateSize(item.id,'weight',item.weight)"
                   @keydown.enter="updateSize(item.id,'weight',item.weight)"/>
            <input type="text" v-model="item.height" class="stature"
                   @blur="updateSize(item.id,'height',item.height)"
                   @keydown.enter="updateSize(item.id,'height',item.height)"/>
            <span class='del' @click="delSize(item.id)">删除</span>
          </div>
          <div class="addSize" @click="addSize()">+</div>
        </div>
      </div>
    </div>


    <div class='right' v-loading="loading">
      <div class="gpt_content">
        <div class="userinfo" v-for=" (item,key) in gptLsit" :key="key">{{ item }}</div>
      </div>
      <div class="text">
        <textarea id="textarea" oninput="this.style.height = ''; this.style.height = this.scrollHeight + 'px'"
                  v-model="userInfo"></textarea>
        <button type="button" class="gpt" @click="context_reply(userInfo)">发送</button>
      </div>
    </div>

  </div>
</template>

<script setup>


import {ref, watch} from "vue";
import {design} from "../api/design.js";
import {useRoute} from "vue-router";
import {ElMessage} from "element-plus";
import {Setting, CirclePlusFilled} from "@element-plus/icons-vue";

const route = useRoute();
const commodities = ref();
const cart_name = route.params.cart_name
const showTags = ref('')
const tagList = ref([])
const tag_id = ref()
//规格
const sizeCodeList = ref()

const addTagName = ref('')
const addTagInput = ref('')
//搭配
const pairingList = ref()
const getDesign = () => {
  design.getDesign(cart_name).then(respnose => {
    commodities.value = respnose.data.message
  }).catch(err => {
    console.log(err)
  })
}
getDesign()
const design_code = ref("")


const getTags = (key, design_id) => {
  design.getTags(design_id).then(respnose => {
    tagList.value = respnose.data.message
    showTags.value = key
  }).catch(err => {
    ElMessage.error(err)
  })
}
// const goodStyle = ref('')
const addTags = (name, design_id) => {
  design.addTags(name, design_id).then(response => {
    addTagName.value = ''
    addTagInput.value = ''
    tagList.value.push(response.data.message)
  }).catch(err => {
    ElMessage.error(err)
  })
}

const delTag = (tag_id, key) => {
  design.delTag(tag_id).then(response => {
    tagList.value.splice(key, 1)
  }).catch(err => {
    ElMessage.error(err)
  })
}

const getSize = (tags_id) => {
  design.getSize(tags_id).then(response => {
    sizeCodeList.value = response.data.message
  }).catch(err => {
    ElMessage.error(err)
  })
}

const updateSize = (tags_id, condition, content) => {
  design.updateSize(tags_id, condition, content).then(response => {
    ElMessage({
      message: response.data.message,
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error(err)
  })
}

const delSize = (size_id) => {
  design.delSize(size_id).then(response => {
    getSize(tag_id.value)
    ElMessage({
      message: response.data.message,
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error(err)
  })
}

const addSize = () => {
  design.addSize(tag_id.value).then(response => {
    getSize(tag_id.value)
  }).catch(err => {
    ElMessage.error(err)
  })
}


const getScript = (tags_id) => {
  design.getScript(tags_id).then(response => {
    contents.value = response.data.message
  }).catch(err => {
    ElMessage.error(err)
  })
}

const updateScript = (id, original, gpt_original) => {
  design.updateScript(id, original, gpt_original).then(response => {
    ElMessage({
      message: response.data.message,
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error(err)
  })
}

const delScript = (id) => {
  design.delScript(id).then(response => {
    getScript(tag_id.value, tags_type.value)
    ElMessage({
      message: response.data.message,
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error(err)
  })
}

const addScript = () => {
  design.addScript(tag_id.value).then(response => {
    getScript(tag_id.value)
  }).catch(err => {
    ElMessage.error(err)
  })
}


const codeStatus = ref({});
const checkCode = async (code) => {
  try {
    if (code.length >= 5) {
      const response = await design.checkCode(code);
      return response.data;
    }
    return "查询不到该商品信息";
  } catch (err) {
    console.error(err);
    throw err;
  }
  ;
};

const updateCode = async (event, item, j) => {
  const newCode = event.target.value;
  const codes = item.codes.split(',');
  codes[j] = newCode;
  item.codes = codes.join(',');

  if (!codeStatus.value[item.id]) {
    codeStatus.value[item.id] = {};
  }
  codeStatus.value[item.id][j] = await checkCode(newCode);
};


const getCollocation = (id) => {
  design.getCollocation(id).then(response => {
    pairingList.value = response.data.message
  }).catch(err => {
    console.log(err)
  })
}


const updateCollocation = (id, codes, notes) => {
  design.updateCollocation(id, codes, notes).then(response => {
    getCollocation(tag_id.value)
    ElMessage({
      message: response.data.message,
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error(err)
  })
}

const addCollocationCode = (item) => {
  const codesArray = item.codes.split(',');
  codesArray.push(" ");
  item.codes = codesArray.join(',');
}

const removeCode = (item, index) => {
  const codesArray = item.codes.split(',');
  codesArray.splice(index, 1);
  item.codes = codesArray.join(',');
  updateCollocation(item.id, item.codes, item.notes);
}


const addCollocation = () => {
  design.addCollocation(tag_id.value, design_code.value).then(response => {
    getCollocation(tag_id.value)
  }).catch(err => {
    ElMessage.error(err)
  })
}

const reply = (content, key) => {
  design.reply(content).then(response => {
    console.log(response.data.result)
    contents.value[key].gpt_original = response.data.result
  }).catch(err => {
    console.log(err)
  })
}

const gptLsit = ref([])
const loading = ref(false)
const context_reply = (content) => {
  loading.value = true
  design.context_reply(content).then(response => {
    gptLsit.value.push(content)
    gptLsit.value.push(response.data.result)
    loading.value = false
    userInfo.value = ''
  }).catch(err => {
    console.log(err)
  })
}


// 这是标签内容
const contents = ref();

//文本内容
const userInfo = ref('')


//换行

// 这是选择显示哪一个
const mixChangeStyle = ref('none') //搭配
const contentChangeStyle = ref('none') //内容
const detailChangeStyle = ref('none') //规格

const tags_type = ref()
const tagContent = (name, id) => {
  tag_id.value = id
  if (name === '搭配') {
    getCollocation(id)
    mixChangeStyle.value = 'block'
    contentChangeStyle.value = 'none'
    detailChangeStyle.value = 'none'
  } else if (name === '尺码') {
    getSize(id)
    mixChangeStyle.value = 'none'
    contentChangeStyle.value = 'none'
    detailChangeStyle.value = 'block'
  } else {
    getScript(id)
    mixChangeStyle.value = 'none'
    contentChangeStyle.value = 'block'
    detailChangeStyle.value = 'none'
  }
}


</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: content-box;
}

img {
  width: 130px;
  height: 120px;
}

.content {
  display: flex;
  margin: 0 auto;
  width: 99vw;
  height: 99vh;
}

.left {
  flex: 5;
  height: 100vh;
  margin-right: 1vh;
  overflow: auto;
}

.left-head {
  display: flex;
  width: 100%;
  height: 5vh;
  background-color: #009879;
  margin-top: 1vw;
  font-size: 1.2vw;
  color: whitesmoke;
  font-weight: 600;
}

.left-head span {
  flex: 1;
  text-align: center;
  line-height: 5vh;
}

.goodsIntro {
  display: flex;
  justify-content: center; /* 水平居中对齐 */
  align-items: center; /* 垂直居中对齐 */
  width: 100%;
  height: auto;
  margin-top: 0.5vh;
  background-color: #f4f9fa;
}

.goodsIntroActive {
  background-color: #e1ba20;
}

.goodsIntro span {
  flex: 1;
  text-align: center;
}

.goodsLabels {
  width: 100%;
  height: auto;
  background-color: #ffffff;
}

.add-tag {
  display: inline-block;
  width: 1.5vw;
  height: 3vh;
  background-color: #008069;
  vertical-align: top;
  margin: 1vh 0 0 1vh;
  text-align: center;
  border-radius: 50%;
  line-height: 2.7vh;
  font-size: 1.5vw;
  color: white;
}

.middle {
  flex: 5;
  background-color: #f4f9fa;
  margin-right: 1vh;
  overflow: auto;
}

/* 隐藏滚动条 */
.middle::-webkit-scrollbar {
  width: 0px; /* Vertical scrollbar width */
  height: 0px; /* Horizontal scrollbar height */
}

.conts {
  display: flex;
  width: 100%;
  height: 8vw;
}

.conts-left {
  flex: 2;
  position: relative;
}

.remove {
  position: absolute;
  width: 1vw;
  height: 1vw;
  top: 1vw;
  left: 0;
  background-color: red;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 2vw;
  line-height: 0;
  color: white;
}

.conts-left textarea {
  margin: 1vw 0 0 1vw;
  width: 12vw;
  height: 12vh;
  font-size: 1vw;
  border: 1px solid #c3c3c3;
  border-radius: 10px;
  background-color: #ffffff;
  outline: none; /* 移除选中状态的边框 */
}

.conts-middle {
  display: flex;
  flex: 0.3;
  justify-content: center;
  align-items: center;
}

.el-icon {
  cursor: pointer;
}

.conts-right {
  flex: 3;
}

.conts-right textarea {
  margin: 1vw 0 0 1vw;
  width: 17vw;
  height: 12vh;
  font-size: 1vw;
  border: 1px solid #c3c3c3;
  border-radius: 10px;
  background-color: #ffffff;
  outline: none; /* 移除选中状态的边框 */
}

.push {
  width: 8vw;
  height: 5vh;
  background-color: #aaaa7f;
  font-size: 3vw;
  line-height: 4vh;
  text-align: center;
  margin-left: 13vw;
  color: white;
  border: 1px solid white;
}


.right {
  position: relative;
  flex: 4;
  background-color: #ebebeb;
}

.gpt_content {
  width: 100%;
  height: 75%;
  overflow: auto;
}

.gpt_content::-webkit-scrollbar {
  width: 0px; /* Vertical scrollbar width */
  height: 0px; /* Horizontal scrollbar height */
}

.userinfo {
  margin-top: 1vh;
  font-size: 1vw;
  background-color: #f4f9fa;
}

.text {
  position: absolute;
  width: 28vw;
  height: 25%;
  overflow: auto;
}

.text::-webkit-scrollbar {
  width: 0px; /* Vertical scrollbar width */
  height: 0px; /* Horizontal scrollbar height */
}

#textarea {
  margin-left: 8px;
  border-radius: 10px;
  font-size: 1vw;
  width: 96%;
  min-height: 1vw;
  resize: vertical;
  overflow: hidden;
  outline: none; /* 移除选中状态的边框 */
  box-shadow: 0 0 5px black, 0 0 10px black;
}

.gpt {
  margin-left: 9vw;
  border-radius: 5px;
  border: 1px solid white;
  width: 10vw;
  height: 5vh;
  background-color: #c6c6c6;
  cursor: pointer;
  font-size: 1.3vw;
  color: white;
}

/*  */
.ab {
  width: 100%;
  height: 100%;
  overflow: auto;
}

.ab::-webkit-scrollbar {
  width: 0px; /* Vertical scrollbar width */
  height: 0px; /* Horizontal scrollbar height */
}

.cd {
  width: 100%;
  height: 100%;
  padding-top: 2vw;
}

/* 标签 */
.tags {
  display: inline-block;
  width: 4vw;
  height: 5vh;
  margin: 0 0 0 1vh;
}

.tag-text {
  display: block;
  width: 1vw;
  height: 2vh;
  background-color: red;
  border-radius: 50%;
  text-align: center;
  line-height: 1.5vh;
  font-size: 1.5vw;
  color: white;
  cursor: pointer;
}

.del-tag {
  display: inline-block;
  width: 3vw;
  height: 3vh;
  text-align: center;
  line-height: 3vh;
  background-color: #009879;
  border-radius: 10px;
  cursor: pointer;
}

/* 规格 */
.box {
  width: 33vw;
  height: 20vw;
  margin: 0 auto;
}

.sizeTable {
  width: 33vw;
  height: 4vw;
  background-color: #000000;
  font-size: 1.5vw;
}

.sizeTable span {
  text-align: center;
  line-height: 4vw;
  color: white;
}

.sizeTable span:nth-child(1) {
  display: inline-block;
  width: 9vw;
  height: 4vw;
}

.sizeTable span:nth-child(2) {
  display: inline-block;
  width: 9vw;
  height: 4vw;
}

.sizeTable span:nth-child(3) {
  display: inline-block;
  width: 9vw;
  height: 4vw;
}

.sizeTable span:nth-child(4) {
  display: inline-block;
  width: 6vw;
  height: 4vw;
}

.sizeCode {
  width: 33vw;
  height: 4vw;
  background-color: #747474;
  font-size: 1.5vw;
}

.sizeCode:nth-child(2n) {
  background-color: #c5c5c5;
}

.sizeCode:nth-child(2n) .mass, .sizeCode:nth-child(2n) .stature, .sizeCode:nth-child(2n) .size {
  background-color: #c5c5c5;
}

.size {
  width: 9vw;
  height: 3vw;
  text-align: center;
  font-size: 1.4vw;
  margin-top: 0.5vw;
  border: none;
  background-color: #747474;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

.size option {
  background-color: #cacaca;
}

.mass {
  width: 9vw;
  height: 3vw;
  text-align: center;
  border: none;
  background-color: #747474;
  font-size: 1.4vw;
}

.stature {
  width: 9vw;
  height: 3vw;
  text-align: center;
  border: none;
  background-color: #747474;
  font-size: 1.4vw;
}

.del {
  display: inline-block;
  width: 4vw;
  height: 4vw;
  margin-left: 1vw;
  text-align: center;
  color: #ffffff;
  cursor: pointer;
  font-size: 1vw;
}

.addSize {
  width: 8vw;
  height: 3vw;
  background-color: #b5b5b5;
  margin: 2vw auto;
  text-align: center;
  line-height: 3vw;
  color: white;
  font-size: 2vw;
  cursor: pointer;
}

/* 这是搭配 */
.pairing {
  margin: 0 auto;
  width: 33vw;
  height: auto;
  overflow: hidden;
}

.pairingHead {
  width: 33vw;
  height: 3vw;
  text-align: center;
  line-height: 3vw;
  font-size: 1.2vw;
}

.pairingHead span {
  text-align: center;
  font-size: 1.2vw;
  line-height: 3vw;
  border-right: 1px solid black;
  background-color: #cccccc;
}

.pairingList {
  width: 33vw;
  height: auto;
  margin-bottom: 1vh;
  overflow-x: auto; /* 水平滚动条 */
  white-space: nowrap; /* 子盒子不换行 */
  background-color: #919191;
  overflow-y: hidden;
}

.pairing-item {
  display: inline-block;
  width: 8vw;
  height: 10vw;
  margin-left: 1vh;
  vertical-align: top; /* 或者使用 'middle' */
}

.pairing-item:nth-child(1) {
  margin: 0;
}

.tips_success {
  display: block;
  width: 100%;
  height: 1vw;
  border-radius: 5px;
  color: black;
}


.inp-del {
  display: flex;
  width: 100%;
  height: 2vw;
  align-items: center; /* 添加align-items属性 */
}

.inp {
  width: 75%;
  height: 1.7vw;
  border: none;
  text-align: center;
  font-size: 1vw;
  border-radius: 5px;
}

.button-del {
  display: inline-block;
  width: 22%;
  height: 1.7vw;
  text-align: center;
  font-size: 1vw;
  line-height: 1.7vw;
  border-radius: 5px;
  margin-left: 5px;
  background-color: rgb(154, 59, 59);
  cursor: pointer;
}

.img {
  display: block;
  width: 100%;
  height: 7vw;
}

.ac {
  display: inline-block;
  width: 2vw;
  height: 10vw;
  vertical-align: top; /* 或者使用 'middle' */
}

.add-item {
  width: 100%;
  height: 2vw;
  cursor: pointer;
  font-size: 1.5vw;
  line-height: 3vh;
  text-align: center;
  margin-top: 1vw;
}


/* 添加搭配 */
.addpairing {
  width: 10vw;
  height: 3vw;
  background-color: #faf3f5;
  text-align: center;
  margin: 0 auto;
  margin-top: 1vw;
  line-height: 3vw;
  font-size: 1.5vw;
  cursor: pointer;
}

.collocation_notes {
  display: block;
  margin-left: 8px;
  border-radius: 10px;
  width: 96%;
  outline: none; /* 移除选中状态的边框 */
  box-shadow: 0 0 5px black, 0 0 10px black;
}
</style>