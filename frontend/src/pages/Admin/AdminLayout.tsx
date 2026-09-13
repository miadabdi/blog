import { Button } from '@/components/ui/button';
import { Link, Outlet, useLocation } from 'react-router-dom';

export default function AdminLayout() {
  const { pathname } = useLocation();
  const tabs = [
    { name: 'Dashboard', href: '/admin' },
    { name: 'Posts', href: '/admin/posts' },
    { name: 'Projects', href: '/admin/projects' },
  ];

  return (
    <div className="container mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Admin</h1>
        <Link to="/">
          <Button variant="outline">Back to site</Button>
        </Link>
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
