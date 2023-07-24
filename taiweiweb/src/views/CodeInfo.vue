<template>
      <el-tag>
        说明： 选择历史日期，能显示每个报表日期的状态，但是，所有详情按钮是一样结果，即今天的状态。
      </el-tag>

  <el-button type="primary" @click="exportToCsv" size="large">
          导出数据
          <el-icon color="white" class="el-icon--right">
            <Download/>
          </el-icon>
        </el-button>
  <div>
  </div>
  <div class="c">
    <div class="f">


      <p>代发：{{ $route.params.wait }}</p>
      <el-table :data="home.query1_results" style="width: 100%" border fit>
        <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
        <el-table-column prop="code" label="款号" sortable width="100" show-overflow-tooltip/>
        <el-table-column prop="category" label="种类" width="120"  show-overflow-tooltip/>
        <el-table-column prop="product_quantity" label="数量" width="80" sortable show-overflow-tooltip/>
        <el-table-column fixed="right" label="图片" width="120">
          <template #default="scope">
            <el-image style="width: 90px; height: 100px"
                    :src="'http://192.168.1.233/web_images/' + scope.row.code + '.jpg'" fit="cover">
          </el-image>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="f">
      <p>取消{{ $route.params.remove }}</p>
      <el-table :data="home.query2_results" style="width: 100%" border fit>
        <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
        <el-table-column prop="code" label="款号" sortable width="100" show-overflow-tooltip/>
        <el-table-column prop="category" label="种类" width="120"  show-overflow-tooltip/>
        <el-table-column prop="product_quantity" label="数量" width="80" sortable show-overflow-tooltip/>
        <el-table-column fixed="right" label="图片" width="120">
          <template #default="scope">
            <el-image style="width: 90px; height: 100px"
                    :src="'http://192.168.1.233/web_images/' + scope.row.code + '.jpg'" fit="cover">
          </el-image>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="f">
      <p>在途{{ $route.params.transit }}</p>
      <el-table :data="home.query3_results" style="width: 100%" border fit>
        <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
        <el-table-column prop="code" label="款号" sortable width="100" show-overflow-tooltip/>
        <el-table-column prop="category" label="种类" width="120"  show-overflow-tooltip/>
        <el-table-column prop="product_quantity" label="数量" width="80" sortable show-overflow-tooltip/>
        <el-table-column fixed="right" label="图片" width="120">
          <template #default="scope">
            <el-image style="width: 90px; height: 100px"
                    :src="'http://192.168.1.233/web_images/' + scope.row.code + '.jpg'">
          </el-image>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="f">
      <p>成功{{ $route.params.success }}</p>
      <el-table :data="home.query4_results" style="width: 100%" border fit>
        <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
        <el-table-column prop="code" label="款号" sortable width="100" show-overflow-tooltip/>
        <el-table-column prop="category" label="种类" width="120"  show-overflow-tooltip/>
        <el-table-column prop="product_quantity" label="数量" width="80" sortable show-overflow-tooltip/>
        <el-table-column fixed="right" label="图片" width="120">
          <template #default="scope">
            <el-image style="width: 90px; height: 100px"
                    :src="'http://192.168.1.233/web_images/' + scope.row.code + '.jpg'">
          </el-image>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="f">
      <p>退回{{ $route.params.back }}</p>
      <el-table :data="home.query5_results" style="width: 100%" border fit>
        <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
        <el-table-column prop="code" label="款号"  width="100" show-overflow-tooltip/>
        <el-table-column prop="category" label="种类" width="120"  show-overflow-tooltip/>
        <el-table-column prop="product_quantity" label="数量" width="80" sortable show-overflow-tooltip/>
        <el-table-column fixed="right" label="图片" width="120">
          <template #default="scope">
            <el-image style="width: 90px; height: 100px"
                    :src="'http://192.168.1.233/web_images/' + scope.row.code + '.jpg'">
          </el-image>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import home from "../api/home.js";

import {useRoute} from 'vue-router';
import {Download} from '@element-plus/icons-vue'


const route = useRoute();

// 报表详情，每个款号的待发、在途、成功、取消、退回件数
const showCodeInfo = () => {
  home.getCodeInfo(route.params.submit_time).then(response => {
    home.query1_results = response.data.query1_results
    home.query2_results = response.data.query2_results
    home.query3_results = response.data.query3_results
    home.query4_results = response.data.query4_results
    home.query5_results = response.data.query5_results
  }).catch(err => {
    console.log(err)
  })
}
showCodeInfo()



// 导出到excel
const exportToCsv = () => {
  // 要导出的字段
  const allDataSets = [
    {title: "代发", data: home.query1_results},
    {title: "取消", data: home.query2_results},
    {title: "在途", data: home.query3_results},
    {title: "成功", data: home.query4_results},
    {title: "退回", data: home.query5_results},
  ];
  let csvContent = "data:text/csv;charset=utf-8,";

  allDataSets.forEach((dataSet, index) => {
    // 在每份数据之前添加对应的标题
    csvContent += dataSet.title + "\n";
    csvContent += "款号,品类,数量,图片\n";
    dataSet.data.forEach(item => {
      csvContent += item.code + "," + item.category + "," + item.product_quantity + "," + item.commodity_image + "\n";
    });
    // 在每份数据之间添加一个空行作为间隔
    if (index < allDataSets.length - 1) {
      csvContent += "\n";
    }
  });

  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "export.csv");
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}


</script>

<style scoped>
.c{
  display: flex;
}
.f{
  flex: 1;
}
p{
  text-align: center;
}
</style>