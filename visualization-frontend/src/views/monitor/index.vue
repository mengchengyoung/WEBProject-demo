<template>
  <div class="app-container" >
    <el-table
      :data="tableData"
      style="width: 100%"
      border
      v-if="isReload"
      empty-text="暂无监控项目"
    >
      <el-table-column
        label="监控项目"
        prop="projectID"
      />
      <el-table-column
        label="监控路径"
        prop="path"
      />
      <el-table-column
        label="扫描间隔"
        prop="scan_iterval"
      />
      <el-table-column
        label="资源占用"
        prop="cache_limit"
      />
      <el-table-column
        label="用户ID"
        prop="user_id"
      />
      <el-table-column
        label="创建日期"
        prop="build_date"
      />
      <el-table-column
        label="最近更新"
        prop="update_date"
      />
      <el-table-column
        label="进程ID"
        prop="processID"
      />
      <el-table-column
        label="监控状态"
        prop="status"
      />
      <el-table-column
        align="center"
        fixed="right"
        width="200px"
      >
        <template slot="header" slot-scope="scope" >
          <el-button
            size="mini"
            type="primary"
            icon="el-icon-plus"
            round
            @click="dialogFormVisible = true"
          >
            创建监控项目
          </el-button>
        </template>
        <template slot-scope="scope" >
          <el-button
            size="mini"
            v-model="button_state"
            @click="handleStop(scope.$index, scope.row)"
          >{{button_state[scope.$index]}}</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="open(scope.$index, scope.row)"
          >删除监控</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      title="创建监控项目"
      :visible.sync="dialogFormVisible"
      center
    >
      <el-form ref="monitorform" size="small">
        <el-form-item label="项目名称">
          <el-input v-model="monitorform.projectID" />
        </el-form-item>
        <el-form-item label="监控路径">
          <el-input v-model="monitorform.path" />
        </el-form-item>
        <el-form-item label="路径偏好">
          <el-input v-model="monitorform.monitor_prefix" placeholder="*"/>
        </el-form-item>
        <el-form-item label="扫描间隔">
          <el-input v-model="monitorform.scan_iterval" />
        </el-form-item>
        <el-form-item label="监控脚本">
          <el-input v-model="monitorform.monitor_script" placeholder="/annoroad/data1/bioinfo/PMO/yangmengcheng/Work/web/Tool-kit-server/Tools/Monitor/bin/Monitor.py"/>
        </el-form-item>
        <el-form-item label="导出类/函数名">
          <el-input v-model="monitorform.monitor_class" placeholder="MT"/>
        </el-form-item>        

      </el-form>
      <template slot='footer'>
          <el-button type="primary" @click="handleBuild()">立即创建</el-button>
          <el-button @click="resetForm('monitorform')">重置</el-button>
          <el-button @click="dialogFormVisible = false">取消</el-button>
          <el-alert
            title="创建失败"
            type="error"
            show-icon
            v-if='buildproject_flag'
            >
          </el-alert>
      </template>
      
    </el-dialog>
  </div>
</template>
<script>
import { delete_Project, stop_Project, get_Project, build_Project } from '@/api/monitor'
export default {
    data() {
        return {
        tableData: [],
        monitorform: {},
        dialogFormVisible: false,
        button_state: {},
        isReload:true,
        buildproject_flag:false,
        }
    },
    methods: {
        handleDelete(row) {
          console.log(row)
          delete_Project(row.projectID)
        },
        handleStop(index, row) {
          if (this.button_state[index] == '暂停监控'){
              let operation = 'stop'
              stop_Project(row.projectID, operation).then(
              resp=>{
                console.log('operation ', resp)
                let state_now = this.button_state[index]
                this.button_state[index] = state_now === '启动监控' ? '暂停监控' : '启动监控'
                //this.button_state[index] = this.button_state[index] === '启动' ?'暂停':'启动'
                //this.reload()
                this.tableData = resp
                console.log(this.button_state)
              }
            )}
          else{
              let operation = 'reboot'
              stop_Project(row.projectID, operation).then(
              resp=>{
                console.log('operation ', resp)
                let state_now = this.button_state[index]
                this.button_state[index] = state_now === '启动监控' ? '暂停监控' : '启动监控'
                //this.button_state[index] = this.button_state[index] === '启动' ?'暂停':'启动'
                //this.reload()
                this.tableData = resp
                console.log(this.button_state)
              }
            )
          }
        },
        // 暂停启动
        state(index){
          //return this.button_state[index]
          console.log(index)
          return this.button_state[index]
        },
        // 创建监控项目
        handleBuild() {
          this.monitorform['status'] = 'new'
          console.log(this.monitorform)
          build_Project(this.monitorform).then(
            resp=>{
              console.log(resp)
              this.tableData = resp
              this.dialogFormVisible=false
              this.$message({
                message: "创建监控项目成功",
                type: 'success'
                })
            }
          ).catch(
            resp=>{
                this.buildproject_flag=true
            }
          )
        },
        // 重置表格
        resetForm(formName) {
          this.$refs.formName.resetFields()
        },
        // 打开创建项目配置框
        open( index, row ) {
        this.$confirm('将删除项目设置及监控数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          delete_Project(row.projectID).then(
            resp=>{
              //this.tableData[index]['status'] = 'delete'
              this.tableData=resp
            }
          )
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
      },
      reload(){
        this.isReload = false
        this.$nextTick(()=>{this.isReload=true})
      }

    },
    created: function() {
          get_Project().then(
            resp => {
              console.log(resp)
              for (let i in resp){
                console.log(i)
                this.button_state[i] = resp[i]['status'] === 'running' ? '暂停监控': '启动监控'
              }
              console.log(this.button_state)
              this.tableData = resp
            }
      )  
    },
    computed: {
      state_now(index){
        return function(index){
          return this.button_state[index]
      }
      }
    }
}
</script>
