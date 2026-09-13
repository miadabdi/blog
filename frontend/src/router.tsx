import RouteError from '@/components/route-error';
import RootLayout from '@/layouts/root-layout';
import Home from '@/pages/Home';
import { createBrowserRouter } from 'react-router-dom';
import AdminDashboard from './pages/Admin/AdminDashboard';
import AdminLayout from './pages/Admin/AdminLayout';
import PostsAdmin from './pages/Admin/PostsAdmin';
import ProjectsAdmin from './pages/Admin/ProjectsAdmin';
import { BlogPage } from './pages/BlogPage';
import { BlogPostPage } from './pages/BlogPostPage';
import { ProjectDetailPage } from './pages/ProjectDetailPage';
import { ProjectsPage } from './pages/ProjectsPage';

const router = createBrowserRouter([
  {
    element: <RootLayout />,
    errorElement: <RouteError />,
    children: [
      { index: true, element: <Home /> },
      {
        element: <BlogPage />,
        path: 'blog',
      },
      {
        path: 'blog/:id',
        element: <BlogPostPage />,
      },
      {
        element: <ProjectsPage />,
        path: 'projects',
      },
      {
        path: 'projects/:id',
        element: <ProjectDetailPage />,
      },
      {
        path: 'admin',
        element: <AdminLayout />,
        children: [
          {
            index: true,
            element: <AdminDashboard />,
          },
          {
            path: 'posts',
            element: <PostsAdmin />,
          },
          {
            path: 'projects',
            element: <ProjectsAdmin />,
          },
        ],
      },
    ],
  },
]);

export default router;
