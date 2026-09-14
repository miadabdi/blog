import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { api, fileUrl } from '@/lib/api';
import { createEditor } from '@/lib/editor';
import { useDeleteProject, useProjects, useSaveProject } from '@/lib/queries';
import type EditorJS from '@editorjs/editorjs';
import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';

type FormState = {
  title: string;
  summary: string;
  tech: string[];
  github_url: string;
  demo_url: string;
  featured: boolean;
  images: string[];
};

const emptyForm: FormState = {
  title: '',
  summary: '',
  tech: [],
  github_url: '',
  demo_url: '',
  featured: false,
  images: [],
};

export default function ProjectsAdmin() {
  const [params] = useSearchParams();
  const editingParam = params.get('id');
  const navigate = useNavigate();

  const { data: projects } = useProjects();

  // editing by numeric id, resolved from the list
  const editing =
    editingParam && editingParam !== 'new'
      ? (projects ?? []).find((p) => p.id === Number(editingParam))
      : undefined;
  const editingId = editing?.id ?? null;

  const [form, setForm] = useState<FormState>(emptyForm);
  const [techInput, setTechInput] = useState('');
  const [busy, setBusy] = useState(false);

  const saveProject = useSaveProject();
  const deleteProject = useDeleteProject();

  const holderRef = useRef<HTMLDivElement>(null);
  const editorRef = useRef<EditorJS | null>(null);

  const sessionKey = editingId ?? 'new';
  useEffect(() => {
    if (editingParam == null && (projects?.length ?? 0) > 0) return;
    if (!holderRef.current) return;

    const editor = createEditor(holderRef.current, editing ? editing.body : null);
    editorRef.current = editor;
    return () => {
      void editor.destroy();
      editorRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionKey, editing?.id]);

  useEffect(() => {
    if (editing) {
      // ponytail: hydrate form when the editing entity loads
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setForm({
        title: editing.title,
        summary: editing.summary,
        tech: editing.tech,
        github_url: editing.github_url ?? '',
        demo_url: editing.demo_url ?? '',
        featured: editing.featured,
        images: editing.images,
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
    setForm((f) => ({
      ...f,
      images: [...f.images, fileUrl(r.bucket_name, r.object_name)],
    }));
  }

  async function save() {
    if (!form.title.trim() || !form.summary.trim()) {
      alert('Title and description are required');
      return;
    }
    setBusy(true);
    try {
      const output = editorRef.current ? await editorRef.current.save() : { blocks: [] };
      await saveProject.mutateAsync({
        id: editingId ?? undefined,
        data: {
          title: form.title,
          summary: form.summary,
          body: output,
          tech: form.tech,
          images: form.images,
          github_url: form.github_url.trim() || null,
          demo_url: form.demo_url.trim() || null,
          featured: form.featured,
        },
      });
      void navigate('/admin/projects');
    } finally {
      setBusy(false);
    }
  }

  function remove(id: number) {
    if (confirm('Delete this project?')) {
      void deleteProject.mutateAsync(id);
    }
  }

  const showEditor = editingParam != null || (projects?.length ?? 0) === 0;

  return (
    <>
      {!editingParam && (
        <div className="mb-8">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-semibold">All Projects</h2>
            <Link to="/admin/projects?id=new">
              <Button variant="outline">New</Button>
            </Link>
          </div>
          <div className="grid gap-2 w-full">
            {(projects ?? []).map((p) => (
              <div
                key={p.id}
                className="flex items-center justify-between border rounded-md p-3 w-full"
              >
                <div>
                  <div className="font-medium">{p.title}</div>
                  <div className="text-xs text-muted-foreground">/projects/{p.slug}</div>
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
            {!projects?.length && (
              <div className="text-sm text-muted-foreground">No projects yet.</div>
            )}
          </div>
        </div>
      )}

      {showEditor && (
        <div className="w-full max-w-none">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-2xl font-bold">{editingId ? 'Edit Project' : 'New Project'}</h2>
            <div className="flex gap-3">
              <Button onClick={() => void save()} disabled={busy}>
                {busy ? 'Saving…' : 'Save'}
              </Button>
              <Button variant="outline" onClick={() => void navigate('/admin/projects')}>
                {editingId ? 'Back to Projects' : 'Cancel'}
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
                          tech: Array.from(new Set([...form.tech, techInput.trim()])),
                        });
                        setTechInput('');
                      }}
                    >
                      Add
                    </Button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {form.tech.map((t) => (
                      <button
                        key={t}
                        type="button"
                        className="text-xs px-2 py-1 rounded border hover:bg-destructive hover:text-destructive-foreground"
                        onClick={() =>
                          setForm({ ...form, tech: form.tech.filter((x) => x !== t) })
                        }
                        title="Remove"
                      >
                        {t} ✕
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <Label htmlFor="github">GitHub URL</Label>
                  <Input
                    id="github"
                    value={form.github_url}
                    onChange={(e) => setForm({ ...form, github_url: e.target.value })}
                    placeholder="https://github.com/…"
                  />
                </div>
                <div>
                  <Label htmlFor="demo">Demo URL</Label>
                  <Input
                    id="demo"
                    value={form.demo_url}
                    onChange={(e) => setForm({ ...form, demo_url: e.target.value })}
                    placeholder="https://…"
                  />
                </div>
                <div className="flex items-center gap-2">
                  <input
                    id="featured"
                    type="checkbox"
                    checked={form.featured}
                    onChange={(e) => setForm({ ...form, featured: e.target.checked })}
                    className="h-4 w-4"
                  />
                  <Label htmlFor="featured">Featured</Label>
                </div>
                <div>
                  <Label htmlFor="images">Images</Label>
                  <Input
                    id="images"
                    type="file"
                    accept="image/*"
                    onChange={(e) => void onImagePicked(e.target.files)}
                  />
                  <div className="mt-2 space-y-2">
                    {form.images.map((src, i) => (
                      <div key={`${src}-${i}`} className="relative">
                        <img
                          src={src}
                          alt={`image ${i + 1}`}
                          className="h-24 w-full object-cover rounded border"
                        />
                        <button
                          type="button"
                          className="absolute top-1 right-1 text-xs px-2 py-1 rounded bg-destructive text-destructive-foreground"
                          onClick={() =>
                            setForm({ ...form, images: form.images.filter((_, x) => x !== i) })
                          }
                          title="Remove"
                        >
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>
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
