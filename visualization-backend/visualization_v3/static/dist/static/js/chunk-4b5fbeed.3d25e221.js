(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-4b5fbeed"],{"02aa":function(t,a,e){"use strict";var n=e("d479"),s=e.n(n);s.a},"22a6":function(t,a,e){},2452:function(t,a,e){"use strict";var n=e("8715"),s=e.n(n);s.a},"364d":function(t,a,e){"use strict";var n=e("c65c"),s=e.n(n);s.a},"7cf8":function(t,a,e){"use strict";e.d(a,"a",function(){return s}),e.d(a,"d",function(){return r}),e.d(a,"b",function(){return l}),e.d(a,"f",function(){return i}),e.d(a,"c",function(){return o}),e.d(a,"e",function(){return c});var n=e("b775");function s(t){return console.log(t),Object(n["a"])({url:"api/monitor/build/",method:"POST",data:t})}function r(){return Object(n["a"])({url:"api/monitor/show/monitorProject/",method:"POST"})}function l(t){return Object(n["a"])({url:"api/monitor/modify/deleteProject/",method:"POST",data:{projectID:t,operation:"delete"}})}function i(t,a){return Object(n["a"])({method:"POST",data:{projectID:t,operation:a}})}function o(t){return Object(n["a"])({url:"api/monitor/data/",method:"POST",data:{projectID:t}})}function c(t){return Object(n["a"])({url:"api/monitor/subprocess/data/",method:"POST",data:{sample_id:t}})}},8715:function(t,a,e){},9406:function(t,a,e){"use strict";e.r(a);var n=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"dashboard-container"},[e(t.currentRole,{tag:"component"})],1)},s=[],r=(e("6762"),e("2fdb"),e("cebc")),l=e("2f62"),i=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"dashboard-editor-container"},[e("panel-group",{attrs:{sample_state:t.sample_state},on:{handleSetLineChartData:t.handleSetLineChartData}}),t._v(" "),e("el-row",{staticStyle:{background:"#fff",padding:"16px 16px 0","margin-bottom":"32px"}},[e("Monitor-Table",{attrs:{"table-data":t.monitorData}})],1),t._v(" "),e("el-row",{attrs:{gutter:32}},[e("el-col",{attrs:{xs:24,sm:24,lg:8}},[e("div",{staticClass:"chart-wrapper"},[e("raddar-chart")],1)]),t._v(" "),e("el-col",{attrs:{xs:24,sm:24,lg:8}},[e("div",{staticClass:"chart-wrapper"},[e("pie-chart")],1)]),t._v(" "),e("el-col",{attrs:{xs:24,sm:24,lg:8}},[e("div",{staticClass:"chart-wrapper"},[e("bar-chart")],1)])],1),t._v(" "),e("el-row",{attrs:{gutter:8}},[e("el-col",{staticStyle:{"padding-right":"8px","margin-bottom":"30px"},attrs:{xs:{span:24},sm:{span:24},md:{span:24},lg:{span:12},xl:{span:12}}},[e("transaction-table")],1),t._v(" "),e("el-col",{staticStyle:{"margin-bottom":"30px"},attrs:{xs:{span:24},sm:{span:12},md:{span:12},lg:{span:6},xl:{span:6}}},[e("todo-list")],1),t._v(" "),e("el-col",{staticStyle:{"margin-bottom":"30px"},attrs:{xs:{span:24},sm:{span:12},md:{span:12},lg:{span:6},xl:{span:6}}},[e("box-card")],1)],1)],1)},o=[],c=e("5d73"),d=e.n(c),u=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("el-row",{staticClass:"panel-group",attrs:{gutter:40},model:{value:t.sample_state,callback:function(a){t.sample_state=a},expression:"sample_state"}},[e("el-col",{staticClass:"card-panel-col",attrs:{xs:12,sm:12,lg:6}},[e("div",{staticClass:"card-panel",on:{click:function(a){return t.handleSetLineChartData("newVisitis")}}},[e("div",{staticClass:"card-panel-icon-wrapper icon-people"},[e("svg-icon",{attrs:{"icon-class":"guide","class-name":"card-panel-icon"}})],1),t._v(" "),e("div",{staticClass:"card-panel-description"},[e("div",{staticClass:"card-panel-text"},[t._v("\n          今日样本\n        ")]),t._v(" "),e("count-to",{staticClass:"card-panel-num",attrs:{"start-val":0,"end-val":t.sample_state.today_sample||0,duration:2600}})],1)])]),t._v(" "),e("el-col",{staticClass:"card-panel-col",attrs:{xs:12,sm:12,lg:6}},[e("div",{staticClass:"card-panel",on:{click:function(a){return t.handleSetLineChartData("messages")}}},[e("div",{staticClass:"card-panel-icon-wrapper icon-message"},[e("svg-icon",{attrs:{"icon-class":"star","class-name":"card-panel-icon"}})],1),t._v(" "),e("div",{staticClass:"card-panel-description"},[e("div",{staticClass:"card-panel-text"},[t._v("\n          已完成样本\n        ")]),t._v(" "),e("count-to",{staticClass:"card-panel-num",attrs:{"start-val":0,"end-val":t.sample_state.sample_done||0,duration:3e3}})],1)])]),t._v(" "),e("el-col",{staticClass:"card-panel-col",attrs:{xs:12,sm:12,lg:6}},[e("div",{staticClass:"card-panel",on:{click:function(a){return t.handleSetLineChartData("purchases")}}},[e("div",{staticClass:"card-panel-icon-wrapper icon-money"},[e("svg-icon",{attrs:{"icon-class":"eye-open","class-name":"card-panel-icon"}})],1),t._v(" "),e("div",{staticClass:"card-panel-description"},[e("div",{staticClass:"card-panel-text"},[t._v("\n          正在运行样本\n        ")]),t._v(" "),e("count-to",{staticClass:"card-panel-num",attrs:{"start-val":0,"end-val":t.sample_state.sample_running||0,duration:3200}})],1)])]),t._v(" "),e("el-col",{staticClass:"card-panel-col",attrs:{xs:12,sm:12,lg:6}},[e("div",{staticClass:"card-panel",on:{click:function(a){return t.handleSetLineChartData("shoppings")}}},[e("div",{staticClass:"card-panel-icon-wrapper icon-shopping"},[e("svg-icon",{attrs:{"icon-class":"bug","class-name":"card-panel-icon"}})],1),t._v(" "),e("div",{staticClass:"card-panel-description"},[e("div",{staticClass:"card-panel-text"},[t._v("\n          异常样本\n        ")]),t._v(" "),e("count-to",{staticClass:"card-panel-num",attrs:{"start-val":0,"end-val":t.sample_state.sample_err||0,duration:3600}})],1)])])],1)},p=[],h=e("ec1b"),m=e.n(h),b={components:{CountTo:m.a},props:["sample_state"],methods:{handleSetLineChartData:function(t){this.$emit("handleSetLineChartData",t)}}},f=b,v=(e("dbe6"),e("2877")),g=Object(v["a"])(f,u,p,!1,null,"a15fe4f6",null),_=g.exports,C=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{class:t.className,style:{height:t.height,width:t.width}})},x=[],y=e("313e"),w=e.n(y),D=e("ed08");e("817d");var S={props:{className:{type:String,default:"chart"},width:{type:String,default:"100%"},height:{type:String,default:"350px"},autoResize:{type:Boolean,default:!0},chartData:{type:Object,required:!0}},data:function(){return{chart:null,sidebarElm:null}},watch:{chartData:{deep:!0,handler:function(t){this.setOptions(t)}}},mounted:function(){var t=this;this.initChart(),this.autoResize&&(this.__resizeHandler=Object(D["b"])(function(){t.chart&&t.chart.resize()},100),window.addEventListener("resize",this.__resizeHandler)),this.sidebarElm=document.getElementsByClassName("sidebar-container")[0],this.sidebarElm&&this.sidebarElm.addEventListener("transitionend",this.sidebarResizeHandler)},beforeDestroy:function(){this.chart&&(this.autoResize&&window.removeEventListener("resize",this.__resizeHandler),this.sidebarElm&&this.sidebarElm.removeEventListener("transitionend",this.sidebarResizeHandler),this.chart.dispose(),this.chart=null)},methods:{sidebarResizeHandler:function(t){"width"===t.propertyName&&this.__resizeHandler()},setOptions:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},a=t.expectedData,e=t.actualData;this.chart.setOption({xAxis:{data:["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],boundaryGap:!1,axisTick:{show:!1}},grid:{left:10,right:10,bottom:20,top:30,containLabel:!0},tooltip:{trigger:"axis",axisPointer:{type:"cross"},padding:[5,10]},yAxis:{axisTick:{show:!1}},legend:{data:["expected","actual"]},series:[{name:"expected",itemStyle:{normal:{color:"#FF005A",lineStyle:{color:"#FF005A",width:2}}},smooth:!0,type:"line",data:a,animationDuration:2800,animationEasing:"cubicInOut"},{name:"actual",smooth:!0,type:"line",itemStyle:{normal:{color:"#3888fa",lineStyle:{color:"#3888fa",width:2},areaStyle:{color:"#f3f8ff"}}},data:e,animationDuration:2800,animationEasing:"quadraticOut"}]})},initChart:function(){this.chart=w.a.init(this.$el,"macarons"),this.setOptions(this.chartData)}}},O=S,j=Object(v["a"])(O,C,x,!1,null,null,null),k=j.exports,E=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"app-container"},[e("el-table",{attrs:{data:t.tableData.filter(function(a){return!t.search||a.sample_id.toLowerCase().includes(t.search.toLowerCase())}),"max-height":"500"},on:{"row-dblclick":t.handleclick}},[e("el-table-column",{attrs:{prop:"sample_id",label:"样本",sortable:""}}),t._v(" "),e("el-table-column",{attrs:{prop:"batch",label:"批次",sortable:""}}),t._v(" "),e("el-table-column",{attrs:{prop:"status",label:"状态",sortable:""}}),t._v(" "),e("el-table-column",{attrs:{prop:"processed",label:"处理"}}),t._v(" "),e("el-table-column",{attrs:{prop:"cost_time",label:"耗时"}}),t._v(" "),e("el-table-column",{attrs:{prop:"submitted",label:"提交"}}),t._v(" "),e("el-table-column",{attrs:{prop:"running",label:"运行"}}),t._v(" "),e("el-table-column",{attrs:{prop:"finished",label:"结束"}}),t._v(" "),e("el-table-column",{attrs:{align:"center",width:"150px"}},[e("template",{slot:"header"},[e("el-input",{attrs:{size:"medium",placeholder:"输入关键字搜索"},model:{value:t.search,callback:function(a){t.search=a},expression:"search"}})],1)],2)],1),t._v(" "),e("el-dialog",{attrs:{center:"",title:"子任务详细信息",visible:t.dialogTableVisible,"close-on-click-modal":!1,width:"70%"},on:{"update:visible":function(a){t.dialogTableVisible=a}}},[e("el-table",{attrs:{data:t.sub_tableData}},[e("el-table-column",{attrs:{prop:"name",label:"name"}}),t._v(" "),e("el-table-column",{attrs:{prop:"sample_id",label:"sample"}}),t._v(" "),e("el-table-column",{attrs:{prop:"batch",label:"batch"}}),t._v(" "),e("el-table-column",{attrs:{prop:"status",label:"status",sortable:"true","sort-by":"string"}}),t._v(" "),e("el-table-column",{attrs:{prop:"swap_usage",label:"swap_usage"}}),t._v(" "),e("el-table-column",{attrs:{prop:"memory",label:"memory"}}),t._v(" "),e("el-table-column",{attrs:{prop:"cpu_usage",label:"cpu_usage"}}),t._v(" "),e("el-table-column",{attrs:{prop:"wallclock",label:"wallclock"}}),t._v(" "),e("el-table-column",{attrs:{prop:"slots",label:"slots"}}),t._v(" "),e("el-table-column",{attrs:{prop:"memory_usage",label:"memory_usage"}})],1)],1)],1)},L=[],T=e("7cf8"),z={props:{tableData:Array,sub_tableData:Array},data:function(){return{search:"",dialogTableVisible:!1}},methods:{handleclick:function(t,a,e){var n=this;this.dialogTableVisible=!0,console.log(t.sample_id),Object(T["e"])(t.sample_id).then(function(t){n.sub_tableData=t})},load_data:function(){return!1}}},M=z,R=Object(v["a"])(M,E,L,!1,null,null,null),$=R.exports,P=e("a4bb"),I=e.n(P),F=e("e814"),H=e.n(F);e("3b2b"),e("a481");function V(t){return"undefined"===typeof t||null==t||""==t}function A(t,a,e){if(V(t)||V(a))return 0;t=t.replace(/\-/g,"/"),a=a.replace(/\-/g,"/"),e=e.toLowerCase();var n=new Date(t),s=new Date(a),r=1;switch(e){case"second":r=1e3;break;case"minute":r=6e4;break;case"hour":r=36e5;break;case"day":r=864e5;break;default:break}return((s.getTime()-n.getTime())/H()(r)).toFixed(2)}function G(){var t=new Date,a="-",e=":",n=t.getMonth()+1,s=t.getDate();n>=1&&n<=9&&(n="0"+n),s>=0&&s<=9&&(s="0"+s);var r=t.getFullYear()+a+n+a+s+" "+t.getHours()+e+t.getMinutes()+e+t.getSeconds();return r}function q(t){var a=(new Date).Format("yyyy-MM-dd"),e=new Date(t["submitted"]).Format("yyyy-MM-dd");return a===e}function N(t){var a={"05":"done","04":"failed","03":"hold","02":"running","01":"qsub"},e=0,n=0,s=0,r=0;for(var l in t){var i=A(t[l]["running"],t[l]["finished"],"hour");switch(i,0==i?(i=A(t[l]["running"],G(),"hour"),t[l]["cost_time"]=i+" (h)"):t[l]["cost_time"]=i+" (h)",q(t[l])&&e++,t[l]["status"]){case"05":n++;break;case"02":r++;break;case"04":s++;default:break}t[l]["status"]=a[t[l]["status"]]}I()(t).length;return{tableData:t,today_sample:e,sample_done:n,sample_err:s,sample_running:r}}Date.prototype.Format=function(t){var a={"M+":this.getMonth()+1,"d+":this.getDate(),"H+":this.getHours(),"m+":this.getMinutes(),"s+":this.getSeconds(),"q+":Math.floor((this.getMonth()+3)/3),S:this.getMilliseconds()};for(var e in/(y+)/.test(t)&&(t=t.replace(RegExp.$1,(this.getFullYear()+"").substr(4-RegExp.$1.length))),a)new RegExp("("+e+")").test(t)&&(t=t.replace(RegExp.$1,1==RegExp.$1.length?a[e]:("00"+a[e]).substr((""+a[e]).length)));return t};var B={newVisitis:{expectedData:[100,120,161,134,105,160,165],actualData:[120,82,91,154,162,140,145]},messages:{expectedData:[200,192,120,144,160,130,140],actualData:[180,160,151,106,145,150,130]},purchases:{expectedData:[80,100,121,104,105,90,100],actualData:[120,90,100,138,142,130,130]},shoppings:{expectedData:[130,140,141,142,145,150,160],actualData:[120,82,91,154,162,140,130]}},J={name:"DashboardAdmin",components:{PanelGroup:_,LineChart:k,MonitorTable:$},data:function(){return{lineChartData:B.newVisitis,monitorData:[],projectID:[],sample_state:{}}},methods:{handleSetLineChartData:function(t){this.lineChartData=B[t]}},created:function(){var t=this;Object(T["d"])().then(function(a){var e=!0,n=!1,s=void 0;try{for(var r,l=d()(a);!(e=(r=l.next()).done);e=!0){var i=r.value;t.projectID.push(i["projectID"])}}catch(o){n=!0,s=o}finally{try{e||null==l.return||l.return()}finally{if(n)throw s}}console.log(t.projectID),Object(T["c"])(t.projectID).then(function(a){console.log(a);var e=N(a);t.monitorData=e["tableData"],t.sample_state=e})})}},Y=J,Z=(e("02aa"),Object(v["a"])(Y,i,o,!1,null,"07af9cb2",null)),W=Z.exports,K=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"dashboard-editor-container"},[e("div",{staticClass:" clearfix"},[e("pan-thumb",{staticStyle:{float:"left"},attrs:{image:t.avatar}},[t._v("\n      Your roles:\n      "),t._l(t.roles,function(a){return e("span",{key:a,staticClass:"pan-info-roles"},[t._v(t._s(a))])})],2),t._v(" "),e("github-corner",{staticStyle:{position:"absolute",top:"0px",border:"0",right:"0"}}),t._v(" "),e("div",{staticClass:"info-container"},[e("span",{staticClass:"display_name"},[t._v(t._s(t.name))]),t._v(" "),e("span",{staticStyle:{"font-size":"20px","padding-top":"20px",display:"inline-block"}},[t._v("Editor's Dashboard")])])],1),t._v(" "),e("div",[e("img",{staticClass:"emptyGif",attrs:{src:t.emptyGif}})])])},Q=[],U=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"pan-item",style:{zIndex:t.zIndex,height:t.height,width:t.width}},[e("div",{staticClass:"pan-info"},[e("div",{staticClass:"pan-info-roles-container"},[t._t("default")],2)]),t._v(" "),e("img",{staticClass:"pan-thumb",attrs:{src:t.image}})])},X=[],tt=(e("c5f6"),{name:"PanThumb",props:{image:{type:String,required:!0},zIndex:{type:Number,default:1},width:{type:String,default:"150px"},height:{type:String,default:"150px"}}}),at=tt,et=(e("2452"),Object(v["a"])(at,U,X,!1,null,"0d3d578f",null)),nt=et.exports,st=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("a",{staticClass:"github-corner",attrs:{href:"https://github.com/PanJiaChen/vue-element-admin",target:"_blank","aria-label":"View source on Github"}},[e("svg",{staticStyle:{fill:"#40c9c6",color:"#fff"},attrs:{width:"80",height:"80",viewBox:"0 0 250 250","aria-hidden":"true"}},[e("path",{attrs:{d:"M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z"}}),t._v(" "),e("path",{staticClass:"octo-arm",staticStyle:{"transform-origin":"130px 106px"},attrs:{d:"M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2",fill:"currentColor"}}),t._v(" "),e("path",{staticClass:"octo-body",attrs:{d:"M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 C139.8,137.7 141.6,141.9 141.8,141.8 Z",fill:"currentColor"}})])])},rt=[],lt=(e("364d"),{}),it=Object(v["a"])(lt,st,rt,!1,null,"4c6d8d88",null),ot=it.exports,ct={name:"DashboardEditor",components:{PanThumb:nt,GithubCorner:ot},data:function(){return{emptyGif:"https://wpimg.wallstcn.com/0e03b7da-db9e-4819-ba10-9016ddfdaed3"}},computed:Object(r["a"])({},Object(l["b"])(["name","avatar","roles"]))},dt=ct,ut=(e("efff"),Object(v["a"])(dt,K,Q,!1,null,"9c953d6a",null)),pt=ut.exports,ht={name:"Dashboard",components:{adminDashboard:W,editorDashboard:pt},data:function(){return{currentRole:"adminDashboard"}},computed:Object(r["a"])({},Object(l["b"])(["roles"])),created:function(){this.roles.includes("admin")||(this.currentRole="editorDashboard")}},mt=ht,bt=Object(v["a"])(mt,n,s,!1,null,null,null);a["default"]=bt.exports},c65c:function(t,a,e){},c958:function(t,a,e){},d479:function(t,a,e){},dbe6:function(t,a,e){"use strict";var n=e("c958"),s=e.n(n);s.a},efff:function(t,a,e){"use strict";var n=e("22a6"),s=e.n(n);s.a}}]);