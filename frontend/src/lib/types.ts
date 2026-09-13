export type Post = {
  id: string; // slug
  title: string;
  description: string;
  date: string; // ISO string
  readTime?: string;
  tags: string[];
  featured?: boolean;
  image?: string;
  content: string;
};

export type Project = {
  id: string; // slug
  title: string;
  description: string;
  tech: string[];
  github?: string;
  demo?: string;
  featured?: boolean;
  content: string;
  images?: string[];
};
