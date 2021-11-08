import styled from "styled-components";
import { Routes, Route } from "react-router";

import { ColorProvider } from "./ContextProviders/ColorContext";

import LandingPage from "./Pages/LandingPage";
import CreateProfilePage from "./Pages/CreateProfilePage";
import SignInPage from "./Pages/SignInPage";

function App() {
  return (
    <ColorProvider>
      {/* This ColorProvider Object provides color context for all things inside it. */}
      <Body>
        {/* The Routes object acts as a router for the single app, moving between provided routes */}
        <Routes>
          {/* each route provides a path relative to the root, and the element object passed into it as a prop is the page that it loads when the router is given that path */}
          <Route path="/" exact element={<LandingPage />} />
          <Route path="/CreateProfile" element={<CreateProfilePage />} />
          <Route path="/SignIn" element={<SignInPage />} />
        </Routes>
      </Body>
    </ColorProvider>
  );
}

export default App;

const Body = styled.div``;
