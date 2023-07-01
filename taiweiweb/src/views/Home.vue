<template>
  <div class="head">
    <div class="left">
      <div>
        <el-tag> -后面代表最后上传日期
        </el-tag>
        <br/>
        <el-dialog :width="600" v-model="home.show_update">
          <Update></Update>
        </el-dialog>
        <el-button v-if="home.update_status[0]" :type="home.buttonType1" @click="home.show_update=true">
          订单数据-{{ home.update_status[0]['date_time'] }}号
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>

        <el-dialog :width="600" v-model="home.show_update_goods">
          <UpdateGoods></UpdateGoods>
        </el-dialog>
        <el-button v-if="home.update_status[2]" :type="home.buttonType3" @click="home.show_update_goods=true">
          货品档案-{{ home.update_status[2]['date_time'] }}号
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>

        <el-dialog :width="600" v-model="home.show_update_commodity">
          <UpdateCommodity></UpdateCommodity>
        </el-dialog>
        <el-button v-if="home.update_status[4]" :type="home.buttonType5" @click="home.show_update_commodity=true">
          30天全量表-{{ home.update_status[4]['date_time'] }}号
          <span></span>
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>
        <el-dialog :width="600" v-model="home.show_update_StockIn">
          <UpdateStockIn></UpdateStockIn>
        </el-dialog>
        <el-button v-if="home.update_status[8]" :type="home.buttonType9" @click="home.show_update_StockIn=true">
          档口调拨表-{{ home.update_status[8]['date_time'] }}号
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>


        <el-dialog :width="600" v-model="home.show_update_repeat_order">
          <UpdateRepeatOredr></UpdateRepeatOredr>
        </el-dialog>
        <el-button v-if="home.update_status[11]" :type="home.buttonType12" @click="home.show_update_repeat_order=true">
          下单简报-{{ home.update_status[11]['date_time'] }}号
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>

      </div>
      <div>
        <el-dialog :width="600" v-model="home.show_update_user">
          <UpdateUser></UpdateUser>
        </el-dialog>
        <el-button v-if="home.update_status[1]" :type="home.buttonType2" @click="home.show_update_user=true">
          用户数据-{{ home.update_status[1]['date_time'] }}号
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>

        <el-dialog :width="600" v-model="home.show_update_stock">
          <UpdateStock></UpdateStock>
        </el-dialog>
        <el-button v-if="home.update_status[6]" :type="home.buttonType7" @click="home.show_update_stock=true">
          多仓库表-{{ home.update_status[6]['date_time'] }}号
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>

        <el-dialog :width="600" v-model="home.show_update_onecommodity">
          <UpdateOneCommodity></UpdateOneCommodity>
        </el-dialog>
        <el-button v-if="home.update_status[5]" :type="home.buttonType6" @click="home.show_update_onecommodity=true">
          &nbsp1天全量表-{{ home.update_status[5]['date_time'] }}号
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>


        <el-dialog :width="600" v-model="home.show_update_SalesRecord">
          <UpdateSalesRecord></UpdateSalesRecord>
        </el-dialog>
        <el-button v-if="home.update_status[9]" :type="home.buttonType10" @click="home.show_update_SalesRecord=true">
          档口销量表-{{ home.update_status[9]['date_time'] }}号
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>

      </div>
      <div>
        <el-dialog :width="600" v-model="home.show_update_size">
          <UpdateSize></UpdateSize>
        </el-dialog>
        <el-button v-if="home.update_status[10]" :type="home.buttonType11" @click="home.show_update_size=true">
          阿良-尺寸信息-{{ home.update_status[10]['date_time'] }}号
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>

        <el-dialog :width="600" v-model="home.show_update_materials">
          <UpdateMaterials></UpdateMaterials>
        </el-dialog>
        <el-button v-if="home.update_status[3]" :type="home.buttonType4" @click="home.show_update_materials=true">
          阿良-辅料记录-{{ home.update_status[3]['date_time'] }}号
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>


        <el-dialog :width="600" v-model="home.show_update_fabric">
          <UpdateFabric></UpdateFabric>
        </el-dialog>
        <el-button v-if="home.update_status[12]" :type="home.buttonType13" @click="home.show_update_fabric=true">
          阿良-面料记录-{{ home.update_status[12]['date_time'] }}号
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>

        <el-dialog :width="600" v-model="home.show_update_factory">
          <UpdateFactory></UpdateFactory>
        </el-dialog>
        <el-button v-if="home.update_status[13]" :type="home.buttonType14" @click="home.show_update_factory=true">
          工厂表-{{ home.update_status[13]['date_time'] }}号
          <el-icon class="el-icon--right">
            <Upload/>
          </el-icon>
        </el-button>
      </div>
      <div></div>
    </div>
    <div class="right">
      <div>
        <el-button color="#CF5BBC" type="primary" @click="exportPageUserExcel"><p style="color: white">
          导出本页汇总数据到Excel</p>
          <el-icon color="white" class="el-icon--right">
            <Download/>
          </el-icon>
        </el-button>
      </div>
      <div>
        <el-button color="#CF5BBC" type="primary" @click="exportUserExcel"><p style="color: white">
          导出所有汇总数据到Excel</p>
          <el-icon color="white" class="el-icon--right">
            <Download/>
          </el-icon>
        </el-button>
      </div>
      <div>

        <el-button color="#F3A627" type="primary" @click="showVipUSer()"><p style="color: white">VIP用户</p>
        </el-button>

        <el-button color="#F3A627" type="primary" @click="showRoom"><p style="color: white">显示直播间数据</p>
        </el-button>


        <el-button color="#F3A627" type="primary" @click="showTracking"><p style="color: white">货品跟踪</p>
        </el-button>
        <el-button color="#F3A627" type="primary" @click="showCodeCommodity"><p style="color: white">全量表款号信息</p>
        </el-button>
        <el-button color="#F3A627" type="primary" @click="showStyleStatus"><p style="color: white">新款状态</p>
        </el-button>
      </div>
      <div>
        <el-button color="#F3A627" type="primary" @click="showReport"><p style="color: white">显示今日报表</p>
        </el-button>
        <el-button color="#F3A627" type="primary" @click="showCart('星露购物车')"><p style="color: white">星露购物车</p>
        </el-button>
        <el-button color="#F3A627" type="primary" @click="showCart('悦仓购物车')"><p style="color: white">悦仓购物车</p>
        </el-button>
        <el-button color="#F3A627" type="primary" @click="showCart('S姐购物车')"><p style="color: white">S姐购物车</p>
        </el-button>


      </div>
      <div>
        <el-button color="#F3A627" type="primary" @click="showRoomBackend('星露直播间')"><p style="color: white">
          星露直播间后台</p>
        </el-button>
        <el-button color="#F3A627" type="primary" @click="showRoomBackend('悦仓直播间')"><p style="color: white">
          悦仓直播间后台</p>
        </el-button>
        <el-button color="#F3A627" type="primary" @click="showRoomBackend('S姐直播间')"><p style="color: white">
          S姐直播间后台</p>
        </el-button>
      </div>
    </div>

  </div>
  <div class="contents">
    <Serach></Serach>


    <el-table :data="home.data_list" style="width: 100%" v-loading="home.loading" border fit v-if="home.is_show_table">
      <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
      <el-table-column prop="order_no" label="主订单编号" width="120" show-overflow-tooltip/>
      <el-table-column prop="sub_order_no" label="子订单编号" width="120" show-overflow-tooltip/>
      <el-table-column prop="product_name" label="选购商品" width="120" show-overflow-tooltip/>
      <el-table-column prop="product_id" label="商品ID" width="120" show-overflow-tooltip/>
      <el-table-column prop="merchant_code" label="商家编码" width="120" show-overflow-tooltip/>
      <el-table-column prop="product_quantity" label="商品数量" sortable width="120" show-overflow-tooltip/>
      <el-table-column prop="product_amount" label="商品金额" sortable width="120" show-overflow-tooltip/>
      <el-table-column prop="order_submit_time" label="订单提交时间" sortable width="140" show-overflow-tooltip/>
      <el-table-column prop="payment_finish_time" label="支付完成时间" sortable width="140" show-overflow-tooltip/>
      <el-table-column prop="order_finish_time" label="订单完成时间" sortable width="140" show-overflow-tooltip/>
      <el-table-column prop="merchant_remark" label="商家备注" width="120" show-overflow-tooltip/>
      <el-table-column prop="order_status" label="订单状态" width="120" show-overflow-tooltip/>
      <el-table-column prop="after_sale_status" label="售后状态" width="120" show-overflow-tooltip/>
      <el-table-column prop="order_total_amount" label="订单应付金额" sortable width="140" show-overflow-tooltip/>
      <el-table-column prop="province" label="省" width="120" show-overflow-tooltip/>
      <el-table-column prop="city" label="市" width="120" show-overflow-tooltip/>
      <el-table-column prop="district" label="区" width="120" show-overflow-tooltip/>
      <el-table-column prop="street" label="街道" width="120" show-overflow-tooltip/>
      <el-table-column prop="influencer_id" label="达人ID" width="120" show-overflow-tooltip/>
      <el-table-column prop="influencer_nickname" label="达人昵称" width="120" show-overflow-tooltip/>
      <el-table-column prop="ad_channel" label="广告渠道" width="120" show-overflow-tooltip/>
    </el-table>


    <el-input v-model="home.searchCode" style="width: 200px" v-if="home.is_show_search3_table"
              placeholder="请输入款号" clearable></el-input>
    <br v-if="home.is_show_search3_table">
    <el-tag v-if="home.is_show_search3_table">按照选择日期，统计区间范围内的千川订单
    </el-tag>
    <el-table :data="home.user_data_list" v-loading="home.loading" style="width: 100%" border fit
              v-if="home.is_show_search3_table" height="600">
      <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
      <el-table-column prop="m" label="款号" width="90" show-overflow-tooltip/>
      <el-table-column label="图片" width="90" show-overflow-tooltip>
        <template #default="scope">
          <el-image style="width: 90px; height: 100px"
                    :src="scope.row.commodity_image"/>
        </template>
      </el-table-column>
      <el-table-column prop="sum_total_amount_3" label="支付跑单金额" width="140" show-overflow-tooltip/>
      <el-table-column prop="sum_product_quantity_3" label="支付跑单数量" width="140" sortable show-overflow-tooltip/>
      <el-table-column prop="sum_total_amount_5" label="成功金额" width="120" show-overflow-tooltip/>
      <el-table-column prop="sum_product_quantity_5" label="成功数量" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="pending_and_in_transit" label="待发+在途" width="120" show-overflow-tooltip/>
      <el-table-column prop="pending_and_in_transit_num" label="数量" width="80" sortable show-overflow-tooltip/>
      <el-table-column prop="returned" label="退回" width="80" show-overflow-tooltip/>
      <el-table-column prop="returned_num" label="数量" width="80" sortable show-overflow-tooltip/>
      <el-table-column prop="inventory" label="库存" width="80" sortable show-overflow-tooltip/>
      <el-table-column label="退款率" width="100" show-overflow-tooltip>
        <template #default="scope">
          {{
            ((((Number(scope.row.returned_num || 0) /
                (Number(scope.row.returned_num || 0) +
                    Number(scope.row.sum_product_quantity_5 || 0) +
                    Number(scope.row.pending_and_in_transit_num || 0))) * 100) || 0).toFixed(2)) + '%'
          }}
        </template>
      </el-table-column>

      <el-table-column label="跑单率" width="100" show-overflow-tooltip>
        <template #default="scope">
          {{
            ((((Number(scope.row.sum_product_quantity_3 || 0) /
                (Number(scope.row.returned_num || 0) +
                    Number(scope.row.sum_product_quantity_5 || 0) +
                    Number(scope.row.pending_and_in_transit_num || 0) +
                    Number(scope.row.sum_product_quantity_3 || 0))) * 100) || 0).toFixed(2)) + '%'
          }}
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="S姐购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.m,'S姐购物车','千川订单')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="悦仓购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.m,'悦仓购物车','千川订单')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="星露购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.m,'星露购物车','千川订单')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-input v-model="home.searchKeyword" style="width: 200px" v-if="home.is_show_search4_table"
              placeholder="请输入名字" clearable></el-input>
    <el-button type="primary" v-if="home.is_show_search4_table" @click="filteredData">搜索</el-button>
    <br v-if="home.is_show_search4_table"/>
    <el-tag v-if="home.is_show_search4_table"> 结束日期就是当前日期，开始日期可选
      成功利润+在途金额*0.5（利润系数）*0.7（发货成功率）= 实际金额 100分打分，退一件扣0.3分
    </el-tag>
    <el-table :data="home.nwe_user_data_list" v-loading="home.loading" style="width: 100%" border fit
              v-if="home.is_show_search4_table" height="550">
      <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
      <el-table-column prop="name" label="名字" width="100" show-overflow-tooltip/>
      <el-table-column prop="first_day" label="最早出现" width="110" show-overflow-tooltip/>
      <el-table-column prop="recently_day" label="最近出现" width="110" show-overflow-tooltip/>
      <el-table-column prop="sum_orders" label="来几次" width="100" show-overflow-tooltip/>
      <el-table-column prop="success_money" label="成功金额" width="100" show-overflow-tooltip/>
      <el-table-column prop="back_money" label="退回金额" width="100" show-overflow-tooltip/>
      <el-table-column prop="wait_money" label="待发货金额" width="100" show-overflow-tooltip/>
      <el-table-column prop="transit_money" label="在途金额" width="100" show-overflow-tooltip/>
      <el-table-column label="退款率" width="80" show-overflow-tooltip>
        <template #default="scope">
          {{ (scope.row.back_rate * 100).toFixed(2) + '%' }}
        </template>
      </el-table-column>
      <el-table-column prop="success_num" label="成功数量" width="100" show-overflow-tooltip/>
      <el-table-column prop="back_num" label="退回数量" width="100" show-overflow-tooltip/>
      <el-table-column prop="wait_num" label="待发货数量" width="100" show-overflow-tooltip/>
      <el-table-column prop="transit_num" label="在途数量" width="100" show-overflow-tooltip/>
      <el-table-column prop="success_rate" label="成功利润" width="100" show-overflow-tooltip/>
      <el-table-column prop="real_rate" label="实际利润" width="100" show-overflow-tooltip/>
      <el-table-column prop="not_day" label="未出现天数" width="100" show-overflow-tooltip/>
      <el-table-column prop="sum_score" label="综合分" width="100" sortable show-overflow-tooltip/>
      <el-table-column prop="new_user" label="新客" width="100" show-overflow-tooltip/>
      <el-table-column fixed="right" label="详细信息" width="120">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addVipUser(scope.row.name)"
          >
            加入VIP
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="详细信息" width="120">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="showUserInfo(scope)"
          >
            查看详细信息
          </el-button>
        </template>
      </el-table-column>
    </el-table>


    <el-input v-model="home.searchCode" style="width: 200px" v-if="home.is_show_search5_table"
              placeholder="请输入款号" clearable></el-input>
    <br v-if="home.is_show_search5_table">
    <el-tag v-if="home.is_show_search5_table"> 结束日期就是当前日期，开始日期可选
    </el-tag>
    <el-table :data="home.user_data_list" v-loading="home.loading" style="width: 100%" border fit
              v-if="home.is_show_search5_table" height="600">
      <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
      <el-table-column prop="name" label="款号" width="80" show-overflow-tooltip/>
      <el-table-column prop="category" label="品类" width="80" show-overflow-tooltip/>
      <el-table-column prop="inventory" label="可卖量" width="80" show-overflow-tooltip/>
      <el-table-column prop="first_day" label="最早出现" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="recently_day" label="最近出现" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="sum_orders" label="来几次" width="100" sortable show-overflow-tooltip/>
      <el-table-column prop="success_money" label="成功金额" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="back_money" label="退回金额" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="wait_money" label="待发货金额" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="transit_money" label="在途金额" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="run_single" label="支付跑单数量" width="140" sortable show-overflow-tooltip/>
      <el-table-column label="退款率" width="80" show-overflow-tooltip>
        <template #default="scope">
          {{ (scope.row.back_rate * 100).toFixed(2) + '%' }}
        </template>
      </el-table-column>
      <el-table-column prop="success_num" label="成功数量" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="back_num" label="退回数量" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="wait_num" label="待发货数量" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="transit_num" label="在途数量" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="success_rate" label="成功利润" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="real_rate" label="实际利润" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="not_day" label="未出现天数" width="120" sortable show-overflow-tooltip/>
    </el-table>


    <el-date-picker
        v-model="home.report_data"
        type="date"
        placeholder="选定日期的往前30天订单记录"
        v-if="home.is_show_report_table"
    />

    <el-date-picker
        v-model="home.report_data_history"
        type="date"
        placeholder="选定日期的每天订单状态变化"
        v-if="home.is_show_report_table"
    />


    <el-table :data="home.report_list" v-loading="home.loading" style="width: 100%" border fit
              v-if="home.is_show_report_table">
      <el-table-column prop="order_submit_time" label="订单产生日期" width="140" sortable show-overflow-tooltip/>
      <el-table-column prop="wait_num" label="待发" width="100" sortable show-overflow-tooltip/>
      <el-table-column prop="remove_num" label="取消" width="100" sortable show-overflow-tooltip/>
      <el-table-column prop="transit_num" label="在途" width="100" sortable show-overflow-tooltip/>
      <el-table-column prop="success_num" label="成功" width="100" sortable show-overflow-tooltip/>
      <el-table-column prop="back_num" label="退回" width="100" sortable show-overflow-tooltip/>
      <el-table-column prop="data_time" label="报表日期" width="120" show-overflow-tooltip/>
      <el-table-column fixed="right" label="详细信息" width="120">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="showCodeInfo(scope)"
          >
            查看详细信息
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-input v-model="home.create_time" style="width: 200px" v-if="home.is_show_search6_table"
              placeholder="请输入日期(2018-2019)" clearable></el-input>
    <el-select v-model="home.season" clearable placeholder="请选择季节" size="default" v-if="home.is_show_search6_table"
               @clear="home.season=null">
      <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
      />
    </el-select>
    <el-input v-model="home.category" style="width: 200px" v-if="home.is_show_search6_table"
              placeholder="请输入品类(可模糊匹配)" clearable></el-input>
    <br v-if="home.is_show_search6_table" height="600">
    <el-tag v-if="home.is_show_search6_table">可卖库存大于5, 30天没播过，结合配去档口的时间，和档口销量选款(30天没播是没有图片的)
    </el-tag>
    <el-table :data="home.user_data_list" v-loading="home.loading" style="width: 100%" border fit
              v-if="home.is_show_search6_table">
      <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
      code
      <el-table-column prop="code" label="款号" width="90" show-overflow-tooltip/>
      <el-table-column prop="category" label="品类" width="90" show-overflow-tooltip/>
      <el-table-column prop="create_time" label="时间" width="120" show-overflow-tooltip/>
      <el-table-column prop="season" label="季节" width="90" show-overflow-tooltip/>
      <el-table-column prop="stock" label="库存" width="80" sortable show-overflow-tooltip/>
      <el-table-column prop="number" label="累计销量" width="110" sortable show-overflow-tooltip/>
      <el-table-column prop="cost" label="成本" width="90" sortable show-overflow-tooltip/>
      <el-table-column prop="sales" label="档口最近15天销量" width="100" sortable show-overflow-tooltip/>
      <el-table-column prop="first_registration_time" label="初次到档口时间" width="120" sortable
                       show-overflow-tooltip/>
      <el-table-column prop="last_registration_time" label="最后到档口时间" width="120" sortable show-overflow-tooltip/>
      <el-table-column fixed="right" label="S姐购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.code,'S姐购物车','A')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="悦仓购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.code,'悦仓购物车','A')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="星露购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.code,'星露购物车','A')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-tag v-if="home.is_show_search7_table">此表是用调拨表，来判断档口热卖款。 有3次或者3次以上调拨记录（采购入库也算），就是热卖款
      显示 款号，货品名称，调拨量，初次到档口时间，最后到档口时间。
    </el-tag>
    <el-table :data="home.user_data_list" v-loading="home.loading" style="width: 100%" border fit
              v-if="home.is_show_search7_table" height="600">
      <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
      <el-table-column prop="product_code" label="货品货号" width="90" show-overflow-tooltip/>
      <el-table-column prop="product_name" label="货品名称" width="100" show-overflow-tooltip/>
      <el-table-column prop="count_quantity" label="档口补单次数" width="120" show-overflow-tooltip/>
      <el-table-column prop="quantity" label="入库数量" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="first_registration_time" label="初次到档口时间" width="120" sortable
                       show-overflow-tooltip/>
      <el-table-column prop="last_registration_time" label="最后到档口时间" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="inventory" label="库存量" width="120" sortable show-overflow-tooltip/>
      <el-table-column fixed="right" label="S姐购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.product_code,'S姐购物车','B')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="悦仓购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.product_code,'悦仓购物车','B')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="星露购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.product_code,'星露购物车','B')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-tag v-if="home.is_show_search8_table">此表是用调拨表，来判断档口滞销款
      最后配去档口，过去6天以上（最近6天还有调拨的，说明还在动），最近15天只有0-2人开单，并且最近15天开单量总数小于10
    </el-tag>
    <el-table :data="home.user_data_list" v-loading="home.loading" style="width: 100%" border fit
              v-if="home.is_show_search8_table" height="600">
      <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
      <el-table-column prop="product_code" label="款号" width="90" show-overflow-tooltip/>
      <el-table-column prop="product_name" label="货品名称" width="120" show-overflow-tooltip/>
      <el-table-column prop="count_quantity" label="总补单次" width="120" show-overflow-tooltip/>
      <el-table-column prop="quantity" label="总调拨量" width="120" show-overflow-tooltip/>
      <el-table-column prop="first_registration_time" label="初次到档口时间" width="120" sortable
                       show-overflow-tooltip/>
      <el-table-column prop="last_registration_time" label="最后到档口时间" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="inventory" label="库存量" width="120" sortable show-overflow-tooltip/>
      <el-table-column fixed="right" label="S姐购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.product_code,'S姐购物车','C')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="悦仓购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.product_code,'悦仓购物车','C')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="星露购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.product_code,'星露购物车','C')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
    </el-table>


    <el-select v-model="home.day" clearable placeholder="请选择最近几天" size="default"
               v-if="home.is_show_search9_table"
               @clear="home.day=null">
      <el-option
          v-for="item in day_list"
          :key="item.value"
          :label="item.label"
          :value="item.value"
      />
    </el-select>
    <br v-if="home.is_show_search9_table"/>
    <el-tag v-if="home.is_show_search9_table">最近3天的，每天全量表， 成交金额前5
    </el-tag>
    <el-table :data="home.user_data_list" v-loading="home.loading" style="width: 100%" border fit
              v-if="home.is_show_search9_table" height="600">
      <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
      <el-table-column prop="code" label="款号" width="90" show-overflow-tooltip/>
      <el-table-column prop="category" label="货品名称" width="120" show-overflow-tooltip/>
      <el-table-column prop="price" label="单价" width="120" show-overflow-tooltip/>
      <el-table-column label="图片" width="100">
        <template #default="scope">
          <el-image style="width: 90px; height: 100px"
                    :src="scope.row.commodity_image"/>
        </template>
      </el-table-column>
      <el-table-column prop="inventory" label="库存" width="120" show-overflow-tooltip/>
      <el-table-column prop="order_quantity" label="订购量" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="live_deal_item_count" label="成交件数" width="120" sortable show-overflow-tooltip/>
      <el-table-column label="转换率" width="120" sortable show-overflow-tooltip>
        <template #default="scope">
          {{ (scope.row.live_deal_conversion_rate * 100).toFixed(2) + '%' }}
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="S姐购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.code,'S姐购物车','D')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="悦仓购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.code,'悦仓购物车','D')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="星露购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.code,'星露购物车','D')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
    </el-table>


    <el-input v-model="home.create_time" style="width: 200px" v-if="home.is_show_search10_table"
              placeholder="请输入日期(2018-2019)" clearable></el-input>
    <el-select v-model="home.season" clearable placeholder="请选择季节" size="default"
               v-if="home.is_show_search10_table"
               @clear="home.season=null">
      <el-option
          v-for="item in options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
      />
    </el-select>
    <el-input v-model="home.category" style="width: 200px" v-if="home.is_show_search10_table"
              placeholder="请输入品类(可模糊匹配)" clearable></el-input>
    <br v-if="home.is_show_search10_table">
    <el-tag v-if="home.is_show_search10_table"> 此表是最后几件库存， 结合档口，热卖程度，进行选款判断。
    </el-tag>
    <el-table :data="home.user_data_list" v-loading="home.loading" style="width: 100%" border fit
              v-if="home.is_show_search10_table" height="600">
      <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
      <el-table-column prop="merchant_code" label="款号" width="90" show-overflow-tooltip/>
      <el-table-column prop="category" label="品类" width="90" show-overflow-tooltip/>
      <el-table-column prop="create_time" label="时间" width="120" show-overflow-tooltip/>
      <el-table-column prop="season" label="季节" width="90" show-overflow-tooltip/>
      <el-table-column prop="date_time" label="最近播的日子" width="120" show-overflow-tooltip/>
      <el-table-column prop="live_exposure_count" label="最近播的直播间曝光" width="120" show-overflow-tooltip/>
      <el-table-column prop="one_live_deal_item_count" label="销量" width="80" show-overflow-tooltip/>
      <el-table-column prop="quantity" label="档口15天销量" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="first_time" label="第一次去档口时间" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="last_time" label="最后一次去档口时间" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="inventory" label="库存" width="80" sortable show-overflow-tooltip/>
      <el-table-column prop="live_deal_item_count" label="30天全量表的销量" width="120" sortable show-overflow-tooltip/>
      <el-table-column fixed="right" label="S姐购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.merchant_code,'S姐购物车','E')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="悦仓购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.merchant_code,'悦仓购物车','E')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="星露购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.merchant_code,'星露购物车','E')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
    </el-table>


    <el-input v-model="home.searchCode" style="width: 200px" v-if="home.is_show_search11_table"
              placeholder="请输入款号" clearable></el-input>
    <br v-if="home.is_show_search11_table">
    <el-table :data="home.user_data_list" v-loading="home.loading" style="width: 100%" border fit
              v-if="home.is_show_search11_table" height="600">
      <el-table-column type="index" label="序号" width="60" show-overflow-tooltip/>
      <el-table-column prop="code" label="款号" width="80" show-overflow-tooltip/>
      <el-table-column prop="category" label="品类" width="90" show-overflow-tooltip/>
      <el-table-column label="图片" width="120" show-overflow-tooltip>
        <template #default="scope">
          <el-image style="width: 90px; height: 100px"
                    :src="scope.row.commodity_image"/>
        </template>
      </el-table-column>
      <el-table-column prop="inventory" label="库存" width="60" show-overflow-tooltip/>
      <el-table-column prop="order_quantity" label="订购量" width="70" show-overflow-tooltip/>
      <el-table-column prop="price" label="单价" width="60" show-overflow-tooltip/>
      <el-table-column prop="live_deal_item_count" label="成交件数" width="110" sortable show-overflow-tooltip/>
      <el-table-column label="发货前退款率" width="120" show-overflow-tooltip>
        <template #default="scope">
          {{ (scope.row.pre_shipment_refund_rate * 100).toFixed(2) + '%' }}
        </template>
      </el-table-column>
      <el-table-column label="发货后退款率" width="120" show-overflow-tooltip>
        <template #default="scope">
          {{ (scope.row.post_shipment_refund_rate * 100).toFixed(2) + '%' }}
        </template>
      </el-table-column>
      <el-table-column prop="order_submit_time" label="订单表第一次上架日期" width="120" show-overflow-tooltip/>
      <el-table-column prop="one_live_exposure_count" label="最近直播间曝光" width="120" show-overflow-tooltip/>
      <el-table-column prop="one_live_deal_item_count" label="销量" width="80" sortable show-overflow-tooltip/>
      <el-table-column prop="quantity" label="档口最近15天销量" width="100" sortable show-overflow-tooltip/>
      <el-table-column prop='first_registration_time' label="初次到档口时间" width="110" sortable
                       show-overflow-tooltip/>
      <el-table-column prop='last_registration_time' label="最后到档口时间" width="110" sortable show-overflow-tooltip/>
      <el-table-column fixed="right" label="S姐购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.merchant_code,'S姐购物车','F')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="悦仓购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.merchant_code,'悦仓购物车','F')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="星露购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.merchant_code,'星露购物车','F')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
    </el-table>


    <el-table :data="home.user_data_list" v-loading="home.loading" style="width: 100%" border fit
              v-if="home.is_show_search12_table" height="600">
      <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
      <el-table-column prop="code" label="款号" width="90" show-overflow-tooltip/>
      <el-table-column prop="category" label="货品名称" width="120" show-overflow-tooltip/>
      <el-table-column prop="price" label="单价" width="120" show-overflow-tooltip/>
      <el-table-column label="图片" width="100">
        <template #default="scope">
          <el-image style="width: 90px; height: 100px"
                    :src="scope.row.commodity_image"/>
        </template>
      </el-table-column>
      <el-table-column prop="inventory" label="库存" width="120" show-overflow-tooltip/>
      <el-table-column prop="order_quantity" label="订购量" width="120" sortable show-overflow-tooltip/>
      <el-table-column prop="live_deal_item_count" label="成交件数" width="120" sortable show-overflow-tooltip/>
      <el-table-column label="转换率" width="120" sortable show-overflow-tooltip>
        <template #default="scope">
          {{ (scope.row.live_deal_conversion_rate * 100).toFixed(2) + '%' }}
        </template>
      </el-table-column>
      <el-table-column prop="date_time" label="日期" width="120" sortable show-overflow-tooltip/>
      <el-table-column fixed="right" label="S姐购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.code,'S姐购物车','D')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="悦仓购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.code,'悦仓购物车','D')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="星露购物车" width="100">
        <template #default="scope">
          <el-button
              link
              type="primary"
              size="small"
              @click.prevent="addCart(scope.row.code,'星露购物车','D')"
          >
            加入购物车
          </el-button>
        </template>
      </el-table-column>
    </el-table>


    <div class="demo-pagination-block">
      <el-pagination
          v-model:current-page="home.page"
          v-model:page-size="home.size"
          :page-sizes="[10, 50, 100,500,home.count]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="home.count"
      />
    </div>
  </div>

</template>

<script setup>
import home from "../api/home.js";
import {h, reactive, ref, watch} from "vue";
import {Upload, Search, Download} from '@element-plus/icons-vue'
import Serach from "../components/Search.vue";
import * as XLSX from 'xlsx';
import FileSaver from 'file-saver';
import {ElMessage} from "element-plus";
import Update from "../components/Update.vue";
import UpdateGoods from "../components/UpdateGoods.vue";
import UpdateMaterials from "../components/UpdateMaterials.vue";
import UpdateSalesRecord from "../components/UpdateSalesRecord.vue";
import cart from "../api/cart.js";
import UpdateRepeatOredr from "../components/UpdateRepeatOredr.vue";
import UpdateFabric from "../components/UpdateFabric.vue";
import UpdateFactory from "../components/UpdateFactory.vue";


// 下拉框数据
const options = [
  // 搜索条件
  {
    value: '10-11月',
    label: '10-11月',
  },
  {
    value: '6-7月',
    label: '6-7月',
  },
  {
    value: '8-9月',
    label: '8-9月',
  },
  {
    value: '4-5月',
    label: '4-5月',
  },
  {
    value: '过年12月-1月',
    label: '过年12月-1月',
  },
  {
    value: '四季',
    label: '四季',
  },
  {
    value: '早春2-3月',
    label: '早春2-3月',
  },
]
const day_list = [
  {
    value: 3,
    label: '3天',
  },
  {
    value: 5,
    label: '5天',
  },
]

// 获取订单信息
const show_tables = () => {
  home.show().then(response => {
    home.count = response.data.count
    home.data_list = response.data.results
    home.loading = false
  }).catch(err => {
    console.log(err)
  })

}


show_tables()


const addCart = (code, name, source) => {
  /**
   * 添加商品到购物车
   * @param {string} code - 款号
   * @param {string} name - 购物车名字
   * @param {string} source - 来源，从哪个地方加入的购物车
   */
  cart.addCart(code, name, source).then(response => {
    alert("添加成功")
    ElMessage("添加成功")
  }).catch(err => {
    alert("添加失败")
    ElMessage(err)
  })
}

// 打开款号跟踪
const showTracking = () => {
  window.open('/Tracking/', '_blank');
}

// 打开全量表款号信息
const showCodeCommodity = () => {
  window.open('/CodeCommodity/', '_blank');
}

const showCart = (cart_name) => {
  /**
   * 打开购物车页面
   * @param {string} cart_name - 购物车名称
   */
  window.open('/Cart/' + cart_name, '_blank');
}

// 打开VIP用户
const showVipUSer = () => {
  window.open('/VipUser/', '_blank');
}


// 打开用户详情信息
const showUserInfo = (scope) => {
  const url = '/UserInfo/' + scope.row.name + '/' + scope.row.success_num + '/' + scope.row.back_num + '/' +
      (scope.row.wait_num + scope.row.transit_num) + '/' + home.search_date;
  window.open(url, '_blank');
}


// 打开每日报表中的详细信息
const showCodeInfo = (scope) => {
  const url = '/CodeInfo/' + scope.row.order_submit_time + '/' + scope.row.wait_num + '/' + scope.row.remove_num + '/' +
      scope.row.transit_num + '/' + scope.row.success_num + '/' + scope.row.back_num
  window.open(url, '_blank')
}

// 打开显示直播间数据
const showRoom = () => {
  window.open('/Room/', '_blank')
}


// 客户信息排名的搜索
const filteredData = () => {
  home.loading = true   // 设置加载状态为true
  if (home.all_user_data_list.length === 0) {         //如果第一次获取用户信息则发生请求
    home.userAll().then(response => {
      home.all_user_data_list = response.data            //所有的用户信息
      const regex = new RegExp(home.searchKeyword, 'i');  // 创建用于匹配搜索关键字的正则表达式
      home.nwe_user_data_list = response.data.filter(item => regex.test(item.name));  //根据关键字过滤筛选出符合条件的用户
      home.loading = false
    })
  } else {
    const regex = new RegExp(home.searchKeyword, 'i');
    home.nwe_user_data_list = home.all_user_data_list.filter(item => regex.test(item.name));
    home.loading = false
  }

};

//添加vip用户
const addVipUser = (name) => {
  home.addVipUser(name).then(response => {
    ElMessage("添加成功")
  }).catch(err => {
    ElMessage(err)
  })
}

// 显示每日报表
const showReport = () => {
  home.loading = true
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
  home.is_show_search12_table = false
  home.is_show_report_table = true
  home.getReportList().then(response => {
    home.report_list = response.data.results
    home.count = response.data.count
    home.loading = false
  }).catch(err => {
    console.log(err)
  })
}

// 打开直播间后台
const showRoomBackend = (room_name) => {
  window.open('/RoomBack/' + room_name, '_blank')
}

// 打开新款状态
const showStyleStatus = () => {
  window.open('/StyleStatus/', '_blank')
}

// 导出订单信息表格的字段


// 千川订单导出字段
const summary3Fields = [
  {key: 'm', label: '款号'},
  {key: 'sum_total_amount_3', label: '支付跑单金额'},
  {key: 'sum_product_quantity_3', label: '支付跑单数量'},
  {key: 'sum_total_amount_5', label: '成功金额'},
  {key: 'pending_and_in_transit', label: '待发+在途'},
  {key: 'pending_and_in_transit_num', label: '数量'},
  {key: 'returned', label: '退回'},
  {key: 'returned_num', label: '数量'},
  {key: 'inventory', label: '库存'},
];


// 客户信息排名导出字段
const summary4Fields = [
  {key: 'name', label: '名字'},
  {key: 'first_day', label: '最早出现'},
  {key: 'recently_day', label: '最近出现'},
  {key: 'sum_orders', label: '订单出现天数'},
  {key: 'success_money', label: '成功金额'},
  {key: 'back_money', label: '退回金额'},
  {key: 'wait_money', label: '待发货金额'},
  {key: 'transit_money', label: '在途金额'},
  {key: 'back_rate', label: '退款率'},
  {key: 'success_num', label: '成功数量'},
  {key: 'back_num', label: '退回数量'},
  {key: 'wait_num', label: '待发货数量'},
  {key: 'transit_num', label: '在途数量'},
  {key: 'success_rate', label: '成功利润'},
  {key: 'real_rate', label: '实际利润'},
  {key: 'not_day', label: '未出现天数'},
  {key: 'new_user', label: '新客'},
  {key: 'sum_score', label: '综合分'}
];

// 款号信息排名导出字段
const summary5Fields = [
  {key: 'name', label: '款号'},
  {key: 'category', label: '品类'},
  {key: 'inventory', label: '可卖量'},
  {key: 'first_day', label: '最早出现'},
  {key: 'recently_day', label: '最近出现'},
  {key: 'sum_orders', label: '订单出现天数'},
  {key: 'success_money', label: '成功金额'},
  {key: 'back_money', label: '退回金额'},
  {key: 'wait_money', label: '待发货金额'},
  {key: 'transit_money', label: '在途金额'},
  {key: 'run_single', label: '支付跑单数量'},
  {key: 'back_rate', label: '退款率'},
  {key: 'success_num', label: '成功数量'},
  {key: 'back_num', label: '退回数量'},
  {key: 'wait_num', label: '待发货数量'},
  {key: 'transit_num', label: '在途数量'},
  {key: 'success_rate', label: '成功利润'},
  {key: 'real_rate', label: '实际利润'},
  {key: 'not_day', label: '未出现天数'},
];


// 选款库存大于5导出字段
const summary6Fields = [
  {key: 'code', label: '款号'},
  {key: 'category', label: '品类'},
  {key: 'create_time', label: '时间'},
  {key: 'season', label: '季节'},
  {key: 'stock', label: '可卖量'},
  {key: 'number', label: '累计销量'},
  {key: 'cost', label: '成本'},
  {key: 'sales', label: '档口最近15天销量'},
  {key: 'first_registration_time', label: '初次到档口时间'},
  {key: 'last_registration_time', label: '最后到档口时间'},
];

// 档口滞销款导出字段
const summary7Fields = [
  {key: 'product_code', label: '货品货号'},
  {key: 'product_name', label: '货品名称'},
  {key: 'quantity', label: '入库数量'},
  {key: 'first_registration_time', label: '初次到档口时间'},
  {key: 'last_registration_time', label: '最后到档口时间'},
];

// 档口热销款导出字段
const summary8Fields = [
  {key: 'product_code', label: '货品货号'},
  {key: 'registration_time', label: '登记时间'},
  {key: 'recipient', label: '收货人个数'},
  {key: 'quantity', label: '销量'},
];

// 最近几天热卖导出字段
const summary9Fields = [
  {key: 'code', label: '款号'},
  {key: 'category', label: '货品名称'},
  {key: 'price', label: '单价'},
  {key: 'commodity_image', label: '图片'},
  {key: 'inventory', label: '库存'},
  {key: 'order_quantity', label: '订购量'},
  {key: 'live_deal_item_count', label: '成交件数'},
  {key: 'live_deal_conversion_rate', label: '转换率'},
];

// 库存1-5导出字段
const summary10Fields = [
  {key: 'merchant_code', label: '款号'},
  {key: 'category', label: '品类'},
  {key: 'create_time', label: '时间'},
  {key: 'season', label: '季节'},
  {key: 'date_time', label: '最近播的日子'},
  {key: 'live_exposure_count', label: '最近播的直播间曝光'},
  {key: 'one_live_deal_item_count', label: '销量'},
  {key: 'quantity', label: '档口15天销量'},
  {key: 'first_time', label: '第一次去档口时间'},
  {key: 'last_time', label: '最后一次去档口时间'},
  {key: 'inventory', label: '库存'},
  {key: 'live_deal_item_count', label: '30天全量表的销量'},
];


// 30天全量表汇总导出字段
const summary11Fields = [
  {key: 'code', label: '款号'},
  {key: 'category', label: '品类'},
  {key: 'commodity_image', label: '图片'},
  {key: 'inventory', label: '库存'},
  {key: 'order_quantity', label: '订购量'},
  {key: 'price', label: '单价'},
  {key: 'live_deal_item_count', label: '成交件数'},
  {key: 'pre_shipment_refund_rate', label: '发货前退款率'},
  {key: 'post_shipment_refund_rate', label: '发货后退款率'},
  {key: 'order_submit_time', label: '订单表第一次上架日期'},
  {key: 'one_live_exposure_count', label: '最近直播间曝光'},
  {key: 'one_live_deal_item_count', label: '销量'},
  {key: 'quantity', label: '档口最近15天销量'},
  {key: 'first_registration_time', label: '初次到档口时间'},
  {key: 'last_registration_time', label: '最后到档口时间'},
];

// 爆款导出字段
const summary12Fields = [
  {key: 'code', label: '款号'},
  {key: 'category', label: '货品名称'},
  {key: 'price', label: '单价'},
  {key: 'commodity_image', label: '图片'},
  {key: 'inventory', label: '库存'},
  {key: 'order_quantity', label: '订购量'},
  {key: 'live_deal_item_count', label: '成交件数'},
  {key: 'live_deal_conversion_rate', label: '转换率'},
  {key: 'date_time', label: '日期'},
];

// 根据用户选择的筛选条件导出本页内容到excel
const exportPageUserExcel = () => {
  if (home.order_status === "千川订单") {
    exportExcel(summary3Fields, home.user_data_list)
  }
  if (home.order_status === "客户信息排名") {
    exportExcel(summary4Fields, home.user_data_list)
  }
  if (home.order_status === "款号信息排名") {
    exportExcel(summary5Fields, home.user_data_list)
  }
  if (home.order_status === "老款大于5,30天没播") {
    exportExcel(summary6Fields, home.user_data_list)
  }
  if (home.order_status === "热销款") {
    exportExcel(summary7Fields, home.user_data_list)
  }
  if (home.order_status === "滞销款") {
    exportExcel(summary8Fields, home.user_data_list)
  }
  if (home.order_status === "最近几天热卖") {
    exportExcel(summary9Fields, home.user_data_list)
  }
  if (home.order_status === "库存1-5") {
    exportExcel(summary10Fields, home.user_data_list)
  }
  if (home.order_status === "选款:30天全量表汇总") {
    exportExcel(summary11Fields, home.user_data_list)
  }
  if (home.order_status === "选款:爆款") {
    exportExcel(summary12Fields, home.user_data_list)
  }
}

// 导出本页订单内容到excel
const exportExcel = (exportFields, data_list) => {
  const sheet = XLSX.utils.json_to_sheet(data_list.map(item => {
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

}

// // 根据用户选择的筛选条件导出所有内容到excel
const exportUserExcel = () => {
  home.userAll().then(response => {
    home.all_user_data_list = response.data
    if (home.order_status === "千川订单") {
      exportExcel(summary3Fields, home.all_user_data_list)
    }
    if (home.order_status === "客户信息排名") {
      exportExcel(summary4Fields, home.all_user_data_list)
    }
    if (home.order_status === "款号信息排名") {
      exportExcel(summary5Fields, home.all_user_data_list)
    }
    if (home.order_status === "老款大于5,30天没播") {
      exportExcel(summary6Fields, home.all_user_data_list)
    }
    if (home.order_status === "热销款") {
      exportExcel(summary7Fields, home.all_user_data_list)
    }
    if (home.order_status === "滞销款") {
      exportExcel(summary8Fields, home.all_user_data_list)
    }
    if (home.order_status === "最近几天热卖") {
      exportExcel(summary9Fields, home.all_user_data_list)
    }
    if (home.order_status === "库存1-5") {
      exportExcel(summary10Fields, home.all_user_data_list)
    }
    if (home.order_status === "选款:30天全量表汇总") {
      exportExcel(summary11Fields, home.all_user_data_list)
    }
    if (home.order_status === "选款:爆款") {
      exportExcel(summary12Fields, home.all_user_data_list)
    }
  }).catch(err => {
    console.log(err)
  })
}


// 监听页码
watch(
    () => home.page,
    () => {
      home.loading = true
      if (home.is_show_report_table) {
        showReport()
      } else if (home.order_status === "请选择订单状态" && home.search_date === null) {
        show_tables();
      } else {
        showSummary()
      }

    }
)

// 监听每页条数
watch(
    () => home.size,
    () => {
      home.loading = true
      if (home.is_show_report_table) {
        showReport()
      }
      if (home.order_status === "请选择订单状态" && home.search_date === null) {
        show_tables();
      } else {
        showSummary()
      }
    }
)


// 监听每日报表的日期
watch(
    () => home.report_data,
    () => {
      home.loading = true
      showReport()
    }
)

// 监听每日报表的日期
watch(
    () => home.report_data_history,
    () => {
      home.loading = true
      showReport()
    }
)


// 库存1-5条件中的 最近几天的数据
watch(
    () => home.day,
    () => {
      home.loading = true
      showSummary()
    }
)

// 监听用户上传的表格状态
watch(
    [() => home.buttonType1, () => home.buttonType2, () => home.buttonType3,
      () => home.buttonType4, () => home.buttonType5, () => home.buttonType6,
      () => home.buttonType7, () => home.buttonType9, () => home.buttonType10,
      () => home.buttonType11, () => home.buttonType12, () => home.buttonType13,
      () => home.buttonType14],
    () => {
      getUpdateStatus()
    }
)

// 获取每个表格上传的最后日期
const getUpdateStatus = () => {
  home.getUpdateStatus().then(response => {
    home.update_status = response.data
  }).catch(err => {
    console.log(err)
  })
}
getUpdateStatus()


// 根据用户选择的条件展示对应的数据
const showSummary = () => {
  home.loading = true
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
      console.log(response)
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
body {
  display: flex;
}

.el-button {
  margin: 7px 10px;
}

.head {
  flex: 1;
  display: flex;
}

.left {
  display: flex;
  flex: 2;
  flex-direction: column;
}

.left div {
  flex: 1;
}

.right {
  display: flex;
  flex: 1;
  flex-direction: column;
}

.right div {
  display: flex;
  flex: 1;
  flex-direction: row-reverse;
}

.contents {
  flex: 5;
  width: 100%;
}
</style>