import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function Card({ className, children, hover = true, ...props }) {
  return (
    <div
      className={twMerge(
        "glass rounded-2xl shadow-glass overflow-hidden backdrop-blur-xl border border-white/20 animate-slide-up",
        hover && "card-hover",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ className, children, gradient = false, ...props }) {
  return (
    <div
      className={twMerge(
        "px-6 py-5 border-b border-white/10",
        gradient && "bg-gradient-to-r from-white/50 to-transparent",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardTitle({ className, children, ...props }) {
  return (
    <h3 className={twMerge("text-xl font-bold text-slate-800 tracking-tight", className)} {...props}>
      {children}
    </h3>
  );
}

export function CardContent({ className, children, ...props }) {
  return (
    <div className={twMerge("p-6", className)} {...props}>
      {children}
    </div>
  );
}
