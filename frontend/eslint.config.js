import js from '@eslint/js';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import { globalIgnores } from 'eslint/config';
import globals from 'globals';
import tseslint from 'typescript-eslint';

export default tseslint.config([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    ignores: ['**/*.config.*', 'vite.config.*'],
    extends: [
      // use type-checked rules for stronger linting
      ...tseslint.configs.recommendedTypeChecked,
      // keep other useful configs
      js.configs.recommended,
      reactHooks.configs['recommended-latest'],
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        project: ['./tsconfig.eslint.json'],
        tsconfigRootDir: import.meta?.dirname ?? undefined,
      },
    },
    rules: {
      // explicitly disable unused-vars for TS
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
      '@typescript-eslint/no-unsafe-assignment': 'off',
    },
  },
  // Also disable for JS/JSX files (in case any exist now or later)
  {
    files: ['**/*.{js,jsx}'],
    extends: [js.configs.recommended],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
    rules: {
      'no-unused-vars': 'off',
    },
  },
  // Lint config files without type-aware parsing
  {
    files: ['**/*.config.*', 'vite.config.*'],
    extends: [
      // non-type-checked ruleset
      ...tseslint.configs.recommended,
      js.configs.recommended,
    ],
    languageOptions: {
      ecmaVersion: 2020,
      globals: { ...globals.node, ...globals.browser },
      parserOptions: {
        // disable type-aware for these files to avoid project lookup
        project: false,
      },
    },
    rules: {
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': 'off',
      '@typescript-eslint/no-unsafe-assignment': 'off',
    },
  },
]);
