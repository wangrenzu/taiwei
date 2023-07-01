<template>

  <el-input v-model="code" style="width: 200px"
            placeholder="请输入款号" clearable></el-input>
  <el-select
      v-model="tags"
      multiple
      placeholder="请选择标签"
      style="width: 150px"
      clearable
  >
    <el-option
        v-for="item in tags_options"
        :key="item.value"
        :label="item.label"
        :value="item.value"
    />
  </el-select>
  <el-date-picker
      v-model="date_time"
      type="daterange"
      start-placeholder="开始日期"
      end-placeholder="结束日期"
      value-format="YYYY-MM-DD"
  />
  <el-button type="primary" @click="getStyleStatus">
    搜索
    <el-icon color="white" class="el-icon--right">
      <Search/>
    </el-icon>
  </el-button>
  <el-button type="primary" @click="exportExcel(Fields)">
    导出
    <el-icon color="white" class="el-icon--right">
      <Download/>
    </el-icon>
  </el-button>
  <el-table :data="home.style_status_list" v-loading="home.loading" style="width: 100%" height="800" border fit>
    <el-table-column type="index" label="序号" width="70" show-overflow-tooltip/>
    <el-table-column prop="date_time" label="上传日期" width="110" show-overflow-tooltip/>
    <el-table-column prop="time" label="下单日期" width="110" show-overflow-tooltip/>
    <el-table-column prop="code" label="款号" width="100" show-overflow-tooltip/>
    <el-table-column prop="cai_chuang" label="裁床" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="che_jian" label="车间" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="hou_dao" label="后道" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="tai_wei" label="泰维" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="yi_fa" label="意法" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="mo_ya" label="茉雅" width="60" sortable show-overflow-tooltip/>
    <el-table-column prop="fabric_price" label="面料总金额" width="100" show-overflow-tooltip/>
    <el-table-column prop="materials_price" label="辅料总金额" width="100" show-overflow-tooltip/>
    <el-table-column prop="factory_price" label="工厂总金额" width="100" show-overflow-tooltip/>
    <el-table-column prop="salesrecord_price" label="档口总金额" width="100" show-overflow-tooltip/>
    <el-table-column prop="order_price" label="订单总金额" width="100" sortable show-overflow-tooltip/>
    <el-table-column prop="num" label="来几次" width="70" show-overflow-tooltip/>
    <el-table-column prop="to_salesrecord_time" label="最近到档口时间" width="110" sortable show-overflow-tooltip/>
    <el-table-column prop="time_num" label="从下单到今天的天数" width="80" sortable show-overflow-tooltip/>
    <el-table-column label="标签" width="200" align="center">
      <template #default="score">
        <el-tag
            v-if="score.row.tags"
            v-for="tag in score.row.tags.split(',')"
            :key="tag"
            class="mx-1"
            closable
            :disable-transitions="false"
            @close="handleClose(tag, score)"
        >
          {{ tag }}
        </el-tag>

        <el-input
            v-if="inputVisible===score.row"
            ref="InputRef"
            v-model="inputValue"
            class="ml-1 w-20"
            size="small"
            @keyup.enter="handleInputConfirm(score)"
            style="width: 70px;"
        />
        <el-button v-else class="button-new-tag ml-1" size="small" @click="showInput(score.row)">
          +
        </el-button>
      </template>
    </el-table-column>
    <el-table-column label="备注" width="200">
      <template #default="score">
        <el-input
            v-model="score.row.remarks"
            :autosize="{ minRows: 2, maxRows: 4 }"
            type="textarea"
            placeholder="备注"
            ref="remarks"
            @blur="handleInputConfirm(score)"

        />
      </template>
    </el-table-column>
  </el-table>
  <div class="demo-pagination-block">
    <el-pagination
        v-model:current-page="home.style_page"
        v-model:page-size="home.style_size"
        :page-sizes="[10, 50, 100,500,home.style_count]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="home.style_count"
    />
  </div>
</template>

<script setup>

import home from "../api/home.js";
import {ElInput} from 'element-plus'
import {Search, Download} from '@element-plus/icons-vue'
import {nextTick, ref, watch} from "vue";
import * as XLSX from "xlsx";
import FileSaver from 'file-saver';


// 添加标签的input的对象
const InputRef = ref(null)
// 是否显示添加标签的input
const inputVisible = ref('')
// 添加标签的内容
const inputValue = ref('')
// 款号
const code = ref('')
// 标签
const tags = ref('')
// 上传日期
const date_time = ref('')

// 标签筛选下拉框
const tags_options = [
  {
    value: '采购面料',
    label: '采购面料',
  },
  {
    value: '采购辅料',
    label: '采购辅料',
  },
  {
    value: '没到车间',
    label: '没到车间',
  },
  {
    value: '刚到车间',
    label: '刚到车间',
  },
  {
    value: '车间加工中',
    label: '车间加工中',
  },
  {
    value: '在后道',
    label: '在后道',
  },
  {
    value: '入仓',
    label: '入仓',
  },
  {
    value: '到档口',
    label: '到档口',
  },
  {
    value: '新款',
    label: '新款',
  },
  {
    value: '翻单',
    label: '翻单',
  },
  {
    value: '其他',
    label: '其他',
  },
  {
    value: '在档口',
    label: '在档口',
  },
]
// 导出的字段
const Fields = [
  {key: 'date_time', label: '上传日期'},
  {key: 'time', label: '下单日期'},
  {key: 'code', label: '款号'},
  {key: 'cai_chuang', label: '裁床'},
  {key: 'che_jian', label: '车间'},
  {key: 'hou_dao', label: '后道'},
  {key: 'tai_wei', label: '泰维'},
  {key: 'yi_fa', label: '意法'},
  {key: 'mo_ya', label: '茉雅'},
  {key: 'fabric_price', label: '面料总金额'},
  {key: 'materials_price', label: '辅料总金额'},
  {key: 'factory_price', label: '工厂总金额'},
  {key: 'salesrecord_price', label: '档口总金额'},
  {key: 'order_price', label: '订单总金额'},
  {key: 'num', label: '来几次'},
  {key: 'to_salesrecord_time', label: '最近到档口时间'},
  {key: 'time_num', label: '从下单到今天的天数'},
  {key: 'tags', label: '标签'},
  {key: 'remarks', label: '备注'},
];
// 导出内容到excel
const exportExcel = (exportFields) => {
  let tagValues = Object.values(tags.value);
  tagValues = tagValues.join(',')
  home.getStyleStatus(code.value, tagValues, date_time.value, 1).then(response => {
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

// 根据筛选条件获取内容
const getStyleStatus = () => {
  let tagValues = Object.values(tags.value);
  tagValues = tagValues.join(',')
  home.getStyleStatus(code.value, tagValues, date_time.value, 0).then(response => {
    console.log(response)
    home.style_status_list = response.data.results
    home.style_count = response.data.count
    home.loading = false
  }).catch(err => {
    console.log(err)
  })
}
getStyleStatus()

// 添加标签或者添加备注
const handleInputConfirm = (score) => {
  let tagsArray = []
  if (score.row.tags) {
    tagsArray = score.row.tags.split(',');
  }
  if (inputValue.value.length !== 0) {
    tagsArray.push(inputValue.value)
    score.row.tags = tagsArray.join(',');
  }
  home.uptStyleStatusTags(score.row.id, score.row.tags, score.row.remarks).then(response => {
  }).catch(err => {
    alert("添加失败")
  })
  inputVisible.value = ''
}

// 打开添加标签对话框
const showInput = (row) => {
  inputValue.value = ''
  inputVisible.value = row
  nextTick(() => {
    InputRef.value?.focus()
  })
}

// 删除标签
const handleClose = (removedTag, score) => {
  let tagsArray = score.row.tags.split(',');
  const index = tagsArray.indexOf(removedTag);
  if (index >= 0) {
    tagsArray.splice(index, 1);
    score.row.tags = tagsArray.join(',');
  }
  home.uptStyleStatusTags(score.row.id, score.row.tags).then(response => {
  }).catch(err => {
    alert("删除失败")
  })
}
watch(
    [() => home.style_page, () => home.style_size],
    () => {
      home.loading = true
      getStyleStatus()
    }
)


</script>

<style scoped>

</style>