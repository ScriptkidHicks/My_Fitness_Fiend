import styled from "styled-components";
import { Link } from "react-router-dom";
import classes from "../CSS/Buttons.module.css";
import { useContext } from "react";
import { ColorContext } from "../ContextProviders/ColorContext";

function LandingPage() {
  const theme = useContext(ColorContext);
  return (
    <Body theme={theme}>
      <LogoContainer theme={theme}>
        <Logo>
          My Fitness Fiend
          <sup>
            <sup style={{ fontSize: "small" }}>TM</sup>
          </sup>
        </Logo>
      </LogoContainer>
      <Link to="/Login" className={classes.LandingPageButton}>
        Start Fiending
      </Link>
    </Body>
  );
}

export default LandingPage;

const Body = styled.div`
  color: ${(props) => props.theme.primaryText};
  height: 100vh;
  width: 100vw;
  background-color: ${(props) => props.theme.primaryBackground};
`;

const Logo = styled.h1`
  color: white;
  background-color: ${(props) => props.theme.primaryBackground};
  font-size: min(10vw, 55px);
`;

const LogoContainer = styled.div`
  align-content: center;
  justify-content: center;
  transform: translate(-50%, -50%);
  position: absolute;
  top: 30vh;
  left: 45vw;
  display: flex;
  width: 90vw;
`;
