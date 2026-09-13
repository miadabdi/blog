import { cn } from '@/utils/cn';
import * as React from 'react';

const Slot = React.forwardRef<HTMLElement, React.HTMLAttributes<HTMLElement>>(
  ({ children, ...props }, ref) => {
    if (!React.isValidElement(children))
      return (
        <span ref={ref} {...props}>
          {children}
        </span>
      );
    const child = children as React.ReactElement<Record<string, unknown>>;
    return React.cloneElement(child, {
      ...props,
      ref,
    } as React.Attributes & Record<string, unknown>);
  },
);

const baseButtonClasses =
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-all cursor-pointer select-none disabled:pointer-events-none disabled:opacity-50 disabled:cursor-not-allowed [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive";

const variantClassMap = {
  default: 'bg-primary text-primary-foreground shadow-xs hover:bg-primary/90',
  destructive:
    'bg-destructive text-white shadow-xs hover:bg-destructive/90 focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 dark:bg-destructive/60',
  outline:
    'border bg-background shadow-xs hover:bg-accent dark:hover:bg-accent hover:text-accent-foreground',
  secondary:
    'bg-secondary text-secondary-foreground shadow-xs hover:bg-secondary/70 dark:hover:bg-secondary/60',
  ghost: 'hover:bg-accent hover:text-accent-foreground dark:hover:bg-accent/85',
  link: 'text-primary underline-offset-4 hover:underline',
} as const;

const sizeClassMap = {
  default: 'h-9 px-4 py-2 has-[>svg]:px-3',
  sm: 'h-8 rounded-md gap-1.5 px-3 has-[>svg]:px-2.5',
  lg: 'h-10 rounded-md px-6 has-[>svg]:px-4',
  icon: 'size-9',
} as const;

type ButtonVariant = keyof typeof variantClassMap;
type ButtonSize = keyof typeof sizeClassMap;

type ButtonVariantOptions = {
  variant?: ButtonVariant;
  size?: ButtonSize;
  className?: string;
};

const buttonVariants = ({
  variant = 'default',
  size = 'default',
  className,
}: ButtonVariantOptions = {}) => {
  const resolvedVariant = variantClassMap[variant] ?? variantClassMap.default;
  const resolvedSize = sizeClassMap[size] ?? sizeClassMap.default;

  return cn(baseButtonClasses, resolvedVariant, resolvedSize, className);
};

function Button({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: React.ComponentProps<'button'> & {
  variant?: ButtonVariant;
  size?: ButtonSize;
  asChild?: boolean;
}) {
  const Comp = asChild ? Slot : 'button';

  return (
    <Comp data-slot="button" className={buttonVariants({ variant, size, className })} {...props} />
  );
}

export { Button };
