import { useContext } from "react";
import { useNavigate } from "react-router";
import styled from "styled-components";
import { ColorContext } from "../ContextProviders/ColorContext";
import jwtDecode from "jwt-decode";

import practiceMonster from "../Images/MonsterImages/MonsterBasic.png";

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
        <MonsterPageWrapper>
          <XPBar>
            <XPSlider></XPSlider>
          </XPBar>
          <MonsterNameWrapper>
            <MonsterName>Klokov</MonsterName>
          </MonsterNameWrapper>
          <MonsterImageWrapper
            monsterImage={practiceMonster}
          ></MonsterImageWrapper>
          <BottomContentWrapper>
            <MonsterInfo>
              Here we have all the information about the workout fiend. We might
              even have some information about your workout today. Possibly a
              daily workout tip or something like that. This can all be easily
              injected. currently I'm just filling this with what is basically a
              lorem ipsum
            </MonsterInfo>
          </BottomContentWrapper>
        </MonsterPageWrapper>
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

const MonsterPageWrapper = styled.div`
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;
  overflow: hidden;
`;

const XPBar = styled.div`
  border: solid black 4px;
  border-radius: 12px;
  flex-grow: 0.5;
  width: min(98%, 700px);
`;

const XPSlider = styled.div`
  height: 100%;
  width: 40%;
  background-color: green;
  border-radius: 12px;
`;

const MonsterNameWrapper = styled.div`
  width: min(98%, 600px);
  flex-grow: 1;
  display: flex;
  flex-direction: row-reverse;
`;

const MonsterName = styled.h2`
  margin-right: 10%;
  width: 20%;
  line-height: 100%;
`;

const MonsterImageWrapper = styled.div`
  background: url(${(props) => props.monsterImage});
  background-size: cover;
  width: min(98%, 500px);
  flex-grow: 5;
  border-radius: 20px;
  box-shadow: 0px 3px 12px black;
`;

const BottomContentWrapper = styled.div`
  width: min(100%, 800px);
  flex-grow: 2;
  text-align: center;
  text-justify: center;
`;

const MonsterInfo = styled.p``;
