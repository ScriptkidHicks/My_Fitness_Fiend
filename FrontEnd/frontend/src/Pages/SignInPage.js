import { useContext } from "react";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";
import { Link } from "react-router-dom";

function SignInPage() {
  const theme = useContext(ColorContext);
  return (
    <Body theme={theme}>
      <LoginWrapper theme={theme}>
        <LoginTitle theme={theme}>Sign In</LoginTitle>
        <LoginInputWrapper>
          <LoginInput
            theme={theme}
            placeholder="Email"
            type="email"
          ></LoginInput>
          <LoginInput
            theme={theme}
            placeholder="Password"
            type="password"
          ></LoginInput>
          <SubmitSwitchWrapper theme={theme}>
            <Link
              to="/CreateProfile"
              style={{
                margin: "auto",
                textAlign: "center",
                color: `${theme.primaryText}`,
                textDecoration: "none",
                width: "60%",
                fontSize: "2.3vh",
                lineHeight: "2",
                fontWeight: "bolder",
              }}
            >
              Haven't made a fiend?
              <br />
              Create Account
            </Link>
            <SubmitButton theme={theme}>SignIn</SubmitButton>
          </SubmitSwitchWrapper>
        </LoginInputWrapper>
      </LoginWrapper>
    </Body>
  );
}

export default SignInPage;

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
  padding-bottom: 0;
  margin-bottom: 0;
  margin-top: auto;
  text-align: center;
  font-size: max(3vw, 5vh);
  color: ${(props) => props.theme.primaryText};
  //text-shadow: -8px 8px 6px black; // I don't know how I feel about the font shadowing on this
`;

const LoginInputWrapper = styled.div`
  display: flex;
  margin: auto;
  height: 60%;
  width: 90%;
  align-items: center;
  flex-direction: column;
  justify-content: space-evenly;
`;

const LoginInput = styled.input`
  width: 85%;
  border-radius: 8px;
  height: min(16%, 35px);
  outline: none;
  text-align: center;
  font-size: max(2.2vh, 110%);
  transition: ease all 0.2s;

  :focus {
    box-shadow: -4px 4px 10px
      ${(props) => props.theme.secondaryBackgroundShadow};
    border: 4px solid ${(props) => props.theme.primaryInputOutline};
  }
`;

const SubmitSwitchWrapper = styled.div`
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
  width: 100%;
  height: 25%;
  padding-top: 20px;
`;

const SubmitButton = styled.button`
  width: 40%;
  background-color: ${(props) => props.theme.primaryButton};
  color: ${(props) => props.theme.primaryText};
  border-radius: 15px;
  border: 3px solid ${(props) => props.theme.primaryButtonOutline};
  transition: ease all 0.2s;
  font-size: 2.5vh;
  font-weight: bold;

  :hover {
    box-shadow: -3px 3px 6px ${(props) => props.theme.secondaryBackgroundShadow};
    border: 3px solid ${(props) => props.theme.primaryButtonHoverOutline};
  }
`;