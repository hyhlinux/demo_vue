import axios from 'axios';
import env from '../config/env';

let util = {

};
util.title = function(title) {
    title = title ? title + ' - Home' : 'iView project';
    window.document.title = title;
};

const ajaxUrl = env === 'development' ?
    'http://127.0.0.1:8000' :
    env === 'production' ?
    'http://127.0.0.1:8000' :
    'http://127.0.0.1:8000';

util.ajax = axios.create({
    baseURL: ajaxUrl,
    timeout: 30000
});
// util.ajax.options.emulateJSON = true;

util.createCode = function() {
    let code = "";    
    var codeLength = 4;//验证码的长度   
    var random = new Array(0,1,2,3,4,5,6,7,8,9,
    'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',   
    'S','T','U','V','W','X','Y','Z');//随机数   
    for(var i = 0; i < codeLength; i++) {//循环操作   
        var index = Math.floor(Math.random()*36);//取得随机数的索引（0~35）   
        code += random[index];//根据索引取得随机数加到code上   
    }   
    return code;//把code值赋给验证码   
};

util.saveData = function(ret) {
    //api ser 返回的状态
    if (ret) {
        localStorage.setItem('token', ret.token);
        localStorage.setItem('expires', ret.expires);
        localStorage.setItem('user_name', ret.user_name);
    }
};
util.isEmail = function(email) {
    let reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/; 
    return reg.test(email); 
};

export default util;