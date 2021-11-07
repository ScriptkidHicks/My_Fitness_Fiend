import { useContext } from "react";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";

function LoginPage() {
  const theme = useContext(ColorContext);
  console.log(theme.secondaryBackground);
  return (
    <Body theme={theme}>
      <LoginWrapper theme={theme} id={"identif"}>
        <LoginTitle theme={theme}>Create Profile</LoginTitle>
        <LoginInputWrapper>
          <LoginInput></LoginInput>
          <LoginInput></LoginInput>
        </LoginInputWrapper>
      </LoginWrapper>
    </Body>
  );
}

export default LoginPage;

const Body = styled.div`
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: ${(props) => props.theme.primaryBackground};
  justify-content: center;
  align-items: center;
`;

const LoginWrapper = styled.div`
  border: 2px solid black;
  margin-bottom: 20vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 50vh;
  width: min(80vw, 500px);
  background-color: ${(props) => props.theme.secondaryBackground};
  box-shadow: -8px 8px 10px black;
  border-radius: 20px;
`;

const LoginTitle = styled.h2`
  margin: auto;
  text-align: center;
  font-size: max(3vw, 5vh);
  color: ${(props) => props.theme.primaryText};
  //text-shadow: -8px 8px 6px black; // I don't know how I feel about the font shadowing on this
`;

const LoginInputWrapper = styled.div`
  display: flex;
  margin: auto;
  background-color: green;
  height: 60%;
  width: 90%;
  align-items: center;
  flex-direction: column;
  justify-content: flex-start;
`;

const LoginInput = styled.input`
  width: 80%;
  margin-top: 10%;
`;
