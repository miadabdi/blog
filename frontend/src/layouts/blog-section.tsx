import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowRightIcon, CalendarIcon, ClockIcon } from '@/components/ui/icons';
import { Link } from 'react-router-dom';
import { posts as blogPosts } from '../lib/storage';

export function BlogSection() {
  return (
    <section id="blog" className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/20">
      <div className="container mx-auto max-w-7xl">
        <div className="text-center mb-10">
          <h2 className="text-4xl sm:text-5xl font-bold text-balance mb-4">Latest Blog Posts</h2>
          <p className="text-lg text-muted-foreground text-balance max-w-3xl mx-auto leading-normal">
            Sharing insights on backend development, DevOps practices, and system architecture
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-2">
          {blogPosts.slice(0, 4).map((post, index) => (
            <Card
              key={index}
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
                  <div className="flex flex-wrap gap-3">
                    {post.tags.map((tag) => (
                      <Badge key={tag} variant="secondary" className="text-xs px-2.5 py-1">
                        {tag}
                      </Badge>
                    ))}
                  </div>
                  <Button variant="ghost" size="lg" className="group-hover:text-primary">
                    Read More
                    <ArrowRightIcon className="ml-2 h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="text-center mt-10">
          <Link to="/blog">
            <Button variant="outline" size="lg" className="text-base px-6 py-4 bg-transparent">
              View All Posts
              <ArrowRightIcon className="ml-3 h-5 w-5" />
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
}
