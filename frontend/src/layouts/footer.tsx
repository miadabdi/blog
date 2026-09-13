import { Button } from '@/components/ui/button';
import { GithubIcon, LinkedinIcon, MailIcon, TerminalIcon } from '@/components/ui/icons';

export function Footer() {
  return (
    <footer className="border-t border-border bg-muted/20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid gap-8 md:grid-cols-3">
          <div className="space-y-6">
            <div className="flex items-center space-x-3">
              <TerminalIcon className="h-7 w-7 text-primary" />
              <span className="font-mono text-2xl font-bold">miad.dev</span>
            </div>
            <p className="text-base text-muted-foreground max-w-sm leading-normal">
              Full stack developer passionate about building scalable backend systems and robust
              infrastructure.
            </p>
          </div>

          <div className="space-y-6">
            <h3 className="text-xl font-semibold">Quick Links</h3>
            <div className="space-y-2.5">
              <a
                href="#blog"
                className="block text-base text-muted-foreground hover:text-foreground transition-colors"
              >
                Blog
              </a>
              <a
                href="#projects"
                className="block text-base text-muted-foreground hover:text-foreground transition-colors"
              >
                Projects
              </a>
              <a
                href="#skills"
                className="block text-base text-muted-foreground hover:text-foreground transition-colors"
              >
                Skills
              </a>
              <a
                href="#resume"
                className="block text-base text-muted-foreground hover:text-foreground transition-colors"
              >
                Resume
              </a>
            </div>
          </div>

          <div className="space-y-6">
            <h3 className="text-xl font-semibold">Connect</h3>
            <div className="flex space-x-2.5">
              <Button variant="ghost" size="lg" className="p-3" aria-label="GitHub">
                <GithubIcon className="h-6 w-6" />
              </Button>
              <Button variant="ghost" size="lg" className="p-3" aria-label="LinkedIn">
                <LinkedinIcon className="h-6 w-6" />
              </Button>
              <Button variant="ghost" size="lg" className="p-3" aria-label="Email">
                <MailIcon className="h-6 w-6" />
              </Button>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-border text-center">
          <p className="text-base text-muted-foreground">
            &copy; 2025 Miad Abdi. Built with React.js
          </p>
        </div>
      </div>
    </footer>
  );
}
