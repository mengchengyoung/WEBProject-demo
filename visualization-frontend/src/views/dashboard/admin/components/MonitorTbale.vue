<template>
  <div class="app-container">
    <el-table
      :data="tableData.filter(data => !search || data.sample_id.toLowerCase().includes(search.toLowerCase()))"
      max-height="500"
      @row-dblclick="handleclick"
    >
      <el-table-column prop="sample_id" label="样本" sortable/>
      <el-table-column prop="batch" label="批次"sortable/>
      <el-table-column prop="status" label="状态"sortable/>
      <el-table-column prop="processed" label="处理" />
      <el-table-column prop="cost_time" label="耗时" />
      <el-table-column prop="submitted" label="提交" />
      <el-table-column prop="running" label="运行" />
      <el-table-column prop="finished" label="结束" />
      <el-table-column
        align="center"
        width="150px"
      >
        <template slot="header">
          <el-input
            v-model="search"
            size="medium"
            placeholder="输入关键字搜索"
          />
        </template>

      </el-table-column>
    </el-table>
    <el-dialog center title="子任务详细信息" :visible.sync="dialogTableVisible" :close-on-click-modal='false' :width="'70%'">
      <el-table :data="sub_tableData">
        <el-table-column prop='name' label='name' />
        <el-table-column prop='sample_id' label='sample' />
        <el-table-column prop='batch' label='batch' />
        <el-table-column prop='status' label='status'sortable="true" sort-by="string"/>
        <el-table-column prop='swap_usage' label='swap_usage' />
        <el-table-column prop='memory' label='memory' />
        <el-table-column prop='cpu_usage' label='cpu_usage' />
        <el-table-column prop='wallclock' label='wallclock' />
        <el-table-column prop='slots' label='slots' />
        <el-table-column prop='memory_usage' label='memory_usage' />
      </el-table>
    </el-dialog>
  </div>
</template>
<script>
import { get_subprocessData } from '@/api/monitor'
export default {
    props: {
        tableData: Array,
        sub_tableData: Array
        },
    data() {
        return {
        search: '',
        dialogTableVisible: false
        }
    },
    methods:{
      handleclick(row, column, event){
        this.dialogTableVisible = true
        console.log(row.sample_id)
        get_subprocessData(row.sample_id).then(
          resp=>{
            this.sub_tableData=resp
            //console.log(resp)
          }
        )        
      },
      load_data(){
        return false
      }
    }

}

</script>
