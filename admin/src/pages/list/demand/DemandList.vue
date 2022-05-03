<template>
  <div>
    <a-card
      style="margin-top: 24px"
      :bordered="false"
      title="标准列表"
    >
      <a-list
          size="large"
          :pagination="pagination"
          :data-source="listData">
        <a-list-item slot="renderItem" key="item.title" slot-scope="item">
          <a-list-item-meta>
            <a slot="title" >{{item.title}}</a>
            <a slot="description"
               class="textbreak"
               href="javascript:void(0)">
              {{item.description|ellipsis}}</a>
          </a-list-item-meta>
          <div class="list-content">
            <div class="list-content-item">
              <span>创建时间</span>
              <p>2018-07-26 22:44</p>
            </div>
            <div class="list-content-item">
              <span>研发周期</span>
              <p>暂定</p>
            </div>
            <div class="list-content-item">
              <span>研发经费</span>
              <p>暂定</p>
            </div>
            <div class="list-content-item">
              <span>研发地点</span>
              <p>暂定</p>
            </div>
          </div>
          <div slot="actions">
            <a>查看详情</a>
          </div>
          <div slot="actions">
            <a-dropdown>
              <a-menu slot="overlay">
                <a-menu-item><a>编辑</a></a-menu-item>
                <a-menu-item><a>删除</a></a-menu-item>
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

const listData = [{
                    title: "随便写写",
                    description: "那是一种内在的东西， 他们到达不了，也无法触及的.那是一种内在的东西， 他们到达不了，也无法触及的."
                  },
                  {
                    title: "随便写写",
                    description: "那是一种内在的东西， 他们到达不了，也无法触及的"
                  }];

export default {
  name: "DemandList",
  filters: {
    ellipsis (value) {
      if (!value) return ''
      if (value.length > 30) {
        return value.slice(0,30) + '...'
      }
      return value
    }
  },
  data() {
    return {
      listData,
      pagination: {
        onChange: (page) => {
          console.log(page);
        },
        pageSize: 10,
      }
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