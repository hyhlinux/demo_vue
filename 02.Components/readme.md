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

#### 09 props 单向绑定
```bash
vue1.x
修改了父组件的数据，同时影响了子组件。
prop默认是单向绑定：当父组件的属性变化时，将传导给子组件，但是反过来不会。
这是为了防止子组件无意修改了父组件的状态
```

#### 09-2/3 props 双向绑定
```bash
vue1.x .sync
vue2.x v-bind:传递是引用时，修改是同一个对象
```
#### 09-4/5 props 单词绑定
```bash
<my-component v-bind:my-name.once="name" v-bind:my-age.once="age"></my-component>
```
组件中使用name, age 来自组件注册时的data
```html
<template id="myComponent">
        <table>
			<tr>
				<th colspan="3">子组件数据</th>
			</tr>
            <tr>
				<td>myname</td>
				<td>{{ name }}</td>
                <td><input type="text" v-model="name"></td>
			</tr>
			<tr>
				<td>myage</td>
                <td>{{ age }}</td>
				<td><input type="text" v-model="age"></td>
			</tr>
		</table>
</template>
```

组件data中的数据来源于props['cpeople'], data 只初始化一次，整个组件生命周期.
```js
<script>
	var vm = new Vue({
		el: '#app',
		data: {
		    people: {
                name: 'hello',
                age: 28,
			},
		},
		components: {
			'my-component': {
				template: '#myComponent',
				props: ['cpeople'],
				data: function () {
					return {
					    name: this.cpeople.name,
                        age: this.cpeople.age,
					}
                }
			}
		},
	});
</script>
```
#### 20 编译作用域
```bash
在子组件中定义的数据，只能用在子组件的模板。在父组件中定义的数据，只能用在父组件的模板。
如果父组件的数据要在子组件中使用，则需要子组件定义props。
```
#### 21/2 单个slot
```bash
为了让组件可以组合，我们需要一种方式来混合父组件的内容与子组件自己的模板。
这个处理称为内容分发，Vue.js 实现了一个内容分发 API，
使用特殊的 <slot> 元素作为原始内容的插槽
```
```html
<div id="app">
    <my-component>
        <h1>Hello Vue.js!</h1>
    </my-component>

    <my-component>
    </my-component>
</div>
<template id="myComponent">
    <div class="content">
        <h2>This is a component!</h2>
        <slot>如果没有分发内容，则显示slot中的内容</slot>
        <p>Say something...</p>
    </div>
</template>
<script src="js/vue.js"></script>
<script>
    Vue.component('my-component', {
        template: '#myComponent'
    })

    new Vue({
        el: '#app'
    })
</script>
```
#### 22 指定名称的slot
```html

```
#### 23/4 提示框组件
#### 25 父子组件之间的访问
. 父组件访问子组件：使用$children或$refs
. 子组件访问父组件：使用$parent
. 子组件访问根组件：使用$root

#### 26 父子组件之间的访问: $refs
#### 27 父子组件之间的访问: $parent
#### 28 父子组件之间的访问: $dispatch 派发事件
1. 子组件的button元素绑定了click事件，该事件指向notify方法
2. 子组件的notify方法在处理时，调用了$dispatch，将事件派发到父组件的child-msg事件，并给该该事件提供了一个msg参数
3. 父组件的events选项中定义了child-msg事件，父组件接收到子组件的派发后，调用child-msg事件
#### 29 父子组件之间的访问: 广播事件

#### 30 CURD实例.
Vue.js组件的API来源于三部分——prop，slot和事件。
. prop 允许外部环境传递数据给组件；
. 事件 允许组件触发外部环境的 action；
. slot 允许外部环境插入内容到组件的视图结构内。
```bash

```
