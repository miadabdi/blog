/**
 * Editor.js factory + image uploader wired to the backend file endpoint.
 */

import EditorJS, { type OutputData } from '@editorjs/editorjs';
import Code from '@editorjs/code';
import Header from '@editorjs/header';
import ImageTool from '@editorjs/image';
import List from '@editorjs/list';
import Quote from '@editorjs/quote';
import type { EditorJSOutput } from 'editorjs-parser';

import { api, fileUrl } from './api';

async function uploadByFile(file: File) {
  const fd = new FormData();
  fd.append('file', file);
  const r = await api<{ bucket_name: string; object_name: string }>(
    '/file/upload?bucket=images',
    { method: 'POST', body: fd },
  );
  return { success: 1, file: { url: fileUrl(r.bucket_name, r.object_name) } };
}

const uploadByUrl = (url: string) => Promise.resolve({ success: 1, file: { url } });

export function createEditor(holder: HTMLElement, data?: EditorJSOutput | null): EditorJS {
  // editorjs-parser's EditorJSOutput differs only in optional-vs-required block data
  const initialData = data as unknown as OutputData | undefined;
  return new EditorJS({
    holder,
    data: initialData,
    tools: {
      header: Header,
      list: List,
      quote: Quote,
      code: Code,
      image: {
        class: ImageTool,
        config: {
          uploader: { uploadByFile, uploadByUrl },
        },
      },
    },
  });
}
