import styled from "styled-components";

function LandingPage() {
  return (
    <Body>
      <LogoContainer>
        <Logo>
          My Fitness Fiend
          <sup style={{ fontSize: "small", backgroundColor: "black" }}>TM</sup>
        </Logo>
      </LogoContainer>
    </Body>
  );
}

export default LandingPage;

const Body = styled.div`
  color: white;
  height: 100vh;
  width: 100vw;
  background-color: black;
`;

const Logo = styled.h1`
  color: white;
  background-color: black;
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
  width: 80vw;
`;
