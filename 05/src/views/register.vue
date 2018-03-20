<template>
    <Form ref="formInline" :model="formInline" :rules="ruleInline" style="width: 300px">
        <FormItem prop="user">
            <Input type="text" v-model="formInline.username" placeholder="Username">
                <Icon type="ios-person-outline" slot="prepend"></Icon>
            </Input>
        </FormItem>
        <FormItem prop="email">
            <Input type="text" v-model="formInline.email" placeholder="xx@[163|qq|*].com">
                <span slot="prepend">
                    <Icon :size="14" type="ios-email"></Icon>
                </span>
            </Input>
        </FormItem>
        <FormItem prop="password">
            <Input type="password" v-model="formInline.password" placeholder="Password">
                <Icon type="ios-locked-outline" slot="prepend"></Icon>
            </Input>
        </FormItem>
      <FormItem prop="passwdCheck" v-show="formInline.showConfirm">
            <Input type="password" v-model="formInline.passwdCheck" placeholder="passwdCheck">
                <span slot="prepend">
                    <Icon :size="14" type="ios-checkmark"></Icon>
                </span>
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
            <Button type="primary" @click="handleSubmit('formInline')">Sinup</Button>
        </FormItem>
    </Form>
</template>
<script>
import util from '../libs/util.js'
    export default {
        data () {
            const validatePass = (rule, value, callback) => {
                if (value === '') {
                    this.formInline.showConfirm = true;
                    callback(new Error('Please enter your password'));
                } else {
                    console.log(this.formInline);
                    if (this.formInline.passwdCheck !== '') {
                        // 对第二个密码框单独验证
                        // this.$refs.formInline.validateField('passwdCheck');
                    }
                    callback();
                }
            };
            const validatePassCheck = (rule, value, callback) => {
                if (value === '') {
                    this.formInline.showConfirm = true;
                    callback(new Error('Please enter your password again'));
                } else if (value !== this.formInline.password) {
                    callback(new Error('The two input passwords do not match!'));
                } else {
                    this.formInline.showConfirm = false;
                    callback();
                }
            };
            const validateEmail = (rule, vlaue, callback) => {
                // let isEmail = util.isEmail(value);
                console.log(vlaue);
                callback();
                // if (!isEmail)  {
                //     callback(new Error('Please enter your isEmail again'));
                // }else{
                //     callback();
                // }
            };
            const validateCode = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('Please enter Verification code'));
                } else if (this.formInline.verifyCode.toUpperCase()!= this.checkCode.toUpperCase()) {
                    callback(new Error('The two input passwords do not match!'));
                } else {
                    this.formInline.showConfirm = false;
                    callback();
                }
            };
            return {
                formInline: {
                    showConfirm: true,
                    username: '',
                    email: '',
                    password: '',
                    passwdCheck: '',
                    verifyCode: ''
                },
                checkCode:'',
                ruleInline: {
                    username: [
                        { required: true, message: 'Please fill in the user name'},
                        { type: 'string', min: 4, message: 'The username length cannot be less than 4 bits', trigger: 'blur' }
                    ],
                    email: [
                        { required: true, type: 'string', message: 'Please fill in the user email'},
                    ],
                    password: [
                       { requied: true, type: 'string', min: 6, message: 'The password length cannot be less than 6 bits'},
                       { validator: validatePass, trigger: 'blur' },
                    ],
                    passwdCheck: [
                        { validator: validatePassCheck, trigger: 'blur', min: 6}
                    ],
                    verifyCode: [
                       { validator: validateCode, trigger: 'blur', min: 4}
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
                        util.ajax.post('/api/register', _this.formInline)
                        .then((response) => {
                            console.log(response);
                            var ret = response.data;
                            console.log(ret);
                            switch(ret.status) {
                            case "0" || 0:
                                util.saveData(ret);
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
                                _this.checkCode = util.createCode()
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
                            _this.checkCode = util.createCode()
                            _this.$Message.info('登陆失败');
                        })
                    } else {
                        _this.$Message.error('Fail!');
                    }
                })
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