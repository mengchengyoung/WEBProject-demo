(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-6e6a2cb1"],{"4b16":function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"app-container"},[a("el-row",[a("el-card",{staticClass:"box-card",attrs:{shadow:"always","body-style":{"margin-right":"0px"}}},[a("el-col",{attrs:{span:18}},[a("el-form",{ref:"infoform",attrs:{inline:!0,model:e.query_dict,rules:e.rules,"label-width":"80px","label-position":"left"}},[a("el-row",[a("el-form-item",{attrs:{label:"癌种",prop:"mode"}},[a("el-select",{attrs:{placeholder:"请选择癌种",change:"Handleselected"},model:{value:e.query_dict.mode,callback:function(t){e.$set(e.query_dict,"mode",t)},expression:"query_dict.mode"}},[a("el-option",{attrs:{label:"实体瘤",value:"solidtumor"}}),e._v(" "),a("el-option",{attrs:{label:"血液病",value:"leukemia"}})],1)],1)],1),e._v(" "),a("el-row",[a("el-form-item",{attrs:{label:"期号",prop:"batch"}},[a("el-input",{staticClass:"input_base_",model:{value:e.query_dict.batch,callback:function(t){e.$set(e.query_dict,"batch","string"===typeof t?t.trim():t)},expression:"query_dict.batch"}})],1),e._v(" "),a("el-form-item",{attrs:{label:"样本名",prop:"sample"}},[a("el-input",{staticClass:"input_base_",model:{value:e.query_dict.sample,callback:function(t){e.$set(e.query_dict,"sample","string"===typeof t?t.trim():t)},expression:"query_dict.sample"}})],1)],1)],1),e._v(" "),"solidtumor"===e.query_dict.mode?a("el-form",{attrs:{"label-width":"80px","label-position":"left"}},[e._l(e.query_dict.HGVSarray,function(t,l){return a("el-form-item",{key:t.key,attrs:{label:"HGVS"+l,prop:"query_dict.HGVSarray."+l+".value"}},[a("el-input",{staticClass:"input_inline",attrs:{placeholder:"输入完整的HGVS, 不能重复"},model:{value:t.value,callback:function(a){e.$set(t,"value","string"===typeof a?a.trim():a)},expression:"hgvs.value"}}),e._v(" "),a("i",{staticClass:"el-icon-circle-plus-outline button_inline",attrs:{type:"success"},on:{click:function(t){return t.preventDefault(),e.addHGVS(t)}}}),e._v(" "),a("i",{staticClass:"el-icon-remove-outline button_inline",attrs:{type:"danger"},on:{click:function(a){return a.preventDefault(),e.removeHGVS(t)}}})],1)}),e._v(" "),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:e.validateHGVS}},[e._v("校验HGVS")]),e._v(" "),a("el-divider",{attrs:{direction:"vertical"}}),e._v(" "),a("el-button",{attrs:{type:"primary",disabled:e.validateflag},on:{click:e.onSubmit}},[e._v("提交查询")])],1)],2):e._e(),e._v(" "),"leukemia"===e.query_dict.mode?a("el-form",{ref:"optionform",attrs:{"label-width":"80px","label-position":"left"}},[a("el-form-item",{attrs:{label:"上传excel"}},[a("el-upload",{ref:"upload",staticClass:"upload-demo",attrs:{action:"http://192.168.2.201:8080/api/trans/upload/","on-change":e.handleChange,"file-list":e.fileList,"on-success":e.handleSuccess,"on-error":e.handleEeror,"auto-upload":!1,limit:1}},[a("el-button",{attrs:{slot:"trigger",size:"small",type:"primary"},slot:"trigger"},[e._v("选取文件")]),e._v(" "),a("el-divider",{attrs:{direction:"vertical"}}),e._v(" "),a("el-button",{staticStyle:{"margin-left":"5px"},attrs:{size:"small",type:"success"},on:{click:e.submitUpload}},[e._v("上传到服务器")]),e._v(" "),a("div",{staticClass:"el-upload__tip",attrs:{slot:"tip"},slot:"tip"},[e._v("查询前先将excel文件上传至服务器校验，只能上传.xls格式文件")])],1)],1),e._v(" "),a("el-form-item",{attrs:{label:"可选项"}},[a("el-switch",{staticStyle:{"margin-left":"10px"},attrs:{"active-text":"输出bam"},model:{value:e.query_dict.bamoption,callback:function(t){e.$set(e.query_dict,"bamoption",t)},expression:"query_dict.bamoption"}})],1),e._v(" "),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:e.onSubmit}},[e._v("提交查询")]),e._v(" "),a("el-divider",{attrs:{direction:"vertical"}}),e._v(" "),a("el-button",{on:{click:function(t){return e.resetForm("optionform")}}},[e._v("重置")])],1)],1):e._e()],1)],1)],1),e._v(" "),e._l(e.labelData,function(t,l){return[a("el-card",{staticStyle:{"margin-top":"20px"}},[a("Ttable",{directives:[{name:"loading",rawName:"v-loading",value:e.query_loading,expression:"query_loading"}],attrs:{labelData:t,tableData:e.tableData[l],bamfile:e.bamfiles[l],"element-loading-text":"正在查询..."}})],1)]})],2)},i=[],s=a("0a0d"),r=a.n(s),o=a("b775"),n="http://192.168.2.201:8080";function c(e){return Object(o["a"])({baseURL:n,url:"/api/trans/get_trans_cis/",method:"POST",data:e})}function u(e){return Object(o["a"])({baseURL:n,url:"/api/trans/validateHGVS/",method:"POST",data:e})}var d=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{staticClass:"appcontainer"},[a("el-table",{staticStyle:{width:"100%"},attrs:{data:e.tableData,border:""}},[e._l(e.labelData,function(e){return a("el-table-column",{key:e.id,attrs:{prop:e.prop,label:e.label}})}),e._v(" "),a("el-table-column",[a("template",{slot:"header"},[a("el-button",[a("a",{attrs:{href:e.bamfile}},[e._v(" 点击下载 ")])])],1)],2)],2)],1)},m=[],p={props:{tableData:Array,labelData:Array,bamfile:String}},f=p,b=a("2877"),_=Object(b["a"])(f,d,m,!1,null,null,null),v=_.exports,h={data:function(){return{query_dict:{batch:"",sample:"",file:"",visualization:!1,bamoption:!1,mode:"",HGVSarray:[{value:""}]},rules:{batch:[{required:!0,message:"请输入样本期号",trigger:"blur"}],sample:[{required:!0,message:"请输入样本名，如HDXXXX",trigger:"blur"}],mode:[{required:!0,message:"请选择癌种"}]},query_loading:!1,file_submit:!1,fileList:[],validateflag:!0,labelData:{},tableData:{},bamfiles:{}}},components:{Ttable:v,document:document},methods:{Handleselected:function(e){console.log(e)},addHGVS:function(){this.query_dict.HGVSarray.push({value:"",key:r()()})},removeHGVS:function(e){var t=this.query_dict.HGVSarray.indexOf(e);-1!==t&&this.query_dict.HGVSarray.splice(t,1)},validateHGVS:function(){var e=this;u(this.query_dict).then(function(t){400!=t.flag?(e.$message({message:"校验成功",type:"success"}),e.updateBatchInfo(t),e.validateflag=!1):e.$message({type:"warning",message:t.info})}).catch(function(t){console.log(t),e.$message({message:t.response.WARN})})},resetForm:function(e){this.$refs[e].resetFields()},onSubmit:function(e){var t=this;this.file_submit?(this.query_loading=!0,this.$message({message:"提交成功, 正在查询...",type:"success",showClose:"true"}),c(this.query_dict).then(function(e){t.tableData=e["result"],t.bamfiles=e["bamfiles"],t.$nextTick(function(){t.tableData=t.tableData}),t.query_loading=!1}).catch(function(){t.query_loading=!1,t.$message({type:"error",message:"查询错误，请检查输入..."}),console.log("trans_cis false")})):this.$message({type:"info",message:"请提交文件"})},submitUpload:function(){console.log(this.fileList),0!==this.fileList.length?this.$refs.upload.submit():this.$message({type:"warning",message:"先选择文件!"})},handleSuccess:function(e){if(400===response.flag)return this.$message({type:"error",message:e.info}),void this.$refs.upload.clearFiles();console.log("submit sucess!"),this.updateBatchInfo(response),this.file_submit=!0},handleEeror:function(e,t,a){this.$message({type:"warnning",message:e}),this.$refs.upload.clearFiles()},handleRemove:function(e,t){console.log(e,t)},updateBatchInfo:function(e){for(var t in e)switch(console.log(t),t){case"label_data":this.labelData=e["label_data"];default:this.query_dict[t]=e[t]}console.log(this.query_dict)}}},y=h,g=(a("efa2"),Object(b["a"])(y,l,i,!1,null,"3f3e621c",null));t["default"]=g.exports},6113:function(e,t,a){},efa2:function(e,t,a){"use strict";var l=a("6113"),i=a.n(l);i.a}}]);