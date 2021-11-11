import { useContext } from "react";
import { useNavigate } from "react-router";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";
import jwtDecode from "jwt-decode";

import RibbonBar from "../Components/RibbonBar";

import SignInPage from "./SignInPage";

function MonsterPage() {
  const theme = useContext(ColorContext);

  // this is how we determine if the user is logged in or not. Syntax may need to become asynchronous if loading times become an issue.
  let token = jwtDecode(localStorage.getItem("id_token"));

  const pageTitles = ["One", "Two", "three"];
  const pageTargets = ["/", "/", "/"];

  if (token.exp * 1000 < Date.now()) {
    return <SignInPage />;
  } else {
    return (
      <Body theme={theme}>
        <RibbonBar pageTargets={pageTargets} pageTitles={pageTitles} />
        Monster Page
      </Body>
    );
  }
}

export default MonsterPage;

const Body = styled.div`
  background-color: ${(props) => props.theme.primaryBackground};
  color: ${(props) => props.theme.primaryText};
  height: 100vh;
  width: 100vw;
`;
