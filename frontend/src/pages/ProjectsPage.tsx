import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import {
  ArrowLeftIcon,
  DatabaseIcon,
  ExternalLinkIcon,
  GithubIcon,
  ServerIcon,
} from '@/components/ui/icons';
import { Link } from 'react-router-dom';
import { projects as projectsData } from '../lib/storage';

const projects = projectsData.map((p) => ({
  ...p,
  icon: p.featured ? ServerIcon : DatabaseIcon,
}));

export function ProjectsPage() {
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
          <h1 className="text-4xl sm:text-5xl font-bold text-balance mb-4">Projects</h1>
          <p className="text-lg text-muted-foreground text-balance max-w-3xl leading-normal">
            A comprehensive showcase of backend systems, infrastructure projects, and DevOps
            implementations
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-2">
          {projects.map((project) => {
            const Icon = project.icon;
            return (
              <Card
                key={project.id}
                className={`group hover:shadow-xl transition-all duration-300 border-0 bg-card/50 backdrop-blur ${
                  project.featured ? 'lg:col-span-2' : ''
                }`}
              >
                <CardHeader className="p-6">
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="p-2.5 bg-primary/10 rounded-xl">
                      <Icon className="h-8 w-8 text-primary" />
                    </div>
                    <CardTitle className="text-xl group-hover:text-primary transition-colors">
                      {project.title}
                    </CardTitle>
                  </div>
                  <CardDescription className="text-base leading-normal">
                    {project.description}
                  </CardDescription>
                </CardHeader>
                <CardContent className="px-6 pb-6">
                  <div className="flex flex-wrap gap-2.5 mb-4">
                    {project.tech.map((tech) => (
                      <Badge key={tech} variant="secondary" className="text-xs px-2.5 py-1">
                        {tech}
                      </Badge>
                    ))}
                  </div>
                  <div className="flex space-x-3">
                    <Button
                      variant="outline"
                      size="lg"
                      className="flex-1 bg-transparent text-base py-4"
                    >
                      <GithubIcon className="mr-2 h-5 w-5" />
                      Code
                    </Button>
                    <Button
                      variant="outline"
                      size="lg"
                      className="flex-1 bg-transparent text-base py-4"
                    >
                      <ExternalLinkIcon className="mr-2 h-5 w-5" />
                      Demo
                    </Button>
                    <Link to={`/projects/${project.id}`} className="flex-1">
                      <Button variant="default" size="lg" className="w-full text-base py-4">
                        View Details
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}
