export default function Input(props: React.ComponentProps<"input">) {
  return (
    <>
      <input
        name="myInput"
        className="flex rounded-xs pl-2 outline-1 h-9"
        {...props}
      />
    </>
  );
}
