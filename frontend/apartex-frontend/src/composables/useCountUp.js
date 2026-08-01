import { ref, onMounted } from 'vue';

export function useCountUp(target, duration = 1500, delay = 0) {
  const current = ref(0);
  const isComplete = ref(false);

  onMounted(() => {
    setTimeout(() => {
      const start = performance.now();
      const targetNum = typeof target === 'function' ? target() : target;

      function step(timestamp) {
        const elapsed = timestamp - start;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const eased = 1 - Math.pow(1 - progress, 3);
        current.value = Math.round(eased * targetNum);

        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          current.value = targetNum;
          isComplete.value = true;
        }
      }

      requestAnimationFrame(step);
    }, delay);
  });

  return { current, isComplete };
}
