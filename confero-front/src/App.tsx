import React from "react";
import logo from "./logo.svg";
import "./App.css";

import { ThemeProvider } from "theme-ui";
import theme from "@rebass/preset";
import { Button } from "rebass";

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <Button sx={{ color: "black" }}>Hi</Button>
          <p>
            Edit <code>src/App.tsx</code> and save to reload.
          </p>
          <a
            className="App-link"
            href="https://reactjs.org"
            target="_blank"
            rel="noopener noreferrer"
          >
            Learn React
          </a>
        </header>
      </div>
    </ThemeProvider>
  );
};

export default App;
