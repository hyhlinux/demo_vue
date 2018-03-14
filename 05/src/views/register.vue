Skip to content
This repository
Search
Pull requests
Issues
Marketplace
Explore
 @hyhlinux
Sign out
1
0 0 kufei88/vue-register
 Code  Issues 0  Pull requests 0  Projects 0  Wiki  Insights
vue-register/src/views/login.vue
e52d3fa  on 11 Jan
@kufei88 kufei88 2018-01-11
     
148 lines (136 sloc)  5.8 KB
<style lang="less">
    @import './login.less';
</style>

<template>
    <div class="login" @keydown.enter="handleSubmit">
        <div class="login-con">
            <Card :bordered="false">
                <p slot="title">
                    <Icon type="log-in"></Icon>
                    欢迎登录
                </p>
                <div class="form-con">
                    <Form ref="loginForm" :model="form" :rules="rules">
                        <FormItem prop="userName">
                            <Input v-model="form.userName" placeholder="请输入用户名">
                                <span slot="prepend">
                                    <Icon :size="16" type="person"></Icon>
                                </span>
                            </Input>
                        </FormItem>
                        <FormItem prop="password">
                            <Input v-model="form.password" type="password" placeholder="请输入密码">
                                <span slot="prepend">
                                    <Icon :size="14" type="locked"></Icon>
                                </span>
                            </Input>
                        </FormItem>
                        <FormItem prop="verifyCode">
                            <Input v-model="form.verifyCode" placeholder="请输入验证码">
                                <span slot="prepend">
                                    
                                    <Icon :size="14" type="lock-combination"></Icon>
                                </span>
                                <Button slot="append" @click="createCode">{{checkCode}}</Button>
                                
                            </Input>
                            
                        </FormItem>
                        <FormItem>
                            <Button @click="handleSubmit" type="primary" long>登录</Button>
                        </FormItem>
                    </Form>
                  
                </div>
            </Card>
        </div>
    </div>
</template>

<script>
import Cookies from 'js-cookie';
import util from '../libs/util.js'
export default {
    data () {
        return {
            form: {
                userName: '',
                password: '',
                verifyCode:'',
            },
            checkCode:'',
            rules: {
                userName: [
                    { required: true, message: '账号不能为空', trigger: 'blur' }
                ],
                password: [
                    { required: true, message: '密码不能为空', trigger: 'blur' }
                ],
                verifyCode: [
                    { required: true, message: '验证码不能为空', trigger: 'blur' }
                ]
            }
        };
    },
    methods: {
        handleSubmit () {
            this.$refs.loginForm.validate((valid) => {
                if (valid) {
                    
                    if(this.form.verifyCode.toUpperCase()!=this.checkCode.toUpperCase()){
                        this.$Message.info('验证码不正确');
                        this.createCode();
                        return;
                    }
                    let _this = this;
                    util.ajax.get('checkLogin.asp?username='+this.form.userName+'&password='+
                    this.form.password)
                    .then(function(response){
                        if(response.data == 'success'){
                            let inFifteenMinutes = new Date(new Date().getTime() + 15 * 60 * 1000);
                            Cookies.set('user', _this.form.userName, {
                                            expires: inFifteenMinutes
                                        });
                            Cookies.set('password', _this.form.password, {
                                            expires: inFifteenMinutes
                                        });
                            _this.$store.commit('setAvator', 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=3448484253,3685836170&fm=27&gp=0.jpg');
                            if (_this.form.userName === 'iview_admin') {
                                Cookies.set('access', 0, {
                                            expires: inFifteenMinutes
                                        });
                            } else {
                                Cookies.set('access', 1, {
                                            expires: inFifteenMinutes
                                        });
                            }
                            _this.$router.push({
                                name: 'home_index'
                            });
                        }else{
                            _this.$Message.info('用户名或密码错误');
                            _this.createCode();
                            return;
                        }
                        
                        
                    })
                   
                }
            });
        },
        createCode(){
          let code = "";    
          var codeLength = 4;//验证码的长度   
          var random = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',   
           'S','T','U','V','W','X','Y','Z');//随机数   
          for(var i = 0; i < codeLength; i++) {//循环操作   
              var index = Math.floor(Math.random()*36);//取得随机数的索引（0~35）   
              code += random[index];//根据索引取得随机数加到code上   
          }   
              this.checkCode = code;//把code值赋给验证码   
      },
    },
    created(){
        this.createCode();
    }
};
</script>

<style>
    .verification1{
    vertical-align: middle;
    transform: translate(-15px,0);
    width: 102px;
}
</style>
© 2018 GitHub, Inc.
Terms
Privacy
Security
Status
Help
Contact GitHub
API
Training
Shop
Blog
About