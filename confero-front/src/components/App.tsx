import React from "react";
import { ThemeProvider } from "theme-ui";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

import theme from "./theme";
import Candidates from "./Candidates";
import Connections from "./connections/Connections";
import Home from "./Home";
import Navbar from "./nav/Navbar";

const App: React.FC = () => {
  return (
    <Router>
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
