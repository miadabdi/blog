'use client';

import React, { createContext } from 'react';

// Types mimicking a subset of next-themes props we actually used
export interface LocalThemeProviderProps {
  attribute?: 'class' | 'data-theme';
  defaultTheme?: 'light' | 'dark' | 'system';
  enableSystem?: boolean;
  disableTransitionOnChange?: boolean;
  storageKey?: string;
  children: React.ReactNode;
}

export interface ThemeContextValue {
  theme: string;
  setTheme: (theme: string) => void;
  resolvedTheme: string; // actual applied theme (light/dark)
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);
export default ThemeContext;
