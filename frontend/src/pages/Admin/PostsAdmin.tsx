import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { posts } from '@/lib/storage';
import type { Post } from '@/lib/types';
import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';

function emptyPost(): Post {
  const today = new Date().toISOString().slice(0, 10);
  return {
    id: '',
    title: '',
    description: '',
    date: today,
    readTime: '5 min read',
    tags: [],
    image: '',
    content: '<p> some </p>',
  };
}

export default function PostsAdmin() {
  const [params] = useSearchParams();
  const editingId = params.get('id');
  const navigate = useNavigate();

  const initial = useMemo(() => {
    const found = editingId ? posts.find((p) => p.id === editingId) : undefined;
    return found ?? emptyPost();
  }, [editingId]);

  const [form, setForm] = useState<Post>(initial);
  useEffect(() => {
    setForm(initial);
  }, [initial]);
  const [tagInput, setTagInput] = useState('');

  function slugify(text: string) {
    return text
      .toLowerCase()
      .trim()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-');
  }

  function save() {
    const id = form.id?.trim() || slugify(form.title || '');
    if (!id) {
      alert('Please add a title to generate an ID');
      return;
    }
    void navigate('/admin/posts');
  }

  function remove(id: string) {
    if (confirm('Delete this post?')) {
      void navigate('/admin/posts');
    }
  }

  return (
    <>
      {/* Show posts list only when not editing */}
      {!editingId && (
        <div className="mb-8">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-semibold">All Posts</h2>
            <Link to="/admin/posts?id=new">
              <Button variant="outline">New</Button>
            </Link>
          </div>
          <div className="grid gap-2 w-full">
            {posts.map((p) => (
              <div
                key={p.id}
                className="flex items-center justify-between border rounded-md p-3 w-full"
              >
                <div>
                  <div className="font-medium">{p.title}</div>
                  <div className="text-xs text-muted-foreground">{p.id}</div>
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
            {!posts.length && <div className="text-sm text-muted-foreground">No posts yet.</div>}
          </div>
        </div>
      )}

      {/* Full-width editor when creating/editing */}
      {(editingId || (!editingId && posts.length === 0)) && (
        <div className="w-full max-w-none">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-2xl font-bold">{editingId ? 'Edit Post' : 'New Post'}</h2>
            <div className="flex gap-3">
              <Button onClick={save}>Save</Button>
              <Button variant="outline" onClick={() => void navigate('/admin/posts')}>
                {editingId ? 'Back to Posts' : 'Cancel'}
              </Button>
            </div>
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
            {/* Metadata sidebar */}
            <div className="xl:col-span-1 space-y-6">
              <div className="space-y-4">
                {/* ID is backend-managed; slug auto-generated on save */}
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
                    value={form.description}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                    rows={3}
                  />
                </div>
                <div className="grid grid-cols-1 gap-4">
                  <div>
                    <Label htmlFor="date">Date</Label>
                    <Input
                      id="date"
                      type="date"
                      value={form.date}
                      onChange={(e) => setForm({ ...form, date: e.target.value })}
                    />
                  </div>
                  <div>
                    <Label htmlFor="readTime">Read Time</Label>
                    <Input
                      id="readTime"
                      value={form.readTime ?? ''}
                      onChange={(e) => setForm({ ...form, readTime: e.target.value })}
                    />
                  </div>
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
                          setForm({
                            ...form,
                            tags: form.tags.filter((x) => x !== t),
                          })
                        }
                        title="Remove"
                      >
                        {t} ✕
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <Label htmlFor="image">Image URL</Label>
                  <Input
                    id="image"
                    value={form.image ?? ''}
                    onChange={(e) => setForm({ ...form, image: e.target.value })}
                  />
                </div>
              </div>
            </div>

            {/* Main content editor */}
            <div className="xl:col-span-3">
              <div className="h-[calc(100vh-12rem)]">
                <Label className="text-lg font-semibold mb-4 block">Content</Label>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
