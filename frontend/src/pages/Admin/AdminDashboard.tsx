import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  CalendarDaysIcon,
  ClockIcon,
  FileTextIcon,
  FolderOpenIcon,
  TagIcon,
  TrendingUpIcon,
} from '@/components/ui/icons';
import { usePosts, useProjects } from '@/lib/queries';
import { postDate, readTime, tagNames } from '@/lib/types';

export default function AdminDashboard() {
  const { data: posts } = usePosts();
  const { data: projects } = useProjects();

  const recentPosts = (posts ?? []).slice(0, 3);
  const recentProjects = (projects ?? []).slice(0, 3);

  const totalTags = Array.from(new Set((posts ?? []).flatMap((p) => tagNames(p)))).length;
  const featuredProjects = (projects ?? []).filter((p) => p.featured).length;

  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Posts</CardTitle>
            <FileTextIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{posts?.length ?? 0}</div>
            <p className="text-xs text-muted-foreground">newest gets the featured slot</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Projects</CardTitle>
            <FolderOpenIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{projects?.length ?? 0}</div>
            <p className="text-xs text-muted-foreground">{featuredProjects} featured</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Unique Tags</CardTitle>
            <TagIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalTags}</div>
            <p className="text-xs text-muted-foreground">across all posts</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Activity</CardTitle>
            <TrendingUpIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {(posts?.length ?? 0) + (projects?.length ?? 0)}
            </div>
            <p className="text-xs text-muted-foreground">total content items</p>
          </CardContent>
        </Card>
      </div>

      {/* Recent Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileTextIcon className="h-5 w-5" />
              Recent Posts
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentPosts.length > 0 ? (
              recentPosts.map((post, i) => (
                <div key={post.id} className="flex items-start justify-between space-x-4">
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none">{post.title}</p>
                    <p className="text-xs text-muted-foreground line-clamp-2">{post.summary}</p>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <CalendarDaysIcon className="h-3 w-3" />
                      {postDate(post)}
                      <>
                        <ClockIcon className="h-3 w-3 ml-2" />
                        {readTime(post.body)}
                      </>
                    </div>
                    <div className="flex flex-wrap gap-1">
                      {tagNames(post)
                        .slice(0, 3)
                        .map((tag) => (
                          <Badge key={tag} variant="secondary" className="text-xs">
                            {tag}
                          </Badge>
                        ))}
                    </div>
                  </div>
                  {i === 0 && (
                    <Badge variant="default" className="text-xs">
                      Featured
                    </Badge>
                  )}
                </div>
              ))
            ) : (
              <p className="text-sm text-muted-foreground">No posts yet</p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FolderOpenIcon className="h-5 w-5" />
              Recent Projects
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentProjects.length > 0 ? (
              recentProjects.map((project) => (
                <div key={project.id} className="flex items-start justify-between space-x-4">
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none">{project.title}</p>
                    <p className="text-xs text-muted-foreground line-clamp-2">
                      {project.summary}
                    </p>
                    <div className="flex flex-wrap gap-1">
                      {project.tech.slice(0, 4).map((tech) => (
                        <Badge key={tech} variant="outline" className="text-xs">
                          {tech}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  {project.featured && (
                    <Badge variant="default" className="text-xs">
                      Featured
                    </Badge>
                  )}
                </div>
              ))
            ) : (
              <p className="text-sm text-muted-foreground">No projects yet</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
