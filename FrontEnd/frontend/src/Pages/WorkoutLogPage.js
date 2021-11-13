import { useContext } from "react";
import styled from "styled-components";
import RibbonBar from "../Components/RibbonBar";
import { ColorContext } from "../ContextProviders/ColorContext";

function WorkoutLogPage() {
  const theme = useContext(ColorContext);
  const pageTargets = ["/AccountPage", "/MonsterPage", "/PastWorkoutsPage"];
  const pageTitles = [
    "Your Account Info",
    "Your Monster",
    "Your Past Workouts",
  ];
  return (
    <Body theme={theme}>
      <RibbonBar pageTitles={pageTitles} pageTargets={pageTargets} />
    </Body>
  );
}

export default WorkoutLogPage;

const Body = styled.div`
  width: 100vw;
  height: 100vh;
  background-color: ${(props) => props.theme.primaryBackground};
`;
