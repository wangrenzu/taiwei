<template>

  <el-button v-if="run" type="primary" @click="runGetGoods">开始抓取</el-button>
  <el-button v-if="close" type="danger" @click="closeGetGoods">停止抓取</el-button>

  <el-input v-model="room.room_id" style="width: 200px"
            placeholder="请输入room_id" clearable></el-input>
  <el-date-picker
      v-model="room.date_time"
      type="date"
      placeholder="请选择日期"

  />
  <el-select v-model="room.session" clearable placeholder="请选择场次" size="default"
             @clear="room.session=null">
    <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
    />
  </el-select>
  <span>本场销售金额总和:<span style="font-size: 20px">{{ totalSalesPrice.salesPrice.toFixed(0) }}</span></span>
  &nbsp;
  <span>本场销售数量总和:<span style="font-size: 20px">{{ totalSalesNum }}&nbsp</span></span>
  <span>上一场销售金额总和:<span style="font-size: 20px">{{ totalSalesPrice.cart_salesPrice.toFixed(0) }}</span></span>
  &nbsp;
  <span>上一场销售数量总和:<span style="font-size: 20px">{{ totalCartSalesNum }}</span></span>

  <div class="live_content">
    <div class="integration" v-if="room.integration[0]">
      <div class="top">
        <div class="top_left">
          {{ room.integration[0].product_id }}
        </div>
        <table class="top_right">
          <tr>
            <th style="background-color: #FFFF00">开发日期</th>
            <th>品类</th>
            <th>季节</th>
            <th>成本</th>
            <th>直播价</th>
            <th>备注</th>
            <th>档口30天价</th>
            <th>档口30天销量</th>
          </tr>
          <tr>
            <td>{{ room.integration[0].creation_date }}</td>
            <td>{{ room.integration[0].category }}</td>
            <td>{{ room.integration[0].season }}</td>
            <td>{{ room.integration[0].cost }}</td>
            <td style="color:red;font-weight: bold;font-size: 28px">
              <el-input
                  style="width: 60px"
                  v-if="room.show_input1"
                  v-model="room.integration[0].order_price"
                  @keyup.enter="editOrderPrice(room.integration[0].code,room.integration[0].order_price)">
              </el-input>
              <span v-else style="width: 30px" @click="room.show_input1=true">{{
                  parseInt(room.integration[0].order_price)
                }}</span>
            </td>
            <td>
              <span v-if="show_notes" @click="show_notes=false">{{ notes }}</span>
              <el-input
                  v-else
                  v-model="notes"
                  style="width: 100px"
                  @keyup.enter="show_notes=true">
                >
              </el-input>
            </td>
            <td>{{ room.integration[0].stall_price }}</td>
            <td>{{ room.integration[0].stall_sales }}</td>
          </tr>
        </table>
      </div>
      <div class="middle">
        <div class="middle_left">
          <div class="middle_left_top">
            <el-image style="width: 100%; height: 100%"
                      :src="room.integration[0].img"/>
          </div>
          <div class="middle_left_bottom">
            <el-input
                v-model="room.room_live_code"
                v-if="room.inp_room_live_code"
                @keyup.enter="room.inp_room_live_code=false">
            </el-input>
            <span v-else @click="room.inp_room_live_code=true">{{ room.room_live_code }}</span>
          </div>
        </div>

        <div class="middle_right">
          <p v-if="room.integration[0].size"
             v-for="sale in room.integration[0].size.split('  ').filter(item => item !== '')">{{ sale }}</p>
        </div>
      </div>
      <div class="bottom">
        <div class="bottom_left">
          <div v-for="item in room.result" class="bottom_left_div">
            <div class="bottom_left_div1">
              <p>{{
                  ((getSumScore(item.name).success_num || '0') === '0' ? '' : '成' + (getSumScore(item.name).success_num || '0')) +
                  ((getSumScore(item.name).back_num || '0') === '0' ? '' : '/退' + (getSumScore(item.name).back_num || '0')) +
                  ((getSumScore(item.name).transit_num || '0') === '0' ? '' : '/回头' + (getSumScore(item.name).transit_num || '0'))
                }}
              </p>
              <p>{{ (getSumScore(item.name).sum_score || '新客') }}</p>
            </div>
            <div class="bottom_left_div2">{{ item.name }}</div>
            <div class="bottom_left_div3">{{ item.content[0] }}</div>
            <div class="bottom_left_div3">{{ item.content[1] }}</div>

          </div>
        </div>
        <div class="bottom_right">
          <div class="bottom_right_top">
            <div class="bottom_right_top_left">
              <div class="bottom_right_top_left_left">
                <p v-if="room.salesArray"
                   v-for="(sale, index) in room.salesArray" :key="index">
                  <span>{{ sale }}</span>
                </p>
              </div>
              <div class="bottom_right_top_left_right">
                <p v-for="(sale_text,index,) in room.sale_text_list">
                  <el-input
                      v-if="room.show_input2===index"
                      style="width: 100px"
                      v-model="room.sale_text_list[index]"
                      @keydown.enter="room.show_input2=' '">
                  </el-input>
                  <span v-else @click="room.show_input2=index">{{ sale_text }}</span>
                </p>
              </div>

            </div>
            <div class="bottom_right_top_right">可卖{{ room.integration[0].available_quantity }}</div>
          </div>
          <div class="bottom_right_bottom">
            <div class="bottom_right_bottom_top">初次到档口时间：{{ room.integration[0].first_registration_time }}</div>
            <div class="bottom_right_bottom_bottom">最后到档口时间：{{
                room.integration[0].last_registration_time
              }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="Object.keys(room.live_data).length > 0" class="right_live">
      <div class="right_live_top">
        <div class="right_live_top_left">
          <div class="right_live_top_left_left">
            <span style="font-size: 30px;position: relative">
              当前库存：{{ room.live_data.stock_cnt }}
              <span style="font-size:15px;position: absolute;right: 0">
                本次金额：{{ (market_price / 100).toFixed(2) }}
              </span>
              <span style="font-size:15px;position: absolute;top:20px;right: 0">
                千次金额：{{ parseInt((1000 / C) * ((market_price / 100))) }}
              </span>
            </span>
            <span style="font-size: 40px;color: #e1ba20;margin-bottom: 20px">已下单：{{
                room.live_data.pay_combo_cnt
              }}</span>
            <div
                style="display: flex; align-items: center; font-size: 25px; border-top: 1px solid white; position: relative">
              <span>曝光：{{ add_product_show_ucnt }}</span>
              <el-progress
                  :percentage="(route.params.room_name === '悦仓直播间')?(C % 100):((C % 200)/2)"
                  :stroke-width="15"
                  :color="getColor"
                  :show-text="false"
                  striped
                  striped-flow
                  :duration="10"
                  style="width: 200px;"
              >
              </el-progress>
              <span style="font-size: 15px;position: absolute;right: 0">
                  本次讲解
                </span>
            </div>
            <span style="font-size: 20px;">点击：{{ add_product_click_ucnt }}</span>
            <span style="font-size: 20px;">点击率：{{
                (success_rate === '') ? '' : (success_rate * 100).toFixed(2) + '%'
              }}
              &nbsp;
              成交率：{{ (add_pay_combo_cnt / DZ * 100).toFixed(2) + '%' }}
            </span>
            <span style="font-size: 15px;color: #e1ba20;">
              总曝光次:
              {{ add_room_live_exposure_sum }}
              进入次数:
              {{ add_in_room_live }}
              进入率:
              {{ ((add_in_room_live / add_room_live_exposure_sum) * 100).toFixed(2) + "%" }}
            </span>
          </div>
          <div class="right_live_top_left_right">
            <span>
                在线人数：{{ room.live_data.online_user_cnt }}
              </span>
            <span>直播成交金额</span>
            <span>
          ¥{{ parseInt(room.live_data.price) }}
          </span>
          </div>
        </div>
        <div class="right_live_top_right">
          <div class="right_live_top_right_top">
            <div class="right_live_top_right_top_left">
              <span class="live_title">进入直播间人数</span>
              <span class="live_num">
                {{ '\n' + room.live_data.in_live }}
              </span>
            </div>
            <div class="right_live_top_right_top_right">
              <span class="live_title">离开直播间人数</span>
              <span class="live_num">
                {{ '\n' + room.live_data.out_live }}
              </span>
            </div>
          </div>
          <div class="right_live_top_right_bottom">
            <div class="right_live_top_right_bottom_left">
              <span class="live_title">新增粉丝数</span>
              <span class="live_num">
                {{ '\n' + room.live_data.add_fan }}
              </span>
            </div>
            <div class="right_live_top_right_bottom_right">
              <span class="live_title">评论次数</span>
              <span class="live_num">
                {{ '\n' + room.live_data.comment_num }}
              </span>
            </div>
          </div>
        </div>


      </div>
      <div class="right_live_bottom">
        <div class="right_live_bottom_top">
          <table class="centered-table">
            <tr>
              <th>成交件数</th>
              <th>成交人数</th>
              <th>点击-成交转化率</th>
              <th>千次观看成交金额</th>
              <th>成交粉丝占比</th>
            </tr>
            <tr>
              <td>{{ room.live_data.pay_cnt }}</td>
              <td>{{ room.live_data.pay_ucnt }}</td>
              <td>{{ (room.live_data.product_click_to_pay_rate * 100).toFixed(2) + '%' }}</td>
              <td>{{ room.live_data.gpm }}</td>
              <td>{{ (room.live_data.pay_fans_ratio * 100).toFixed(2) + '%' }}</td>

            </tr>
          </table>
        </div>
        <div class="right_live_bottom_bottom">
          <table class="centered-table2">
            <tr>
              <th>累计观看人数</th>
              <th>新加直播团人数</th>
              <th>新增粉丝数</th>

            </tr>
            <tr>
              <td>{{ room.live_data.online_user_ucnt }}</td>
              <td>{{ room.live_data.fans_club_ucnt }}</td>
              <td>{{ room.live_data.incr_fans_cnt }}</td>

            </tr>
          </table>


        </div>
      </div>
    </div>
    <div v-else>
      <el-tag>未抓取数据请输入room_id</el-tag>
    </div>

  </div>
  <span style="width: auto">
    <el-card class="box-card" style="max-height: 40px; overflow: auto;">
    <div class="text item">{{ room.message[room.message.length - 1] }}</div>
  </el-card>
  <el-button type="primary" @click="exportRoom()">导出</el-button>
  </span>

  <div style="display: flex; justify-content: space-between;">
    <div v-if="list2.length!==0" ref="chartDom2" style="width: 600px; height: 400px;"></div>
    <div v-if="list3.length!==0" ref="chartDom3" style="width: 600px; height: 400px;"></div>
    <div v-if="list4.length!==0" ref="chartDom4" style="width: 600px; height: 400px;"></div>
  </div>

  <el-table
      :data="room.room_list"
      style="width: 100%" border fit height="800"
  >
    <el-table-column type="expand">
      <template #default="props">
        <el-table :data="getProductCode(props.row.code)" fit style="width: 70%;">
          <el-table-column prop="exposure_count" label="曝光" show-overflow-tooltip></el-table-column>
          <el-table-column prop="click_count" label="点击" show-overflow-tooltip></el-table-column>
          <el-table-column prop="click_rate" label="点击率" show-overflow-tooltip></el-table-column>
          <el-table-column prop="success_reta" label="成交率" show-overflow-tooltip></el-table-column>
          <el-table-column prop="total_exposure" label="总曝光次" show-overflow-tooltip></el-table-column>
          <el-table-column prop="entry_count" label="进入次数" show-overflow-tooltip></el-table-column>
          <el-table-column prop="in_live_rate" label="进入率" show-overflow-tooltip></el-table-column>
          <el-table-column prop="pay_combo_cnt" label="销量" show-overflow-tooltip></el-table-column>
          <el-table-column prop="live_time" label="讲解时间" show-overflow-tooltip></el-table-column>
          <el-table-column prop="start_time" label="开始时间" width="200" show-overflow-tooltip>
            <template #default="scope">
              {{ formatMyDate(scope.row.start_time) }}
            </template>
          </el-table-column>
          <el-table-column prop="end_time" label="结束时间" width="200" show-overflow-tooltip>
            <template #default="scope">
              {{ formatMyDate(scope.row.end_time) }}
            </template>
          </el-table-column>
        </el-table>
      </template>
    </el-table-column>
    <el-table-column prop="product_id" label="商品序号" width="80" show-overflow-tooltip/>
    <el-table-column label="款号" width="120">
      <template #default="scope">
        <el-input
            v-if="room.editingRow === scope.row"
            v-model="scope.row.code"
            @keyup.enter="editCode(scope.row.id,scope.row.code)"
        />
        <span v-else @click="room.editingRow = scope.row">{{ scope.row.code }}</span>
      </template>
    </el-table-column>

    <el-table-column label="图片" width="100">
      <template #default="scope">
        <el-image style="width: 90px; height: 100px"
                  :src="scope.row.img"/>
      </template>
    </el-table-column>
    <el-table-column prop="characteristic" label="特征" width="150" align="center" show-overflow-tooltip>
      <template #default="scope">
        <p v-for="characteristic in scope.row.characteristic.split(' ').filter(item => item !== '')">{{
            characteristic
          }}</p>
      </template>
    </el-table-column>
    <el-table-column prop="back_num" label="自然成交跑单数" width="100" show-overflow-tooltip/>
    <el-table-column prop="pending_and_in_transit_num" label="自然成交待发+在途数" width="100" show-overflow-tooltip/>
    <el-table-column prop="exposure" label="曝光量" width="120" sortable show-overflow-tooltip>
      <template #default="scope">
        <p :style="{
              backgroundColor: '#409eff',
              color: '000000FF',
              width: scope.row.exposure > scope.row.cart_exposure ? '100%' : (scope.row.exposure / scope.row.cart_exposure * 100) + '%'
            }">
          {{ scope.row.exposure }}
        </p>
        <br>
        <p :style="{
              backgroundColor: '#d7a51d',
              color: '000000FF',
              width: scope.row.cart_exposure > scope.row.exposure ? '100%' : (scope.row.cart_exposure / scope.row.exposure * 100) + '%'
            }">
          {{ scope.row.cart_exposure }}
        </p>
      </template>
    </el-table-column>
    <el-table-column label="曝光点击率" width="100" show-overflow-tooltip>
      <template #default="scope">
        <p>
          {{ (scope.row.clickExposure * 100).toFixed(2) + '%' }}
        </p>
        <br>
        <p>
          {{ (scope.row.cart_clickExposure * 100).toFixed(2) + '%' }}
        </p>
      </template>
    </el-table-column>
    <el-table-column label="点击成交率" width="100" show-overflow-tooltip>
      <template #default="scope">
        <p>
          {{ (scope.row.clickDeal * 100).toFixed(2) + '%' }}
        </p>
        <br>
        <p>
          {{ (scope.row.cart_clickDeal * 100).toFixed(2) + '%' }}
        </p>
      </template>
    </el-table-column>
    <el-table-column prop="salesPrice" label="销售金额" width="100" sortable show-overflow-tooltip>
      <template #default="scope">
        <p :style="{
              backgroundColor: '#409eff',
              color: '000000FF',
              width: scope.row.salesPrice > scope.row.cart_salesPrice ? '100%' : (scope.row.salesPrice / scope.row.cart_salesPrice * 100) + '%'
            }">
          {{ scope.row.salesPrice }}
        </p>
        <br>
        <p :style="{
              backgroundColor: '#d7a51d',
              color: '000000FF',
              width: scope.row.cart_salesPrice > scope.row.salesPrice ? '100%' : (scope.row.cart_salesPrice / scope.row.salesPrice * 100) + '%'
            }">
          {{ scope.row.cart_salesPrice }}
        </p>
      </template>
    </el-table-column>
    <el-table-column prop="salesNum" label="件数" width="80" sortable show-overflow-tooltip>
      <template #default="scope">

        <p :style="{
              backgroundColor: '#409eff',
              color: '000000FF',
              width: scope.row.salesNum > scope.row.cart_salesNum ? '100%' : (scope.row.salesNum / scope.row.cart_salesNum * 100) + '%'
            }">
          {{ scope.row.salesNum }}
        </p>
        <br>
        <p :style="{
            backgroundColor: '#d7a51d',
            color: '000000FF',
            width: scope.row.cart_salesNum > scope.row.salesNum ? '100%' : (scope.row.cart_salesNum / scope.row.salesNum * 100) + '%'
          }">

          {{ scope.row.cart_salesNum }}
        </p>
      </template>
    </el-table-column>

    <el-table-column align="center" prop="order_number" label="广告结算订单数" width="80" sortable
                     show-overflow-tooltip>
      <template #default="scope">

        <p>
          {{ scope.row.order_number }}
        </p>
        <br>


      </template>
    </el-table-column>

    <el-table-column prop="order_rate" label="广告结算成本" width="100" sortable show-overflow-tooltip/>
    <el-table-column prop="back_rate" label="退款订单数占比" width="100" sortable show-overflow-tooltip>
      <template #default="scope">

        <p>

          {{ scope.row.back_rate ? ((1 - scope.row.back_rate) * 100).toFixed(2) + '%' : '' }}
        </p>
        <br>


      </template>
    </el-table-column>
    <el-table-column prop="clickDeal2" label="千川点击转化率" width="100" sortable show-overflow-tooltip>
      <template #default="scope">

        <p>
          {{ (scope.row.clickDeal2 * 100).toFixed(2) + '%' }}
        </p>
        <br>


      </template>
    </el-table-column>

    <el-table-column prop="GPM" label="GPM" width="80" sortable show-overflow-tooltip>
      <template #default="scope">
        <p>
          {{ scope.row.GPM }}
        </p>
        <br>

      </template>
    </el-table-column>


    <el-table-column fixed="right" label="购物车" width="100">
      <template #default="scope">
        <el-button
            link
            type="primary"
            size="small"
            @click.prevent="addCart(scope.row.code)"
        >
          加入购物车
        </el-button>
      </template>
    </el-table-column>


  </el-table>
</template>

<script setup>

import {useRoute} from 'vue-router';
import {computed} from 'vue';
import room from "../api/room.js";
import FileSaver from 'file-saver';
import {watch, ref} from "vue";
import {ElMessage} from "element-plus";
import cart from "../api/cart.js";
import home from "../api/home.js";
import {format} from 'date-fns'
import * as XLSX from "xlsx";
import * as echarts from 'echarts/core';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent
} from 'echarts/components';
import {LineChart, ScatterChart} from 'echarts/charts';
import {CanvasRenderer} from 'echarts/renderers';


echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  LineChart,
  CanvasRenderer,
  ScatterChart
]);

const updateCode = (code, img, id, number) => {
  room.update_code(code, img, id, number).then(response => {
  }).catch(err => {
    console.log(err)
  })
}

//备注
let notes = ref('无')
//是否可编辑备注
let show_notes = ref(true)
// 该商品本次开始讲解时的金额
let start_market_price = ref(0)
// 该商品本次讲解的金额
let market_price = ref(0)

// 获取所有客户信息
const getRoomDate = () => {
  home.roomAll().then(response => {
    home.loading = false;
    home.new_user_list = response.data
  }).catch(err => {
    console.log(err)
  })
}
getRoomDate()


// 计算出每个某个用户的分数
const getSumScore = (name) => {
  const matchedUser = home.new_user_list.find(user => user.name === name);
  if (matchedUser) {
    return matchedUser;
  } else {
    return "";
  }
}

const getProductCode = (code) => {
  const ProductCodeInfos = room.product_info.filter(info => info.code.includes(code.slice(1)));
  if (ProductCodeInfos) {
    return ProductCodeInfos;
  } else {
    return [];
  }
}

const route = useRoute();
// 是否开始抓取
let run = ref(true)
// 是否停止抓取
let close = ref(false)
// 定时器
let intervalId;
// 运行出错的次数
let err_num = 0


// 抓取直播间信息
const runGetGoods = () => {
  // 开启抓取弹幕
  room.Barrage(route.params.room_name).then(response => {
  }).catch(err => {
    console.log(err)
  })
  // 定义抓取直播间数据函数
  const execute = () => {
    if (room.room_id === null) {
      alert('请输入room_id')
      return
    }
    run.value = false
    close.value = true
    // 直播间名称
    const room_name = route.params.room_name

    const now = new Date();
    const hours = now.getHours();
    const minutes = ("0" + now.getMinutes()).slice(-2);
    const seconds = now.getSeconds();
    // 获取当前的时间
    const time = hours + ':' + minutes + ":" + seconds
    room.run(room_name).then(response => {
      ElMessage({
        message: '抓取成功',
        type: 'success',
      })
      room.message.push(time + '抓取成功')
      err_num = 0
      // 每次抓取成功重新渲染一次数据
      getRoomBack()
    }).catch(err => {
      // 当运行出错次数达到10次时关闭定时器
      err_num = err_num + 1
      if (err_num >= 10) {
        // 断开websocket连接
        socket2.close();
        // 关闭定时任务
        closeGetGoods();
        return; // Added return statement to prevent further execution
      }
      room.message.push(time + '抓取失败')
      ElMessage.error(err)
    })
  }

  // 执行第一次
  execute()

  // 设置间隔，每5秒执行一次
  intervalId = setInterval(execute, 5 * 1000);
}
const closeGetGoods = () => {
  run.value = true
  close.value = false
  if (intervalId) {
    clearInterval(intervalId);  // 停止setInterval
  }
}


// 计算出销售金额总和
const totalSalesPrice = computed(() => {
  let salesPriceSum = 0;
  let cartSalesPriceSum = 0;
  for (const item of room.room_list) {
    // 本场销售金额总和
    salesPriceSum += item.salesPrice;
    // 上一场销售金额总和
    cartSalesPriceSum += item.cart_salesPrice;
  }
  return {salesPrice: salesPriceSum, cart_salesPrice: cartSalesPriceSum};
});

// 计算出本场销售数量总和
const totalSalesNum = computed(() => {
  let salesNumSum = 0;
  for (const item of room.room_list) {
    salesNumSum += item.salesNum;
  }
  return salesNumSum;
});
// 计算出上场销售数量总和
const totalCartSalesNum = computed(() => {
  let cartSalesNumSum = 0;
  for (const item of room.room_list) {
    cartSalesNumSum += item.cart_salesNum;
  }
  return cartSalesNumSum;
});


// 本次讲解增加的曝光量
let add_product_show_ucnt = ref(0)
// 本次讲解增加的点击量
let add_product_click_ucnt = ref(0)
// 点击率
let success_rate = ref(0)
// 本次讲解增加的销量
let add_pay_combo_cnt = ref(0)
// 本次讲解增加的总曝光人数
let add_room_live_exposure_sum = ref(0)
// 本次讲解增加的总进入直播间人数
let add_in_room_live = ref(0)

//和上面的值一样作用也一样
// 本次讲解增加的点击量
let DZ = ref(0)
// 本次讲解增加的曝光量
let C = ref(0)
//总曝光次
const room_live_exposure_sum = ref(0)
// 进入直播间-广告
const enter_room_ad = ref(0)
// 点击商品-广告
const click_product_ad = ref(0)
// 创建订单-广告
const create_order_ad = ref(0)
// 成交订单-广告
const deal_order_ad = ref(0)
// 进入直播间-自然
const enter_room_organic = ref(0)
// 点击商品-自然
const click_product_organic = ref(0)
// 创建订单-自然
const create_order_organic = ref(0)
// 成交订单-自然
const deal_order_organic = ref(0)
//商品曝光人数
const product_exposure_users = ref(0)
//商品点击人数
const product_click_users = ref(0)
//金额
const cumulative_deal_amount = ref(0)
const getRoomBack = () => {
  // 直播间名称
  const room_name = route.params.room_name
  room.getRoomInfo(room_name).then(response => {

    getProductInfo()
    // 商品信息
    room.room_list = response.data.data1
    if (response.data.data2) {
      //规程和库存量
      room.integration = response.data.data2
      if (room.integration[0].specification_sales) {
        room.salesArray = room.integration[0].specification_sales.split(' ')
      }
    }
    if (response.data.data3) {
      // 本次讲解商品的整合表数据
      if (room.live_code !== response.data.data4) {
        addProductInfo()
        room.sale_text_list = ["备注1", "备注2", "备注3", "备注4"]
        room.live_code = response.data.data4
        room.room_live_code = response.data.data4
        // 当讲解中的商品发生改变清空之前的数据重新计算
        room.add_dict = {}
        room.product_info_add_dict = {}
        notes.value = '无'
        // 获取本场的金额
        start_market_price.value = response.data.data3.market_price
      } else {
        // 如果商品没有改变就计算本次讲解增加的金额
        market_price.value = response.data.data3.market_price - start_market_price.value
      }

      room.live_data = response.data.data3

      // 总曝光次
      room_live_exposure_sum.value = room.live_data.room_live_exposure_sum
      enter_room_ad.value = room.live_data.in_room_live1
      click_product_ad.value = room.live_data.click_product_ad1
      create_order_ad.value = room.live_data.create_order_ad1
      deal_order_ad.value = room.live_data.deal_order_ad1
      enter_room_organic.value = room.live_data.in_room_live2
      click_product_organic.value = room.live_data.click_product_ad2
      create_order_organic.value = room.live_data.create_order_ad2
      deal_order_organic.value = room.live_data.deal_order_ad2
      product_exposure_users.value = room.live_data.product_show_ucnt
      product_click_users.value = room.live_data.product_click_ucnt
      cumulative_deal_amount.value = room.live_data.market_price
      LiveRoomData()
      updateCode(room.room_live_code, room.integration[0].img, room.integration[0].product_id, room.live_data.pay_combo_cnt)

      if (!room.add_dict.hasOwnProperty(response.data.data4)) {
        room.add_dict[response.data.data4] = {
          'product_show_ucnt': room.live_data.product_show_ucnt,
          'product_click_ucnt': room.live_data.product_click_ucnt,
          'pay_combo_cnt': room.live_data.pay_combo_cnt,
          'room_live_exposure_sum': room.live_data.room_live_exposure_sum,
          'in_room_live': room.live_data.in_room_live,
        }
        add_product_click_ucnt.value = room.live_data.product_click_ucnt
        add_product_show_ucnt.value = room.live_data.product_show_ucnt
        add_pay_combo_cnt.value = room.live_data.pay_combo_cnt
        add_room_live_exposure_sum.value = room.live_data.room_live_exposure_sum
        add_in_room_live.value = room.live_data.in_room_live
      } else {
        C.value = room.live_data.product_show_ucnt - room.add_dict[response.data.data4]['product_show_ucnt']
        DZ.value = room.live_data.product_click_ucnt - room.add_dict[response.data.data4]['product_click_ucnt']
        add_pay_combo_cnt.value = room.live_data.pay_combo_cnt - room.add_dict[response.data.data4]['pay_combo_cnt']
        add_room_live_exposure_sum.value = room.live_data.room_live_exposure_sum - room.add_dict[response.data.data4]['room_live_exposure_sum']
        add_in_room_live.value = room.live_data.in_room_live - room.add_dict[response.data.data4]['in_room_live']
        add_product_click_ucnt.value = DZ.value
        add_product_show_ucnt.value = C.value
        room.live_code = response.data.data4
        success_rate.value = (C.value === 0 || DZ.value / C.value > 0.9) ? '' : DZ.value / C.value
      }
      room.product_info_add_dict[response.data.data4] = {
        "add_product_show_ucnt": add_product_show_ucnt.value,
        "add_product_click_ucnt": add_product_click_ucnt.value,
        "success_rate": success_rate.value,
        "add_pay_combo_cnt": add_pay_combo_cnt.value,
        "add_room_live_exposure_sum": add_room_live_exposure_sum.value,
        "add_in_room_live": add_in_room_live.value,
        "click_rate": (success_rate.value === '') ? '' : (success_rate.value * 100).toFixed(2) + '%',
        "deal_rate": (add_pay_combo_cnt.value / DZ.value * 100).toFixed(2) + '%',
        "in_live_rate": ((add_in_room_live.value / add_room_live_exposure_sum.value) * 100).toFixed(2) + "%",
        'time': 1,
      }
      setInterval(function () {
        if (room.product_info_add_dict[response.data.data4]) {
          room.product_info_add_dict[response.data.data4].time++;
        }
      }, 1000);
    }
  }).catch(err => {
    console.log(err)
  })
}
getRoomBack()


//添加商品讲解信息
const addProductInfo = () => {
  room.ProductInfo(route.params.room_name).then(response => {
  }).catch(err => {
    console.log(err)
  })
}

// 判断更改进度条的颜色
const getColor = percentage => {
  if (percentage < 50) {
    return '#F56C6C' // 绿色
  } else if (percentage < 75) {
    return '#E6A23C' // 橙色
  } else {
    return '#67C23A' // 红色
  }
}


// 更改直播价
const editOrderPrice = (code, price) => {
  room.show_input1 = false
  room.editOrderPrice(code, price).then(response => {
    ElMessage({
      message: "更改成功",
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error("修改失败")
  })
}

// 场次的筛选条件
const options = [
  // 搜索条件
  {
    value: '第一场',
    label: '第一场',
  },
  {
    value: '第二场',
    label: '第二场',
  },
  {
    value: '第三场',
    label: '第三场',
  },
]

// 修改款号
const editCode = (id, code) => {
  room.editingRow = null
  room.editCode(id, code).then(response => {
    ElMessage({
      message: "修改成功",
      type: 'success',
    })
    getRoomBack()
  }).catch(err => {
    ElMessage.error(err)
  })
}


// 监听日期和场次展示对应的数据
watch(
    () => [room.session, room.date_time],
    () => {
      getRoomBack()
    }
)

const exportFields = [
  {key: 'datetime', label: '时间点-月日时秒'},
  {key: 'total_exposure', label: '总曝光'},
  {key: 'enter_room_ad', label: '进入直播间-广告'},
  {key: 'click_product_ad', label: '点击商品-广告'},
  {key: 'create_order_ad', label: '创建订单-广告'},
  {key: 'deal_order_ad', label: '成交订单-广告'},
  {key: 'enter_room_organic', label: '进入直播间-自然'},
  {key: 'click_product_organic', label: '点击商品-自然'},
  {key: 'create_order_organic', label: '创建订单-自然'},
  {key: 'deal_order_organic', label: '成交订单-自然'},
  {key: 'product_sequence', label: '商品序号'},
  {key: 'product_code', label: '商品款号'},
  {key: 'ad_gmv', label: '广告GMV'},
  {key: 'expenditure', label: '消耗'},
  {key: 'product_ctr', label: '商品千次曝光成交'},
  {key: 'ad_settlement_orders', label: '广告结算订单数'},
  {key: 'ad_deal_orders', label: '广告成交订单数'},
  {key: 'ad_settlement_cost', label: '广告结算成本'},
  {key: 'click_deal_conversion_rate', label: '点击成交转化率'},
  {key: 'product_exposure_users', label: '商品曝光人数'},
  {key: 'product_click_users', label: '商品点击人数'},
  {key: 'cumulative_deal_amount', label: '累计成交金额'},
  {key: 'cumulative_deal_orders', label: '累计成交订单数'},
  {key: 'room_name', label: '直播间名称'},
]

const exportRoom = () => {
  room.getLiveRoomData(route.params.room_name).then(response => {
    const sheet = XLSX.utils.json_to_sheet(response.data.map(item => {
      const row = {};
      exportFields.forEach(field => {
        row[field.label] = item[field.key];
      });
      return row;
    }));
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, sheet, 'Sheet1');
    const filename = 'table.xlsx';
    const wbout = XLSX.write(workbook, {bookType: 'xlsx', type: 'array'});
    const blob = new Blob([wbout], {type: 'application/octet-stream'});
    FileSaver.saveAs(blob, filename);
  }).catch(err => {
    console.log(err)
  })
}

// 添加商品到购物车
const addCart = (code) => {
  name = route.params.room_name.substring(0, 2) + '购物车'
  cart.addCart(code, name, route.params.room_name).then(response => {
    ElMessage({
      message: "添加成功",
      type: 'success',
    })
  }).catch(err => {
    ElMessage.error(err)
  })
}
// 进入弹幕的websocket
let socket2 = new WebSocket(`ws://192.168.1.137:8000/ws/barrage/${route.params.room_name}`);
socket2.onmessage = function (event) {
  const item = JSON.parse(event.data).content
  const name = item["nick_name"];
  const content = item["content"];
  const tags = item["tags"];

  if (room.not_name.includes(name) || room.not_content.includes(content)) {
    // 在黑名单中，不执行任何操作
    return;
  }
  // 不在黑名单中，将{name: content}对象添加到room.banner数组中
  room.banner.push({name, content, tags});
  // 获取最后4名用户发送的弹幕，如果有多条就显示最新的两条记录
  let map = new Map();
  for (let i = room.banner.length - 1; i >= 0; i--) {
    let item = room.banner[i];
    if (map.has(item.name)) {
      map.get(item.name).content.push(item.content);
    } else if (map.size < 5) {
      map.set(item.name, {name: item.name, content: [item.content]});
    }
    if (map.size >= 5) break;
    room.result = Array.from(map.values()).reverse();
  }

}
const getProductInfo = () => {
  room.getProductInfo(route.params.room_name).then(response => {
    room.product_info = response.data
  }).catch(err => {
    console.log(err)
  })
}


const formatMyDate = (dateString) => {
  if (!dateString) return '日期未定义';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return '无效的日期';
  return format(date, 'yyyy-MM-dd HH:mm:ss');
}


const LiveRoomData = () => {
  room.LiveRoomData(room_live_exposure_sum.value, enter_room_ad.value, click_product_ad.value, create_order_ad.value,
      deal_order_ad.value, enter_room_organic.value, click_product_organic.value, create_order_organic.value,
      deal_order_organic.value, room.integration[0].product_id, room.room_live_code, product_exposure_users.value,
      product_click_users.value, cumulative_deal_amount.value, room.live_data.pay_combo_cnt, room.room_list, route.params.room_name
  ).then(response => {
    getEcharts2()
    getEcharts3()
    getEcharts4()
  }).catch(err => {
    console.log(err)
  })
}


const chartDom2 = ref(null);
let chartInstance2 = null;
const list2 = ref([])


const getEcharts2 = () => {
  room.getEcharts2(route.params.room_name).then(response => {
    list2.value = []
    response.data.list1.forEach(item => {
      list2.value.push(
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


const chartDom3 = ref(null);
let chartInstance3 = null;
const list3 = ref([])


const getEcharts3 = () => {
  room.getEcharts3(route.params.room_name, room.room_live_code).then(response => {
    list3.value = []
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
  room.getEcharts4(route.params.room_name, room.room_live_code).then(response => {
    list4.value = []
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

<style scoped>
p {
  margin-top: 0.02vw;
  align-content: center;
}

.text {
  font-size: 14px;
}

.item {
  padding: 5px 0;
}

.box-card {
  width: 300px;
}

.el-input {

}

/*.el-card {*/
/*  margin-top: -2vw;*/
/*  margin-left: 15vw;*/
/*}*/
.live_content {
  display: flex;

}

.integration {
  display: flex;
  flex: 1;
  flex-direction: column;
}

.right_live {
  display: flex;
  flex: 1;
  flex-direction: column;
  background-color: #7866FC;
  border-radius: 3%;
}

.right_live_top {
  flex: 1;
  flex-direction: row;
  display: flex;
}

.right_live_top_left {
  flex: 3;
  flex-direction: row;
  display: flex;
  font-size: 50px;
  font-weight: bold;
  color: white;
}

.right_live_top_left_left {
  flex: 5;
  flex-direction: column;
  display: flex;
  justify-content: center; /* 上下居中 */
  text-align: left;
  margin-left: 10px;
}

.right_live_top_left_right {
  flex: 3;
  flex-direction: column;
  display: flex;
  justify-content: center; /* 上下居中 */
  text-align: center;
  margin-right: 40px;

}


.right_live_top_right {
  flex: 1.5;
  display: flex;
  flex-direction: column;
  background-color: #2f3c68;
  border-radius: 20px;
}

.live_title {
  color: white;
  padding-left: 10%;
  padding-top: 10%;
}

.live_num {
  font-size: 30px;
  font-weight: bold;
  color: white;
  padding-left: 10%;

}

.right_live_top_right_top {
  flex: 1;
  display: flex;
  flex-direction: row;
}

.right_live_top_right_bottom {
  flex: 1;
  display: flex;
  flex-direction: row;
}

.right_live_top_right_top_left {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.right_live_top_right_top_right {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.right_live_top_right_bottom_left {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.right_live_top_right_bottom_right {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.right_live_top_left_right span:nth-child(1) {
  font-size: 20px;
  font-weight: bold;
  color: white;
  padding-left: 20%;
}

.right_live_top_left_right span:nth-child(2) {
  font-size: 20px;
  color: white;
  padding-left: 20%;
}

.right_live_top_left_right span:nth-child(3) {
  font-size: 50px;
  font-weight: bold;
  color: white;
  padding-left: 20%;
}


.right_live_bottom {
  flex: 2;
  flex-direction: column;
  display: flex;

}

.right_live_bottom_top {
  flex: 1;

}

.right_live_bottom table {
  text-align: center;
  font-size: 20px;
  margin-left: auto;
  margin-right: auto;
}

.centered-table {
  position: relative;
  top: 50%;
  transform: translateY(-50%);
}

.centered-table2 {
  position: relative;
  top: 0%;
  transform: translateY(-100%);
}


.right_live_bottom table td {
  font-size: 30px;
  color: white;
  width: 20%; /* Set the width of the table cells */
  text-align: center; /* Center the text */
  padding-left: 20px;
}

.right_live_bottom table th {
  font-size: 16px;
  color: #b0b0b0;
  width: 20%; /* Set the width of the table cells */
  text-align: center; /* Center the text */
  padding-left: 30px;
}

.right_live_bottom_bottom {
  flex: 1;
  position: relative;
  top: 50%;
  transform: translateY(-50%);
}

.integration .top {
  display: flex;
  flex: 1;
}

.integration .middle {
  display: flex;
  flex: 2;
  border: 0.8px solid black;
}

.middle_left_top {
  border-right: 0.8px solid black;
  flex: 2;
}

.middle_left_bottom {
  flex: 1;
  display: flex;
  text-align: center;
  font-weight: bold;
  align-items: center;
  justify-content: center;
  border-top: 0.8px solid black;
  border-right: 0.8px solid black;
}

.integration .bottom {
  display: flex;
  flex: 3;
}

.top_left {
  flex: 1;
  background-color: #FFFF00;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60px;
  color: red;
  font-weight: bold;
}


.top_right {
  border-collapse: collapse;
  border: 0.8px solid black;
  flex: 5;

}

.top_right th, .top_right td {
  border: 0.5px solid black;
  text-align: center;
  font-weight: bold;
}

.middle_left {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.middle_right {
  flex: 5;
  flex-direction: column;
  background-color: #EBF1DE;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  white-space: pre-line;
  font-size: 1.3vw;
}

.bottom_left {
  flex: 3;
  display: flex;
  flex-direction: column;
  border: 0.8px solid black;
}

.bottom_right {
  display: flex;
  flex-direction: column;
  flex: 2;

}

.bottom_right_top {
  flex: 2;
  display: flex;
}

.bottom_right_bottom {
  display: flex;
  flex-direction: column;
  flex: 1;
  border: 0.8px solid black;
}

.bottom_right_bottom_top {
  display: flex;
  align-items: center;
  flex: 1;
  border-bottom: 0.8px solid black;
  justify-content: center;
  font-weight: bold;
}

.bottom_right_bottom_bottom {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  font-weight: bold;
}

.bottom_left_div {
  flex: 1;
  display: flex;
}

.bottom_left_div1 {
  flex-direction: column;
  display: flex;
  flex: 0.7;
  border: 0.8px solid black;
  font-weight: bold;
}

.bottom_left_div1 p:nth-child(1) {
  display: flex;
  flex: 1;

  align-items: center;
  justify-content: center;
}

.bottom_left_div1 p:nth-child(2) {
  display: flex;
  flex: 4;
  color: red;
  font-size: 20px;
  align-items: center;
  justify-content: center;
}

.bottom_left_div2 {
  display: flex;
  align-items: center;
  font-size: 25px;
  flex: 0.8;
  border: 0.8px solid black;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.bottom_left_div3 {
  display: flex;
  flex: 1;
  border: 0.2px solid #7c858c;
  color: white;
  font-weight: bold;
  font-size: 20px;
  align-items: center;
  justify-content: center;
  text-align: center;
  background-color: #3c4c8a;
}

.bottom_right_top_left {
  background-color: #EBF1DE;
  flex: 3;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-weight: bold;
  font-size: 1.2vw;
}

.bottom_right_top_left_left {
  background-color: #EBF1DE;
  flex: 1.5;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-weight: bold;
  font-size: 1.2vw;
}

.bottom_right_top_left_right {
  background-color: #EBF1DE;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-weight: bold;
  font-size: 1.2vw;
}

.bottom_right_top_right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-weight: bold;
  border: 0.8px solid black;
  border-top: none;
}
</style>