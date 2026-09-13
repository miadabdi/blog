import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeftIcon, ArrowRightIcon, CalendarIcon, ClockIcon } from '@/components/ui/icons';
import { Link } from 'react-router-dom';
import { posts as blogPosts } from '../lib/storage';

export function BlogPage() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16">
        <div className="mb-10">
          <Link
            to="/"
            className="inline-flex items-center text-muted-foreground hover:text-foreground transition-colors mb-6"
          >
            <ArrowLeftIcon className="mr-2 h-4 w-4" />
            Back to Home
          </Link>
          <h1 className="text-4xl sm:text-5xl font-bold text-balance mb-4">Blog Posts</h1>
          <p className="text-lg text-muted-foreground text-balance max-w-3xl leading-normal">
            Deep dives into backend development, DevOps practices, and system architecture
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-2">
          {blogPosts.map((post) => (
            <Card
              key={post.id}
              className={`group hover:shadow-xl transition-all duration-300 overflow-hidden border-0 bg-card/50 backdrop-blur ${
                post.featured ? 'lg:col-span-2' : ''
              }`}
            >
              <div className="relative overflow-hidden">
                <img
                  src={post.image || '/placeholder.svg'}
                  alt={post.title}
                  width={post.featured ? 800 : 500}
                  height={post.featured ? 400 : 300}
                  className="w-full h-56 object-cover group-hover:scale-105 transition-transform duration-500"
                  loading="lazy"
                />
              </div>
              <CardHeader className="p-8">
                <div className="flex items-center justify-between text-sm text-muted-foreground mb-3">
                  <div className="flex items-center space-x-6">
                    <div className="flex items-center space-x-2">
                      <CalendarIcon className="h-4 w-4" />
                      <span>{new Date(post.date).toLocaleDateString()}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <ClockIcon className="h-4 w-4" />
                      <span>{post.readTime}</span>
                    </div>
                  </div>
                </div>
                <CardTitle className="text-2xl group-hover:text-primary transition-colors leading-tight">
                  {post.title}
                </CardTitle>
                <CardDescription className="text-base leading-normal mt-2">
                  {post.description}
                </CardDescription>
              </CardHeader>
              <CardContent className="px-8 pb-6">
                <div className="flex items-center justify-between">
                  <div className="flex flex-wrap gap-2.5">
                    {post.tags.map((tag) => (
                      <Badge key={tag} variant="secondary" className="text-xs px-2.5 py-1">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                  <Link to={`/blog/${post.id}`}>
                    <Button variant="ghost" size="lg" className="group-hover:text-primary">
                      Read More
                      <ArrowRightIcon className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
