import React from "react";
import { Button, ButtonProps } from "@theme-ui/components";

export interface TextButtonProps {}

const TextButton = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (props, ref) => {
    return (
      <Button ref={ref} backgroundColor="transparent" color="text" {...props} />
    );
  }
);

export default TextButton;
