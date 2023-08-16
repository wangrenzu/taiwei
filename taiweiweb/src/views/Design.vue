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
      <div v-if="commodities" class='commodity' v-for="(commodity, key) in commodities" :key=key>
        <div class="goodsIntro" @click="getTags(key, commodity.id); design_code = commodity.code"
             :class='{ goodsIntroActive: showTags === key }'>
          <el-input
              v-if="showuniqueIndex === key"
              style="width: 100px"
              v-model="commodity.uniqueIndex"
              @blur="sortuniqueIndex"
              @click="sortuniqueIndex"
          ></el-input>
          <span v-else @click="showuniqueIndex=key">{{ commodity.uniqueIndex }}</span>
          <span>{{ commodity.code }}</span>
          <span>{{ commodity.name }}</span>
          <span>{{ commodity.designer }}</span>
          <span>{{ commodity.material }}</span>
          <span>
            <p v-for="i in commodity.specification_quantity.split(' ')">
              {{ i }}
            </p>
          </span>
        </div>
        <div class="goodsLabels" v-if="showTags === key">
          <span class="tags" v-for="(item, tagKey) in tagList" :key="tagKey">
            <span class="tag-text" @click="delTag(item.id, tagKey)">-</span>
            <span class="del-tag" @click='tagContent(item.tags, item.id,item.notes)'>{{ item.tags }}</span>
          </span>


          <span class="add-tag" @click="addTagInput = key">
            <el-input v-if="addTagInput === key" style="width: 100px" v-model="addTagName"
                      @blur="addTags(addTagName, commodity.id)" @keydown.enter="addTags(addTagName, commodity.id)">
            </el-input>
            <span v-else>+</span>
          </span>

        </div>
      </div>

    </div>
    <!-- 这是描述 -->
    <div class='middle' :class="{ magnify: moveRight }">
      <div class='middle-left'>
        <div class='price-item' :style="{ display: contentChangeStyle }">
          <div class="box1" :class="{box2:priceItem}">
            <div class="price-img" :class="{priceTmg2:priceItem}">
              <span style="font-size:20px;">{{ tags_name }}介绍</span>
              <img :src="'http://192.168.1.233/web_images/' + design_code+ '.jpg'" alt="">
              <el-input
                  v-if="contents"
                  placeholder="请输入整体描述"
                  type="textarea" v-model="tag_notes" @blur="updateTagNotes(tag_id,tag_notes)"></el-input>
            </div>
            <div class="price-info" :class="{priceInfo2:priceItem}">
              <el-input
                  disabled
                  type="textarea"
                  placeholder="加工的话术"
                  value="润色加工一下这句话，让产品看起来更有信任感和吸引力，产品类目是女装，文字适合口语，让消费者有购买的理由和冲动，可以展开2到3个方面讲，总的字数控制稍微简洁些，记得要口语化">
              </el-input>
              <div class='conts' v-for='(item, key) in contents' :key='key'>
            <span class='conts-left'>
              <button class='remove' @click="delScript(item.id)">-</button>
              <el-input
                  v-model="item.original"
                  autosize
                  type="textarea"
                  :class="{textarea__inner_open:priceItem}"
                  placeholder="请输入内容"
                  @blur="updateScript(item.id, item.original, item.gpt_original)"
              />
            </span>
                <el-icon>
                  <Tools/>
                </el-icon>
                <span class='conts-middle'>
              <el-icon size="30" @click="reply(item.original, key)">
                <Setting/>
              </el-icon>
            </span>
                <span class='conts-right'>
                  <div style="position: relative;">
                      <el-input
                          v-model="item.gpt_original"
                          autosize
                          type="textarea"
                          style="position: relative;"
                          :class="{textarea__inner_open:priceItem}"
                          placeholder="加工后的内容"
                          @blur="updateScript(item.id, item.original, item.gpt_original)"
                      />
                      <el-icon
                          v-if="video===item.id"
                          @click="audio.pause();video=''"
                          style="position: absolute; bottom: 1px; right: 5px;"
                          size="30px" color="red">
                      <VideoPause/>
                    </el-icon>
                      <el-icon
                          v-else
                          size="30px"
                          color="green"
                          style="position: absolute; bottom: 1px; right: 5px;"
                          @click="processGETRequest(item.gpt_original);video=item.id">
                        <VideoPlay/>
                      </el-icon>

                  </div>
            </span>
              </div>
              <button class='push' @click="addScript()">+</button>
              <div class="inner_text" style="display: flex;margin-bottom: 20px">
                <el-input style="width: 400px;" type="textarea" v-model="old_text"></el-input>
                <el-icon size="30" style="margin: 70px 50px;" @click="processText">
                  <Setting/>
                </el-icon>
                <el-input style="width: 400px;" v-model="new_text" type="textarea"></el-input>
              </div>


            </div>

          </div>


        </div>
        <!-- 这是搭配 -->
        <div class='ab' :style="{ display: mixChangeStyle }" ref="myDiv">
          <div v-for="(item,key) in pairingList" :key="key">
            <span class="tag-name" v-for="code in item.child_code.split(',')">
              <span>{{ code + "" + codeData[code].category }}</span>
              <span>{{ "库存" + codeData[code].inventory }}</span>
            </span>
            <span class="tag-icon">
              <el-popconfirm
                  title="是否确认删除？"
                  @confirm="delCollocation(item.id,item.codes)">
                <template #reference>
                  <el-icon><Close/></el-icon>
                </template>
              </el-popconfirm>
              </span>
            <img :src="'http://192.168.1.233/dapei/' + item.codes" alt="">
            <textarea
                cols="29"
                :rows="count"
                @input="autoGrow"
                v-model="item.notes"
                placeholder="此处输入搭配建议话术。"
                @blur="updateCollocation(item.id,item.notes)"></textarea>
          </div>
        </div>
        <!-- 这是规格选择 -->
        <div class='cd' :style="{ display: detailChangeStyle }">
          <div class="box">
            <div class="sizeTable">
              <span>尺码</span>
              <span>体重</span>
              <span>身高</span>
              <span>管理</span>
            </div>
            <div class='sizeCode' v-for="item in sizeCodeList" :key="item.id">
              <select v-model="item.size" @change="updateSize(item.id, 'size', item.size)" class="size">
                <!-- 假设这些是可能的尺寸，您可以根据需要更改 -->
                <option>S</option>
                <option>M</option>
                <option>L</option>
                <option>XL</option>
              </select>
              <input type="text" v-model="item.weight" class="mass" @blur="updateSize(item.id, 'weight', item.weight)"
                     @keydown.enter="updateSize(item.id, 'weight', item.weight)"/>
              <input type="text" v-model="item.height" class="stature"
                     @blur="updateSize(item.id, 'height', item.height)"
                     @keydown.enter="updateSize(item.id, 'height', item.height)"/>
              <span class='del' @click="delSize(item.id)">删除</span>
            </div>
            <div class="addSize" @click="addSize()">+</div>
          </div>
        </div>
      </div>
      <div class='middle-right' @click="changStyle">
        <span :class="{ left_arrow: moveRight }"></span>
      </div>

    </div>


    <div class='right' v-loading="loading" :class="{ tsy: moveRight }">
      <div class="gpt_content" v-if="priceItem">
        <div class="userinfo" v-for=" (item, key) in gptLsit" :key="key">{{ item }}</div>
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


import {reactive, ref, nextTick} from "vue";
import {design} from "../api/design.js";
import {useRoute} from "vue-router";
import {ElMessage} from "element-plus";
import {Setting, Close, VideoPlay, VideoPause} from "@element-plus/icons-vue";
import {useCounterStore} from "../stores/store.js";

const route = useRoute();
const commodities = ref();
const cart_name = route.params.cart_name
const showTags = ref('')
const tagList = ref([])
const tag_id = ref()
//规格
const sizeCodeList = ref()
const video = ref()

const addTagName = ref('')
const addTagInput = ref('')
const tag_notes = ref()
//搭配
const pairingList = ref()
const store = useCounterStore()
let cart_codes = Object.values(store.code_list);
const showuniqueIndex = ref('')

const audio = ref(new Audio());


const sortuniqueIndex = () => {
  showuniqueIndex.value = ''
  commodities.value = commodities.value.sort((a, b) => a.uniqueIndex - b.uniqueIndex);
}
const getDesign = () => {
  design.getDesign(cart_name, cart_codes).then(respnose => {
    commodities.value = respnose.data.message
    commodities.value = commodities.value.map((item, index) => {
      return {
        ...item,  // 使用扩展运算符保留原有的属性
        uniqueIndex: index + 1  // 添加新的字段
      };
    });
    console.log(commodities.value)
  }).catch(err => {
    console.log(err)
  })
}
getDesign()
const design_code = ref("")

const processGETRequest = (text) => {
  design.processGETRequest(text).then(response => {
    audio.value.pause()
    let urls = 'http://192.168.1.137:8000/static/syAudio.wav'
    audio.value = new Audio(urls)
    audio.value.play()
    audio.value.addEventListener('ended', () => {
      video.value = ''; // 在音频播放完成后执行 video.value = ''
    });
  }).catch(err => {
    console.log(err)
  })
}

const getTags = (key, design_id) => {
  design.getTags(design_id).then(respnose => {
    tagList.value = respnose.data.message
    showTags.value = key
    tagContent(tagList.value[0].tags, tagList.value[0].id, tagList.value[0].notes)
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

const old_text = ref()
const new_text = ref()

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


const codeData = reactive({});
const getCollocation = (id) => {
  design.getCollocation(id).then(response => {
    pairingList.value = response.data.message

    const checkCode = async (code) => {
      try {
        const response = await design.checkCode(code);
        codeData[code] = response.data;
      } catch (err) {
        console.log(err);
      }
    };
    for (let item of pairingList.value) {
      const codes = item.child_code.split(',');
      for (let code of codes) {
        checkCode(code);
      }
    }
  }).catch(err => {
    console.log(err)
  })
}


const updateCollocation = (id, notes) => {
  design.updateCollocation(id, notes).then(response => {
    getCollocation(tag_id.value)
    ElMessage({
      message: response.data.message,
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error(err)
  })
}


const addCollocation = () => {
  design.addCollocation(tag_id.value, design_code.value).then(response => {
    getCollocation(tag_id.value)
  }).catch(err => {
    ElMessage.error(err)
  })
}

const delCollocation = (id, file_name) => {
  design.delCollocation(id, file_name).then(response => {
    ElMessage({
      message: response.data.message,
      type: 'success',
    })
    getCollocation(tag_id.value)
  }).catch(err => {
    ElMessage.error(err)
  })
}

const reply = (content, key) => {
  design.reply(content).then(response => {
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

const updateTagNotes = (tag_id, tag_notes) => {
  design.updateNotes(tag_id, tag_notes).then(response => {
    ElMessage({
      message: response.data.message,
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error(err)
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

const tags_name = ref('')
const tagContent = (name, id, notes) => {
  tags_name.value = name
  tag_id.value = id
  tag_notes.value = notes
  if (name === '搭配') {
    addCollocation()
    mixChangeStyle.value = 'block'
    contentChangeStyle.value = 'none'
    detailChangeStyle.value = 'none'
    nextTick();
    resizeObserver = new ResizeObserver(entries => {
      for (let entry of entries) {
        layoutImages(entry); // 重新布局图片
      }
      // 观察目标元素
      resizeObserver.observe(myDiv.value);
    });

    // 在组件卸载时停止观察
    if (resizeObserver && myDiv.value) {
      resizeObserver.unobserve(myDiv.value);
    }
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


const moveRight = ref(true)
const myDiv = ref(null);

let resizeObserver = null;

const layoutImages = (entry) => {
  let imgs = entry.target.children;

  // 重置所有图片的定位
  for (let i = 0; i < imgs.length; i++) {
    imgs[i].style.position = 'relative';
    imgs[i].style.left = '';
    imgs[i].style.top = '';
  }

  let imgWidth = imgs[0].offsetWidth;

  // 计算第一行可以排列多少张图片
  let nums = Math.floor(entry.target.offsetWidth / imgWidth);

  // 收集第一排的所有高度
  let arrHeight = []
  for (let i = 0; i < imgs.length; i++) {
    if (i < nums) { // 这里都是第一行的元素
      arrHeight.push(imgs[i].offsetHeight)
    } else {
      // 创建一个元素的对象
      let obj = {
        minH: arrHeight[0],
        minI: 0
      }
      for (let j = 0; j < arrHeight.length; j++) {
        if (arrHeight[j] < obj.minH) {
          obj.minH = arrHeight[j],
              obj.minI = j
        }
      }
      imgs[i].style.position = 'absolute'
      imgs[i].style.left = imgs[obj.minI].offsetLeft + 'px'
      imgs[i].style.top = obj.minH + 'px'
      arrHeight[obj.minI] = arrHeight[obj.minI] + imgs[i].offsetHeight
    }
  }
}
const autoGrow = (event) => {
  let textarea = event.target;
  textarea.style.height = "auto"; // 首先重置 textarea 的高度
  textarea.style.height = textarea.scrollHeight + "px"; // 然后根据 scrollHeight 调整高度
  layoutImages({target: myDiv.value}); // 重新计算布局
}


const count = ref(2)

const priceItem = ref(false)
const changStyle = () => {
  priceItem.value = !priceItem.value
  moveRight.value = !moveRight.value
}

const processText = () => {
  const processed = old_text.value
      .split('\n')  // 根据换行符切分文本
      .map(line =>
          line
              .replace(/^\d+\.\s*/, '')  // 移除行开始的数字和点
              .replace(/[？！。]$/, '')  // 移除行尾的中文标点符号
          + '\\'
      )
      .join('\n');  // 使用换行符连接各行

  new_text.value = processed;
};


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
  height: 100vh;
  overflow: hidden;
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

.inner_text .el-textarea__inner {
  width: 350px;
  height: 200px;
}


.left-head span {
  flex: 1;
  text-align: center;
  line-height: 5vh;
}

.goodsIntro {
  display: flex;
  justify-content: center;
  /* 水平居中对齐 */
  align-items: center;
  /* 垂直居中对齐 */
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
  display: flex;
  position: relative;
  flex: 5;
  background-color: #f4f9fa;
  margin-right: 1vh;
  overflow: auto;
}

/* 隐藏滚动条 */
.middle::-webkit-scrollbar {
  width: 0px;
  /* Vertical scrollbar width */
  height: 0px;
  /* Horizontal scrollbar height */
}

.middle-left {
  flex: 1;
}

.middle-right {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 1.5vw;
  height: 3vw;
  background-color: rgb(119, 152, 119);
  cursor: pointer;
  border-top-left-radius: 30px;
  border-bottom-left-radius: 30px;
}

.middle-right span {
  display: block;
  width: 1vw;
  height: 1vw;
  transform: translateY(80%) rotate(45deg);
  border-top: 2px solid white;
  border-right: 2px solid white;
}

.price-item {
  width: 100%;
  height: 100%;
}

.box1 {
  display: flex;
  width: 100%;
  height: 100%;
}

.box2 {
  flex-direction: column;
}

.price-img {
  margin-top: 5vw;
  margin-left: 1vw;
  width: 280px;
  /*min-width: 140px;*/
  height: 400px;
  vertical-align: middle;
  text-align: center
}

.box1 .priceTmg2 {
  margin: 0 auto;
  transition: all 1.5s;
}

.price-img img {
  width: 100%;
}

.price-info {
  width: 35vw;
  /*height: 500px;*/
  margin-left: 3vw;
}

.priceInfo2 {
  margin-left: 0;
  transition: all 1.5s;
}

.conts {
  display: flex;
  width: 100%;
  height: auto;
}

.conts-left {
  flex: 2;
  position: relative;
}

/*收回去的*/
.conts-left .el-textarea__inner {
  min-height: 150px !important;
  font-size: 10px !important;
  width: 20vw !important;
}

.conts-right .el-textarea__inner {
  min-height: 150px !important;
  font-size: 10px !important;
  width: 20vw !important;
}

.textarea__inner_open {

}

.textarea__inner_open .el-textarea__inner {
  min-height: 150px !important;
  font-size: 10px !important;
  width: 15vw !important;
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
  z-index: 1;
}

.conts-left textarea {
  margin: 1vw 0 0 1vw;
  width: 12vw;
  height: 12vh;
  font-size: 1vw;
  border: 1px solid #c3c3c3;
  border-radius: 10px;
  background-color: #ffffff;
  outline: none;
  /* 移除选中状态的边框 */
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
  outline: none;
  /* 移除选中状态的边框 */
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
  transition: all 1s;
}

.gpt_content {
  width: 100%;
  height: 75%;
  overflow: auto;
}

.gpt_content::-webkit-scrollbar {
  width: 0px;
  /* Vertical scrollbar width */
  height: 0px;
  /* Horizontal scrollbar height */
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
  width: 0px;
  /* Vertical scrollbar width */
  height: 0px;
  /* Horizontal scrollbar height */
}

#textarea {
  margin-left: 8px;
  border-radius: 10px;
  font-size: 1vw;
  width: 96%;
  min-height: 1vw;
  resize: vertical;
  overflow: hidden;
  outline: none;
  /* 移除选中状态的边框 */
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
  height: 100vh;
}

.ab div {
  position: relative;
  float: left;
  /* border: 1px solid white; */
  padding: 10px 10px 0 10px;
  overflow: hidden;
}

.tag-name {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 8vw;
  height: 6vh;
  z-index: 1;
  color: white;
  border-radius: 5px;
}

.tag-icon {
  position: absolute;
  top: 10px;
  right: 10px;
}

.tag-name span:nth-child(1):hover + span:nth-child(2) {
  display: block;
}

.tag-name span:nth-child(1) {
  min-width: 4vw;
  width: auto; /* 宽度随内容变化 */
  white-space: nowrap; /* 使内容在一行中显示，不换行 */
  line-height: 3vh;
  height: 3vh;
  background-color: #0909094d;
  border-top-left-radius: 10px;
}

.tag-name span:nth-child(2) {
  margin-top: -0.4vh;
  line-height: 3vh;
  display: none;
  width: 4vw;
  height: 3vh;
  background-color: #0909094d;
}

.tag-name:nth-child(2) {
  top: 70px;
}

.tag-name:nth-child(3) {
  top: 130px;
}

.ab div img {
  width: 280px;
  border-radius: 10px;
  vertical-align: middle;
}

.ab div textarea {
  display: block;
  overflow: hidden;
  resize: none;
  font-size: 0.9vw;
  border: none;
  outline: none;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  /* 禁止手动调整大小 */
}

.ab div textarea:hover {
  transform: translateY(18%);
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
  height: auto;
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

.sizeCode:nth-child(2n) .mass,
.sizeCode:nth-child(2n) .stature,
.sizeCode:nth-child(2n) .size {
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

/* 这下面是把gpt移动过来的样式 */
/* 箭头旋转 */
.left_arrow {
  transform: translate(40%, 80%) rotate(230deg) !important;
}

.tsy {
  position: absolute;
  transform: translateX(100%);
}

.magnify {
  flex: 9;
}

</style>