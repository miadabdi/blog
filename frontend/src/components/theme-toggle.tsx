'use client';

import { Button } from '@/components/ui/button';
import { MoonIcon, SunIcon } from '@/components/ui/icons';
import useTheme from '../hooks/use-theme';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="sm"
      onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
    >
      <SunIcon
        className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
        aria-hidden
      />
      <MoonIcon
        className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
        aria-hidden
      />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
