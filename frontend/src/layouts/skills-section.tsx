import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  CloudIcon,
  CodeIcon,
  DatabaseIcon,
  DownloadIcon,
  ServerIcon,
  WrenchIcon,
} from '@/components/ui/icons';

const skillCategories = [
  {
    title: 'Backend Development',
    icon: ServerIcon,
    skills: ['Node.js', 'Python', 'Go', 'Java'],
  },
  {
    title: 'Databases',
    icon: DatabaseIcon,
    skills: ['PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch'],
  },
  {
    title: 'Cloud & DevOps',
    icon: CloudIcon,
    skills: ['AWS', 'Docker', 'Kubernetes', 'Terraform'],
  },
  {
    title: 'Tools & Frameworks',
    icon: WrenchIcon,
    skills: ['GraphQL', 'REST APIs', 'Microservices', 'Event Streaming'],
  },
];

export function SkillsSection() {
  return (
    <section id="skills" className="py-16 px-4 sm:px-6 lg:px-8 bg-muted/20">
      <div className="container mx-auto max-w-7xl">
        <div className="text-center mb-10">
          <h2 className="text-4xl sm:text-5xl font-bold text-balance mb-4">Skills & Expertise</h2>
          <p className="text-lg text-muted-foreground text-balance max-w-3xl mx-auto leading-normal">
            Technical proficiencies across backend development, cloud infrastructure, and DevOps
            practices
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 mb-10">
          {skillCategories.map((category, index) => {
            const Icon = category.icon;
            return (
              <Card
                key={index}
                className="border-0 bg-card/50 backdrop-blur hover:shadow-lg transition-shadow"
              >
                <CardHeader className="p-6">
                  <CardTitle className="flex items-center space-x-3 text-xl">
                    <Icon className="h-6 w-6 text-primary" />
                    <span>{category.title}</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="px-6 pb-6">
                  <div className="flex flex-wrap gap-2.5">
                    {category.skills.map((skill) => (
                      <Badge key={skill} variant="outline" className="text-xs px-3 py-1.5">
                        {skill}
                      </Badge>
                    ))}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="flex justify-center">
          <Card id="resume" className="w-full max-w-lg border-0 bg-card/50 backdrop-blur">
            <CardHeader className="p-6">
              <CardTitle className="flex items-center space-x-3 text-2xl">
                <CodeIcon className="h-6 w-6 text-primary" />
                <span>Resume</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="px-6 pb-6 space-y-4">
              <p className="text-base text-muted-foreground leading-normal">
                Download my complete resume with detailed work experience, education, and project
                portfolio.
              </p>
              <Button size="lg" className="w-full text-base py-4">
                <DownloadIcon className="mr-3 h-5 w-5" />
                Download Resume (PDF)
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
