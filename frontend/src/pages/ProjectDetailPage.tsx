import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ArrowLeftIcon, ExternalLinkIcon, GithubIcon } from '@/components/ui/icons';
import { getProject } from '@/lib/storage';
import { Link, useParams } from 'react-router-dom';

export function ProjectDetailPage() {
  const { id } = useParams<{ id: string }>();
  console.log('id', id);
  const project = id ? getProject(id) : null;
  console.log('project', project);

  if (!project) {
    return (
      <div className="min-h-screen bg-background">
        <div className="container mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-4">Project Not Found</h1>
            <p className="text-muted-foreground mb-8">
              The project you're looking for doesn't exist.
            </p>
            <Link to="/projects">
              <Button>
                <ArrowLeftIcon className="mr-2 h-4 w-4" />
                Back to Projects
              </Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Icons were previously dynamic; optional future enhancement to store an icon key

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto max-w-4xl px-4 sm:px-6 lg:px-8 py-16">
        <Link
          to="/projects"
          className="inline-flex items-center text-muted-foreground hover:text-foreground transition-colors mb-8"
        >
          <ArrowLeftIcon className="mr-2 h-4 w-4" />
          Back to Projects
        </Link>

        <div className="mb-8">
          <div className="mb-6">
            <h1 className="text-4xl font-bold">{project.title}</h1>
            <p className="text-xl text-muted-foreground mt-2">{project.description}</p>
          </div>

          <div className="flex flex-wrap gap-2 mb-6">
            {project.tech.map((tech) => (
              <Badge key={tech} variant="secondary">
                {tech}
              </Badge>
            ))}
          </div>

          <div className="flex space-x-4 mb-8">
            <Button variant="outline" className="flex-1">
              <GithubIcon className="mr-2 h-5 w-5" />
              View Source Code
            </Button>
            <Button variant="outline" className="flex-1">
              <ExternalLinkIcon className="mr-2 h-5 w-5" />
              Live Demo
            </Button>
          </div>
        </div>

        {project.images && project.images.length > 0 && (
          <div className="mb-8">
            <img
              src={project.images[0]}
              alt={project.title}
              className="w-full h-64 object-cover rounded-lg"
            />
          </div>
        )}

        <Card className="border-0 bg-card/50 backdrop-blur">
          <CardHeader>
            <CardTitle>Project Details</CardTitle>
          </CardHeader>
          <CardContent>
            <div
              className="prose prose-lg max-w-none prose-headings:text-foreground prose-p:text-foreground prose-li:text-foreground prose-strong:text-foreground"
              dangerouslySetInnerHTML={{
                __html: project.content,
              }}
            />
          </CardContent>
        </Card>

        <div className="mt-12 pt-8 border-t border-border">
          <div className="flex justify-between items-center">
            <Link to="/projects">
              <Button variant="outline">
                <ArrowLeftIcon className="mr-2 h-4 w-4" />
                More Projects
              </Button>
            </Link>
            <div className="flex space-x-3">
              <Button variant="outline" size="sm">
                <GithubIcon className="mr-2 h-4 w-4" />
                GitHub
              </Button>
              <Button variant="outline" size="sm">
                <ExternalLinkIcon className="mr-2 h-4 w-4" />
                Live Demo
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
