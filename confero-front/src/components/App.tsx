import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { CssBaseline } from "@material-ui/core";
import { ThemeProvider } from "@material-ui/core/styles";

import theme from "./theme";
import Candidates from "./candidates/Candidates";
import Connections from "./connections/Connections";
import Home from "./Home";
import Navbar from "./nav/Navbar";

const App: React.FC = () => {
  return (
    <Router>
      <CssBaseline />

      <ThemeProvider theme={theme}>
        <Navbar />
        <Switch>
          <Route path="/candidates">
            <Candidates />
          </Route>

          <Route path="/connections">
            <Connections />
          </Route>

          <Route path="/">
            <Home />
          </Route>
        </Switch>
      </ThemeProvider>
    </Router>
  );
};

export default App;
