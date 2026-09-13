import type { ReactNode, SVGProps } from 'react';

export type IconProps = SVGProps<SVGSVGElement>;

const iconDefaults = {
  xmlns: 'http://www.w3.org/2000/svg',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.8,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
} as const;

function createIcon(content: ReactNode) {
  return function Icon({ width = 24, height = 24, role = 'img', ...props }: IconProps) {
    return (
      <svg
        width={width}
        height={height}
        viewBox="0 0 24 24"
        focusable="false"
        aria-hidden={props['aria-label'] ? undefined : true}
        role={role}
        {...iconDefaults}
        {...props}
      >
        {content}
      </svg>
    );
  };
}

export const SunIcon = createIcon([
  <circle key="c" cx="12" cy="12" r="4" />,
  <line key="l1" x1="12" y1="2" x2="12" y2="4" />,
  <line key="l2" x1="12" y1="20" x2="12" y2="22" />,
  <line key="l3" x1="4.93" y1="4.93" x2="6.34" y2="6.34" />,
  <line key="l4" x1="17.66" y1="17.66" x2="19.07" y2="19.07" />,
  <line key="l5" x1="2" y1="12" x2="4" y2="12" />,
  <line key="l6" x1="20" y1="12" x2="22" y2="12" />,
  <line key="l7" x1="4.93" y1="19.07" x2="6.34" y2="17.66" />,
  <line key="l8" x1="17.66" y1="6.34" x2="19.07" y2="4.93" />,
]);

export const MoonIcon = createIcon(
  <path d="M21 12.79A9 9 0 0 1 11.21 3 7 7 0 0 0 12 17a7 7 0 0 0 9-4.21z" />,
);

export const MenuIcon = createIcon([
  <line key="m1" x1="4" y1="6" x2="20" y2="6" />,
  <line key="m2" x1="4" y1="12" x2="20" y2="12" />,
  <line key="m3" x1="4" y1="18" x2="20" y2="18" />,
]);

export const XIcon = createIcon([
  <line key="x1" x1="18" y1="6" x2="6" y2="18" />,
  <line key="x2" x1="6" y1="6" x2="18" y2="18" />,
]);

export const CodeIcon = createIcon([
  <polyline key="c1" points="16 18 22 12 16 6" />,
  <polyline key="c2" points="8 6 2 12 8 18" />,
]);

export const FileTextIcon = createIcon([
  <path key="f1" d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />,
  <polyline key="f2" points="14 3 14 9 20 9" />,
  <line key="f3" x1="16" y1="13" x2="8" y2="13" />,
  <line key="f4" x1="16" y1="17" x2="8" y2="17" />,
]);

export const FolderOpenIcon = createIcon([
  <path
    key="fo1"
    d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"
  />,
  <path key="fo2" d="M2 11h20" />,
]);

export const TerminalIcon = createIcon([
  <polyline key="t1" points="4 17 10 11 4 5" />,
  <line key="t2" x1="12" y1="19" x2="20" y2="19" />,
]);

export const UserIcon = createIcon([
  <path key="u1" d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />,
  <circle key="u2" cx="12" cy="7" r="4" />,
]);

export const GithubIcon = createIcon([
  <path
    key="g1"
    d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"
  />,
  <path key="g2" d="M9 18c-4.51 2-5-2-7-2" />,
]);

export const LinkedinIcon = createIcon([
  <path
    key="l1"
    d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"
  />,
  <rect key="l2" width="4" height="12" x="2" y="9" />,
  <circle key="l3" cx="4" cy="4" r="2" />,
]);

export const MailIcon = createIcon([
  <path key="m1" d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7" />,
  <rect key="m2" x="2" y="4" width="20" height="16" rx="2" />,
]);

export const CloudIcon = createIcon([
  <path key="c1" d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z" />,
]);

export const DatabaseIcon = createIcon([
  <ellipse key="d1" cx="12" cy="5" rx="9" ry="3" />,
  <path key="d2" d="M3 5V19A9 3 0 0 0 21 19V5" />,
  <path key="d3" d="M3 12A9 3 0 0 0 21 12" />,
]);

export const DownloadIcon = createIcon([
  <path key="d1" d="M12 15V3" />,
  <path key="d2" d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />,
  <path key="d3" d="m7 10 5 5 5-5" />,
]);

export const ServerIcon = createIcon([
  <rect key="s1" width="20" height="8" x="2" y="2" rx="2" ry="2" />,
  <rect key="s2" width="20" height="8" x="2" y="14" rx="2" ry="2" />,
  <line key="s3" x1="6" x2="6.01" y1="6" y2="6" />,
  <line key="s4" x1="6" x2="6.01" y1="18" y2="18" />,
]);

export const ArrowRightIcon = createIcon([
  <line key="a1" x1="5" y1="12" x2="19" y2="12" />,
  <polyline key="a2" points="12 5 19 12 12 19" />,
]);

export const ArrowLeftIcon = createIcon([
  <line key="a1" x1="19" y1="12" x2="5" y2="12" />,
  <polyline key="a2" points="12 19 5 12 12 5" />,
]);

export const CalendarIcon = createIcon([
  <rect key="c1" x="3" y="4" width="18" height="18" rx="2" ry="2" />,
  <line key="c2" x1="16" y1="2" x2="16" y2="6" />,
  <line key="c3" x1="8" y1="2" x2="8" y2="6" />,
  <line key="c4" x1="3" y1="10" x2="21" y2="10" />,
]);

export const ClockIcon = createIcon([
  <circle key="c1" cx="12" cy="12" r="10" />,
  <polyline key="c2" points="12 6 12 12 16 14" />,
]);

export const ExternalLinkIcon = createIcon([
  <path key="e1" d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />,
  <polyline key="e2" points="15 3 21 3 21 9" />,
  <line key="e3" x1="10" y1="14" x2="21" y2="3" />,
]);

export const ZapIcon = createIcon([
  <polygon key="z1" points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />,
]);

export const WrenchIcon = createIcon([
  <path
    key="w1"
    d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"
  />,
]);

export const TagIcon = createIcon([
  <path
    key="t1"
    d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"
  />,
  <line key="t2" x1="7" y1="7" x2="7.01" y2="7" />,
]);

export const TrendingUpIcon = createIcon([
  <polyline key="tu1" points="22 7 13.5 15.5 8.5 10.5 2 17" />,
  <polyline key="tu2" points="16 7 22 7 22 13" />,
]);

export const CalendarDaysIcon = createIcon([
  <rect key="cd1" x="3" y="4" width="18" height="18" rx="2" ry="2" />,
  <line key="cd2" x1="16" y1="2" x2="16" y2="6" />,
  <line key="cd3" x1="8" y1="2" x2="8" y2="6" />,
  <line key="cd4" x1="3" y1="10" x2="21" y2="10" />,
  <path key="cd5" d="M8 14h.01" />,
  <path key="cd6" d="M12 14h.01" />,
  <path key="cd7" d="M16 14h.01" />,
  <path key="cd8" d="M8 18h.01" />,
  <path key="cd9" d="M12 18h.01" />,
  <path key="cd10" d="M16 18h.01" />,
]);
