import React from "react";
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps
} from "react-router-dom";
import {
  Link as ThemeLink,
  LinkProps as ThemeLinkProps
} from "@theme-ui/components";

export type LinkProps = ThemeLinkProps & RouterLinkProps;

const Link = React.forwardRef<HTMLAnchorElement, LinkProps>((props, ref) => (
  <ThemeLink ref={ref} as={RouterLink} {...props} />
));

export default Link;
