/**
 * react-query hooks for the blog API.
 */

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { api } from './api';
import type { ApiPost, ApiProject, ApiTag, ApiUser, EditorBody } from './types';

export const qk = {
  posts: ['posts'] as const,
  post: (id: number) => ['posts', id] as const,
  postSlug: (slug: string) => ['posts', 'slug', slug] as const,
  projects: ['projects'] as const,
  project: (id: number) => ['projects', id] as const,
  projectSlug: (slug: string) => ['projects', 'slug', slug] as const,
  tags: ['tags'] as const,
  me: ['me'] as const,
};

export const usePosts = () =>
  useQuery({ queryKey: qk.posts, queryFn: () => api<ApiPost[]>('/post/') });

export const usePostById = (id: number | null) =>
  useQuery({
    queryKey: qk.post(id ?? 0),
    queryFn: () => api<ApiPost>(`/post/${id}`),
    enabled: id != null,
  });

export const usePostBySlug = (slug: string | undefined) =>
  useQuery({
    queryKey: qk.postSlug(slug ?? ''),
    queryFn: () => api<ApiPost>(`/post/slug/${slug}`),
    enabled: !!slug,
    retry: false,
  });

export const useProjects = () =>
  useQuery({ queryKey: qk.projects, queryFn: () => api<ApiProject[]>('/project/') });

export const useProjectBySlug = (slug: string | undefined) =>
  useQuery({
    queryKey: qk.projectSlug(slug ?? ''),
    queryFn: () => api<ApiProject>(`/project/slug/${slug}`),
    enabled: !!slug,
    retry: false,
  });

export const useTags = () =>
  useQuery({ queryKey: qk.tags, queryFn: () => api<ApiTag[]>('/tag/') });

export const useMe = () =>
  useQuery({
    queryKey: qk.me,
    queryFn: () => api<ApiUser>('/auth/get-me'),
    enabled: !!localStorage.getItem('blog_token'),
    retry: false,
  });

export type PostInput = {
  title: string;
  summary: string;
  body: string;
  featured_image: string;
  tag_ids?: number[] | null;
};

export const useSavePost = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id?: number; data: PostInput }) =>
      id != null
        ? api<ApiPost>(`/post/${id}`, { method: 'PATCH', body: JSON.stringify(data) })
        : api<ApiPost>('/post/', { method: 'POST', body: JSON.stringify(data) }),
    onSuccess: () => qc.invalidateQueries({ queryKey: qk.posts }),
  });
};

export const useDeletePost = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api<ApiPost>(`/post/${id}`, { method: 'DELETE' }),
    onSuccess: () => qc.invalidateQueries({ queryKey: qk.posts }),
  });
};

export type ProjectInput = {
  title: string;
  summary: string;
  body: EditorBody;
  tech: string[];
  images: string[];
  github_url: string | null;
  demo_url: string | null;
  featured: boolean;
};

export const useSaveProject = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id?: number; data: ProjectInput }) =>
      id != null
        ? api<ApiProject>(`/project/${id}`, { method: 'PATCH', body: JSON.stringify(data) })
        : api<ApiProject>('/project/', { method: 'POST', body: JSON.stringify(data) }),
    onSuccess: () => qc.invalidateQueries({ queryKey: qk.projects }),
  });
};

export const useDeleteProject = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api<ApiProject>(`/project/${id}`, { method: 'DELETE' }),
    onSuccess: () => qc.invalidateQueries({ queryKey: qk.projects }),
  });
};

/** Reconcile tag names against existing tags, creating missing ones; returns tag ids. */
export async function ensureTagIds(names: string[]): Promise<number[]> {
  if (names.length === 0) return [];
  const existing = await api<ApiTag[]>('/tag/');
  const byName = new Map(existing.map((t) => [t.name.toLowerCase(), t.id]));
  const ids: number[] = [];
  for (const name of names) {
    const key = name.toLowerCase();
    let id = byName.get(key);
    if (id == null) {
      const created = await api<ApiTag>('/tag/', {
        method: 'POST',
        body: JSON.stringify({ name }),
      });
      id = created.id;
      byName.set(key, id);
    }
    ids.push(id);
  }
  return ids;
}
