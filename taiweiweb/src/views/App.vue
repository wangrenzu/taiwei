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
            <img class="img" :src="'http://192.168.1.233/dapei/' + item.codes"/>
            <p v-for="code in item.child_code.split(',')">{{ code+""+codeData[code].category+"库存"+codeData[code].inventory}}</p>
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