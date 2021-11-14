import { useContext, useState } from "react";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";

// this is the first time quiz page. It will be gated by both login status, and whether they have completed the first time quiz. If they have then we will send them back to the monster main page. There will also be no ribbon bar on this page, to prevent them from manually
function FirstTimeQuizPage() {
  const theme = useContext(ColorContext);
  const loading = useState(true);

  if (loading) {
    return (
      <LoadingWrapper theme={theme}>
        <LoadingText theme={theme}>
          <LoadingTextWrapper theme={theme}>Loading...</LoadingTextWrapper>
        </LoadingText>
      </LoadingWrapper>
    );
  } else {
    return <Body>Welcome to the first time quiz</Body>;
  }
}

export default FirstTimeQuizPage;

const Body = styled.div``;

const LoadingWrapper = styled.div`
  background-color: ${(props) => props.theme.primaryBackground};
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
`;

const LoadingTextWrapper = styled.div`
  background-color: ${(props) => props.theme.secondaryBackground};
  display: flex;
  justify-content: center;
  align-items: center;
  width: max(20vw, 200px);
  height: 10vh;
  border-radius: 20px;
  box-shadow: -4px 4px 14px black;
`;

const LoadingText = styled.h1`
  color: ${(props) => props.theme.primaryText};
  font-weight: bolder;
  text-align: center;
`;
