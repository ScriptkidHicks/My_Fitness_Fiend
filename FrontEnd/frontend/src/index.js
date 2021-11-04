import React from "react";
import ReactDOM from "react-dom";
import "./CSS/index.css";
import App from "./App";
import { BrowserRouter } from "react-router-dom";

ReactDOM.render(
  <BrowserRouter basename={process.env.PUBLIC_URL}>
    <App id="content" />
  </BrowserRouter>,
  document.getElementById("root")
);
