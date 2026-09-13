import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { projects } from '@/lib/storage';
import type { Project } from '@/lib/types';
import { useEffect, useMemo, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';

function emptyProject(): Project {
  return {
    id: '',
    title: '',
    description: '',
    tech: [],
    github: '',
    demo: '',
    content: '<p> ... </p>',
    images: ['/placeholder.jpg'],
  };
}

export default function ProjectsAdmin() {
  const [params] = useSearchParams();
  const editingId = params.get('id');
  const navigate = useNavigate();

  const initial = useMemo(() => {
    const found = editingId ? projects.find((p) => p.id === editingId) : undefined;
    return found ?? emptyProject();
  }, [editingId]);

  const [form, setForm] = useState<Project>(initial);
  useEffect(() => {
    setForm(initial);
  }, [initial]);
  const [techInput, setTechInput] = useState('');

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
    void navigate('/admin/projects');
  }

  function remove(id: string) {
    if (confirm('Delete this project?')) {
      void navigate('/admin/projects');
    }
  }

  return (
    <>
      {/* Show projects list only when not editing */}
      {!editingId && (
        <div className="mb-8">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-semibold">All Projects</h2>
            <Link to="/admin/projects?id=new">
              <Button variant="outline">New</Button>
            </Link>
          </div>
          <div className="grid gap-2 w-full">
            {projects.map((p) => (
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
            {!projects.length && (
              <div className="text-sm text-muted-foreground">No projects yet.</div>
            )}
          </div>
        </div>
      )}

      {/* Full-width editor when creating/editing */}
      {(editingId || (!editingId && projects.length === 0)) && (
        <div className="w-full max-w-none">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-2xl font-bold">{editingId ? 'Edit Project' : 'New Project'}</h2>
            <div className="flex gap-3">
              <Button onClick={save}>Save</Button>
              <Button variant="outline" onClick={() => void navigate('/admin/projects')}>
                {editingId ? 'Back to Projects' : 'Cancel'}
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
                  <Label htmlFor="description">Short Description</Label>
                  <Textarea
                    id="description"
                    value={form.description}
                    onChange={(e) => setForm({ ...form, description: e.target.value })}
                    rows={3}
                  />
                </div>
                <div>
                  <Label>Tech</Label>
                  <div className="flex gap-2 mb-2">
                    <Input
                      placeholder="Add tech"
                      value={techInput}
                      onChange={(e) => setTechInput(e.target.value)}
                    />
                    <Button
                      type="button"
                      size="sm"
                      onClick={() => {
                        if (!techInput.trim()) return;
                        setForm({
                          ...form,
                          tech: Array.from(new Set([...(form.tech || []), techInput.trim()])),
                        });
                        setTechInput('');
                      }}
                    >
                      Add
                    </Button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {(form.tech || []).map((t) => (
                      <button
                        key={t}
                        type="button"
                        className="text-xs px-2 py-1 rounded border hover:bg-destructive hover:text-destructive-foreground"
                        onClick={() =>
                          setForm({
                            ...form,
                            tech: (form.tech || []).filter((x) => x !== t),
                          })
                        }
                        title="Remove"
                      >
                        {t} ✕
                      </button>
                    ))}
                  </div>
                </div>
                <div className="grid grid-cols-1 gap-4">
                  <div>
                    <Label htmlFor="github">GitHub URL</Label>
                    <Input
                      id="github"
                      value={form.github ?? ''}
                      onChange={(e) => setForm({ ...form, github: e.target.value })}
                    />
                  </div>
                  <div>
                    <Label htmlFor="demo">Demo URL</Label>
                    <Input
                      id="demo"
                      value={form.demo ?? ''}
                      onChange={(e) => setForm({ ...form, demo: e.target.value })}
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="images">First Image URL</Label>
                  <Input
                    id="images"
                    value={form.images?.[0] ?? ''}
                    onChange={(e) => setForm({ ...form, images: [e.target.value] })}
                  />
                </div>
              </div>
            </div>

            {/* Main content editor */}
            <div className="xl:col-span-3">
              <div className="h-[calc(100vh-12rem)]">
                <Label className="text-lg font-semibold mb-4 block">Long Description</Label>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
