import { useContext } from "react";
import styled from "styled-components";
import RibbonBar from "../Components/RibbonBar";
import { ColorContext } from "../ContextProviders/ColorContext";

function WorkoutLogPage() {
  // this is so we can distribute the color context to the individual components.
  const theme = useContext(ColorContext);
  // page targets and page titles are distributed individually to each page. We don't want a page to have a load button for the page that it is already on. Make sure that the page targets correlate correctly to the page titles. They will be unpacked in the same order.
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
