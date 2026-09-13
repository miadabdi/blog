import { BlogSection } from '../layouts/blog-section';
import { Hero } from '../layouts/hero';
import { ProjectsSection } from '../layouts/projects-section';
import { SkillsSection } from '../layouts/skills-section';

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <main className="space-y-12">
        <Hero />
        <BlogSection />
        <ProjectsSection />
        <SkillsSection />
      </main>
    </div>
  );
}
