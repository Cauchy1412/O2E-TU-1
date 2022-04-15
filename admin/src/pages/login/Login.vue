<template>
  <common-layout>
    <div class="top">
      <div class="header">
        <img alt="logo" class="logo" src="@/assets/img/logo.png" />
        <span class="title">{{ systemName }}</span>
      </div>
      <div class="desc">希望是一个好东西，也许是最好的，好东西是不会消亡的</div>
    </div>
    <div class="login">
      <a-form @submit="onSubmit" :form="form">
        <a-tabs
          size="large"
          :tabBarStyle="{ textAlign: 'center' }"
          style="padding: 0 2px;"
        >
          <a-tab-pane tab="账户密码登录" key="1">
            <a-alert
              type="error"
              :closable="true"
              v-show="error"
              :message="error"
              showIcon
              style="margin-bottom: 24px;"
            />
            <a-form-item>
              <a-input
                autocomplete="autocomplete"
                size="large"
                placeholder="用户名"
                v-decorator="[
                  'name',
                  {
                    rules: [
                      {
                        required: true,
                        message: '请输入账户名',
                        whitespace: true,
                      },
                    ],
                  },
                ]"
              >
                <a-icon slot="prefix" type="user" />
              </a-input>
            </a-form-item>
            <a-form-item>
              <a-input
                size="large"
                placeholder="密码"
                autocomplete="autocomplete"
                type="password"
                v-decorator="[
                  'password',
                  {
                    rules: [
                      {
                        required: true,
                        message: '请输入密码',
                        whitespace: true,
                      },
                    ],
                  },
                ]"
              >
                <a-icon slot="prefix" type="lock" />
              </a-input>
            </a-form-item>
          </a-tab-pane>
        </a-tabs>

        <a-form-item>
          <a-button
            :loading="logging"
            style="width: 100%;margin-top: 24px"
            size="large"
            htmlType="submit"
            type="primary"
            >登录</a-button
          >
        </a-form-item>
      </a-form>
    </div>
  </common-layout>
</template>

<script>
import CommonLayout from "@/layouts/CommonLayout";
import { login, getRoutesConfig } from "@/services/user";
import { setAuthorization } from "@/utils/request";
import { loadRoutes } from "@/utils/routerUtil";
import { mapMutations } from "vuex";

export default {
  name: "Login",
  components: { CommonLayout },
  data() {
    return {
      logging: false,
      error: "",
      form: this.$form.createForm(this),
    };
  },
  computed: {
    systemName() {
      return this.$store.state.setting.systemName;
    },
  },
  methods: {
    ...mapMutations("account", ["setUser", "setPermissions", "setRoles"]),
    onSubmit(e) {
      e.preventDefault();
      this.form.validateFields((err) => {
        if (!err) {
          this.logging = true;
          const name = this.form.getFieldValue("name");
          const password = this.form.getFieldValue("password");
          if(name!="SUPERMAN"){
            // login(name, password)
            this.$message.error("账号或密码错误")
            // this.$router.push("");
            this.logging = false;
          }else{
            login(name, password).then(this.afterLogin)
            .catch((error) => {
            this.$message.error("账号或密码错误")
            this.logging=false;
            console.log(error);
            // console.log(name);
            // console.log(password);
          });
          }
          
        }
      });
    },
    afterLogin(res) {
      // console.log(res)
      const positions = [
        {
          CN: "管理员 | PAP-WE-1-后台管理",
          HK: "Java工程師 | 螞蟻金服-計算服務事業群-微信平台部",
          US:
            "Java engineer | Ant financial - Computing services business group - WeChat platform division",
        },
      ];
      const user1 = {
        name: res.data.userInfo.username,
        avatar:
          "https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png",
        address: "重庆市",
        position: positions[0],
      };
      const role = [{id: 'admin', operation: ['add', 'edit', 'delete']}]

      this.logging = false;
      const loginRes = res.data;
      // console.log(res);
      loginRes.message='欢迎回来'
      // const { permissions, roles } = loginRes.data;
      this.setUser(user1);
      // this.setPermissions(permissions);
      this.setRoles(role);
      setAuthorization({
        token: res.data.access_token,
        expireAt: new Date(new Date().getTime() + 30 * 60 * 1000),
      });
      // 获取路由配置
      getRoutesConfig().then((result) => {
        const routesConfig = result.data.data;
        loadRoutes(routesConfig);
        this.$router.push("/dashboard");
        this.$message.success(loginRes.message, 3);
      });
      // console.log(res);
    },
  },
};
</script>

<style lang="less" scoped>
.common-layout {
  .top {
    text-align: center;
    .header {
      height: 44px;
      line-height: 44px;
      a {
        text-decoration: none;
      }
      .logo {
        height: 44px;
        vertical-align: top;
        margin-right: 16px;
      }
      .title {
        font-size: 33px;
        color: @title-color;
        font-family: "Myriad Pro", "Helvetica Neue", Arial, Helvetica,
          sans-serif;
        font-weight: 600;
        position: relative;
        top: 2px;
      }
    }
    .desc {
      font-size: 14px;
      color: @text-color-second;
      margin-top: 12px;
      margin-bottom: 40px;
    }
  }
  .login {
    width: 368px;
    margin: 0 auto;
    @media screen and (max-width: 576px) {
      width: 95%;
    }
    @media screen and (max-width: 320px) {
      .captcha-button {
        font-size: 14px;
      }
    }
    .icon {
      font-size: 24px;
      color: @text-color-second;
      margin-left: 16px;
      vertical-align: middle;
      cursor: pointer;
      transition: color 0.3s;

      &:hover {
        color: @primary-color;
      }
    }
  }
}
</style>
