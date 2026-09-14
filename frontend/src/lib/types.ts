/**
 * API entity types — mirror the backend public schemas.
 *
 * Note: post bodies are JSON-encoded strings (legacy posts pipeline),
 * project bodies are real objects. EditorContent handles both.
 */

import type { EditorJSOutput } from 'editorjs-parser';

export type ApiUser = {
  id: number;
  email: string;
  fname: string;
  lname: string;
  role: 'ADMIN' | 'USER';
  is_active: boolean;
};

export type ApiTag = { id: number; name: string; slug: string };

export type ApiCategory = { id: number; name: string; slug: string; description: string | null };

export type ApiPost = {
  id: number;
  title: string;
  summary: string;
  body: string; // JSON-encoded Editor.js output
  featured_image: string;
  slug: string;
  published_at: string | null;
  created_at: string;
  view_count: number;
  categories: ApiCategory[] | null;
  tags: ApiTag[] | null;
  author_id: number;
  author: ApiUser;
};

export type ApiProject = {
  id: number;
  title: string;
  slug: string;
  summary: string;
  body: EditorJSOutput; // real object
  tech: string[];
  github_url: string | null;
  demo_url: string | null;
  featured: boolean;
  images: string[];
  view_count: number;
  published_at: string | null;
  created_at: string;
  author_id: number;
  author: ApiUser;
};

export type EditorBody = string | EditorJSOutput | null;

/** Display date: published_at falls back to created_at. */
export const postDate = (p: { published_at: string | null; created_at: string }) =>
  (p.published_at ?? p.created_at).slice(0, 10);

/** Rough reading time from body word count. */
export const readTime = (body: EditorBody): string => {
  const data = typeof body === 'string' ? safeParse(body) : body;
  const words = (data?.blocks ?? []).reduce((n, b) => {
    const d = (b.data ?? {}) as Record<string, unknown>;
    const text = typeof d.text === 'string' ? d.text : typeof d.caption === 'string' ? d.caption : '';
    return n + text.trim().split(/\s+/).filter(Boolean).length;
  }, 0);
  return `${Math.max(1, Math.round(words / 200))} min read`;
};

export const tagNames = (p: ApiPost): string[] => (p.tags ?? []).map((t) => t.name);

function safeParse(s: string): EditorJSOutput | null {
  try {
    return JSON.parse(s) as EditorJSOutput;
  } catch {
    return null;
  }
}
