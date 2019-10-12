<template>
  <div class="app-container">
    <el-row>
      <el-card class="box-card" shadow="always" :body-style="{ 'margin-right': '0px' }" >
        <el-col :span="18">

        <el-form ref="infoform" :inline="true" :model="query_dict" :rules="rules" label-width="80px" label-position="left">
          <el-row>
          <el-form-item label="癌种" prop="mode">
            <el-select v-model="query_dict.mode" placeholder="请选择癌种" change="Handleselected">
              <el-option label="实体瘤" value="solidtumor"></el-option>
              <el-option label="血液病" value="leukemia"></el-option>
            </el-select>
          </el-form-item>
          </el-row>
          <el-row>
            <el-form-item label="期号" prop="batch" >
              <el-input v-model.trim="query_dict.batch" class="input_base_"/>
            </el-form-item>
            <el-form-item label="样本名" prop="sample" >
              <el-input v-model.trim="query_dict.sample" class="input_base_"/>
            </el-form-item>
          </el-row>
        </el-form>

        <el-form v-if="query_dict.mode ==='solidtumor'" label-width="80px" label-position="left" >
          <el-form-item
            v-for="(hgvs, index) in query_dict.HGVSarray"
            :label="'HGVS'+index"
            :key="hgvs.key"
            :prop="'query_dict.HGVSarray.'+index+'.value'"
          >
            <el-input v-model.trim="hgvs.value" placeholder="输入完整的HGVS, 不能重复" class="input_inline"></el-input> 
            <i type="success" class="el-icon-circle-plus-outline button_inline" @click.prevent="addHGVS"></i>
            <i type="danger" class="el-icon-remove-outline button_inline" @click.prevent="removeHGVS(hgvs)" ></i>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="validateHGVS">校验HGVS</el-button>
            <el-divider direction="vertical"></el-divider>
            <el-button type="primary" @click="onSubmit" :disabled="validateflag">提交查询</el-button>
          </el-form-item>
        </el-form>

        <el-form label-width="80px" label-position="left" ref="optionform" v-if="query_dict.mode==='leukemia'">
          <el-form-item label="上传excel" >
            <el-upload
              class="upload-demo"
              action="http://192.168.2.201:8080/api/trans/upload/"
              ref="upload"
              :on-change="handleChange"
              :file-list="fileList"
              :on-success="handleSuccess"
              :on-error="handleEeror"
              :auto-upload="false"
              :limit=1
            >
              <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
              <el-divider direction="vertical"></el-divider>
              <el-button style="margin-left: 5px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
              <div slot="tip" class="el-upload__tip">查询前先将excel文件上传至服务器校验，只能上传.xls格式文件</div>
            </el-upload>
          </el-form-item>
          <el-form-item label="可选项">
            <el-switch
            active-text="输出bam"
            v-model="query_dict.bamoption"
            style="margin-left: 10px;"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">提交查询</el-button>
            <el-divider direction="vertical"></el-divider>
            <el-button @click="resetForm('optionform')">重置</el-button>
          </el-form-item>
        </el-form>
        </el-col>
      </el-card>
    </el-row>
    <template v-for="value, name in labelData" >
      <el-card style="margin-top:20px" >
        <Ttable :labelData="value" :tableData="tableData[name]" :bamfile="bamfiles[name]" v-loading="query_loading" element-loading-text="正在查询..."/>
      </el-card>
    </template>
  </div>
</template>

<script>
import { get_trans_cis, validateHGVS } from "@/api/trans_cis"
import Ttable  from "./components/TransTable"

export default {
    data() {
        return {
          query_dict: {
                batch: '',
                sample: '',
                file: '',
                visualization: false,
                bamoption: false,
                mode:'',
                HGVSarray:[
                  {'value': ''},
                ]
            },
          rules: {
                batch: [
                    { required: true, message: '请输入样本期号', trigger: 'blur' },
                    //{ min: 3, max: 5, message: '长度在 3 到 5 个数字，如666', trigger: 'blur' }
                ],
                sample: [
                  {required: true, message: '请输入样本名，如HDXXXX', trigger: 'blur'},
                  //{min:5, max: 15, message: "以H开头,长度在5到10个字符，如HXXXX", trigger: 'blur'}
                ],
                mode:[
                  {required:true, message: '请选择癌种'}
                ]
            },
          query_loading: false,
          file_submit: false,
          fileList: [],
          validateflag: true,
          labelData: {},
          tableData: {},
          bamfiles: {},
        }
    },
    components:{
      Ttable,
      document
    },
    methods: {
      Handleselected(value){
        console.log(value)
      },
      addHGVS(){
        this.query_dict.HGVSarray.push({
          value: '',
          key: Date.now()
        })
      },
      removeHGVS(item){
        let index = this.query_dict.HGVSarray.indexOf(item)
        if (index !== -1){
          this.query_dict.HGVSarray.splice(index, 1)
        }
      },
      validateHGVS(){
        validateHGVS(this.query_dict).then(
          resp => {
            if (resp.flag==400){
              this.$message({
                type: 'warning',
                message: resp.info
              })
              return
            }
            this.$message({
              message: "校验成功",
              type: 'success'
            })
            this.updateBatchInfo(resp)
            this.validateflag = false //关闭校验按钮，避免重复校验
          } 
        ).catch(
          err => {
            console.log(err)
            this.$message({
              message: err.response.WARN
              })
          }
        )
      },
      resetForm(form2) {
      //this.$refs[form1].resetFields();
      this.$refs[form2].resetFields();
      },
      onSubmit(file) {
        //console.log(this.query_dict)
        if (!this.file_submit){
          this.$message({
            type: 'info',
            message: '请提交文件'
          })
          return
        }

        this.query_loading=true
        this.$message({
          message: '提交成功, 正在查询...',
          type: 'success',
          showClose: 'true'
        })
        get_trans_cis(this.query_dict).then(
            //this.query_loading = true
            res => {
              this.tableData = res['result']
              this.bamfiles = res['bamfiles']
              // 将查询结果更新到前端表格
              this.$nextTick(
                ()=>{
                  this.tableData = this.tableData
                }
              )
              this.query_loading = false
            }
        ).catch(
          () => {
            this.query_loading = false
            this.$message({
              type: 'error',
              message: '查询错误，请检查输入...'
            })
            console.log('trans_cis false')
          }
        )
      },
      submitUpload() {
        console.log(this.fileList)
        if (this.fileList.length===0){
          this.$message({
            type: "warning",
            message: '先选择文件!'
          })
          return 
        }
        this.$refs.upload.submit()
      },

      handleSuccess(resp){
        
        if (response.flag === 400){
          this.$message({
            type: 'error',
            message: resp.info
          })
          this.$refs.upload.clearFiles()
          return
        }
        console.log('submit sucess!')
        this.updateBatchInfo(response)
        this.file_submit = true
        //console.log(this.labelData)
      },

      handleEeror(err, file, fileList){
        this.$message({
          type: "warnning",
          message: err
        })
        this.$refs.upload.clearFiles()
      },

      handleRemove(file, fileList) {
        console.log(file, fileList)
      },

      updateBatchInfo(response) {
        for(let i in response){
          console.log(i)
          switch (i) {
          case 'label_data':
            this.labelData = response['label_data']
          default: 
            this.query_dict[i] = response[i]
          }
        }
        console.log(this.query_dict)        
      }
    } 
}
</script>
<style scoped>
  .input_inline {
    float: left;
    width: 433px
  }
  .button_inline {
    margin-left:5px;
    margin-top: 5px;
    cursor: pointer;
    font-size: 25px
  }
  .input_base_ {
    width: 200px;
  }
</style>
