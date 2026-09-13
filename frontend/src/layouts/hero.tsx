import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  CloudIcon,
  DatabaseIcon,
  DownloadIcon,
  GithubIcon,
  LinkedinIcon,
  MailIcon,
  ServerIcon,
} from '@/components/ui/icons';

export function Hero() {
  return (
    <section className="py-16 px-4 sm:px-6 lg:px-8">
      <div className="container mx-auto max-w-5xl">
        <div className="text-center space-y-6">
          <div className="flex justify-center mb-4">
            <div className="flex items-center space-x-4 text-muted-foreground">
              <ServerIcon className="h-8 w-8" />
              <DatabaseIcon className="h-8 w-8" />
              <CloudIcon className="h-8 w-8" />
            </div>
          </div>

          <div className="space-y-4">
            <h1 className="text-5xl sm:text-7xl font-bold text-balance leading-tight">
              Full Stack Developer
              <span className="block text-primary mt-1">Backend & DevOps</span>
            </h1>

            <p className="text-lg sm:text-xl text-muted-foreground text-balance max-w-3xl mx-auto leading-normal">
              Building scalable systems, optimizing infrastructure, and crafting robust backend
              solutions. Passionate about clean code, automation, and distributed systems.
            </p>
          </div>

          <div className="flex flex-wrap justify-center gap-2 py-2">
            <Badge variant="secondary" className="text-sm px-4 py-2">
              Node.js
            </Badge>
            <Badge variant="secondary" className="text-sm px-4 py-2">
              Python
            </Badge>
            <Badge variant="secondary" className="text-sm px-4 py-2">
              Docker
            </Badge>
            <Badge variant="secondary" className="text-sm px-4 py-2">
              Kubernetes
            </Badge>
            <Badge variant="secondary" className="text-sm px-4 py-2">
              AWS
            </Badge>
            <Badge variant="secondary" className="text-sm px-4 py-2">
              PostgreSQL
            </Badge>
            <Badge variant="secondary" className="text-sm px-4 py-2">
              Redis
            </Badge>
            <Badge variant="secondary" className="text-sm px-4 py-2">
              GraphQL
            </Badge>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
            <Button size="lg" className="w-full sm:w-auto text-base px-6 py-4">
              <MailIcon className="mr-3 h-5 w-5" />
              Get In Touch
            </Button>
            <Button
              variant="outline"
              size="lg"
              className="w-full sm:w-auto text-base px-6 py-4 bg-transparent"
            >
              <DownloadIcon className="mr-3 h-5 w-5" />
              Download Resume
            </Button>
          </div>

          <div className="flex justify-center space-x-4 pt-2">
            <Button variant="ghost" size="lg" className="p-3" aria-label="GitHub">
              <GithubIcon className="h-6 w-6" />
            </Button>
            <Button variant="ghost" size="lg" className="p-3" aria-label="LinkedIn">
              <LinkedinIcon className="h-6 w-6" />
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}
