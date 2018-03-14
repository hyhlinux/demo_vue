<style scoped>
    .index {
        width: 100%;
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        text-align: center;
    }

    .index h1 {
        height: 150px;
    }

    .index h1 img {
        height: 100%;
    }

    .index h2 {
        color: #666;
        margin-bottom: 200px;
    }

    .index h2 p {
        margin: 0 0 50px;
    }

    .index .ivu-row-flex {
        height: 100%;
    }
</style>
<template>
    <div class="index">
        <Row type="flex" justify="center" align="middle">
            <Col span="24">
                <h2>
                    <p>Welcome to Home!</p>
                </h2>
                <Input v-model="value" placeholder="Enter something..." style="width: 300px"></Input>
            </Col>
        </Row>
    </div>
</template>
<script>
    export default {
        data: function() {
            return {
                value: ''
            }
        },
        methods: {
        }
    };
</script>