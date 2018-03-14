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
                    <p>Welcome to {{ $route.params.id }} !</p>
                    <p>Welcome to {{ $route.params }} !</p>
                </h2>
                <br>
                <router-link to="/">/</router-link>
                <br>
                <router-link to="/user/foo">/user/foo</router-link>
                <br>
                <router-link to="/user/foo/profile">/user/foo/profile</router-link>
                <br>
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
        watch: {
            '$route' (to, from) {
                console.log(to, from);
            }
        },
        methods: {

        }
    };
</script>