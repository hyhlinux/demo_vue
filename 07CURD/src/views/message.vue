<template>
    <Table :columns="columns1" :data="data1"></Table>
</template>
<script>
    export default {
        data () {
            return {
                columns1: [
                    {
                        title: 'FromUserId',
                        key: 'fromUserId'
                    },
                    {
                        title: 'ToUserId',
                        key: 'toUserId'
                    },
                    {
                        title: 'Status',
                        key: 'status'
                    },
                    {
                        title: 'Title',
                        key: 'title'
                    },
                    {
                        title: 'Date',
                        key: 'date'
                    },
                    {
                        title: 'Text',
                        key: 'text'
                    },
                ],
                data1: [
                    {
                        fromUserId: '000',
                        toUserId: '001',
                        status: 0,
                        title: "欢迎成为开发者",
                        text: "欢迎成为开发， xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                        date: '2016-10-03'
                    },
                ]
            }
        }
    }
</script>