#### src
```bash
http://www.cnblogs.com/keepfool/p/5625583.html
```
#### 01 第一个组件
#### 02 组件必须挂载到实例
#### 03 组件全局注册/局部注册
#### 04 父子组件
#### 05 组件注册语法糖
####
#### 06 js和html分离
```js
<script type="text/x-template" id="myComponent">
		<div>This is my first component</div>
</script>
```
#### 06-2 使用template定义
```html
不需要type指定.
<template id="myComponent">
		<div>This is my first component</div>
</template>
```
#### 07 组件的el和data选项
```bash
Vue.js规定：在定义组件的选项时，data和el选项必须使用函数。
错误demo:
Vue.component('my-component', {
    data: {
        a: 1
    }
})
处理方法:
Vue.component('my-component', {
    data: function(){
        return {a : 1}
    }
})
```
#### 08 使用props
```bash
组件实例的作用域是孤立的。
这意味着不能并且不应该在子组件的模板内直接引用父组件的数据。
可以使用props把数据传给子组件
```
```html
<div id="app">
    <my-component v-bind:my-name="name" v-bind:my-age="age"></my-component>
</div>
```
```js
var vm = new Vue({
    el: '#app',
    data: {
        name: 'keepfool',
        age: 28
    },
    components: {
        'my-component': {
            template: '#myComponent',
            props: ['myName', 'myAge']
        }
    }
})
```
```bash
注意：在子组件中定义prop时，使用了camelCase命名法。由于HTML特性不区分大小写，
camelCase的prop用于特性时，需要转为 kebab-case（短横线隔开）。
例如，在prop中定义的myName，在用作特性时需要转换为my-name。
<child-component v-bind:子组件prop="父组件数据属性"></child-component>
```

#### 09 组件注册语法糖
#### 05 组件注册语法糖
#### 05 组件注册语法糖
