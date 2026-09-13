import { isRouteErrorResponse, useRouteError } from 'react-router-dom';

export default function RouteError() {
  const error = useRouteError();
  if (isRouteErrorResponse(error)) {
    return (
      <div style={{ padding: 16 }}>
        <h2>
          {error.status} – {error.statusText}
        </h2>
        {error.data && <pre style={{ whiteSpace: 'pre-wrap' }}>{String(error.data)}</pre>}
      </div>
    );
  }
  return (
    <div style={{ padding: 16 }}>
      <h2>Something went wrong loading this page.</h2>
      <pre style={{ whiteSpace: 'pre-wrap' }}>{String((error as Error)?.message ?? error)}</pre>
    </div>
  );
}
