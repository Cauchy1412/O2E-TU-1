<template>
  <a-card :bordered="false">
    <a-table :data-source="data" :columns="columns">
      <template
        v-for="col in ['name', 'truename', 'email', 'type', 'verified_type']"
        :slot="col"
        slot-scope="text, record"
      >
        <div :key="col">
          <a-input
            v-if="record.editable"
            style="margin: -5px 0"
            :value="text"
            @change="(e) => handleChange(e.target.value, record.key, col)"
          />
          <template v-else>
            {{ text }}
          </template>
        </div>
      </template>
      <template slot="operation" slot-scope="text, record">
        <div class="editable-row-operations">
          <span v-if="record.editable">
            <a-space>
              <a @click="() => save(record.key)">Save</a>
              <a-popconfirm
                title="Sure to cancel?"
                @confirm="() => cancel(record.key)"
              >
                <a>Cancel</a>
              </a-popconfirm>
            </a-space>
          </span>
          <span v-else>
            <a :disabled="editingKey !== ''" @click="() => edit(record.key)"
              >编辑</a
            >
          </span>
        </div>
        <a-popconfirm
          v-if="data.length"
          title="Sure to delete?"
          @confirm="() => onDelete(record.key)"
        >
          <a href="javascript:0;">删除</a>
        </a-popconfirm>
      </template>
    </a-table>
    
    
  </a-card>
</template>

<script>
import { getUserAll,UserDel,UserModify } from "@/services/dataSource";
const columns = [
  {
    title: "用户名",
    dataIndex: "name",
    width: "20%",
    scopedSlots: { customRender: "name" },
  },
  {
    title: "真实姓名/企业名",
    dataIndex: "truename",
    width: "25%",
    scopedSlots: { customRender: "truename" },
  },
  {
    title: "邮箱",
    dataIndex: "email",
    width: "20%",
    scopedSlots: { customRender: "email" },
  },
  {
    title: "用户类型",
    dataIndex: "type",
    width: "15%",
    scopedSlots: { customRender: "type" },
    filters: [
      {
        text: '专家',
        value: '专家',
      },
      {
        text: '企业',
        value: '企业',
      },
    ],
    filterMultiple: false,
    onFilter: (value, record) => record.type.indexOf(value) === 0,
  },
  {
    title: "认证状态",
    dataIndex: "verified_type",
    width: "10%",
    scopedSlots: { customRender: "verified_type" },
    filters: [
      {
        text: '未认证',
        value: '未认证',
      },
      {
        text: '已通过',
        value: '已通过',
      },
      {
        text: '未通过',
        value: '未通过',
      },
    ],
    filterMultiple: false,
    onFilter: (value, record) => record.verified_type.indexOf(value) === 0,
  },
  {
    title: "操作",
    dataIndex: "operation",
    scopedSlots: { customRender: "operation" },
  },
];

const data = [];

export default {
  name: "UserForm",
  i18n: require("./i18n-user"),
  data() {
    this.cacheData = data.map((item) => ({ ...item }));
    return {
      type:"",
      verified_type:"",
      type1:0,
      data,
      columns,
      editingKey: "",
      curindex:0,
    };
  },
  // computed: {
  //   dataColumns() {
  //     return this.columns.map(column => {
  //       column.title = this.$t('table.' + column.key)
  //       return column
  //     })
  //   }
  // },
  mounted() {
    this.init();
  },

  methods: {
    init: async function() {
      this.loadUser();
    },

    loadUser: function() {
      this.loading = true;
      data.length=0;
      getUserAll()
        .then((res) => {
          console.log(res);
          for (let i = 0; i < res.data.length; i++) {
            this.type = (res.data[i].user_type==0)?"专家":(res.data[i].user_type==2)?"企业":"无"
            this.verified_type = (res.data[i].verified_type==1)?"已通过":
                                 (res.data[i].verified_type==2)?"未通过":"未认证"
            data.push({
              key: res.data[i].id,
              name: res.data[i].username,
              truename: (res.data[i].meta)?res.data[i].meta['name']:"无",  //本地数据库的坏数据可能没有meta
              verified_type: this.verified_type,
              type: this.type,
              email: res.data[i].email,
            });
          }
          this.totalCnt = res.data.total_count;
          this.loading = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    onDelete(key) {
      const newData = [...this.data];
      this.data = newData.filter((item) => item.key !== key);
      const target = newData.filter((item) => key === item.key)[0];
      if(target.type=="个人"){
        this.type1=0
      }else if(target.type=="学校"){
        this.type1=1
      }else{
        this.type1=2
      }
      const params = {
        id:target.key,
        name: target.name,
        usertype: this.type1,
        //institution:target.ins,
        mail: target.email,
      };
      UserDel(params)
        .then((res) => {
          this.$message.info("成功删除");
          // this.loadUser();
          console.log(res)
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleChange() {
      this.loadUser()
    },
    edit(key) {
      const newData = [...this.data];
      const target = newData.filter((item) => key === item.key)[0];
      this.editingKey = key;
      if (target) {
        target.editable = true;
        this.data = newData;
      }
    },
    save(key) {
      const newData = [...this.data];
      const newCacheData = [...this.cacheData];
      const target = newData.filter((item) => key === item.key)[0];
      const targetCache = newCacheData.filter((item) => key === item.key)[0];
      if (target && targetCache) {
        delete target.editable;
        this.data = newData;
        Object.assign(targetCache, target);
        this.cacheData = newCacheData;
      }
      this.editingKey = "";
      if(target.type=="个人"){
        this.type1=0
      }else if(target.type=="学校"){
        this.type1=1
      }else{
        this.type1=2
      }
      const params = {
        id:target.key,
        name: target.name,
        usertype: this.type1,
        //institution:target.ins,
        mail: target.email,
      };
      UserModify(params)
        .then((res) => {
          this.$message.info("成功修改");
          console.log(res)
        })
        .catch((error) => {
          this.$message.error("无法修改")
          console.log(error);
        });
      if (target) {
        Object.assign(
          target,
          this.cacheData.filter((item) => key === item.key)[0]
        );
        delete target.editable;
        this.data = newData;
      }
      // this.loadUser()
      // console.log(target.editable)
      
    },
    cancel(key) {
      const newData = [...this.data];
      const target = newData.filter((item) => key === item.key)[0];
      this.editingKey = "";
      if (target) {
        Object.assign(
          target,
          this.cacheData.filter((item) => key === item.key)[0]
        );
        delete target.editable;
        this.data = newData;
      }
    },
    switchtab(index) {
      this.curindex = index
    },
  },
};
</script>

<style scoped>
.tab {
  display: flex;
  position: relative;
  top: 1px;
}
.tab li {
  list-style: none;
  margin-right: 10px;
  padding: 0 20px;
  line-height: 35px;
  border: 1px solid #AAA;
  background: #EEE;
  cursor: pointer;
}
.tab li.active {
  background: #FFF;
  border-bottom-color: #FFF;
}
.highlight {
  background-color: rgb(255, 192, 105);
  padding: 0px;
}
.editable-row-operations a {
  margin-right: 8px;
}
</style>
