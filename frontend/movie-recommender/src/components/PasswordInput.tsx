import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";
import Input from "./Input";

export default function PasswordInput(
  props: Omit<React.ComponentProps<"input">, "type">,
) {
  const [textHidden, setTextHidden] = useState<boolean>(true);

  return (
    <div className="relative">
      <Input type={textHidden ? "password" : "text"} {...props}></Input>
      <button
        className="absolute right-2 top-1/6"
        type="button"
        onClick={() => setTextHidden(!textHidden)}
      >
        {textHidden ? <EyeOff /> : <Eye />}
      </button>
    </div>
  );
}
