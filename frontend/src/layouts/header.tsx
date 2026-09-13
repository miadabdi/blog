'use client';

import { ThemeToggle } from '@/components/theme-toggle';
import { Button } from '@/components/ui/button';
import {
  CodeIcon,
  FileTextIcon,
  MenuIcon,
  TerminalIcon,
  UserIcon,
  XIcon,
} from '@/components/ui/icons';
import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: 'Blog', href: '/blog', icon: FileTextIcon },
    { name: 'Projects', href: '/projects', icon: CodeIcon },
    { name: 'Admin', href: '/admin', icon: TerminalIcon },
    { name: 'Skills', href: '/#skills', icon: TerminalIcon },
    { name: 'Resume', href: '/#resume', icon: UserIcon },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-20 items-center justify-between">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-3">
              <TerminalIcon className="h-7 w-7 text-primary" aria-hidden />
              <span className="font-mono text-2xl font-bold">miad.dev</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-10">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isExternal = item.href.startsWith('/#');

              if (isExternal) {
                return (
                  <a
                    key={item.name}
                    href={item.href}
                    className="flex items-center space-x-2 text-base font-medium text-muted-foreground hover:text-foreground transition-colors"
                  >
                    <Icon className="h-4 w-4" aria-hidden />
                    <span>{item.name}</span>
                  </a>
                );
              }

              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center space-x-2 text-base font-medium transition-colors ${
                    location.pathname === item.href
                      ? 'text-foreground'
                      : 'text-muted-foreground hover:text-foreground'
                  }`}
                >
                  <Icon className="h-4 w-4" aria-hidden />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </nav>

          <div className="flex items-center space-x-4">
            <ThemeToggle />

            {/* Mobile menu button */}
            <Button
              variant="ghost"
              size="sm"
              className="md:hidden"
              onClick={() => setIsMenuOpen((prev) => !prev)}
            >
              {isMenuOpen ? (
                <XIcon className="h-5 w-5" aria-hidden />
              ) : (
                <MenuIcon className="h-5 w-5" aria-hidden />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-6 space-y-2 border-t border-border">
              {navigation.map((item) => {
                const Icon = item.icon;
                const isExternal = item.href.startsWith('/#');

                if (isExternal) {
                  return (
                    <a
                      key={item.name}
                      href={item.href}
                      className="flex items-center space-x-3 px-4 py-3 text-base font-medium text-muted-foreground hover:text-foreground hover:bg-accent rounded-lg transition-colors"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      <Icon className="h-5 w-5" />
                      <span>{item.name}</span>
                    </a>
                  );
                }

                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center space-x-3 px-4 py-3 text-base font-medium hover:bg-accent rounded-lg transition-colors ${
                      location.pathname === item.href
                        ? 'text-foreground'
                        : 'text-muted-foreground hover:text-foreground'
                    }`}
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <Icon className="h-5 w-5" />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
