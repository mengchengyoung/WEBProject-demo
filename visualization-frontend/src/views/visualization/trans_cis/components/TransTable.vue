<template>
    <div class="appcontainer">
        <el-table
        :data="tableData"
        style="width: 100%"
        border   
        >
            <el-table-column
            v-for = "item in labelData"
            :prop = "item.prop"
            :label = "item.label"
            :key = "item.id"
            >         
            </el-table-column>
            <el-table-column>
                <template slot="header">
                    <el-button >
                        <a :href="bamfile"> 点击下载 </a>
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>
<script>

export default {
    props:{
        tableData: Array,
        labelData: Array,
        bamfile: String
    },
}
</script>
