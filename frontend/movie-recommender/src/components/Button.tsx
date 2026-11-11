import type { ReactNode } from "react";

export default function Button({
  children,
  ...props
}: React.ComponentProps<"button">) {
  return (
    <button
      className="rounded-md mt-auto mb-3 bg-blue-500 hover:bg-blue-600 text-white border-1 border-solid focus-within:outline-2 focus-within:outline-indigo-400 outline-offset-1 h-10 w-30 cursor-pointer"
      {...props}
    >
      {children}
    </button>
  );
}
