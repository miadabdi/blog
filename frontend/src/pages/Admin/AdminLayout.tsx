import { Button } from '@/components/ui/button';
import { clearToken } from '@/lib/api';
import { useQueryClient } from '@tanstack/react-query';
import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom';

export default function AdminLayout() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const tabs = [
    { name: 'Dashboard', href: '/admin' },
    { name: 'Posts', href: '/admin/posts' },
    { name: 'Projects', href: '/admin/projects' },
  ];

  function logout() {
    clearToken();
    queryClient.clear();
    void navigate('/login');
  }

  return (
    <div className="container mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Admin</h1>
        <div className="flex gap-3">
          <Link to="/">
            <Button variant="outline">Back to site</Button>
          </Link>
          <Button variant="destructive" onClick={logout}>
            Logout
          </Button>
        </div>
      </div>
      <div className="flex gap-3 mb-8">
        {tabs.map((t) => (
          <Link key={t.href} to={t.href}>
            <Button variant={pathname === t.href ? 'default' : 'outline'}>{t.name}</Button>
          </Link>
        ))}
      </div>
      <Outlet />
    </div>
  );
}
