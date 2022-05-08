<template>
  <a-card :bordered="false">
    <a-table :data-source="data" :columns="columns">
      <template
        slot-scope="text, record"
      >
        <div :key="col">
          <a-input
            v-if="record.editable"
            style="margin: -5px 0"
            :value="text"
            @change="(e) => handleChange(e.target.value, record.key)"
          />
          <template v-else>
            <div class="meta-content">
              {{ text }}
            </div>
          </template>
        </div>
      </template>
      <!--<template slot="operation" slot-scope="text, record">
        <a-popconfirm
          v-if="data.length"
          title="确定通过认证吗?"
          @confirm="() => onVerified(record.key)"
        >
          <a>查看</a>
        </a-popconfirm>
        <div></div>
        <a-popconfirm
          v-if="data.length"
          title="确定打回认证吗?"
          @confirm="() => onFailed(record.key)"
        >
          <a>编辑</a>
        </a-popconfirm>
      </template>-->
    </a-table>


  </a-card>
</template>

<script>
import {get_resolution_all} from "../../../services/demand";

const data = [];

const columns = [
  {
    title: "需求标题",
    dataIndex: "title",
    width: "18%",
    scopedSlots: { customRender: "title" },
  },
  {
    title: "企业名",
    dataIndex: "company",
    width: "18%",
    scopedSlots: { customRender: "company" },
  },
  {
    title: "专家名",
    dataIndex: "expert",
    width: "10%",
    scopedSlots: { customRender: "expert" },
  },
  {
    title: "维持时间",
    dataIndex: "time",
    width: "10%",
    scopedSlots: { customRender: "time" },
  },
  {
    title: "发起时间",
    dataIndex: "created_at",
    width: "15%",
    scopedSlots: { customRender: "created_at" },
  },
  {
    title: "订单状态",
    dataIndex: "state",
    width: "10%",
    scopedSlots: { customRender: "state" },
  },
  {
    title: "订单价格",
    dataIndex: "price",
    width: "10%",
    scopedSlots: { customRender: "price" },
  },
  /*{
    title: "操作",
    dataIndex: "operation",
    scopedSlots: { customRender: "operation" },
  }*/
];

export default {
  name: "ResolutionForm",
  data() {
    this.cacheData = data.map((item) => ({ ...item }));
    return {
      data,
      columns,
    }
  },
  mounted() {
    this.init();
    console.log(data)
  },
  methods: {
    init: async function() {
      this.getResolution();
    },
    getResolution() {
      this.loading = true
      data.length = 0       // 两个语句避免数据重复写
      get_resolution_all()
        .then((res) => {
          console.log(res)
          for (let i = 0; i < res.data.resolution_list.length; i++) {
            data.push({
              key:res.data.resolution_list[i].id,
              company:res.data.resolution_list[i].company_meta['name'],
              expert:res.data.resolution_list[i].scholar_meta['name'],
              time:res.data.resolution_list[i].time,
              created_at:this.dateTrans(res.data.resolution_list[i].created_at),
              title: res.data.resolution_list[i].title,
              state: this.status(res.data.resolution_list[i].state),
              price: res.data.resolution_list[i].price + "元",
            })
          }
          this.loading = false
        })
        .catch((error) => {
          console.log(error)
        })
    },
    dateTrans(date) {
      let dateTime = new Date(new Date(date).getTime() + 8 * 3600 * 1000)
      dateTime = dateTime.toJSON()
      dateTime = dateTime.substring(0,19).replace('T', ' ')
      return dateTime
    },
    status(state) {
      switch (state) {
        case 1:
          return "等待专家接受"
        case 2:
          return "已接受"
        case 3:
          return "已完成"
        case 4:
          return "已拒绝"
        default:
          return "未形成"
      }
    },
    handleChange() {
      this.getResolution()
    },
    onVerified() {

    },
    onFailed() {

    },
  }
}
</script>

<style scoped>
.meta-content{
  white-space: pre-wrap;
}
</style>