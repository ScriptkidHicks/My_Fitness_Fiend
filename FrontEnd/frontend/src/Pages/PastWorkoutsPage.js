import { useContext } from "react";
import styled from "styled-components";
import RibbonBar from "../Components/RibbonBar";
import { ColorContext } from "../ContextProviders/ColorContext";

function PastWorkoutsPage() {
  const theme = useContext(ColorContext);
  const pageTargets = ["/AccountPage", "/MonsterPage", "/WorkoutLogPage"];
  const pageTitles = ["Your Account Info", "Your Monster", "Daily workout Log"];
  return (
    <Body theme={theme}>
      <RibbonBar pageTitles={pageTitles} pageTargets={pageTargets} />
    </Body>
  );
}

export default PastWorkoutsPage;

const Body = styled.div`
  width: 100vw;
  height: 100vh;
  background-color: ${(props) => props.theme.primaryBackground};
`;
