<template>
    <Table border :columns="columns7" :data="data"></Table>
</template>
<script>
import util from '../libs/util.js'
    export default {
        data () {
            return {
                columns7: [
                    {
                        title: 'FromUserId',
                        key: 'fromUserId',
                        render: (h, params) => {
                            return h('div', [
                                h('Icon', {
                                    props: {
                                        type: 'person'
                                    }
                                }),
                                h('strong', params.row.fromUserId)
                            ]);
                        }
                    },
                    {
                        title: 'ToUserId',
                        key: 'toUserId',
                        render: (h, params) => {
                            return h('div', [
                                h('Icon', {
                                    props: {
                                        type: 'person'
                                    }
                                }),
                                h('strong', params.row.fromUserId)
                            ]);
                        }
                    },
                    {
                        title: 'Status',
                        key: 'status',
                        render: (h, params) => {
                            return h('div', [
                                h('Icon', {
                                    props: {
                                        type: 'message'
                                    }
                                }),
                                h('strong', params.row.status>0? "已读":"未读")
                            ]);
                        }
                    },
                    {
                        title: 'Date',
                        key: 'date',
                        sortable: true,
                    },
                    // {
                    //     title: 'Title',
                    //     key: 'title'
                    // },
                    // {
                    //     title: 'Text',
                    //     key: 'text'
                    // },
                    {
                        title: 'Action',
                        key: 'action',
                        width: 150,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.show(params.index)
                                        }
                                    }
                                }, 'View'),
                                h('Button', {
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.remove(params.index)
                                        }
                                    }
                                }, 'Delete')
                            ]);
                        }
                    }
                ],
                queryData: {

                },
                data: [
                    {
                        id: 1,
                        fromUserId: '000',
                        toUserId: '001',
                        status: 0,
                        title: "欢迎成为开发者",
                        text: "欢迎成为开发， xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                        date: '2016-10-04 10:23:21'
                    },
                     {
                        id: 2,
                        fromUserId: '000',
                        toUserId: '002',
                        status: 0,
                        title: "欢迎成为开发者",
                        text: "欢迎成为开发， xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                        date: '2016-10-03 10:22:23'
                    },
                ]
            }
        },
        methods: {
            getMessages() {
                console.log("API GET Message list");
                let _this = this;
                util.ajax.post('/api/message', _this.queryData)
                .then((response) => {
                    console.log(response);
                    _this.data = response.data;
                })
                .catch(function(response) {
                    console.log("获取消息失败");
                    console.log(response);
                }) 
            },
            show (index) {
                let status = this.data[index].status;
                console.log('API GET', status);
                this.$Modal.info({
                    title: 'Message Info',
                    content: `<li>FromUserId:&nbsp;&nbsp;${this.data[index].fromUserId}</li><br><li>ToUserId:&nbsp;&nbsp;${this.data[index].toUserId}</li><br><p>Text:&nbsp;&nbsp;${this.data[index].text}</p>`
                })
                this.data[index].status = 1;  
                console.log('API mesage Update: ', this.data[index].status, 'Id:', this.data[index].id);
            },
            remove (index) {
                console.log('API REMOVE: fake delete');
                this.data.splice(index, 1);
            }
        },
        created: function() {
            console.log('Create');
            this.getMessages();
        },
    }
</script>