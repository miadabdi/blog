import * as React from 'react';

type BadgeVariant = 'default' | 'secondary' | 'outline' | 'destructive';

const baseClasses =
  'inline-flex items-center justify-center rounded-md border px-2 py-0.5 text-xs font-medium w-fit whitespace-nowrap shrink-0 gap-1 [&>svg]:size-3 [&>svg]:pointer-events-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 transition-colors';

const variantClassMap: Record<BadgeVariant, string> = {
  default: 'border-transparent bg-primary text-primary-foreground hover:bg-primary/90',
  secondary: 'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/90',
  outline: 'border-border text-foreground hover:bg-accent hover:text-accent-foreground',
  destructive:
    'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/90',
};

type BadgeProps = React.ComponentPropsWithoutRef<'span'> & {
  variant?: BadgeVariant;
};

const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant = 'default', ...props }, ref) => {
    const variantClasses = variantClassMap[variant] ?? variantClassMap.default;

    const classes = [baseClasses, variantClasses, className].filter(Boolean).join(' ');

    return <span ref={ref} data-slot="badge" className={classes} {...props} />;
  },
);

Badge.displayName = 'Badge';

export { Badge };
export type { BadgeProps, BadgeVariant };
