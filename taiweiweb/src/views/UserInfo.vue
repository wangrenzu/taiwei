<template>
  <div class="c">
    <div class="f">
      <p>成功：{{ $route.params.success }}</p>
      <el-table :data="home.query1_results" style="width: 100%" border fit>
        <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
        <el-table-column prop="name" label="名字" sortable width="100" show-overflow-tooltip/>
        <el-table-column prop="merchant_code" label="款号" width="100" show-overflow-tooltip/>
        <el-table-column prop="category" label="种类" width="120" show-overflow-tooltip/>
        <el-table-column prop="price" label="金额" width="60" show-overflow-tooltip/>
        <el-table-column fixed="right" label="图片" width="120">
          <template #default="scope">
            <el-image style="width: 90px; height: 100px"
                      :src="scope.row.commodity_image" fit="cover"/>
          </template>
        </el-table-column>
        <el-table-column prop="product_name" label="尺码" width="80" show-overflow-tooltip/>
      </el-table>
    </div>
    <div class="f">
      <p>退回：{{ $route.params.back }}</p>
      <el-table :data="home.query2_results" style="width: 100%" border fit>
        <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
        <el-table-column prop="name" label="名字" sortable width="100" show-overflow-tooltip/>
        <el-table-column prop="merchant_code" label="款号" width="100" show-overflow-tooltip/>
        <el-table-column prop="category" label="种类" width="120" show-overflow-tooltip/>
        <el-table-column prop="price" label="金额" width="60" show-overflow-tooltip/>
        <el-table-column fixed="right" label="图片" width="120">
          <template #default="scope">
            <el-image style="width: 90px; height: 100px"
                      :src="scope.row.commodity_image" fit="cover"/>
          </template>
        </el-table-column>
        <el-table-column prop="product_name" label="尺码" width="80" show-overflow-tooltip/>
      </el-table>
    </div>
    <div class="f">
      <p>待发+在途{{ $route.params.wait }}</p>
      <el-table :data="home.query3_results" style="width: 100%" border fit>
        <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
        <el-table-column prop="name" label="名字" sortable width="100" show-overflow-tooltip/>
        <el-table-column prop="merchant_code" label="款号" width="100" show-overflow-tooltip/>
        <el-table-column prop="category" label="种类" width="120" show-overflow-tooltip/>
        <el-table-column prop="price" label="金额" width="60" show-overflow-tooltip/>
        <el-table-column fixed="right" label="图片" width="120">
          <template #default="scope">
            <el-image style="width: 90px; height: 100px"
                      :src="scope.row.commodity_image" fit="cover"/>
          </template>
        </el-table-column>
        <el-table-column prop="product_name" label="尺码" width="80" show-overflow-tooltip/>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import home from "../api/home.js";
import {useRoute} from 'vue-router';


const route = useRoute();


//获取每个用户成功、退回、待发+在途 的件数
const showUserInfo = () => {
  home.getUserInfo(route.params.name, route.params.search_date).then(response => {
    home.query1_results = response.data.query1_results
    home.query2_results = response.data.query2_results
    home.query3_results = response.data.query3_results
  }).catch(err => {
    console.log(err)
  })
}
showUserInfo()


</script>

<style scoped>
.c {
  display: flex;
}

.f {
  flex: 1;
}

p {
  text-align: center;
}
</style>