const RESPONSIVE_BREAKPOINT = 768

export default {
    data() {
        return {
            isMobile: window.innerWidth < RESPONSIVE_BREAKPOINT,
            windowWidth: window.innerWidth
        }
    },
    mounted() {
        window.addEventListener('resize', this._handleResize)
    },
    beforeDestroy() {
        window.removeEventListener('resize', this._handleResize)
    },
    methods: {
        _handleResize() {
            const w = window.innerWidth
            this.windowWidth = w
            this.isMobile = w < RESPONSIVE_BREAKPOINT
        }
    }
}
