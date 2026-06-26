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

        <!-- Bottom Sheet Drawer -->
        <transition name="slide-up">
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
/* ===== Apple Design System Tokens ===== */
:root {
    --font: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', 'Helvetica Neue', sans-serif;
    --bg-primary: #ffffff;
    --bg-secondary: #f5f5f7;
    --text-primary: #1d1d1f;
    --text-secondary: #86868b;
    --accent: #0071e3;
    --accent-pressed: #0060c9;
    --separator: rgba(60, 60, 67, 0.08);
    --safe-bottom: env(safe-area-inset-bottom, 0px);
}

.mobile-shell {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    background: var(--bg-secondary);
    font-family: var(--font);
    -webkit-font-smoothing: antialiased;
}

/* ===== Header ===== */
.mobile-header {
    height: 52px;
    flex: 0 0 52px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 8px;
    padding-top: 8px;
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 0.5px solid var(--separator);
    z-index: 100;
}

.header-back,
.header-menu {
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: var(--accent);
    cursor: pointer;
    border-radius: 12px;
    transition: background 0.15s ease;
    -webkit-tap-highlight-color: transparent;
}

.header-back:active,
.header-menu:active {
    background: rgba(0, 113, 227, 0.1);
}

.header-title {
    font-size: 17px;
    font-weight: 600;
    color: var(--text-primary);
    flex: 1;
    text-align: center;
    letter-spacing: -0.02em;
}

/* ===== Content ===== */
.mobile-content {
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    -webkit-overflow-scrolling: touch;
    padding-bottom: calc(50px + var(--safe-bottom));
}

/* ===== Bottom Tab Bar ===== */
.mobile-bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: calc(50px + var(--safe-bottom));
    display: flex;
    align-items: flex-start;
    padding-top: 4px;
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-top: 0.5px solid var(--separator);
    z-index: 100;
    padding-bottom: var(--safe-bottom);
}

.nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 46px;
    font-size: 10px;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    -webkit-tap-highlight-color: transparent;
    transition: color 0.15s ease;
    letter-spacing: 0.01em;
}

.nav-item i {
    font-size: 22px;
    margin-bottom: 1px;
    transition: transform 0.2s cubic-bezier(0.25, 0.1, 0.25, 1);
}

.nav-item:active i {
    transform: scale(0.9);
}

.nav-item.active {
    color: var(--accent);
}

/* ===== Bottom Sheet Drawer ===== */
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
    background: rgba(0, 0, 0, 0.3);
}

.drawer-panel {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    background: #fff;
    border-radius: 20px 20px 0 0;
    padding: 16px 0 calc(20px + var(--safe-bottom));
    box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.08);
}

/* Pull indicator */
.drawer-panel::before {
    content: '';
    display: block;
    width: 36px;
    height: 5px;
    background: rgba(60, 60, 67, 0.15);
    border-radius: 3px;
    margin: 0 auto 16px;
}

.drawer-user {
    display: flex;
    align-items: center;
    padding: 12px 24px 16px;
    font-size: 17px;
    font-weight: 600;
    color: var(--text-primary);
}

.drawer-user i {
    font-size: 32px;
    margin-right: 14px;
    color: var(--text-secondary);
}

.drawer-divider {
    height: 0.5px;
    background: var(--separator);
    margin: 0 24px 8px;
}

.drawer-item {
    display: flex;
    align-items: center;
    padding: 14px 24px;
    font-size: 16px;
    font-weight: 400;
    color: var(--text-primary);
    cursor: pointer;
    border-radius: 12px;
    margin: 0 8px;
    -webkit-tap-highlight-color: transparent;
    transition: background 0.15s ease;
}

.drawer-item i {
    width: 24px;
    margin-right: 14px;
    font-size: 18px;
    color: var(--accent);
    text-align: center;
}

.drawer-item:active {
    background: var(--bg-secondary);
}

/* ===== Drawer Animations ===== */
.slide-up-enter-active,
.slide-up-leave-active {
    transition: opacity 0.25s ease;
}
.slide-up-enter-active .drawer-panel,
.slide-up-leave-active .drawer-panel {
    transition: transform 0.3s cubic-bezier(0.25, 0.1, 0.25, 1);
}
.slide-up-enter,
.slide-up-leave-to {
    opacity: 0;
}
.slide-up-enter .drawer-panel,
.slide-up-leave-to .drawer-panel {
    transform: translateY(100%);
}
</style>
