<template>
    <Card style="width:400px">
        <div style="text-align:center">
            <img src="https://raw.githubusercontent.com/iview/iview/master/assets/logo.png">
        </div>
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
    </Card>
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
                            this.checkCode = util.createCode();
                            return;
                        }

                        let _this = this;
                        console.log(_this.formInline);
                        util.ajax.post('/api/login', _this.formInline)
                        .then((response) => {
                            console.log(response);
                            //状态码
                            // var ret = JSON.parse(response.data);
                            var ret = response.data;
                            let redirect = this.$route.query.redirect;
                            console.log(ret, redirect);
                            switch(ret.status) {
                            case "0" || 0:
                                util.saveData(ret);
                                _this.$Message.success('Success!');
                                _this.redirect(redirect); 
                                break;
                            case "4106":
                                _this.show = true;
                                _this.formInline = {
                                    userName: '',
                                    password: '', 
                                    verifyCode: '',
                                };
                                _this.checkCode = util.createCode();;
                                _this.$Message.error(ret.msg);
                                break;
                            case "4104":
                                _this.show = false;
                                _this.$router.push({ path: '/register'});
                                break;
                            default:
                                _this.$Message.info('登陆异常, 稍后重试');
                            }
                        })
                        .catch(function(response) {
                            console.log(response);
                            _this.checkCode = util.createCode();
                            _this.$Message.info('登陆失败');
                        })
                    } else {
                        _this.$Message.error('Fail!');
                    }
                })
            },
            redirect(redirect) {
                if(redirect !=='/login' && redirect !=='' && !!redirect) {
                    this.$router.push(redirect)
                } else {
                    this.$router.push({path:'/'})
                }
            },
            createCode() {
                this.checkCode = util.createCode();
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