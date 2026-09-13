'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';
import type { LocalThemeProviderProps } from '../stores/ThemeContext';
import ThemeContext from '../stores/ThemeContext';

const prefersDark = () =>
  typeof window !== 'undefined' &&
  window.matchMedia &&
  window.matchMedia('(prefers-color-scheme: dark)').matches;

export function ThemeProvider({
  children,
  attribute = 'class',
  defaultTheme = 'system',
  enableSystem = true,
  disableTransitionOnChange = false,
  storageKey = 'app-theme',
}: LocalThemeProviderProps) {
  const [theme, setThemeState] = useState<string>(() => {
    if (typeof window === 'undefined') return defaultTheme;
    const stored = window.localStorage.getItem(storageKey);
    return stored || defaultTheme;
  });

  const getResolved = useCallback((t: string) => {
    if (t === 'system') {
      return prefersDark() ? 'dark' : 'light';
    }
    return t;
  }, []);

  const resolvedTheme = getResolved(theme);

  const applyTheme = useCallback(
    (t: string) => {
      const root = window.document.documentElement;
      const applied = getResolved(t);

      // Manage transitions if requested
      if (disableTransitionOnChange) {
        const css = document.createElement('style');
        css.appendChild(
          document.createTextNode(
            `*{transition:none!important}*::before{transition:none!important}*::after{transition:none!important}`,
          ),
        );
        document.head.appendChild(css);
        requestAnimationFrame(() => {
          if (css.parentNode) css.parentNode.removeChild(css);
        });
      }

      if (attribute === 'class') {
        root.classList.remove('light', 'dark');
        root.classList.add(applied);
      } else if (attribute === 'data-theme') {
        root.setAttribute('data-theme', applied);
      }
    },
    [attribute, disableTransitionOnChange, getResolved],
  );

  // Initial & theme changes
  useEffect(() => {
    applyTheme(theme);
    window.localStorage.setItem(storageKey, theme);
  }, [theme, applyTheme, storageKey]);

  // Listen for system changes if system theme enabled
  useEffect(() => {
    if (!enableSystem) return;
    if (theme !== 'system') return;
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = () => applyTheme('system');
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, [enableSystem, theme, applyTheme]);

  const setTheme = useCallback((t: string) => setThemeState(t), []);

  const value = useMemo(
    () => ({ theme, setTheme, resolvedTheme }),
    [theme, resolvedTheme, setTheme],
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}
