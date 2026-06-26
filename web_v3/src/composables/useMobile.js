import { ref, onMounted, onBeforeUnmount } from 'vue'

export function useMobile(breakpoint = 768) {
  const isMobile = ref(window.innerWidth < breakpoint)

  function handleResize() {
    isMobile.value = window.innerWidth < breakpoint
  }

  onMounted(() => window.addEventListener('resize', handleResize))
  onBeforeUnmount(() => window.removeEventListener('resize', handleResize))

  return { isMobile }
}
