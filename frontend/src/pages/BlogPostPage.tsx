import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  ArrowLeftIcon,
  CalendarIcon,
  ClockIcon,
  ExternalLinkIcon,
  GithubIcon,
} from '@/components/ui/icons';
import { getPost } from '@/lib/storage';
import { Link, useParams } from 'react-router-dom';

export function BlogPostPage() {
  const { id } = useParams<{ id: string }>();
  const post = id ? getPost(id) : null;

  if (!post) {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-4">Post Not Found</h1>
            <p className="text-muted-foreground mb-8">
              The blog post you're looking for doesn't exist.
            </p>
            <Link to="/blog">
              <Button>
                <ArrowLeftIcon className="mr-2 h-4 w-4" />
                Back to Blog
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-16">
        <Link
          to="/blog"
          className="inline-flex items-center text-muted-foreground hover:text-foreground transition-colors mb-8"
        >
          <ArrowLeftIcon className="mr-2 h-4 w-4" />
          Back to Blog
        </Link>

        <article className="prose prose-lg max-w-none">
          <div className="mb-8">
            <img
              src={post.image}
              alt={post.title}
              className="w-full h-64 object-cover rounded-lg mb-6"
            />

            <div className="flex items-center space-x-4 text-sm text-muted-foreground mb-4">
              <div className="flex items-center space-x-2">
                <CalendarIcon className="h-4 w-4" />
                <span>{new Date(post.date).toLocaleDateString()}</span>
              </div>
              <div className="flex items-center space-x-2">
                <ClockIcon className="h-4 w-4" />
                <span>{post.readTime}</span>
              </div>
            </div>

            <h1 className="text-4xl font-bold mb-4">{post.title}</h1>
            <p className="text-xl text-muted-foreground mb-6">{post.description}</p>

            <div className="flex flex-wrap gap-2 mb-8">
              {post.tags.map((tag) => (
                <Badge key={tag} variant="secondary">
                  {tag}
                </Badge>
              ))}
            </div>
          </div>

          <div
            className="prose prose-lg max-w-none prose-headings:text-foreground prose-p:text-foreground prose-li:text-foreground prose-strong:text-foreground"
            dangerouslySetInnerHTML={{ __html: post.content }}
          />
        </article>

        <div className="mt-12 pt-8 border-t border-border">
          <div className="flex justify-between items-center">
            <Link to="/blog">
              <Button variant="outline">
                <ArrowLeftIcon className="mr-2 h-4 w-4" />
                More Posts
              </Button>
            </Link>
            <div className="flex space-x-3">
              <Button variant="outline" size="sm">
                <GithubIcon className="mr-2 h-4 w-4" />
                View Source
              </Button>
              <Button variant="outline" size="sm">
                <ExternalLinkIcon className="mr-2 h-4 w-4" />
                Share
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
