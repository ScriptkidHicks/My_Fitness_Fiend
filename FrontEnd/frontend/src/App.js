import styled from "styled-components";
import { Routes, Route } from "react-router";

import LandingPage from "./Pages/LandingPage";

function App() {
  return (
    <Body>
      <Routes>
        <Route path="/Landing" exact element={<LandingPage />} />
      </Routes>
    </Body>
  );
}

export default App;

const Body = styled.div`
  background-color: black;
`;
