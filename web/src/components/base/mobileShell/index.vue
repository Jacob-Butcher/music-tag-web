<template>
    <div class="mobile-shell">
        <!-- Header -->
        <div class="mobile-header">
            <span class="header-back" v-if="$route.meta.hasOwnProperty('back')" @click="goBack">
                <i class="fa fa-chevron-left"></i>
            </span>
            <span class="header-title">{{ pageTitle }}</span>
            <span class="header-menu" @click="drawerOpen = true">
                <i class="fa fa-bars"></i>
            </span>
        </div>

        <!-- Content -->
        <div class="mobile-content">
            <router-view></router-view>
        </div>

        <!-- Bottom Tab Bar -->
        <div class="mobile-bottom-nav">
            <div class="nav-item" :class="{ active: $route.name === 'home' }" @click="goHome">
                <i class="fa fa-home"></i>
                <span>首页</span>
            </div>
            <div class="nav-item" v-if="userRole === 'admin'" :class="{ active: $route.name === 'user' }" @click="goUser">
                <i class="fa fa-users"></i>
                <span>用户</span>
            </div>
        </div>

        <!-- Right Drawer -->
        <transition name="slide-right">
            <div class="mobile-drawer" v-if="drawerOpen">
                <div class="drawer-backdrop" @click="drawerOpen = false"></div>
                <div class="drawer-panel">
                    <div class="drawer-user">
                        <i class="fa fa-user-circle-o"></i>
                        <span>{{ userData.username || '用户' }}</span>
                    </div>
                    <div class="drawer-divider"></div>
                    <div class="drawer-item" @click="goAdmin">
                        <i class="fa fa-cog"></i>
                        <span>后台管理</span>
                    </div>
                    <div class="drawer-item" @click="goManual">
                        <i class="fa fa-book"></i>
                        <span>使用手册</span>
                    </div>
                    <div class="drawer-item" @click="goAbout">
                        <i class="fa fa-heart"></i>
                        <span>关于作者</span>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { clearStore } from '../../../common/store.js'

export default {
    data() {
        return {
            drawerOpen: false,
            userData: {},
            pageTitle: '音乐标签Web版',
        }
    },
    computed: {
        ...mapGetters(['getUserRole']),
        userRole() {
            return this.$store.state.userRole
        },
    },
    created() {
        this.loginUser()
    },
    watch: {
        $route(val) {
            this.pageTitle = val.meta.title || '音乐标签Web版'
        },
    },
    methods: {
        loginUser() {
            this.$api.Task.loginInfo().then((res) => {
                if (res.result) {
                    this.userData = res.data
                    this.$store.commit('setUserRole', res.data.role)
                } else {
                    this.$router.push({ name: 'login' })
                }
            })
        },
        goHome() {
            this.$router.push({ path: '/' })
        },
        goUser() {
            this.$router.push({ path: '/user' })
        },
        goBack() {
            this.$router.go(-1)
        },
        goAdmin() {
            this.drawerOpen = false
            const btn = document.createElement('a')
            btn.setAttribute('href', '/admin/')
            document.body.appendChild(btn)
            btn.click()
        },
        goManual() {
            this.drawerOpen = false
            const btn = document.createElement('a')
            btn.setAttribute('href', 'https://xiers-organization.gitbook.io/music-tag-web/')
            document.body.appendChild(btn)
            btn.click()
        },
        goAbout() {
            this.drawerOpen = false
            const btn = document.createElement('a')
            btn.setAttribute('href', 'https://github.com/xhongc/music-tag-web')
            document.body.appendChild(btn)
            btn.click()
        },
    },
}
</script>

<style scoped>
.mobile-shell {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    background: #f5f5f5;
}

/* Header */
.mobile-header {
    height: 44px;
    flex: 0 0 44px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 12px;
    background: #fff;
    border-bottom: 1px solid #dcdee5;
    z-index: 100;
}

.header-back {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    color: #3A84FF;
    cursor: pointer;
}

.header-title {
    font-size: 16px;
    font-weight: 500;
    color: #313238;
    flex: 1;
    text-align: center;
}

.header-menu {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: #63656E;
    cursor: pointer;
}

/* Content */
.mobile-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 50px;
}

/* Bottom Nav */
.mobile-bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 50px;
    flex: 0 0 50px;
    display: flex;
    align-items: center;
    background: #fff;
    border-top: 1px solid #dcdee5;
    z-index: 100;
    padding-bottom: env(safe-area-inset-bottom, 0);
}

.nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    font-size: 12px;
    color: #979BA5;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
}

.nav-item i {
    font-size: 20px;
    margin-bottom: 2px;
}

.nav-item.active {
    color: #3A84FF;
}

.nav-item:active {
    color: #3A84FF;
}

/* Drawer */
.mobile-drawer {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 200;
}

.drawer-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.4);
}

.drawer-panel {
    position: absolute;
    top: 0;
    right: 0;
    width: 280px;
    height: 100%;
    background: #fff;
    box-shadow: -2px 0 8px rgba(0, 0, 0, 0.15);
    padding: 20px 0;
}

.drawer-user {
    display: flex;
    align-items: center;
    padding: 16px 20px;
    font-size: 16px;
    color: #313238;
}

.drawer-user i {
    font-size: 28px;
    margin-right: 12px;
    color: #3A84FF;
}

.drawer-divider {
    height: 1px;
    background: #f0f1f5;
    margin: 8px 16px;
}

.drawer-item {
    display: flex;
    align-items: center;
    padding: 14px 20px;
    font-size: 14px;
    color: #63656E;
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
}

.drawer-item i {
    width: 20px;
    margin-right: 12px;
    font-size: 16px;
    color: #979BA5;
}

.drawer-item:active {
    background: #F0F1F5;
    color: #3A84FF;
}

/* Drawer transition */
.slide-right-enter-active,
.slide-right-leave-active {
    transition: opacity 0.2s;
}
.slide-right-enter-active .drawer-panel,
.slide-right-leave-active .drawer-panel {
    transition: transform 0.2s;
}
.slide-right-enter,
.slide-right-leave-to {
    opacity: 0;
}
.slide-right-enter .drawer-panel,
.slide-right-leave-to .drawer-panel {
    transform: translateX(100%);
}

/* Safe area */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
    .mobile-bottom-nav {
        padding-bottom: env(safe-area-inset-bottom);
    }
}
</style>
