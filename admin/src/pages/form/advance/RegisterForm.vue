<template>
  <a-card :bordered="false">
    <a-table :data-source="data" :columns="columns">
      <template
        v-for="col in ['name', 'email', 'type', 'meta']"
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
            <div class="meta-content">
              {{ text }}
            </div>
          </template>
        </div>
      </template>
      <template slot="operation" slot-scope="text, record">
        <a-popconfirm
          v-if="data.length"
          title="确定通过认证吗?"
          @confirm="() => onVerified(record.key)"
        >
          <a>通过</a>
        </a-popconfirm>
        <div></div>
        <a-popconfirm
          v-if="data.length"
          title="确定打回认证吗?"
          @confirm="() => onFailed(record.key)"
        >
          <a>拒绝</a>
        </a-popconfirm>
      </template>
    </a-table>


  </a-card>
</template>

<script>
import { getUserAll,set_verified,set_failed } from "@/services/dataSource";
const columns = [
  {
    title: "用户名",
    dataIndex: "name",
    width: "20%",
    scopedSlots: { customRender: "name" },
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
  },
  {
    title: "详情",
    dataIndex: "meta",
    width: "25%",
    scopedSlots: { customRender: "meta" },
  },
  {
    title: "操作",
    dataIndex: "operation",
    scopedSlots: { customRender: "operation" },
  }
];

const data = [];
export default {
  name: "RegisterForm",
  i18n: require("./i18n-user"),
  data() {
    this.cacheData = data.map((item) => ({ ...item }));
    return {
      type:"",
      type1:0,
      data,
      columns,
      editingKey: "",
      expert_model:{
        name:'',

      },
      business_model:{

      },
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
            if(res.data[i].user_type==0){
              this.type="专家"
            }else if(res.data[i].user_type==2){
              this.type="企业"
            }else{
              this.type="其他"
            }
            if(res.data[i].verified_type==0){  //仅展示未认证用户
               data.push({
                key: res.data[i].id,
                name: res.data[i].username,
                email: res.data[i].email,
                type: this.type,
                meta: this.meta_tostring(res.data[i].user_type, res.data[i].meta),
              });
            }
          }
          this.totalCnt = res.data.total_count;
          this.loading = false;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    meta_tostring(type, meta) {
      if(type===0) {
        let domain_str = "";
        for (let i = 0; i < meta['domains'].length; i++) {
          domain_str = domain_str + meta['domains'][i] + ' '
        }
        return "真实姓名：" + meta['name'] + "\n" +
            "性别：" + meta['gender'] + "\n" +
            "职称：" + meta['professor'] + "\n" +
            "研究领域：" + domain_str;
      }else if(type===2) {
        return "企业名：" + meta['name'] + "\n" +
            "公司类型：" + meta['business_type'] + "\n" +
            "注册地：" + meta['place'] + "\n" +
            "注册号：" + meta['regisnumber'] + "\n" +
            "法定代表人：" + meta['legalperson'];
      }
      return "";
    },
    onVerified(key) {
      const newData = [...this.data];
      this.data = newData.filter((item) => item.key !== key);
      const target = newData.filter((item) => key === item.key)[0];
      const params = {
        id:target.key,
      };
      set_verified(params)
        .then((res) => {
          this.$message.info("该用户认证成功！");
          // this.loadUser();
          console.log(res)
        })
        .catch((error) => {
          console.log(error);
        });
    },
    onFailed(key) {
      const newData = [...this.data];
      this.data = newData.filter((item) => item.key !== key);
      const target = newData.filter((item) => key === item.key)[0];
      const params = {
        id:target.key,
      };
      set_failed(params)
        .then((res) => {
          this.$message.info("该用户已拒绝认证！");
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
  },
}
</script>

<style scoped>
.meta-content{
  white-space: pre-wrap;
}
</style>