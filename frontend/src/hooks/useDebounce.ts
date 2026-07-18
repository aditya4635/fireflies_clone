import { useEffect, useRef, useState } from 'react';

/**
 * Debounce a value by a given delay in milliseconds.
 * Used to avoid firing API calls on every keystroke.
 */
export function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}
