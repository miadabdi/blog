import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import {
  DatabaseIcon,
  ExternalLinkIcon,
  GithubIcon,
  ServerIcon,
} from '@/components/ui/icons';
import { useProjects } from '@/lib/queries';
import { Link } from 'react-router-dom';

export function ProjectsSection() {
  const { data: projects } = useProjects();

  return (
    <section id="projects" className="py-16 px-4 sm:px-6 lg:px-8">
      <div className="container mx-auto max-w-7xl">
        <div className="text-center mb-10">
          <h2 className="text-4xl sm:text-5xl font-bold text-balance mb-4">Featured Projects</h2>
          <p className="text-lg text-muted-foreground text-balance max-w-3xl mx-auto leading-normal">
            A showcase of backend systems, infrastructure projects, and DevOps implementations
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-2">
          {(projects ?? [])
            .slice()
            .sort((a, b) => Number(b.featured) - Number(a.featured))
            .slice(0, 4)
            .map((project) => {
              const Icon = project.featured ? ServerIcon : DatabaseIcon;
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
                      {project.summary}
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
                      {project.github_url && (
                        <a href={project.github_url} target="_blank" rel="noreferrer" className="flex-1">
                          <Button
                            variant="outline"
                            size="lg"
                            className="w-full bg-transparent text-base py-4"
                          >
                            <GithubIcon className="mr-2 h-5 w-5" />
                            Code
                          </Button>
                        </a>
                      )}
                      {project.demo_url && (
                        <a href={project.demo_url} target="_blank" rel="noreferrer" className="flex-1">
                          <Button
                            variant="outline"
                            size="lg"
                            className="w-full bg-transparent text-base py-4"
                          >
                            <ExternalLinkIcon className="mr-2 h-5 w-5" />
                            Demo
                          </Button>
                        </a>
                      )}
                      <Link to={`/projects/${project.slug}`} className="flex-1">
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

        <div className="text-center mt-10">
          <Link to="/projects">
            <Button variant="outline" size="lg" className="text-base px-6 py-4 bg-transparent">
              View All Projects
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
}
