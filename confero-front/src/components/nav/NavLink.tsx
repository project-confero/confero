import React from "react";
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps
} from "react-router-dom";
import {
  NavLink as ThemeNavLink,
  NavLinkProps as ThemeNavLinkProps
} from "@theme-ui/components";

export type NavLinkProps = ThemeNavLinkProps & RouterLinkProps;

const NavLink = React.forwardRef<HTMLAnchorElement, NavLinkProps>(
  (props, ref) => <ThemeNavLink ref={ref} as={RouterLink} {...props} />
);

export default NavLink;
