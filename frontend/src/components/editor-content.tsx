/**
 * Renders Editor.js JSON as HTML via editorjs-parser.
 * Accepts posts' JSON-encoded string bodies and projects' object bodies.
 */

import edjsParser, { type EditorJSOutput } from 'editorjs-parser';
import { useMemo } from 'react';

const parser = new edjsParser();

export function EditorContent({
  body,
  className,
}: {
  body: string | EditorJSOutput | null;
  className?: string;
}) {
  const html = useMemo(() => {
    if (!body) return '';
    let output: EditorJSOutput | null;
    if (typeof body === 'string') {
      try {
        output = JSON.parse(body) as EditorJSOutput;
      } catch {
        return '';
      }
    } else {
      output = body;
    }
    return parser.parse(output);
  }, [body]);

  if (!html) return null;
  return <div className={className} dangerouslySetInnerHTML={{ __html: html }} />;
}
