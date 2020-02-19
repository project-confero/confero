import React from "react";
import MaterialLink, { LinkProps } from "@material-ui/core/Link";
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps
} from "react-router-dom";

// Suggested Material-UI/ReactRouter integration from https://material-ui.com/guides/composition/#link
const LinkWithRef = React.forwardRef<HTMLAnchorElement, RouterLinkProps>(
  (props, ref) => <RouterLink innerRef={ref} {...props} />
);

const Link: React.FC<LinkProps & RouterLinkProps> = props => {
  return <MaterialLink component={LinkWithRef} {...props} />;
};

export default Link;
