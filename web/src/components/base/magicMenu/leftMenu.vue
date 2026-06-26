<template>
    <bk-navigation-menu ref="menu" :default-active="nav.id" :before-nav-change="beforeNavChange"
        :toggle-active="nav.toggle">
        <bk-navigation-menu-item v-for="item in permNavList" :key="item.name"
            :has-child="item.children && !!item.children.length"
            :group="item.group" :icon="item.icon" :disabled="item.disabled" :url="item.to"
            :id="item.name" @click="handleRouterJump(item, false)">
            <span>{{ item.cnName }}</span>
            <div slot="child">
                <bk-navigation-menu-item :key="child.name" v-for="child in item.children" :id="child.name"
                    :disabled="child.disabled"
                    :icon="child.icon" :default-active="child.active"
                    @click="handleRouterJump(child, true)">
                    <span>{{ child.cnName }}</span>
                </bk-navigation-menu-item>
            </div>
        </bk-navigation-menu-item>
    </bk-navigation-menu>
</template>

<script>
    import {mapGetters} from 'vuex'

    export default {
        data() {
            return {
                nav: {
                    id: '',
                    toggle: false
                }
            }
        },
        watch: {
            $route(val) {
                this.nav.id = val.meta.hasOwnProperty('fatherName') ? val.meta.fatherName : val.name
            }
        },
        methods: {
            beforeNavChange(newId, oldId) {
                return true
            },
            handleRouterJump(item) {
                this.$router.push({
                    path: `${item.to}`
                })
            }
        },
        computed: {
            ...mapGetters(['getUserRole']),
            permNavList() {
                const items = [
                    {
                        'name': 'home',
                        'cnName': '首页',
                        'to': '/',
                        'icon': 'fa fa-home',
                        'hasChild': false,
                        'children': []
                    }
                ]
                if (this.getUserRole === 'admin') {
                    items.push({
                        'name': 'user',
                        'cnName': '用户管理',
                        'to': '/user',
                        'icon': 'fa fa-home',
                        'hasChild': false,
                        'children': []
                    })
                }
                return items
            }
        }
    }
</script>

<style>
/* 以下样式是为了适应例子父级的宽高而设置 */
.bk-navigation {
    /* width: 100vw; */
    width: 100% !important;
    /* width: 100vw; */
    height: 100vh;
    outline: 1px solid #ebebeb;
}

.bk-navigation .bk-navigation-wrapper {
    height: 100%;
    /* height: calc(100vh - 252px) !important; */
    width: 100%;
}

.monitor-navigation-nav {
    width: 150px;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    -ms-flex-direction: column;
    flex-direction: column;
    background: #FFFFFF;
    border: 1px solid #E2E2E2;
    -webkit-box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
    box-shadow: 0px 3px 4px 0px rgba(64, 112, 203, 0.06);
    padding: 6px 0;
    margin: 0;
    color: #63656E;
}

.monitor-navigation-nav .nav-item {
    -webkit-box-flex: 0;
    -ms-flex: 0 0 32px;
    flex: 0 0 32px;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    padding: 0 20px;
    list-style: none
}

.monitor-navigation-nav .nav-item:hover {
    color: #3A84FF;
    cursor: pointer;
    background-color: #F0F1F5;
}
</style>
