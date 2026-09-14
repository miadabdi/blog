import { useMe } from '@/lib/queries';
import { getToken } from '@/lib/api';
import type { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';

export function RequireAuth({ children }: { children: ReactNode }) {
  const { data, isLoading } = useMe();

  if (!getToken()) return <Navigate to="/login" replace />;
  if (isLoading) return null;
  if (!data) return <Navigate to="/login" replace />;
  return children;
}
