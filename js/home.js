var menus = [{
            href: 'picture.html',
            name: '相册',
            value: '1'
        },
        {
            href: 'news.html',
            name: '看点',
            value: '2'
        },
        {
            href: 'y2b.html',
            name: 'y2b',
            value: '3'
        },
        {
            href: 'gp.html',
            name: '股票',
            value: '4'
        },
        {
            href: 'python.html',
            name: '技术博客',
            value: '5'
        },
        {
            href: 'zl.html',
            name: '技术资料',
            value: '6'
        }
];
var myApp = new Vue({
        el: '#myApp',
        data: {
            logoMsg: 'Home',
            menus: menus,
            mSelected: menus[1].value,
        },
});
