<template>

    <Form ref="formInline" :model="formInline" :rules="ruleInline" style="width: 300px">
        <FormItem prop="user">
            <Input type="text" v-model="formInline.username" placeholder="Username">
                <Icon type="ios-person-outline" slot="prepend"></Icon>
            </Input>
        </FormItem>
        <FormItem prop="password">
            <Input type="password" v-model="formInline.password" placeholder="Password">
                <Icon type="ios-locked-outline" slot="prepend"></Icon>
            </Input>
        </FormItem>
        <FormItem prop="verifyCode">
                <Input v-model="formInline.verifyCode" placeholder="请输入验证码">
                    <span slot="prepend">
                    <Icon :size="14" type="lock-combination"></Icon>
                    </span>
                    <Button slot="append" @click="createCode">{{checkCode}}</Button>
                </Input>
        </FormItem>
        <FormItem>
            <Button type="primary" @click="handleSubmit('formInline')">Signin</Button>
        </FormItem>
    </Form>
</template>
<script>
import util from '../libs/util.js'
    export default {
        data () {
            return {
                formInline: {
                    username: '',
                    password: '',
                    verifyCode: ''
                },
                checkCode:'',
                ruleInline: {
                    username: [
                        { required: true, message: 'Please fill in the user name', trigger: 'blur' }
                    ],
                    password: [
                        { required: true, message: 'Please fill in the password.', trigger: 'blur' },
                        { type: 'string', min: 6, message: 'The password length cannot be less than 6 bits', trigger: 'blur' }
                    ],
                    verifyCode: [
                        { required: true, message: '验证码不能为空', trigger: 'blur' }
                    ]
                }
            }
        },
        methods: {
            handleSubmit(name) {
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        if(this.formInline.verifyCode.toUpperCase()!= this.checkCode.toUpperCase()){
                            this.$Message.info('验证码不正确');
                            this.createCode();
                            return;
                        }

                        let _this = this;
                        util.ajax.post('/api/login', _this.formInline)
                        .then((response) => {
                            console.log(response);
                            //状态码
                            // var ret = JSON.parse(response.data);
                            var ret = response.data;
                            // _this.$Message.debug(ret.msg);
                            console.log(ret);
                            switch(ret.status) {
                            case "0" || 0:
                                console.log(ret);
                                localStorage.setItem('token', ret.token);
                                // localStorage.setItem('expires', ret.expires);
                                // localStorage.setItem('user_name', ret.user_name);
                                _this.$Message.success('Success!');
                                _this.$router.push({
                                    name: 'register'
                                });
                                break;
                            case "4106":
                                _this.show = true;
                                _this.formInline = {
                                    userName: '',
                                    password: '', 
                                    verifyCode: '',
                                };
                                _this.createCode();
                                _this.$Message.error(ret.msg);
                                break;
                            case "4104":
                                _this.show = false;
                                _this.$router.push({
                                    name: 'register'
                                });
                                break;
                            default:
                                _this.$Message.info('登陆异常, 稍后重试');
                            }
                        })
                        .catch(function(response) {
                            console.log(response);
                            _this.createCode();
                            _this.$Message.info('登陆失败');
                        })
                    } else {
                        _this.$Message.error('Fail!');
                    }
                })
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
    }
</script>

<style>
    .verification1{
    vertical-align: middle;
    transform: translate(-15px,0);
    width: 102px;
}
</style>