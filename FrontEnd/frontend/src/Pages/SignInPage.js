import { useContext, useState } from "react";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

function SignInPage() {
  // these states will let us track the user input
  const [password, setPassword] = useState(null);
  const [email, setEmail] = useState(null);
  // this object is how we supply color context
  const theme = useContext(ColorContext);
  // this object is how we move the user between pages
  // it has replaced useHistory in react-router-dom v6.0
  const navigate = useNavigate();

  function ChangHandler(value, setFunction) {
    setFunction(value);
  }

  function SubmitHandler() {
    // we start off by doing some basic error checking to make sure that they
    if (password === null || password === "") {
      alert("Please enter a password");
      return;
    } else if (email === null || email === "") {
      alert("Please enter a valid email");
      return;
    }

    // now we package up an object for deliver.
    const userInfo = {
      method: "POST",
      headers: { "Content-Type": "application/JSON", Contents: "accountInfo" },
      body: JSON.stringify({ email: email, password: password }),
    };

    // and now we try to send it off to back end
    //NOTE: WE WILL HAVE TO CHANGE THIS ENDPOINT ONCE I START HOSTING IT. ADDING THE /API PREFIX WILL BE NECESSARY
    fetch("/login", userInfo).then((response) => {
      if (response.status === 200) {
        response.json().then((json) => {
          localStorage.setItem("id_token", json.token);
          navigate("/monsterpage");
        });
      } else {
        // anything other than a 201 indicates failure. Eventually we should add more status code checks, to account for backend going down, etc
        alert("That appears to be incorrect account information");
      }
    });
  }

  return (
    <Body theme={theme}>
      <LoginWrapper theme={theme}>
        <LoginTitle theme={theme}>Sign In</LoginTitle>
        <LoginInputWrapper>
          <LoginInput
            theme={theme}
            placeholder="Email"
            type="email"
            onChange={(e) => ChangHandler(e.target.value, setEmail)}
          ></LoginInput>
          <LoginInput
            theme={theme}
            placeholder="Password"
            type="password"
            onChange={(e) => ChangHandler(e.target.value, setPassword)}
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
            <SubmitButton theme={theme} onClick={SubmitHandler}>
              SignIn
            </SubmitButton>
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
