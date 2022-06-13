<template>
  <div>
    <a-card :bordered="false">
      <a-list
          size="large"
          :pagination="pagination"
          :data-source="listData">
        <a-list-item slot="renderItem" key="item.title" slot-scope="item">
          <a-list-item-meta>
            <a slot="title" >{{item.title}}</a>
            <a slot="description"
               class="textbreak"
               href="javascript:void(0)"
               @click="handleClick(item.key)">
              {{item.description|ellipsis}}</a>
          </a-list-item-meta>
          <a-Modal v-model="showDetail" title="" @ok="handleOk" width="750px" v-bind="showData">
            <a-card :bordered="false" dis-hover>
              <div slot="title">
                发布用户:
                <a href="javascript:0">{{showData.username}}</a>
              </div>
              <p slot="extra"> 该需求发布于: {{showData.created_at}}</p>
              <a-Row> 标题: {{showData.title}}</a-Row>
              <br />
              <br />
              <br />
              <a-Row> 需求描述: {{showData.description}}</a-Row>
              <br />
              <a-Row> 研发周期: {{showData.period}}</a-Row>
              <a-Row> 研发经费: {{showData.fund}}</a-Row>
              <a-Row> 研发地点: {{showData.place}}</a-Row>
              <a-Row> 关键词: {{showData.keywords}}</a-Row>
            </a-card>
          </a-Modal>
          <div class="list-content">
            <div class="list-content-item">
              <span>发布用户</span>
              <p>{{item.username}}</p>
            </div>
            <div class="list-content-item">
              <span>创建时间</span>
              <p>{{item.created_at}}</p>
            </div>
            <div class="list-content-item">
              <span>研发周期</span>
              <p>{{item.period}}</p>
            </div>
            <div class="list-content-item">
              <span>研发经费</span>
              <p>{{item.fund}}</p>
            </div>
            <div class="list-content-item">
              <span>研发地点</span>
              <p>{{item.place}}</p>
            </div>
            <div class="list-content-item">
              <span>关键词</span>
              <p>{{item.keywords}}</p>
            </div>
          </div>
          <div slot="actions">
            <a-dropdown>
              <a-menu slot="overlay">
                <a-menu-item @click="handleClick(item.key)"><a>查看详情</a></a-menu-item>
                <a-menu-item>
                  <a-popconfirm
                  title="确定要删除此需求？"
                  ok-text="确定"
                  cancel-text="取消"
                  @confirm="delDemand(item.key)"
                >
                  <a>删除</a>
                </a-popconfirm>
                </a-menu-item>
              </a-menu>
              <a>更多<a-icon type="down"/></a>
            </a-dropdown>
          </div>

        </a-list-item>
      </a-list>
    </a-card>
  </div>
</template>



<script>
import {get_demand_all, del_demand} from "../../../services/demand";

const listData = [];

export default {
  name: "DemandList",
  filters: {
    ellipsis (value) {
      if (!value) return ''
      if (value.length > 25) {
        return value.slice(0,25) + '...'
      }
      return value
    }
  },
  data() {
    return {
      listData,
      showData: {},
      showDetail:false,
      pagination: {
        onChange: (page) => {
          console.log(page);
        },
        pageSize: 10,
      }
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init:async function() {
      this.getDemand()
    },
    getDemand() {
      this.loading = true;
      listData.length=0;
      get_demand_all()
          .then((res) => {
            console.log(res);
            for(let i = 0; i < res.data.demand_list.length; i++) {
              listData.push({
                key: res.data.demand_list[i].id,
                username: res.data.demand_list[i].user['username'],
                title: res.data.demand_list[i].title,
                description: res.data.demand_list[i].description,
                created_at:this.dateTrans(res.data.demand_list[i].created_at),
                fund:res.data.demand_list[i]['meta'].fund?res.data.demand_list[i]['meta'].fund:"暂定",
                period:res.data.demand_list[i]['meta'].period?res.data.demand_list[i]['meta'].period:"暂定",
                place:res.data.demand_list[i]['meta'].place?res.data.demand_list[i]['meta'].place:"暂定",
                keywords:res.data.demand_list[i].keywords?this.keywordTrans(res.data.demand_list[i].keywords):"无",
              })
            }
            console.log(listData)
            this.loading = false
          })
          .catch((error) => {
            console.log(error)
          });
    },
    dateTrans(date) {
      let dateTime = new Date(new Date(date).getTime() + 8 * 3600 * 1000)
      dateTime = dateTime.toJSON()
      dateTime = dateTime.substring(0,19).replace('T', ' ')
      return dateTime
    },
    keywordTrans(list) {
      let words = ""
      for(let i = 0; i < list.length - 1; i++) {
        words = words + list[i] + ","
      }
      words = words + list[list.length - 1]
      return words
    },
    delDemand(index) {
      let del_data = listData.filter((item) => index === item.key)[0];
      const params = {
        id: del_data.key
      };
      del_demand(params)
      .then((res) => {
        this.$message.info("成功删除");
        this.getDemand()
        console.log(res)
      })
      .catch((error) => {
        console.log(error)
      })
    },
    handleClick(index) {
      this.showData = listData.filter((item) => index === item.key)[0];
      this.showDetail = true;
    },
    handleOk() {
      this.showDetail = false;
    }
  }
}
</script>

<style scoped>
.textbreak {
    white-space: nowrap;
    word-break: break-all;
}

.list-content-item{
  color: @text-color-second;
  display: inline-block;
  min-width: 70px;
  vertical-align: middle;
  font-size: 14px;
  margin-left: 40px;
  margin-top: 10px;
  span{
    line-height: 20px;
  }
  p{
    margin: 4px 0 0;
    line-height: 22px;
  }
}
</style>