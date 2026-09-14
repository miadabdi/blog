import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { api, fileUrl } from '@/lib/api';
import { createEditor } from '@/lib/editor';
import { ensureTagIds, qk, useDeletePost, usePostById, usePosts, useSavePost } from '@/lib/queries';
import { tagNames } from '@/lib/types';
import type { EditorJSOutput } from 'editorjs-parser';
import type EditorJS from '@editorjs/editorjs';
import { useQueryClient } from '@tanstack/react-query';
import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';

type FormState = {
  title: string;
  summary: string;
  featured_image: string;
  tags: string[];
};

const emptyForm: FormState = { title: '', summary: '', featured_image: '', tags: [] };

export default function PostsAdmin() {
  const [params] = useSearchParams();
  const editingParam = params.get('id');
  const editingId = editingParam && editingParam !== 'new' ? Number(editingParam) : null;
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: posts } = usePosts();
  const { data: editing } = usePostById(editingId);

  const [form, setForm] = useState<FormState>(emptyForm);
  const [tagInput, setTagInput] = useState('');
  const [busy, setBusy] = useState(false);

  const savePost = useSavePost();
  const deletePost = useDeletePost();

  // Editor.js lifecycle: one editor per editing session
  const holderRef = useRef<HTMLDivElement>(null);
  const editorRef = useRef<EditorJS | null>(null);

  const sessionKey = editingId ?? 'new';
  useEffect(() => {
    if (editingParam == null && (posts?.length ?? 0) > 0) return; // list view
    if (!holderRef.current) return;

    let initialData: EditorJSOutput | null = null;
    if (editing && editing.id === editingId) {
      try {
        initialData = JSON.parse(editing.body) as EditorJSOutput;
      } catch {
        initialData = null;
      }
    }

    const editor = createEditor(holderRef.current, initialData);
    editorRef.current = editor;
    return () => {
      void editor.destroy();
      editorRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionKey, editing?.id]);

  // hydrate form when the editing post loads
  useEffect(() => {
    if (editing && editing.id === editingId) {
      // ponytail: hydrate form when the editing entity loads
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setForm({
        title: editing.title,
        summary: editing.summary,
        featured_image: editing.featured_image,
        tags: tagNames(editing),
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [editing?.id]);

  async function onImagePicked(files: FileList | null) {
    if (!files?.length) return;
    const fd = new FormData();
    fd.append('file', files[0]);
    const r = await api<{ bucket_name: string; object_name: string }>(
      '/file/upload?bucket=images',
      { method: 'POST', body: fd },
    );
    setForm((f) => ({ ...f, featured_image: fileUrl(r.bucket_name, r.object_name) }));
  }

  async function save() {
    if (!form.title.trim() || !form.summary.trim()) {
      alert('Title and description are required');
      return;
    }
    setBusy(true);
    try {
      const output = editorRef.current ? await editorRef.current.save() : { blocks: [] };
      const tag_ids = await ensureTagIds(form.tags);
      await savePost.mutateAsync({
        id: editingId ?? undefined,
        data: {
          title: form.title,
          summary: form.summary,
          body: JSON.stringify(output),
          featured_image: form.featured_image || '/placeholder.svg',
          tag_ids,
        },
      });
      await queryClient.invalidateQueries({ queryKey: qk.tags });
      void navigate('/admin/posts');
    } finally {
      setBusy(false);
    }
  }

  function remove(id: number) {
    if (confirm('Delete this post?')) {
      void deletePost.mutateAsync(id);
    }
  }

  const showEditor = editingParam != null || (posts?.length ?? 0) === 0;

  return (
    <>
      {!editingParam && (
        <div className="mb-8">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-semibold">All Posts</h2>
            <Link to="/admin/posts?id=new">
              <Button variant="outline">New</Button>
            </Link>
          </div>
          <div className="grid gap-2 w-full">
            {(posts ?? []).map((p) => (
              <div
                key={p.id}
                className="flex items-center justify-between border rounded-md p-3 w-full"
              >
                <div>
                  <div className="font-medium">{p.title}</div>
                  <div className="text-xs text-muted-foreground">/blog/{p.slug}</div>
                </div>
                <div className="flex gap-2">
                  <Link to={`?id=${p.id}`}>
                    <Button size="sm" variant="secondary">
                      Edit
                    </Button>
                  </Link>
                  <Button size="sm" variant="destructive" onClick={() => remove(p.id)}>
                    Delete
                  </Button>
                </div>
              </div>
            ))}
            {!posts?.length && (
              <div className="text-sm text-muted-foreground">No posts yet.</div>
            )}
          </div>
        </div>
      )}

      {showEditor && (
        <div className="w-full max-w-none">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-2xl font-bold">{editingId ? 'Edit Post' : 'New Post'}</h2>
            <div className="flex gap-3">
              <Button onClick={() => void save()} disabled={busy}>
                {busy ? 'Saving…' : 'Save'}
              </Button>
              <Button variant="outline" onClick={() => void navigate('/admin/posts')}>
                {editingId ? 'Back to Posts' : 'Cancel'}
              </Button>
            </div>
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
            {/* Metadata sidebar */}
            <div className="xl:col-span-1 space-y-6">
              <div className="space-y-4">
                <div>
                  <Label htmlFor="title">Title</Label>
                  <Input
                    id="title"
                    value={form.title}
                    onChange={(e) => setForm({ ...form, title: e.target.value })}
                  />
                </div>
                <div>
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    value={form.summary}
                    onChange={(e) => setForm({ ...form, summary: e.target.value })}
                    rows={3}
                  />
                </div>
                <div>
                  <Label>Tags</Label>
                  <div className="flex gap-2 mb-2">
                    <Input
                      placeholder="Add tag"
                      value={tagInput}
                      onChange={(e) => setTagInput(e.target.value)}
                    />
                    <Button
                      type="button"
                      size="sm"
                      onClick={() => {
                        if (!tagInput.trim()) return;
                        setForm({
                          ...form,
                          tags: Array.from(new Set([...form.tags, tagInput.trim()])),
                        });
                        setTagInput('');
                      }}
                    >
                      Add
                    </Button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {form.tags.map((t) => (
                      <button
                        key={t}
                        type="button"
                        className="text-xs px-2 py-1 rounded border hover:bg-destructive hover:text-destructive-foreground"
                        onClick={() =>
                          setForm({ ...form, tags: form.tags.filter((x) => x !== t) })
                        }
                        title="Remove"
                      >
                        {t} ✕
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <Label htmlFor="image">Featured Image</Label>
                  <Input
                    id="image"
                    type="file"
                    accept="image/*"
                    onChange={(e) => void onImagePicked(e.target.files)}
                  />
                  {form.featured_image && (
                    <img
                      src={form.featured_image}
                      alt="cover preview"
                      className="mt-2 h-24 w-full object-cover rounded border"
                    />
                  )}
                </div>
              </div>
            </div>

            {/* Editor.js content editor */}
            <div className="xl:col-span-3">
              <div className="h-[calc(100vh-12rem)] overflow-auto border rounded-md p-4 bg-card">
                <Label className="text-lg font-semibold mb-4 block">Content</Label>
                <div ref={holderRef} />
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
