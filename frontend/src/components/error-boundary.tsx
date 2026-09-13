import React from 'react';
import shallowArrayEqual from '../utils/shallow-array-equal';

type RuntimeEnv = { DEV?: boolean; MODE?: string };
type ImportMeta = { env?: RuntimeEnv };
const env: RuntimeEnv =
  (typeof import.meta !== 'undefined' && (import.meta as ImportMeta).env) || {};

type ErrorBoundaryState = {
  hasError: boolean;
  error: unknown;
};

export type FallbackRenderArgs = {
  error: unknown;
  reset: () => void;
};

export type ErrorBoundaryProps = {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  fallbackRender?: (args: FallbackRenderArgs) => React.ReactNode;
  onError?: (error: unknown, info: React.ErrorInfo) => void;
  onReset?: () => void;
  /**
   * When this value changes, the boundary will automatically reset.
   * Useful to reset on route changes.
   */
  resetKey?: unknown;
  /**
   * Like resetKey but accepts multiple keys. If any value changes (shallow compare),
   * the boundary will reset.
   */
  resetKeys?: unknown[];
};

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false, error: null };

  static getDerivedStateFromError(error: unknown): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: unknown, info: React.ErrorInfo) {
    // Basic logging; integrate with your observability tool here.
    if (env.MODE !== 'test') {
      console.error('ErrorBoundary caught an error', error, info);
    }
    this.props.onError?.(error, info);
  }

  componentDidUpdate(prevProps: Readonly<ErrorBoundaryProps>) {
    // Reset when resetKey or any resetKeys change
    if (this.state.hasError) {
      const singleChanged = prevProps.resetKey !== this.props.resetKey;
      const arrayChanged = !shallowArrayEqual(prevProps.resetKeys, this.props.resetKeys);
      if (singleChanged || arrayChanged) {
        this.reset();
      }
    }
  }

  reset = () => {
    this.setState({ hasError: false, error: null });
    this.props.onReset?.();
  };

  render() {
    const { hasError, error } = this.state;
    const { children, fallback, fallbackRender } = this.props;

    if (!hasError) return children;

    if (fallbackRender) return fallbackRender({ error, reset: this.reset });
    if (fallback) return fallback;

    // Minimal default fallback to avoid blank screen
    const isDev = !!env.DEV;
    const err = error;
    const message = err instanceof Error ? err.message : String(err);
    const stack = err instanceof Error ? err.stack : undefined;

    return (
      <div
        role="alert"
        aria-live="assertive"
        style={{ padding: 16, fontFamily: 'system-ui, sans-serif' }}
      >
        <h2>Something went wrong.</h2>
        <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{message}</pre>
        {isDev && stack ? (
          <details style={{ marginTop: 8 }}>
            <summary>Stack trace</summary>
            <pre style={{ whiteSpace: 'pre-wrap' }}>{stack}</pre>
          </details>
        ) : null}
        <button onClick={this.reset} style={{ marginTop: 8 }}>
          Try again
        </button>
      </div>
    );
  }
}

export default ErrorBoundary;
