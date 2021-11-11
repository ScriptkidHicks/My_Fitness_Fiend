import styled from "styled-components";
import { useContext, useState } from "react";
import { ColorContext } from "../ContextProviders/ColorContext";
import { useNavigate } from "react-router";

function RibbonBar(props) {
  // this is the state we use to modify the visiblity of the bar
  // do not use a boolean value, instead use 0 or 1 for truthiness
  const [visibility, setVisiblity] = useState(0);
  // the new version of useHistory()
  const navigate = useNavigate();

  // this is the generic function which is passed a page target from props, and loads that page target on click
  function LoadPage(targetPage) {
    navigate(targetPage);
  }

  function displayHandler() {
    if (visibility) {
      setVisiblity(0);
    } else {
      setVisiblity(1);
    }
  }

  const theme = useContext(ColorContext);
  return (
    <Body>
      <DisplayButton theme={theme} onClick={displayHandler}>
        <DisplayButtonBar theme={theme} visibility={visibility} />
      </DisplayButton>
      <Ribbon theme={theme} visibility={visibility}>
        <NavButton theme={theme} onClick={() => LoadPage(props.pageTargets[0])}>
          {props.pageTitles[0]}
        </NavButton>
        <NavButton theme={theme} onClick={() => LoadPage(props.pageTargets[1])}>
          {props.pageTitles[1]}
        </NavButton>
        <NavButton theme={theme} onClick={() => LoadPage(props.pageTargets[2])}>
          {props.pageTitles[2]}
        </NavButton>
      </Ribbon>
    </Body>
  );
}

export default RibbonBar;

const Ribbon = styled.div`
  visibility: ${(props) => (props.visibility ? "visible" : "hidden")};
  width: ${(props) => (props.visibility ? "min(30vw, 200px)" : "0")};
  background-color: ${(props) => props.theme.secondaryBackground};
  border-right: 3px solid black;
  height: 100vh;
  transition: ease all 0.5s;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  box-shadow: 3px 3px 12px ${(props) => props.theme.secondaryBackgroundShadow};
`;

const DisplayButton = styled.button`
  z-index: 90;
  opacity: 1;
  visibility: visible;
  position: absolute;
  bottom: 3vh;
  left: 2vw;
  width: min(15vw, 80px);
  height: min(15vw, 80px);
  background-color: ${(props) => props.theme.primaryButton};
  border-radius: 10px;
  box-shadow: 3px 3px 12px ${(props) => props.theme.secondaryBackgroundShadow};
  color: ${(props) => props.theme.primaryText};
  justify-items: center;
  align-content: center;
  display: flex;
`;

const DisplayButtonBar = styled.div`
  border: 3px solid ${(props) => props.theme.primaryButtonOutline};
  border-radius: 20px;
  margin: auto;
  background-color: ${(props) => props.theme.primaryButtonHighlight};
  width: ${(props) =>
    props.visibility ? "min(12vw, 60px)" : "min(3vw, 20px)"};
  height: min(3vw, 20px);
  transition: ease-in-out 0.4s;
`;

const Body = styled.div`
  position: absolute;
  height: 100vh;
  width: min(30vw, 200px);
  display: flex;
`;

const NavButton = styled.button`
  color: ${(props) => props.theme.primaryText};
  background-color: ${(props) => props.theme.secondaryButton};
  width: min(80%, 130px);
  height: 10%;
  border-radius: 10px;
  text-align: center;
  text-justify: center;
  margin-top: 12vh;
  box-shadow: 3px 3px 12px ${(props) => props.theme.secondaryBackgroundShadow};
  transition: ease all 0.2s;

  :hover {
    background-color: ${(props) => props.theme.secondaryButtonHover};
  }
`;
